from django.shortcuts import render
from app.modules.common.auth import login_required
from app.models.blog.article import BlogArticle
from app.models.account.info import UserInfo
from django.http.response import HttpResponse
import json


def user_info_handler(request, user_id):
    user = request.META["user_info"]

    result = dict()
    result["user_info"] = UserInfo.query_format_info_by_user_id(user.id) if user else None
    result["author"] = None if id == 0 else UserInfo.query_format_info_by_user_id(user_id)
    result["article_list"] = BlogArticle.query_articles_by_user(user_id)

    for article in result["article_list"]:
        if len(article["content"]) > 200:
            article["content"] = article["content"][:200]

    return render(request, "about/user.html", result)


def user_info_api_handler(request):
    user_id = request.GET.get("user_id")
    user_info = UserInfo.query_format_info_by_user_id(user_id)
    return HttpResponse(json.dumps({"user_info": user_info}))


