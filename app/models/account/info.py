import hashlib
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
    def query_user_by_nick_name(nick_name):
        try:

            user_list = UserInfo.objects.filter(nick_name__contains=nick_name).order_by("-id")[:10]
            result = list()
            for user in user_list:
                result.append(UserInfo.format_user_info(user))
            return result

        except UserInfo.DoesNotExist:
            return []

    @staticmethod
    def query_user_role(user_id):
        """
        查询用户角色
        不要使用缓存
        """
        try:
            user_info = UserInfo.objects.filter(user_id=user_id, status=1).get()
            return user_info.role_id
        except UserInfo.DoesNotExist:
            return 0

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

        # 生成用户头像
        avatar = Image.query_image_by_id(user_info.avatar)
        if not avatar:
            avatar = user_info.generate_gr_avatar()
        result["avatar"] = avatar

        result["fans"] = UserFollow.query_user_meta_count(user_info.user_id, False)
        result["follows"] = UserFollow.query_user_meta_count(user_info.user_id)
        result["articles"] = app.models.blog.article.BlogArticle.query_published_article_count(user_id=user_info.user_id)
        return result

    def generate_gr_avatar(self):
        """
        生成 http://www.gravatar.com的默认头像
        """
        import app.models.account.account as account
        user_account = account.UserAccount.query_user_by_id(self.user_id)
        md5 = hashlib.md5()
        md5.update(user_account.email.strip().lower().encode("utf-8"))
        md5 = md5.hexdigest()
        base_url = "https://www.gravatar.com/avatar/"+md5+"?d=retro&r=PG"
        result = dict()
        result["image_o"] = base_url + "&s=200"
        result["image_a"] = base_url + "&s=100"
        result["image_width"] = 200
        result["image_height"] = 200
        return result

    class Meta:
        app_label = "b_account"
        db_table = "user_info"
