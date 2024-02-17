import json
import os
import time
from datetime import datetime

from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from dotenv import load_dotenv

load_dotenv()

# Connect to the Kafka server where you'll be capturing the data.
KAFKA_SERVER = [os.getenv("KAFKA_HOST") + ":" + os.getenv("KAFKA_PORT")]
TOPIC_NAME = os.getenv("TOPIC_NAME")

consumer = KafkaConsumer(TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

# Connect to the Cassandra cluster where you'll be saving the data.
CASSANDRA_CLUSTER = str(os.getenv("CASSANDRA_CLUSTER"))
CASSANDRA_PORT = str(os.getenv("CASSANDRA_PORT"))

cluster = Cluster([CASSANDRA_CLUSTER], port=9042)
session = cluster.connect()

def main():
    for message in consumer:
        kafka_message = message.value
        timestamp = datetime.fromtimestamp(int(time.time()))

        # Load product views data into Cassandra
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

if __name__ == "__main__":
    main()

cluster.shutdown()
