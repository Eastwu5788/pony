from app.modules.common.auth import login_required
from app.modules.common.struct import *
from app.models.blog.article import BlogArticle
from app.models.blog.like import BlogLike
from app.models.blog.article_meta import BlogArticleMeta


@login_required
def like_edit_handler(request):
    """
    点赞状态编辑 POST
    article_id: 需要点赞的博客ID
    type_id: 编辑类型 1、添加点赞 0、取消点赞
    """
    user_info = request.META["user_info"]
    article_id = eval(request.POST.get("article_id"))
    type_id = eval(request.POST.get("type_id"))

    # 1、检查要处理的动态，是否允许被点赞
    try:
        blog = BlogArticle.objects.get(id=article_id)
        if blog.status == 10:
            return json_fail_response("当前动态已被删除!")
        elif blog.status == 2 or blog.status == 3:
            return json_fail_response("当前动态无法点赞!")
    except BlogArticle.DoesNotExist:
        return json_fail_response("当前动态不存在或已被删除")

    like = BlogLike.query_like_blog(user_info.id, article_id)
    # 2、添加点赞
    if type_id == 1:
        if like:
            return json_fail_response("您已经点过赞了!")
        else:
            BlogLike.insert_like_record(user_info.id, article_id)
            BlogArticleMeta.change_meta_record(article_id, user_info.id, ["like"])
            # 更新文章缓存
            BlogArticle.query_article_by_id(article_id, False)
            # TODO: MongoDB 统计用户点赞、粉丝等信息
            return json_success_response()

    # 3、取消点赞
    elif type_id == 0:
        if like:
            like.status = 0
            like.save()
            # 修改meta统计记录
            BlogArticleMeta.change_meta_record(article_id, user_info.id, ["like"], False)
            # 更新缓存
            BlogArticle.query_article_by_id(article_id, False)
            return json_success_response()
        else:
            return json_fail_response("您当前尚未点赞该动态")
    else:
        return json_fail_response("type_id取值错误")
