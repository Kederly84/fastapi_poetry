from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_learning.app.config import settings

celery_app = Celery(
    "tasks",
    broker='amqp://guest:guest@localhost:5672/',
    include=['fastapi_learning.app.tasks.tasks',
             'fastapi_learning.app.tasks.scheduled'
             ]
)

celery_app.conf.beat_schedule = {
    'scheduled_tasks': {
        'task': 'scheduled_task',
        # examples in crontab.guru
        'schedule': 5
    },
    'scheduled_day_task': {
        'task': 'send_booking_tomorrow_alert_email',
        'schedule': crontab(hour='9'),
        'args': (1,)
    },
    'scheduled_three_day_task': {
        'task': 'send_booking_tomorrow_alert_email',
        'schedule': crontab(hour='15', minute='30'),
        'args': (3,)
    }
}

engine = create_engine(settings.sync_driver)
sync_session = sessionmaker(engine)


# def main():
#     argv = ['worker', '--loglevel=INFO', '-E']
#     celery_app.worker_main(argv)

def tasks():
    argv = ['worker', '--loglevel=INFO', '-E']
    celery_app.worker_main(argv)


def periodic_task():
    argv = ['worker', '--loglevel=INFO', '-B']
    celery_app.worker_main(argv)


