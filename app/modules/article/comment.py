from app.modules.common.struct import *
from app.modules.common.auth import login_required

from app.models.blog.article import BlogArticle
from app.models.blog.comment import BlogComment
from app.models.blog.article_meta import BlogArticleMeta


@login_required
def comment_add_handler(request):
    if request.method == "GET":
        return json_fail_response("get method is not supported!")

    account = request.META["user_info"]
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")

    try:
        article = BlogArticle.objects.get(id=article_id)
        if article.status != 1:
            return json_fail_response("当前文章无法评论")
    except BlogArticle.DoesNotExist:
        return json_fail_response("文章不存在")

    # 添加评论记录
    comment = BlogComment(share_id=article_id, user_id=account.id, content=content, status=1)
    comment.save()

    # 添加评论数量记录
    BlogArticleMeta.change_meta_record(article_id, account.id, ["comment"])
    return json_success_response()
