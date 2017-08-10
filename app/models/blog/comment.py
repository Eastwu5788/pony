from django.db import models
import django.utils.timezone as timezone

from app.models.account.info import UserInfo
from app.models.blog.comment_meta import CommentMeta


class BlogComment(models.Model):

    share_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    reply_id = models.IntegerField(default=0)
    reply_user_id = models.IntegerField(default=0)
    content = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_comment_list(share_id=0, visitor_id=0):
        try:
            comment_list = BlogComment.objects.filter(share_id=share_id, status=1).order_by("-id").all().only("id", "user_id", "reply_id", "content", "created_time")
            result = list()
            for comment in comment_list:
                result.append(BlogComment.format_comment_item(comment, visitor_id=visitor_id))
            return result
        except BlogComment.DoesNotExist:
            return list()

    @staticmethod
    def query_comment_by_id(comment_id, visitor_id=0, need_reply=True):
        try:
            comment = BlogComment.objects.get(id=comment_id)
            return BlogComment.format_comment_item(comment, visitor_id=visitor_id, need_reply=need_reply)
        except BlogComment.DoesNotExist:
            return dict()

    @staticmethod
    def query_comment_reply_list(comment_id, visitor_id=0):
        try:
            reply_list = BlogComment.objects.filter(reply_id=comment_id, status=1).order_by("-id").all()
            result = list()
            for comment in reply_list:
                # 如果是回复，则不需要再查找回复列表
                result.append(BlogComment.format_comment_item(comment, visitor_id=visitor_id, need_reply=False))
            return result
        except BlogComment.DoesNotExist:
            return None

    @staticmethod
    def format_comment_item(comment, visitor_id=0, need_reply=True):
        result = dict()

        result["id"] = comment.id
        result["user_info"] = UserInfo.query_format_info_by_user_id(comment.user_id)
        result["meta_info"] = CommentMeta.get_format_meta(comment.id, visitor_id=visitor_id)
        result["content"] = comment.content

        # 该条评论的回复列表
        if need_reply:
            result["reply_list"] = BlogComment.query_comment_reply_list(comment.id, visitor_id=visitor_id)
        else:
            result["reply_list"] = None

        # 该条评论的回复信息
        result["reply_info"] = None if comment.reply_id == 0 else BlogComment.query_comment_by_id(comment.reply_id, visitor_id, False)

        result["created_time"] = str(comment.created_time.strftime("%Y %b %d %H:%M"))

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "blog_comment"
