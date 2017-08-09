from django.db import models
import django.utils.timezone as timezone


class CommentLike(models.Model):

    comment_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def add_comment_like(comment_id=0, user_id=0):
        """增加一条点赞记录"""
        like = CommentLike(comment_id=comment_id, user_id=user_id,status=1)
        like.save()
        return like

    @staticmethod
    def user_liked(comment_id=0, user_id=0):
        """查询某人是否点赞了评论"""
        try:
            like = CommentLike.objects.filter(status=1).get(comment_id=comment_id, user_id=user_id)
            return like
        except CommentLike.DoesNotExist:
            return None

    class Meta:
        app_label = "b_blog"
        db_table = "comment_like"
