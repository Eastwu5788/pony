import pika
import json

from app.modules.common.util_email import Email
from app.modules.common.secret import get_secret_password
from pony.settings import INI_RABBIT

# RabbitMQ的主机地址和端口地址
_RABBIT_MQ_HOST = INI_RABBIT["rabbit"]["rabbit.host"]

# 发送激活邮箱的队列名称
_ACTIVE_EMAIL_QUEUE = INI_RABBIT["rabbit"]["rabbit.queue.active"]


def send_active_email(ch, method, properties, body):
    params = json.loads(body)

    token = params["access_token"]
    address = "http://10.0.138.237:8000/auth/active?access_token=" + token
    pass_port = get_secret_password(token + params["salt"])
    address += "&pass_port=" + pass_port

    message = "欢迎注册eastwu.cn，点击链接激活账号:" + address
    email_client = Email("账号激活邮件", params["email"], message)
    email_client.send_email()

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成


def get_connection():
    params = pika.ConnectionParameters(host=_RABBIT_MQ_HOST)
    connection = pika.BlockingConnection(params)
    return connection


def listen_active_email_channel():
    connection = get_connection()

    channel = connection.channel()
    channel.queue_declare(queue=_ACTIVE_EMAIL_QUEUE)
    channel.basic_consume(send_active_email, queue=_ACTIVE_EMAIL_QUEUE)
    channel.start_consuming()


if __name__ == '__main__':
    listen_active_email_channel()
