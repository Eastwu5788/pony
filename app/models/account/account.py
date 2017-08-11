from django.db import models
from django.core.cache import cache
from app.models.account.info import UserInfo
import django.utils.timezone as timezone


CACHE_KEY = "Pony:UserAccount:CacheId:"
CACHE_EMAIL_KEY = "Pony:UserAccount:CacheEmail:"
CACHE_TIME = 60*60*24


class UserAccount(models.Model):

    user_name = models.CharField(default='')
    mobile = models.CharField(default='')
    email = models.CharField(default='')
    password = models.CharField(default='')
    type = models.IntegerField(default=0)
    open_id = models.CharField(default='')
    banned = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_account_by_email(email, use_cache=True):
        key = CACHE_EMAIL_KEY+email
        if use_cache:
            account = cache.get(key)
            if account:
                return account
        try:
            account = UserAccount.objects.get(email=email)
            cache.set(key, account, CACHE_TIME)
            return account
        except UserAccount.DoesNotExist:
            return None

    @staticmethod
    def query_user_by_id(user_id=0, use_cache=True):
        """
        查询用户账户信息
        :param user_id: 用户的ID
        :param use_cache: 是否启用缓存
        """
        key = CACHE_KEY+str(user_id)
        if use_cache:
            account = cache.get(key)
            if account:
                return account
        try:
            account = UserAccount.objects.get(id=user_id)
            cache.set(key, account, CACHE_TIME)
            return account
        except UserAccount.DoesNotExist:
            return None

    @staticmethod
    def query_format_user(user_id=0, use_cache=True):
        """
        获取格式化的用户账户信息
        """
        user = UserAccount.query_user_by_id(user_id, use_cache)
        return UserAccount.format_user(user)

    @staticmethod
    def format_user(user):
        result = UserInfo.query_format_info_by_user_id(user.id)
        return result

    class Meta:
        app_label = "b_account"
        db_table = "user_account"
