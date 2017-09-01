# 使用RabbitMQ作为消息代理
BROKER_URL = "amqp://"


# 任务结果存放在Redis
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# 任务序列化和反序列化使用msgpack方案
CELERY_TASK_SERIALIZER = "json"


# 读取结果序列化
CELERY_RESULT_SERIALIZER = 'json'


# 任务过期时间
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24


# 指定接受的内容类型
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
