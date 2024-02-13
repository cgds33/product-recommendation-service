import json
import os

from kafka import KafkaConsumer
from cassandra.cluster import Cluster

KAFKA_SERVER = [os.getenv("KAFKA_HOST") + ":" + os.getenv("KAFKA_PORT")]
TOPIC_NAME = os.getenv("TOPIC_NAME")

consumer = KafkaConsumer(TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

cluster = Cluster(['cassandra'], port=9042)
session = cluster.connect()

for message in consumer:
    kafka_message = message.value
    print(kafka_message)

    session.execute(
        """
        INSERT INTO productViews.product_views (messageid, event, userid, productid, source, timestamp)
        VALUES (:messageid, :event, :userid, :productid, :source, :timestamp)
        """,
        {
            'messageid': kafka_message['messageid'], 
            'event': kafka_message['event'], 
            'userid': kafka_message['userid'], 
            'productid': kafka_message['properties']['productid'], 
            'source': kafka_message['context']['source'], 
            'timestamp': kafka_message['timestamp'],
        }
    )

cluster.shutdown()
