from django.db import models


class BlogComment(models.Model):

    share_id = models.IntegerField()
    user_id = models.IntegerField()
    reply_id = models.IntegerField()
    content = models.CharField()
    status = models.IntegerField()
    created_time = models.CharField()
    updated_time = models.CharField()

    class Meta:
        app_label = "b_blog"
        db_table = "blog_comment"
