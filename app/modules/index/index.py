from django.shortcuts import render

from app.models.blog.recommend import HomeRecommend
from app.models.account.info import UserInfo
from app.models.blog.article_meta import BlogArticleMeta
from app.models.blog.article import BlogArticle

PAGE_COUNT = 10


def index_handler(request):
    data = dict()

    data["section_info"] = "1"

    account = request.META["user_info"]
    if account:
        account = UserInfo.query_format_info_by_user_id(account.id)
    data["user_info"] = account

    data["recommend_list"] = HomeRecommend.query_recommend_list(0)
    # 阅读榜单
    data["hit_list"] = get_format_top_article_list(order="hit")
    # 点赞榜单
    data["like_list"] = get_format_top_article_list(order="like")
    # 评论榜单
    data["comment_list"] = get_format_top_article_list(order="comment")
    return render(request, "index/index.html", data)


def get_format_top_article_list(order="hit"):
    """
    查询格式化的榜单信息
    :param order: 排序规则
    """
    query_list = BlogArticleMeta.query_top_list(order)
    hit_top_list = list()
    for meta in query_list:
        article = BlogArticle.query_article_by_id(meta.share_id)
        if article:
            hit_top_list.append(article)
    return hit_top_list
