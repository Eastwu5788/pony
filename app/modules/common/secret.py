import hashlib
from pony.settings import SECRET_KEY
import time


def get_secret_password(ori_password):
    """
    执行密码加密操作
    执行同样的步骤，可以生成相同的字符串
    """
    hash_lib = hashlib.md5(bytes(SECRET_KEY, encoding="utf-8"))
    hash_lib.update(bytes(ori_password, encoding="utf-8"))
    return hash_lib.hexdigest()


def verify_password(password, secret_password):
    """
    执行密码校验操作
    """
    password = get_secret_password(password)
    return password == secret_password


def get_seed(input_str='', secret_length=32):
    """
    获取一定长度的随机字符串，任意两次不会相同
    """
    input_str += str(time.time())
    input_str += SECRET_KEY
    hash_lib = hashlib.sha512()
    hash_lib.update(bytes(input_str, encoding="utf-8"))
    hash_str = hash_lib.hexdigest()
    return hash_str[:secret_length]
