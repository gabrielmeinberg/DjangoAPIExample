import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "order",
    group_id="grp1",
    bootstrap_servers=["kafka:29092"],
    value_deserializer=lambda m: json.loads(m.decode("ascii")),
)
for m in consumer:
    print(m)
