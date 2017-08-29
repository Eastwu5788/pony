from app.modules.common.util_struct import *
from app.modules.common.auth import login_required
from app.modules.common.logger import add_error_log

from app.models.blog.article import BlogArticle
from app.models.blog.comment import BlogComment
from app.models.blog.article_meta import BlogArticleMeta
from app.models.blog.comment_like import CommentLike
from app.models.blog.comment_meta import CommentMeta


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
    BlogArticleMeta.change_meta_record(article_id, article.user_id, ["comment"])
    # 更新文章
    BlogArticle.query_article_by_id(article_id, False)
    return json_success_response()


@login_required
def comment_like_edit_handler(request):
    """
    评论点赞的处理
    """
    if request.method == "GET":
        return json_fail_response("get method is not supported!")

    comment_id = request.POST.get("comment_id")
    edit_type = eval(request.POST.get("type"))

    # 1、检查是否可以进行该操作
    # 1.1 检查评论
    try:
        comment = BlogComment.objects.get(id=comment_id)
    except BlogComment.DoesNotExist:
        return json_fail_response("该条评论不存在")

    if comment.status == 0:
        return json_fail_response("当前评论已被删除")
    # 1.2 检查动态
    try:
        article = BlogArticle.objects.get(id=comment.share_id)
        if article.status != 1:
            return json_fail_response("当前动态不无法操作！")
    except BlogArticle.DoesNotExist:
        """评论存在，但是动态不存在，是奇怪的现象！需要添加error_log"""
        # TODO: 数据库数据出错log
        add_error_log(561, {"comment_id": comment_id, "share_id": comment.share_id})
        return json_fail_response("数据错误!")

    # 执行操作
    user = request.META["user_info"]
    try:
        comment_like = CommentLike.objects.filter(status=1).get(comment_id=comment_id, user_id=user.id)
    except CommentLike.DoesNotExist:
        comment_like = None

    if edit_type == 1:
        """添加点赞"""
        if comment_like:
            return json_fail_response("您当前已经点过赞了")
        else:
            CommentLike.add_comment_like(comment_id, user.id)
            meta = CommentMeta.get(comment_id)
            if meta:
                meta.like += 1
            else:
                meta = CommentMeta(comment_id, like=1)
            meta.save()
            return json_success_response()

    elif edit_type == 0:
        """取消点赞"""
        if not comment_like:
            return json_fail_response("您当前尚未点赞")
        comment_like.status = 0
        comment_like.save()

        meta = CommentMeta.get(comment_id)
        if meta:
            meta.like -= 1
        else:
            meta = CommentMeta(comment_id)
        meta.save()
        return json_success_response()
    else:
        return json_fail_response("type参数错误!")


