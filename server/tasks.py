from flask import Flask
from celery import Celery
from celery.schedules import crontab
import time

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(flask_app)


@celery.task()
def add_together(a, b):
    return a + b


@celery.task
def sleep_asynchronously():
    """
    This function simulates a task that takes 20 seconds to
    execute to completion.
    """
    time.sleep(5)


@celery.task
def wait(arg):
    time.sleep(1)
    return arg


@celery.task
def test(arg):
    print(arg)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


import tweepy

auth = tweepy.OAuthHandler('EPvaQslEjmSKTRHMm9zedSwWp', 'mU0rNGzSnRg7KCqyrBp9uyHV7bDlZFpyBDv5WLNOXuHdGxXh46')
auth.set_access_token('1237163957758169089-1wMrePcRA2LOWArNm5P4UDdTjvkPM8',
                      'GkiR44PWeuZMNA3yAAHMrkZCFJB7j8J5N9KKSksePScSZ')

api = tweepy.API(auth)
for tweet in api.search('arxiv.org'):
    print(tweet)