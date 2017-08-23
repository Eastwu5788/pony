import mistune
from django.shortcuts import render
from app.modules.common.util_struct import *
from app.models.blog.article import BlogArticle
from app.models.blog.kind import BlogKind
from app.modules.common.auth import *


@login_required
def edit_article_handler(request, article_id):
    """
    编辑文章 处理模块
    """
    result = base_result()

    if article_id != "0":
        result["data"] = BlogArticle.query_article_by_id(article_id)

        renderer = mistune.Renderer(hard_wrap=True, parse_inline_html=True)
        markdown = mistune.Markdown(renderer=renderer)

        result["mark_down"] = markdown(result["data"]["content"])
    else:
        result["mark_down"] = None
        del result["data"]

    result["kind_list"] = BlogKind.query_user_kind(1)

    return render(request, "manage/edit.html", result)
