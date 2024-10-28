import os
import sys

from celery import Celery

current2 = os.path.dirname(os.path.realpath(__file__))
current1 = os.path.dirname(current2)
parent = os.path.dirname(current1)
sys.path.append(parent)


celery = Celery(__name__)
celery.conf.update(
    broker_url=os.environ.get("REDIS_URL"),
    result_backend=None,
    broker_connection_retry_on_startup=True,
)

celery.autodiscover_tasks(["src.worker"])
