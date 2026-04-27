from datetime import datetime
import logging
import asyncio
from threading import Thread
from fastapi import FastAPI
from common.kafka_client import KafkaClient
from common.config import AgentConfig
from .metrics_calculator import MetricsCalculator

app = FastAPI()
logger = logging.getLogger(__name__)
config = AgentConfig(
    agent_name="bias_detection",
    agent_id="agent-1"
)

kafka_client = KafkaClient(config.kafka_config)
metrics_calculator = MetricsCalculator()
consumer_thread = None

@app.on_event("startup")
async def startup():
    kafka_client.init_producer()
    kafka_client.init_consumer("agent-bias-detection-requests")
    logger.info("Agent 1: Bias Detection started")

    def run_consumer_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_bias_detection())

    global consumer_thread
    consumer_thread = Thread(target=run_consumer_loop, daemon=True)
    consumer_thread.start()

@app.on_event("shutdown")
async def shutdown():
    kafka_client.close()
    if consumer_thread is not None and consumer_thread.is_alive():
        consumer_thread.join(timeout=1)

async def process_bias_detection():
    """Listen for requests and process bias detection"""
    for message in kafka_client.consume_messages("agent-bias-detection-requests"):
        try:
            workflow_id = message['workflow_id']
            dataset_path = message['dataset_path']
            model_path = message['model_path']
            protected_attributes = message['protected_attributes']
            target_column = message['target_column']

            logger.info(f"Processing bias detection for workflow: {workflow_id}")

            dataset = metrics_calculator.load_dataset(dataset_path)
            model = metrics_calculator.load_model(model_path)

            metrics = metrics_calculator.compute_all_metrics(
                dataset=dataset,
                model=model,
                protected_attributes=protected_attributes,
                target_column=target_column
            )

            result = {
                'workflow_id': workflow_id,
                'agent_name': 'bias_detection',
                'status': 'COMPLETED',
                'metrics': metrics,
                'timestamp': str(datetime.now())
            }

            kafka_client.send_message('agent-results', result)

        except Exception as e:
            logger.error(f"Error in bias detection: {str(e)}")
            error_result = {
                'workflow_id': message.get('workflow_id'),
                'agent_name': 'bias_detection',
                'status': 'FAILED',
                'error': str(e),
                'timestamp': str(datetime.now())
            }
            kafka_client.send_message('agent-results', error_result)

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "bias_detection"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
