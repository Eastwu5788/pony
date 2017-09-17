import redis
from pony.settings import REDIS


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

_pool = redis.ConnectionPool(host=REDIS["host"], port=REDIS["port"])
_redis = redis.Redis(connection_pool=_pool)


class Redis(Singleton):

    @staticmethod
    def set(key=None, value=None, timeout=0):
        """
        设置key、value
        :param key: 键
        :param value: 值
        :param timeout: 超时事件
        """
        if not Redis.check_key(key):
            return False
        if timeout == 0:
            return _redis.set(key, value=value)
        else:
            return _redis.set(key, value=value, ex=timeout)

    @staticmethod
    def get(key=None):
        """
        获取一个存储的键值对
        :param key: 要查询的key
        :return:
        """
        if not Redis.check_key(key):
            return None
        result = _redis.get(key)
        if result:
            result = eval(result)
        return result

    @staticmethod
    def set_model(key, value, timeout=0):
        """
        数据对象存储
        """
        if not Redis.check_key(key):
            return False

        if not isinstance(value, object):
            return Redis.set(key, value, timeout)

        import pickle
        if timeout==0:
            return _redis.set(key, value=pickle.dumps(value))
        else:
            return _redis.set(key, value=pickle.dumps(value), ex=timeout)

    @staticmethod
    def get_model(key):
        """
        数据对象检索
        """
        if not Redis.check_key(key):
            return None
        result = _redis.get(key)
        if result:
            import pickle
            result = pickle.loads(result)
        return result

    @staticmethod
    def increment(key, default=1):
        """
        自增value，如果key不存在，则创建并设置默认值为default
        :param key: 需要改变的key
        :param default: 默认值
        """
        if not Redis.check_key(key):
            return False
        return _redis.incr(key, default)

    @staticmethod
    def decrement(key, default=1):
        """
        自减value，如果key不存在，则创建并设置值为default
        """
        if not Redis.check_key(key):
            return False
        return _redis.decr(key, default)

    @staticmethod
    def check_key(key):
        """
        检查key是否合法
        :param key: 需要检查的key
        :return: bool
        """
        if not key:
            return False
        if not isinstance(key, str):
            return False
        return True


