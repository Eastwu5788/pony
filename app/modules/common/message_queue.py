import pika
import json
from app.modules.common.encoder import DateEncoder
from pony.settings import INI_RABBIT

# RabbitMQ的主机地址和端口地址
RABBIT_MQ_HOST = INI_RABBIT["rabbit"]["rabbit.host"]
RABBIT_MQ_PORT = int(INI_RABBIT["rabbit"]["rabbit.port"])

# 发送激活邮箱的队列名称
ACTIVE_EMAIL_QUEUE = INI_RABBIT["rabbit"]["rabbit.queue.active"]


def send_active_mail(params):
    # 获取连接
    connection = get_connection()
    # 配置频道
    channel = config_channel(connection, ACTIVE_EMAIL_QUEUE)
    # 发送消息
    data = json.dumps(params, cls=DateEncoder)
    channel.basic_publish(exchange='', routing_key=ACTIVE_EMAIL_QUEUE, body=data)
    # 关闭连接
    connection.close()


def get_connection():
    # 设置变量
    parameters = pika.ConnectionParameters(RABBIT_MQ_HOST, RABBIT_MQ_PORT)
    # 建立一个连接实例
    connection = pika.BlockingConnection(parameters)

    return connection


def config_channel(connection, queue=ACTIVE_EMAIL_QUEUE):
    # 声明一个管道
    channel = connection.channel()
    # 在管道里声明queue
    channel.queue_declare(queue=queue)
    # 返回channel
    return channel
