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
        if count:
            cache.set(cache_key, count, CACHE_COUNT_TIME)

        return count

    class Meta:
        app_label = "b_account"
        db_table = "user_follow"




