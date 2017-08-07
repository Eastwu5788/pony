from django.shortcuts import render

from app.models.blog.article import BlogArticle
from app.models.blog.recommend import HomeRecommend
from app.models.account.info import UserInfo
from app.modules.common.struct import *


PAGE_COUNT = 10


def index_handler(request):
    data = dict()

    data["section_info"] = "1"

    account = request.META["user_info"]
    if account:
        account = UserInfo.query_format_info_by_user_id(account.id)
    data["user_info"] = account

    data["recommend_list"] = HomeRecommend.query_recommend_list(0)

    return render(request, "index/index.html", data)




