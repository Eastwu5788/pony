from __future__ import absolute_import
from .celery import celery_app


@celery_app.task
def celery_send_active_email(params):
    print("发送激活邮件")
    print(params)


