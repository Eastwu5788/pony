from django.shortcuts import render
from app.modules.common.auth import login_required
from app.modules.common.struct import base_result

from app.models.blog.article import BlogArticle


@login_required
def home_recommend_handler(request):
    result = base_result()
    if request.method == "GET":
        article_id = request.GET.get("article_id")
        result["data"] = BlogArticle.query_article_by_id(article_id)
        result["operator"] = request.META["user_info"]
        return render(request, "manage/recommend.html", result)
    pass
