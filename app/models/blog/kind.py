from django.db import models
import django.utils.timezone as timezone


class BlogKind(models.Model):

    user_id = models.IntegerField(default=0)
    title = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_user_kind(user_id=0, cache=True):
        kind_list = BlogKind.objects.filter(user_id=user_id, status=1).all()
        result = []

        for kind in kind_list:
            result.append(BlogKind.format_kind_info(kind))

        return result

    @staticmethod
    def query_format_kind(kind_id=0, cache=True):
        obj = BlogKind.objects.get(id=kind_id)
        if not obj:
            return {}
        return BlogKind.format_kind_info(obj)

    @staticmethod
    def format_kind_info(kind):
        result = dict()
        result["kind_id"] = kind.id
        result["title"] = kind.title
        result["created_time"] = kind.created_time
        return result

    class Meta:
        app_label = "b_blog"
        db_table = "blog_kind"
