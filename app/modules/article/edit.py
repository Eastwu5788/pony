import json
from django.http import HttpResponse
from app.modules.common.auth import *
from app.models.blog.article import BlogArticle
from app.modules.common.struct import base_result
from app.modules.common.encoder import DateEncoder


@login_required
def edit_article_handler(request):

    result = base_result()

    article_id = request.POST.get("article_id")
    title = request.POST.get("title")
    content = request.POST.get("content")

    user_info = request.META["user_info"]

    if article_id == '0':

        # insert new article
        article = BlogArticle()
        article.user_id = user_info.id
        article.kind_id = 1
        article.title = title
        article.content = content
        article.status = 2
        article.save()

        # format article
        article = BlogArticle.query_article_by_id(article.id)
        result["data"] = article

        # return
        return HttpResponse(json.dumps(result, cls=DateEncoder))

    else:

        # update article
        BlogArticle.objects.filter(id=article_id).update(title=title, content=content)
        return HttpResponse(json.dumps(result))


@login_required
def change_article_status_handler(request):
    result = base_result()
    if request.method == "GET":
        result["code"] = 500
        result["message"] = "get method is not supported!"
        return HttpResponse(json.dumps(result))

    article_id = request.POST.get("article_id")
    status = eval(request.POST.get("status"))

    # article = BlogArticle.objects.get(id=article_id)
    # print(article.status)
    # article.status = 1 if status == 1 else 2
    # article.save()
    #
    # print(article.status)

    BlogArticle.objects.filter(id=article_id).update(status=1 if status == 1 else 2)

    return HttpResponse(json.dumps(result))
