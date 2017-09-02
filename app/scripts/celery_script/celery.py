from __future__ import absolute_import

from celery import Celery

celery_app = Celery("CeleryQueue", include=["celery_script.tasks"])

celery_app.config_from_object("celery_script.config")

if __name__ == "__main__":
    celery_app.start()

# 运行命令
# celery -A celery_script.celery worker -l info
