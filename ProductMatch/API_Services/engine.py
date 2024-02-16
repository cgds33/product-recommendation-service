from cassandra.cluster import Cluster
from collections import Counter
from datetime import datetime, timedelta

cluster = Cluster(['cassandra'])
session = cluster.connect('productviews')


def get_nav_history_latest(userid):

    rows = session.execute(
        f"""
            SELECT productid, messagetime
            FROM product_views
            WHERE userid = '{userid}'
            ALLOW FILTERING;
        """
    )

    products = []
    for row in sorted(rows, key=lambda x: x.messagetime, reverse=True)[:10]:
        products.append(row.productid)
    return products

def delete_nav_history(userid, productid):

    session.execute(
        f"""
            DELETE FROM product_views
            WHERE userid = '{userid}' AND productid = '{productid}';
        """
    )
    return

def history_recommendations(userid):
    rows = session.execute(
        f"""
        SELECT productid
        FROM product_views
        WHERE userid = '{userid}'
        """
    )
    top_10_products = Counter(map(lambda row: row.productid, rows)).most_common(10)

    if len(top_10_products) == 10:
        return [product[0] for product in top_10_products], "personalized"
    else:
        current_date = datetime.now()
        one_month_ago = current_date - timedelta(days=30)
        two_months_ago = current_date - timedelta(days=60)

        rows = session.execute("SELECT * FROM order_views ALLOW FILTERING")

        filtered_rows = [row for row in rows if two_months_ago <= row.messagetime < one_month_ago]
        product_ids = [row.productid for row in filtered_rows]

        return [product_id for product_id, _ in Counter(product_ids).most_common(10)], "non-personalized"
