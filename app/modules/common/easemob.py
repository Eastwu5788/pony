"""
EaseMob服务器端接口封装
"""
import requests
import json
import hashlib
from django.core.cache import cache
from pony.settings import SECRET_KEY

_MOB_ORG_NAME = "1169170818115229"
_MOB_APP_NAME = "we-chat"

_MOB_CLIENT_ID = "YXA6_sadEIPoEeeqyf_s7XVxig"
_MOB_CLIENT_SECRET = "YXA6R9vNgOTxIVgB85Ihb8xWultRon8"

_HTTP_BASE_PATH = "https://a1.easemob.com/"+_MOB_ORG_NAME+"/"+_MOB_APP_NAME
_HTTP_TOKEN_PATH = _HTTP_BASE_PATH+"/token"
_HTTP_REGISTER_PATH = _HTTP_BASE_PATH+"/users"

_EASE_MOB_CACHE_TOKEN = "Pony:EaseMob:CacheToken"
_EASE_MOB_CACHE_TIME = 60*30


def generate_ease_mob_id(user_id):
    """
    生成唯一的用户环信账号，每一个项目都是唯一的
    :param user_id: 用户的ID
    """
    ease_mob_id = str(user_id) + SECRET_KEY
    md5obj = hashlib.md5()
    md5obj.update(ease_mob_id.encode('utf-8'))
    return md5obj.hexdigest()


def request_ease_mob_token(use_cache=True):
    if use_cache:
        token = cache.get(_EASE_MOB_CACHE_TOKEN)
        if token:
            return token

    header = {"Content-Type": "application/json"}
    params = {"grant_type": "client_credentials", "client_id": _MOB_CLIENT_ID, "client_secret": _MOB_CLIENT_SECRET}
    request = requests.post(_HTTP_TOKEN_PATH, headers=header, data=json.dumps(params))
    access_token = request.json().get("access_token", None)

    if access_token:
        cache.set(_EASE_MOB_CACHE_TOKEN, access_token, _EASE_MOB_CACHE_TIME)

    return access_token


def register_ease_mob(ease_mob_id):
    access_token = request_ease_mob_token()
    access_token = "Bearer " + access_token

    header = {"Content-Type": "application/json", "Authorization": access_token}
    params = {"username": ease_mob_id, "password": ease_mob_id}
    request = requests.post(_HTTP_REGISTER_PATH, headers=header, data=json.dumps(params))
    if request.status_code == 200:
        return True
    else:
        return False
