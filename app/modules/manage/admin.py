from django.shortcuts import render
from app.models.blog.recommend import HomeRecommend
from app.models.blog.article import BlogArticle
from app.models.account.info import UserInfo
from app.modules.common.auth import login_required


@login_required
def manage_handler(request):

    result = dict()
    result["home_recommend"] = HomeRecommend.query_recommend_list(0)
    result["blog_list"] = get_blog_list()
    result["user_info"] = UserInfo.query_format_info_by_user_id(request.META["user_info"].id)

    return render(request, "manage/index.html", result)


def get_blog_list():
    blog_list = BlogArticle.query_all_articles_list(0)
    for blog in blog_list:
        recommend = HomeRecommend.query_recommend_by_share_id(blog["id"])
        blog["recommend"] = 1 if recommend else 0
    return blog_list
