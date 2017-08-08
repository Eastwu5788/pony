from app.modules.common.auth import *
from app.models.blog.article import BlogArticle
from app.modules.common.struct import *
from app.models.blog.recommend import HomeRecommend


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

        # format article, we need update cache at this time
        article = BlogArticle.query_article_by_id(article.id, False)
        result["data"] = article

        # return
        return HttpResponse(json.dumps(result, cls=DateEncoder))

    else:
        # update article
        BlogArticle.objects.filter(id=article_id).update(title=title, content=content)
        # update cache
        BlogArticle.query_article_by_id(article_id, False)
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
    # update status
    BlogArticle.objects.filter(id=article_id).update(status=1 if status == 1 else 2)
    # update cache
    BlogArticle.query_article_by_id(article_id, False)
    return HttpResponse(json.dumps(result))


@login_required
def delete_article_handler(request):
    if request.method == "GET":
        return json_fail_response("get method is not support!")

    # 0、prepare params
    article_id = request.POST.get("article_id")
    operator = request.META["user_info"]

    # 1、删除文章
    article = BlogArticle.objects.get(id=article_id)

    # 2、检查删除权限
    if article.user_id != operator.id:
        return json_fail_response("您只能删除自己的文章!")

    if article.status == 10:
        return json_fail_response("文章已经被删除了!")

    article.status = 10
    article.save()
    # update article cache
    BlogArticle.query_article_by_id(article_id)
    # 3、删除首页推荐
    HomeRecommend.objects.filter(share_id=article_id).update(status=0)
    return json_success_response()

