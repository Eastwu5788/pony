from django.db import models
from app.models.blog.kind import BlogKind
from app.models.account.account import UserAccount
from app.models.blog.article_meta import BlogArticleMeta
import django.utils.timezone as timezone


class BlogArticle(models.Model):

    user_id = models.IntegerField(default=0)
    kind_id = models.IntegerField(default=0)
    title = models.CharField(default='')
    content = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_articles_by_user(user_id, start=0, per_page=10):
        """
        查询某一个人的所有文章
        :param user_id: 用户的ID
        :param start: 开始页
        :param per_page: 分页数量
        """
        try:
            obj_list = BlogArticle.objects.exclude(status=10).filter(user_id=user_id).order_by('-id').all()[start:per_page]
            return BlogArticle.format_articles(obj_list)
        except BlogArticle.DoesNotExist:
            return []

    @staticmethod
    def query_all_articles_list(start=0, per_page=10):
        """
        查询所有的文章列表
        :param start: 开始页
        :param per_page: 分页数量
        """
        obj_list = BlogArticle.objects.exclude(status=10).all().order_by('-id')[start:per_page]
        format_list = BlogArticle.format_articles(obj_list)
        return format_list

    @staticmethod
    def query_published_articles_list(start=0, per_page=10):
        """
        查询所有公开文章列表
        :param start: 开始页
        :param per_page: 分页数量
        """
        obj_list = BlogArticle.objects.filter(status=1).all().order_by('-id')[start:per_page]
        format_list = BlogArticle.format_articles(obj_list)
        return format_list

    @staticmethod
    def query_article_by_id(article_id=0, cache=True):
        """
        根据文章ID查询某一篇文章
        :param article_id: 文章ID
        :param cache: 是否启用缓存
        """
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
        result["meta_info"] = BlogArticleMeta.query_article_meta_info(article.id)
        result["title"] = article.title
        result["content"] = article.content
        result["status"] = article.status
        result["created_time"] = str(article.created_time.strftime("%Y-%b-%d %H:%M:%S"))

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "blog_article"
