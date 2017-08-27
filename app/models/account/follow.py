from django.db import models
from django.db.models import Count
from django.core.cache import cache
import django.utils.timezone as timezone

CACHE_FOLLOW_COUNT_KEY = "Pony:UserFollow:FollowCount:"
CACHE_FANS_COUNT_KEY = "Pony:UserFollow:FansCount:"
CACHE_COUNT_TIME = 60*60


class UserFollow(models.Model):

    user_id = models.IntegerField(default=0)
    follow_user = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_user_relation(user_id, follow_user):
        """查询用户是user_id与另外一个用户follow_user的关系，查询主角是user_id"""
        # 如果用户未登录，则双方无关系
        if user_id == 0:
            return 0

        # 查询用户是否关注了follow_user
        if user_id == follow_user:
            return 0

        try:
            follow = UserFollow.objects.order_by("-id").filter(user_id=user_id, follow_user=follow_user, status=1).first()
        except UserFollow.DoesNotExist:
            follow = None

        try:
            fans = UserFollow.objects.order_by("-id").filter(user_id=follow_user, follow_user=user_id, status=1).first()
        except UserFollow.DoesNotExist:
            fans = None

        # 即关注了对方，对方也关注了我
        if follow and fans:
            return 3

        # 我关注了对方，对方没有关注我 （我是对方的粉丝）
        if follow and not fans:
            return 1

        # 我没有关注对方，但是对方关注了我（对方是我的粉丝）
        if fans and not follow:
            return 2

        # 双方无关系
        return 0

    @staticmethod
    def query_user_meta_count(user_id, is_follow=True, use_cache=True):
        """
        查询用户的关注数量或者粉丝数量
        :param user_id: 需要查询的用户ID
        :param is_follow: 如果是True表示查询的是关注列表否则是粉丝
        :param use_cache: 是否启用缓存
        """
        cache_key = CACHE_FANS_COUNT_KEY + str(user_id)
        if is_follow:
            cache_key = CACHE_FOLLOW_COUNT_KEY + str(user_id)

        if use_cache:
            count = cache.get(cache_key)
            if count:
                return count

        if is_follow:
            count = UserFollow.objects.filter(user_id=user_id, status=1).aggregate(Count("id"))
        else:
            count = UserFollow.objects.filter(follow_user=user_id, status=1).aggregate(Count("id"))

        count = count["id__count"]
        cache.set(cache_key, count, CACHE_COUNT_TIME)

        return count

    class Meta:
        app_label = "b_account"
        db_table = "user_follow"




