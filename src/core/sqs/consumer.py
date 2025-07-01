import json
import time
from typing import Any

import boto3
from src.core.logger import logger


class SQSConsumer:
    def __init__(
        self,
        queue_url: str,
        max_number_of_message: int = 1,
        wait_time_seconds: int = 20,
    ):
        self._running = False
        self.queue_url = queue_url
        self.wait_time_seconds = wait_time_seconds
        self.max_number_of_message = max_number_of_message
        self._sqs_client = boto3.client("sqs", region_name="ap-southeast-1")

    @property
    def _sqs_client_params(self) -> dict[str, Any]:
        return {
            "QueueUrl": self.queue_url,
            "MaxNumberOfMessages": self.max_number_of_message,
            "WaitTimeSeconds": self.wait_time_seconds,
        }

    async def start_consume(self) -> None:
        self._running = True
        while self._running:
            time.sleep(15)
            message = self.get_message()
            logger.info("Message received from queue %s", str(message))
            if message is not None:
                payload = json.loads(message["Body"])
                await self.process_task(payload=payload, receipt_handle=message["ReceiptHandle"])
            else:
                time.sleep(15)

    def get_message(self) -> Any:
        response = self._sqs_client.receive_message(**self._sqs_client_params)
        if len(response.get("Messages", [])) > 0:
            return response["Messages"][0]
        return None

    def delete_sqs_message(self, receipt_handle: str) -> None:
        try:
            self._sqs_client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)
            logger.info("Message deleted from queue")
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error deleting message from queue: {e}")

    async def process_task(self, payload: Any, receipt_handle: str) -> None:
        """Override this method in derived classes to implement custom task processing logic."""  # noqa
        raise NotImplementedError("Subclasses must implement this method")
