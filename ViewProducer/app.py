import json
import time
import os

from kafka import KafkaProducer

KAFKA_SERVER = [os.getenv("KAFKA_HOST") + ":" + os.getenv("KAFKA_PORT")]
TOPIC_NAME = os.getenv("TOPIC_NAME")

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

with open('product-views.json', 'r') as file:
    lines = file.readlines()

for line in lines:
    data = json.loads(line)
    data['timestamp'] = int(time.time())
    producer.send(TOPIC_NAME, value=data)

    print(data) #!
    time.sleep(1)
        
producer.close()
