from app.modules.common.util_struct import *
from app.modules.common.auth import login_required

from app.models.blog.comment import BlogComment
from app.models.blog.comment_meta import CommentMeta


@login_required
def comment_reply_handler(request):

    if request.method == "GET":
        return json_fail_response("get method is not supported")

    comment_id = request.POST.get("comment_id")
    reply_content = request.POST.get("content")
    reply_add = eval(request.POST.get("reply_add"))

    if len(reply_content) == 0:
        return json_fail_response("回复内容不能为空!")

    try:
        comment = BlogComment.objects.get(id=comment_id)
        if comment.status == 0:
            return json_fail_response("该条评论已被删除!")
    except BlogComment.DoesNotExist:
        return json_fail_response("您回复的评论不存在")

    reply_comment = None
    if reply_add == 1:
        try:
            reply_comment = BlogComment.objects.get(id=comment.reply_id)
            if reply_comment.status == 0:
                return json_fail_response("该条评论已被删除!")
        except BlogComment.DoesNotExist:
            return json_fail_response("您回复的评论不存在")

    account = request.META["user_info"]

    new_comment = BlogComment(user_id=account.id, reply_id=comment_id)
    new_comment.reply_id = comment.id if not reply_comment else reply_comment.id
    new_comment.reply_user_id = comment.user_id if not reply_comment else reply_comment.user_id
    new_comment.content = reply_content
    new_comment.status = 1
    new_comment.save()

    # 修改评论meta
    CommentMeta.edit(reply_comment.id if reply_comment else comment_id, ["comment"])

    return json_success_response()

