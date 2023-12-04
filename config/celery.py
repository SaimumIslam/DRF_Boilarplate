import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")  # name of main module
app.config_from_object("django.conf:settings", namespace="CELERY")  # celery configuration starts with `CELERY_`.
app.autodiscover_tasks()  # Load tasks from all installed apps.


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request}")
