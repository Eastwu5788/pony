from django.db import models


class BlogArticleMeta(models.Model):

    share_id = models.IntegerField()
    user_id = models.IntegerField()
    hit = models.IntegerField()
    like = models.IntegerField()
    comment = models.IntegerField()
    status = models.IntegerField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    class Meta:
        app_label = "b_blog"
        db_table = "blog_article_meta"
