from django.db import models
import django.utils.timezone as timezone


class BlogLike(models.Model):

    share_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_like_blog(user_id, share_id):
        """
        查询某人是否点赞了某条动态
        """
        try:
            blog = BlogLike.objects.filter(user_id=user_id, share_id=share_id, status=1).order_by("-id").get()
            return blog
        except BlogLike.DoesNotExist:
            return None

    @staticmethod
    def insert_like_record(user_id, share_id):
        """
        添加一条点赞动态
        """
        blog_like = BlogLike()
        blog_like.share_id = share_id
        blog_like.user_id = user_id
        blog_like.status = 1
        blog_like.save()
        return blog_like

    class Meta:
        app_label = "b_blog"
        db_table = "blog_like"
