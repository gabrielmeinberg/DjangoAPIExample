import json
from kafka import KafkaProducer

kafka_producer = KafkaProducer(
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
    bootstrap_servers="kafka:29092",
)
