import os
import psutil
from celery import Celery


# Use project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_stream.settings')
app = Celery('media_stream', result_extended=True)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(name='tasks.log_cpu_usage')
def log_cpu_usage(usage_percent):
    print(f'CPU usage: {usage_percent}')
    return usage_percent

@app.task(name='tasks.read_cpu_usage')
def read_cpu_usage():
    print('Reading CPU usage')
    usage_percent = psutil.cpu_percent(interval=1)
    app.send_task('tasks.log_cpu_usage', args=(usage_percent,))
