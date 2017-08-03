from django.db import models
from app.models.blog.kind import BlogKind


class BlogArticle(models.Model):

    user_id = models.IntegerField()
    kind_id = models.IntegerField()
    title = models.CharField()
    content = models.CharField()
    status = models.IntegerField()
    created_time = models.CharField()
    updated_time = models.CharField()

    @staticmethod
    def query_articles_list(start=0, per_page=10):
        obj_list = BlogArticle.objects.filter(status=1).all().order_by('-id')[start:per_page]
        format_list = BlogArticle.format_articles(obj_list)
        return format_list

    @staticmethod
    def query_article_by_id(article_id=0, cache=True):
        article = BlogArticle.objects.get(id=article_id)
        return BlogArticle.format_article(article)

    @staticmethod
    def format_articles(article_list):
        """
        格式化文章列表
        """
        result = []
        if not article_list:
            return result

        for obj in article_list:
            format_obj = BlogArticle.format_article(obj)
            result.append(format_obj)

        return result

    @staticmethod
    def format_article(article):
        """
        格式化单个文章
        :type article: BlogArticle
        """
        result = dict()

        result["id"] = article.id
        result["kind_info"] = BlogKind.query_format_kind(article.kind_id)
        result["title"] = article.title
        result["content"] = article.content
        result["created_time"] = article.created_time

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "blog_article"
