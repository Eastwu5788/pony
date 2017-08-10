import mistune

from django.shortcuts import render

from app.models.blog.article import BlogArticle
from app.models.blog.like import BlogLike
from app.models.blog.article_meta import BlogArticleMeta
from app.models.blog.comment import BlogComment
from app.models.account.account import UserInfo

import json

def article_detail_handler(request, article_id):
    account = request.META["user_info"]
    result = dict()

    renderer = mistune.Renderer(hard_wrap=True, parse_inline_html=True)
    markdown = mistune.Markdown(renderer=renderer)

    article = BlogArticle.query_article_by_id(article_id)
    article["content"] = markdown(article["content"])
    article["comment_list"] = BlogComment.query_comment_list(article_id, account.id if account else 0)
    print(json.dumps(article["comment_list"]))
    result["article"] = article

    if account:
        article["meta_info"]["liked"] = 1 if BlogLike.query_like_blog(account.id, article_id) else 0
        result["user_info"] = UserInfo.query_format_info_by_user_id(request.META["user_info"].id)

    # 添加访问记录 匿名访问、非本人访问，会添加一条访问记录
    author_id = article["user_info"]["id"]
    if not account or author_id != account.id:
        BlogArticleMeta.change_meta_record(article_id, author_id, ["hit"])

    return render(request, "article/detail.html", result)


