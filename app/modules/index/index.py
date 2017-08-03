from django.shortcuts import render

from app.models.blog.article import BlogArticle
from app.models.blog.recommend import HomeRecommend
from app.modules.common.struct import BASE_RESULT


PAGE_COUNT = 10


def index_handler(request):
    result = BASE_RESULT
    data = dict()

    data["section_info"] = "1"
    data["user_info"] = None
    data["recommend_list"] = HomeRecommend.query_recommend_list(0)

    result["data"] = data
    return render(request, "index/index.html", result)




