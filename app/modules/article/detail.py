import mistune

from django.shortcuts import render

from app.models.blog.article import BlogArticle
from app.modules.common.struct import base_result


def article_detail_handler(request, article_id):
    result = base_result()
    data = dict()

    renderer = mistune.Renderer(hard_wrap=True, parse_inline_html=True)
    markdown = mistune.Markdown(renderer=renderer)

    article = BlogArticle.query_article_by_id(article_id)
    article["content"] = markdown(article["content"])

    data["article"] = article
    result["data"] = data

    return render(request, "article/detail.html", result)
