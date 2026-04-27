import json
from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List

class KafkaConfig(BaseSettings):
    bootstrap_servers: List[str] = ["localhost:9092"]
    group_id: str = "fairness-agents"
    auto_offset_reset: str = "earliest"

class AgentConfig(BaseSettings):
    agent_name: str
    agent_id: str
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_group_id: str = "fairness-agents"
    kafka_auto_offset_reset: str = "earliest"
    log_level: str = "INFO"
    timeout_seconds: int = 300

    class Config:
        env_prefix = ""
        env_file = ".env"

    @property
    def kafka_config(self) -> KafkaConfig:
        raw_servers = self.kafka_bootstrap_servers
        if isinstance(raw_servers, str):
            try:
                parsed = json.loads(raw_servers)
                if isinstance(parsed, list):
                    parsed_servers = parsed
                else:
                    parsed_servers = [raw_servers]
            except json.JSONDecodeError:
                parsed_servers = [item.strip() for item in raw_servers.split(",") if item.strip()]
        else:
            parsed_servers = raw_servers

        return KafkaConfig(
            bootstrap_servers=parsed_servers,
            group_id=self.kafka_group_id,
            auto_offset_reset=self.kafka_auto_offset_reset,
        )
