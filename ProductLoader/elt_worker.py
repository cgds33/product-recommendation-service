from celery import Celery
from influxdb import InfluxDBClient
import psycopg2

app = Celery('etl_tasks', broker='redis://redis:6379/0')

influxdb_client = InfluxDBClient(host='influxdb', port=8086, username='user', password='123456', database='product_views')
pg_conn = psycopg2.connect(host='postgresdb', port=5432, dbname='product_views', user='postgres', password='123456')

@app.task
def etl_task():
    # Veri çıkarma
    result = influxdb_client.query('SELECT * FROM measurement')
    influx_data = result.get_points()
    
    # Veri dönüştürme ve yükleme
    pg_cursor = pg_conn.cursor()
    for data_point in influx_data:
        pg_cursor.execute("INSERT INTO postgres_table (column1, column2) VALUES (%s, %s)", (data_point['field1'], data_point['field2']))
    pg_conn.commit()
    pg_cursor.close()

if __name__ == "__main__":
    argv = [
        'worker',
        '--loglevel=DEBUG',
    ]
    app.worker_main(argv)