from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import logging
from .config import KafkaConfig

class KafkaClient:
    def __init__(self, config: KafkaConfig):
        self.config = config
        self.producer = None
        self.consumer = None
        self.logger = logging.getLogger(__name__)

    def init_producer(self):
        """Initialize Kafka Producer"""
        self.producer = KafkaProducer(
            bootstrap_servers=self.config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        self.logger.info("Kafka Producer initialized")

    def init_consumer(self, topic: str):
        """Initialize Kafka Consumer"""
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.config.bootstrap_servers,
            auto_offset_reset=self.config.auto_offset_reset,
            group_id=self.config.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            session_timeout_ms=30000
        )
        self.logger.info(f"Kafka Consumer initialized for topic: {topic}")

    def send_message(self, topic: str, message: dict):
        """Send message to Kafka topic"""
        try:
            future = self.producer.send(topic, value=message)
            record_metadata = future.get(timeout=10)
            self.logger.info(f"Message sent to {topic}: {record_metadata}")
            return True
        except KafkaError as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    def consume_messages(self, topic: str, timeout: int = 60000):
        """Consume messages from Kafka topic"""
        for message in self.consumer:
            yield message.value

    def close(self):
        """Close connections"""
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()
