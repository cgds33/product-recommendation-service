import json
import os

from kafka import KafkaConsumer

KAFKA_SERVER = [os.getenv("KAFKA_HOST") + ":" + os.getenv("KAFKA_PORT")]
TOPIC_NAME = os.getenv("TOPIC_NAME")

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    print(message.value)
