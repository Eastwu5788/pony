from django.shortcuts import render
from app.models.blog.recommend import HomeRecommend
from app.models.blog.article import BlogArticle
from app.modules.common.struct import *
from app.modules.common.auth import login_required


@login_required
def manage_handler(request):
    result = base_result()

    data = dict()
    data["home_recommend"] = HomeRecommend.query_recommend_list(0)
    data["blog_list"] = get_blog_list()
    result["data"] = data

    return render(request, "manage/index.html", result)


def get_blog_list():
    blog_list = BlogArticle.query_all_articles_list(0)
    for blog in blog_list:
        recommend = HomeRecommend.query_recommend_by_share_id(blog["id"])
        blog["recommend"] = 1 if recommend else 0
    return blog_list
