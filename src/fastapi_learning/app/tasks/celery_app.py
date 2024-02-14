from celery import Celery

celery_app = Celery(
    "tasks",
    broker='amqp://guest:guest@localhost:5672/',
    include=['fastapi_learning.app.tasks.tasks', ]
)


def main():
    argv = ['worker', '--loglevel=INFO', '-E']
    celery_app.worker_main(argv)
