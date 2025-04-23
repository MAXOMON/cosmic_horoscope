import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zodiac.settings')

app = Celery('zodiac_app',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    task_result_expires=0,
)
app.autodiscover_tasks(['zodiac_app'])

app.conf.visibility_timeout = 43200

app.conf.result_backend_transport_options = {
    'result_chord_ordered': True    # or False
}

app.conf.beat_schedule = {
    'update_zodiac_signs': {
        'task': 'update_zodiac_signs',
        'schedule': crontab(minute='0', hour='*')
    },
    'update_weather': {
        'task': 'update_weather',
        'schedule': crontab(minute='*/15')
    }
}
