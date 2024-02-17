import json
import time
import os

from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

# Connect to the Kafka server where you'll be sending the data.
KAFKA_SERVER = [os.getenv("KAFKA_HOST") + ":" + os.getenv("KAFKA_PORT")]
TOPIC_NAME = os.getenv("TOPIC_NAME")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    retry_backoff_ms=1000,
    retries=3, 
    request_timeout_ms=5000
)

def main():
    # Retrieve the browsing history from a JSON file.
    with open('product-views.json', 'r') as file:
        lines = file.readlines()

    # Send the data to a Kafka topic.
    for line in lines:
        data = json.loads(line)
        producer.send(TOPIC_NAME, value=data)
        time.sleep(1)

if __name__ == "__main__":
    main()

producer.close()
