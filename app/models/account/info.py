from django.db import models
from django.core.cache import cache
import django.utils.timezone as timezone

from app.models.blog.image import Image
from app.models.account.follow import UserFollow
import app.models.blog.article


CACHE_KEY = "Pony:UserInfo:Cache:"
CACHE_EASE_MOB_KEY = "Pony:UserEaseMob:Cache:"
CACHE_TIME = 60*60*24


class UserInfo(models.Model):

    user_id = models.IntegerField(default=0)
    ease_mob = models.CharField(default='')
    role_id = models.IntegerField(default=0)
    nick_name = models.CharField(default='')
    gender = models.IntegerField(default=0)
    avatar = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_format_info_by_ease_mob(ease_mob, use_cache=True):
        """
        查询格式化的用户信息，根据用户环信
        """
        key = CACHE_EASE_MOB_KEY + ease_mob
        if use_cache:
            result = cache.get(key)
            if result:
                return result

        try:
            user_info = UserInfo.objects.get(ease_mob=ease_mob)
            format_user_info = UserInfo.format_user_info(user_info)
            cache.set(key, format_user_info, CACHE_TIME)
            return format_user_info
        except UserInfo.DoesNotExist:
            return None

    @staticmethod
    def query_format_info_by_user_id(user_id, use_cache=True):
        """
        根据用户ID查询用户信息
        :param user_id: 用户ID
        :param use_cache: 是否使用缓存
        """
        key = CACHE_KEY + str(user_id)
        if use_cache:
            result = cache.get(key)
            if result:
                return result

        try:
            user_info = UserInfo.objects.get(user_id=user_id)
            format_user_info = UserInfo.format_user_info(user_info)
            cache.set(key, format_user_info, CACHE_TIME)
            return format_user_info
        except UserInfo.DoesNotExist:
            return None

    @staticmethod
    def format_user_info(user_info):
        result = dict()
        result["id"] = user_info.user_id
        result["ease_mob"] = user_info.ease_mob
        result["nick_name"] = user_info.nick_name
        result["gender"] = user_info.gender
        result["avatar"] = Image.query_image_by_id(user_info.avatar)
        result["fans"] = UserFollow.query_user_meta_count(user_info.user_id, False)
        result["follows"] = UserFollow.query_user_meta_count(user_info.user_id)
        result["articles"] = app.models.blog.article.BlogArticle.query_published_article_count(user_id=user_info.user_id)
        return result

    class Meta:
        app_label = "b_account"
        db_table = "user_info"
