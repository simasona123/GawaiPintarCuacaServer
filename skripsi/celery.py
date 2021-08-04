from celery import Celery
import os
from django.conf import settings

# default setting untuk environment variable celery untuk celery command line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skripsi.settings")

app = Celery('skripsi')

# Berdasarkan doc dari celery penggunaan disini agar worker tidak perlu
# serialize config object ke child proses dan namespace berfungsi agar
# semua celery konfigurasi harus memiliki prefix 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules (tasks.py) dari semua django app yang teregristrasi
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def print_hello():
    print("Celery Berhasil")
