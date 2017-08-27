from django.shortcuts import render
from app.models.blog.article import BlogArticle
from app.models.account.info import UserInfo
from app.models.account.follow import UserFollow
from app.modules.common.util_struct import *
from django.http.response import HttpResponse
import json


def user_info_handler(request, user_id):
    user = request.META["user_info"]

    result = dict()
    result["user_info"] = UserInfo.query_format_info_by_user_id(user.id) if user else None
    result["author"] = None if user_id == 0 else UserInfo.query_format_info_by_user_id(user_id)
    result["article_list"] = BlogArticle.query_articles_by_user(user_id)

    # 查询双方的关系
    if user_id != 0 and user:
        result["author"]["relation"] = UserFollow.query_user_relation(user.id, user_id)
    else:
        result["author"]["relation"] = 0

    for article in result["article_list"]:
        if len(article["content"]) > 200:
            article["content"] = article["content"][:200]

    return render(request, "about/user.html", result)


def user_info_api_handler(request):
    user_id = request.GET.get("user_id")
    user_info = UserInfo.query_format_info_by_user_id(user_id)
    return HttpResponse(json.dumps({"user_info": user_info}))


def user_info_api_by_ease_mob_handler(request):
    ease_mob = request.GET.get("ease_mob")
    user_info = UserInfo.query_format_info_by_ease_mob(ease_mob)
    return HttpResponse(json.dumps({"user_info": user_info}))


def user_search_api(request):

    nick_name = request.GET.get("nick_name")
    if not nick_name:
        return json_fail_response("搜索内容不能为空")

    user_list = UserInfo.query_user_by_nick_name(nick_name)
    return json_success_response(user_list)
