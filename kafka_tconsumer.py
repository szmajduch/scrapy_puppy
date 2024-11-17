from kafka import KafkaConsumer
import json

# Kafka configuration
KAFKA_BROKER = "localhost:29092"  # Change to your broker address
TOPIC_NAME = "test-topic"

# Create Kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"Subscribed to topic: {TOPIC_NAME}")

# Read messages from Kafka
for message in consumer:
    print(f"Received: {message.value}")
