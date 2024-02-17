import os
import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from cassandra.cluster import Cluster
import psycopg2

## Contains a DAG (Directed Acyclic Graph) to perform scheduled tasks in Airflow.

# Function containing scheduled tasks.
def etl_process():

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="product_views",
        user="postgres",
        password="123456",
        host="postgresdb"
    )
    cur_postgres = conn.cursor()

    # Connect to Cassandra
    cluster = Cluster(['cassandra'])
    session = cluster.connect('productviews')

    # Fetch order data from PostgreSQL
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

    # Load order data into Cassandra
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


# Airflow DAG Args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 16),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Airflow DAG 
dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL process DAG',
    schedule_interval='@hourly',
)

# ETL Process
transform_load_data = PythonOperator(
    task_id='transform_load_data',
    python_callable=etl_process,
    dag=dag,
    executor_config={'LocalExecutor'}
)

