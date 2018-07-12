import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyonic_sign_up.settings')

app = Celery('beyonic_sign_up')

app.config_from_object('django.conf:settings', namespace='CELERY') # use django settings file, namespace i.e. starts with CELERY_

app.autodiscover_tasks() # auto discover tasks in tasks.py files, dont have to manually add files to CELERY_IMPORT setting


if __name__ == '__main__':
    app.start()