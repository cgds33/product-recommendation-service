from cassandra.cluster import Cluster
from collections import Counter
from datetime import datetime, timedelta

cluster = Cluster(['cassandra'])
session = cluster.connect('productviews')

## Recent history: The last 10 products will be returned and sorted by viewing date
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

## Delete history: A function where they can delete a product from their history
def delete_nav_history(userid, productid):

    session.execute(
        f"""
            DELETE FROM product_views
            WHERE userid = '{userid}' AND productid = '{productid}';
        """
    )
    return

## Product Recommendation: 
# identifies a user's interests based on their browsing history items and recommends only the best-selling ones to them
def history_recommendations(userid):
    rows = session.execute(
        f"""
        SELECT productid
        FROM product_views
        WHERE userid = '{userid}'
        """
    )
    top_10_products = Counter(map(lambda row: row.productid, rows)).most_common(10)

    # If the user has no browsing history, return a list as a second strategy.
    # Return the top ten products purchased by the most users without any filters.
    if len(top_10_products) == 10:
        return [product[0] for product in top_10_products], "personalized"
    else:
        # These products should be from orders placed last month.
        current_date = datetime.now()
        one_month_ago = current_date - timedelta(days=30)
        two_months_ago = current_date - timedelta(days=60)

        rows = session.execute("SELECT * FROM order_views ALLOW FILTERING")

        filtered_rows = [row for row in rows if two_months_ago <= row.messagetime < one_month_ago]
        product_ids = [row.productid for row in filtered_rows]

        return [product_id for product_id, _ in Counter(product_ids).most_common(10)], "non-personalized"
