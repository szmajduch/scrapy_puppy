from kafka import KafkaProducer
import json
import time

# Kafka configuration
KAFKA_BROKER = "localhost:29092"  # Change to your broker address
TOPIC_NAME = "test-topic"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_response(keyword, response, topic):
    # Send messages to Kafka
    message = {"keyword": keyword, "response": response, "timestamp": time.time()}
    producer.send(topic, value=message)
    print(f"Sent: {message}")
    # Close the producer
    producer.close()
