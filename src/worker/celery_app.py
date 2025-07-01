from celery import Celery

celery = Celery(__name__)


task_queues: list[str] = []


CELERY_CONFIG = {
    "celery_task_serializer": "json",
    "celery_accept_content": ["json"],
    "celery_result_serializer": "json",
    "celery_result_backend": None,
    "celery_enable_remote_control": False,
    "broker_url": "sqs://",
    "broker_transport": "sqs",
    "task_queues": task_queues,
    "default_task_queue": "send_sms",
    "broker_transport_options": {
        "region": "ap-southeast-1",
        "sqs_base64_encoding": False,
    },
    "broker_connection_retry_on_startup": True,
    "celery_create_missing_queues": False,
}


celery.conf.update(**CELERY_CONFIG)
celery.autodiscover_tasks(["src.worker"])
