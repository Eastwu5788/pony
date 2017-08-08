from django.db import models
from django.core.cache import cache
import django.utils.timezone as timezone


CACHE_KEY_ID = "Pony:BlogArticleMeta:CacheId:"
CACHE_TIME = 60*60*24


class BlogArticleMeta(models.Model):

    share_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    hit = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_article_meta_info(share_id, use_cache=True):
        key = CACHE_KEY_ID+str(share_id)
        if use_cache:
            meta = cache.get(key)
            if meta:
                return meta
        try:
            meta = BlogArticleMeta.objects.filter(status=1).get(share_id=share_id)
            meta = BlogArticleMeta.format_article_meta_info(meta)
            cache.set(key, meta, CACHE_TIME)
            return meta
        except BlogArticleMeta.DoesNotExist:
            return BlogArticleMeta.format_article_meta_info()

    @staticmethod
    def format_article_meta_info(meta=None):
        result = {"hit": 0, "like": 0, "comment": 0, "liked": 0}
        if not meta:
            return result

        result["hit"] = meta.hit
        result["like"] = meta.like
        result["comment"] = meta.comment
        return result

    @staticmethod
    def change_meta_record(share_id, user_id, meta=list(), meta_add=True):
        """
        添加一条记录
        :param share_id: 动态文章的ID
        :param user_id: 文章作者的ID
        :param meta: 需要修改的字段
        :param meta_add: 是否是增加记录
        """
        if len(meta) == 0:
            return

        try:
            blog = BlogArticleMeta.objects.filter(share_id=share_id, user_id=user_id, status=1).get()
        except BlogArticleMeta.DoesNotExist:
            if not meta_add:
                return
            blog = BlogArticleMeta(share_id=share_id, user_id=user_id, status=1)

        # change meta count
        if "hit" in meta:
            if meta_add:
                blog.hit += 1
            else:
                blog.hit -= 1
        if "like" in meta:
            if meta_add:
                blog.like += 1
            else:
                blog.like -= 1
        if "comment" in meta:
            if meta_add:
                blog.comment += 1
            else:
                blog.comment -= 1

        blog.save()
        # 更新缓存
        BlogArticleMeta.query_article_meta_info(share_id, False)

    class Meta:
        app_label = "b_blog"
        db_table = "blog_article_meta"
