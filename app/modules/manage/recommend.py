from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from app.modules.common.auth import login_required
from app.modules.common.struct import base_result
from app.modules.common.upload import UploadImage

from app.models.blog.article import BlogArticle
from app.models.blog.recommend import HomeRecommend

@login_required
def home_recommend_handler(request):
    result = base_result()

    operator = request.META["user_info"]

    if request.method == "GET":
        article_id = request.GET.get("article_id")
        result["data"] = BlogArticle.query_article_by_id(article_id)
        result["operator"] = operator
        return render(request, "manage/recommend.html", result)

    image_list = UploadImage(request).save()
    article_id = request.POST.get("article_id")
    introl = request.POST.get("intro")
    weight = request.POST.get("weight")

    # TODO:参数检测

    recommend = HomeRecommend()
    recommend.share_id = article_id
    recommend.reco_cover = image_list[0].id
    recommend.reco_intro = introl
    recommend.weight = weight
    recommend.operator_id = operator.id
    recommend.status = 1
    recommend.save()

    return HttpResponseRedirect("/manage")
