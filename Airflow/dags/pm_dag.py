import os
import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from cassandra.cluster import Cluster
import psycopg2

def etl_process():
    conn = psycopg2.connect(
        dbname="product_views",
        user="postgres",
        password="123456",
        host="postgresdb"
    )
    cur_postgres = conn.cursor()

    cluster = Cluster(['cassandra'])
    session = cluster.connect('productviews')

    cur_postgres.execute("""
        SELECT 
            order_items.id,
            orders.order_id,
            orders.user_id,
            products.product_id,
            products.category_id,
            order_items.quantity
        FROM 
            order_items
        INNER JOIN orders ON order_items.order_id = orders.order_id
        INNER JOIN products ON order_items.product_id = products.product_id
    """)
    rows = cur_postgres.fetchall()

    timestamp = datetime.fromtimestamp(int(time.time()))
    for row in rows:
        session.execute("""
            INSERT INTO order_views (orderid, userid, productid, categoryid, quantity, messagetime)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (row[1], row[2], row[3] ,row[4], row[5], timestamp)
        )

    cur_postgres.close()
    cluster.shutdown()


# Airflow DAG 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 16),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL process DAG',
    schedule_interval='@hourly',
)


transform_load_data = PythonOperator(
    task_id='transform_load_data',
    python_callable=etl_process,
    dag=dag,
    executor_config={'LocalExecutor'}
)

