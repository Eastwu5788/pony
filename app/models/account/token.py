from django.db import models
from django.core.cache import cache
from app.modules.common.secret import get_seed
import django.utils.timezone as timezone

CACHE_TOKEN_ID = "Pony:AccessToken:CacheId:"
CACHE_TOKEN = "Pony:AccessToken:CacheToken:"
CACHE_TIME = 60*60*24


class AccessToken(models.Model):

    user_id = models.IntegerField(default=0)
    access_token = models.CharField(default='')
    salt = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_token_by_user_id(user_id, use_cache=True):
        """
        根据用户的ID查询用户的Token
        :param user_id: 用户ID
        :param use_cache: 是否启用缓存
        """
        key = CACHE_TOKEN_ID+str(user_id)
        if use_cache:
            token = cache.get(key)
            if token:
                return token
        try:
            token = AccessToken.objects.order_by("-id").filter(status=1).get(user_id=user_id)
            cache.set(key, token, CACHE_TIME)
            return token
        except AccessToken.DoesNotExist:
            return None

    @staticmethod
    def query_token(token, use_cache=True):
        """
        根据用户token查询用户信息
        """
        key = CACHE_TOKEN+token
        if use_cache:
            token_result = cache.get(key)
            if token_result:
                return token_result

        try:
            token = AccessToken.objects.order_by("-id").filter(status=1).get(access_token=token)
            cache.set(key, token, CACHE_TIME)
            return token
        except AccessToken.DoesNotExist:
            return None

    @staticmethod
    def create_new_toke(user_id):
        token = AccessToken()
        token.user_id = user_id
        token.access_token = get_seed(str(user_id))
        token.salt = get_seed(str(user_id), 10)
        token.status = 1
        token.save()
        return token

    class Meta:
        app_label = "b_account"
        db_table = "user_access_token"
