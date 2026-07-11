import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.worker_enable_remote_control = False
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')