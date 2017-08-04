from django.db import models
from app.models.blog.kind import BlogKind
from app.models.account.account import UserAccount


class BlogArticle(models.Model):

    user_id = models.IntegerField(default=0)
    kind_id = models.IntegerField(default=0)
    title = models.CharField(default='')
    content = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    @staticmethod
    def query_all_articles_list(start=0, per_page=10):
        obj_list = BlogArticle.objects.exclude(status=10).all().order_by('-id')[start:per_page]
        format_list = BlogArticle.format_articles(obj_list)
        return format_list

    @staticmethod
    def query_published_articles_list(start=0, per_page=10):
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
        result["user_info"] = UserAccount.query_format_user(article.user_id)
        result["kind_info"] = BlogKind.query_format_kind(article.kind_id)
        result["title"] = article.title
        result["content"] = article.content
        result["status"] = article.status
        result["created_time"] = str(article.created_time.strftime("%Y-%b-%d %H:%M:%S"))

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "blog_article"
