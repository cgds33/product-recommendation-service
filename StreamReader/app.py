import json
import os
import time
from datetime import datetime

from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVER = [os.getenv("KAFKA_HOST") + ":" + os.getenv("KAFKA_PORT")]
TOPIC_NAME = os.getenv("TOPIC_NAME")

consumer = KafkaConsumer(TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

CASSANDRA_CLUSTER = str(os.getenv("CASSANDRA_CLUSTER"))
CASSANDRA_PORT = str(os.getenv("CASSANDRA_PORT"))

cluster = Cluster([CASSANDRA_CLUSTER], port=9042)
session = cluster.connect()

for message in consumer:
    kafka_message = message.value
    timestamp = datetime.fromtimestamp(int(time.time()))

    session.execute(
        """
        INSERT INTO productViews.product_views (messageid, event, userid, productid, source, messagetime)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            kafka_message['messageid'], 
            kafka_message['event'], 
            kafka_message['userid'], 
            kafka_message['properties']['productid'], 
            kafka_message['context']['source'], 
            timestamp,
        )
    )

cluster.shutdown()
