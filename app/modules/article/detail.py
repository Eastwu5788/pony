import mistune

from django.shortcuts import render

from app.models.blog.article import BlogArticle


def article_detail_handler(request, article_id):
    result = dict()

    renderer = mistune.Renderer(hard_wrap=True, parse_inline_html=True)
    markdown = mistune.Markdown(renderer=renderer)

    article = BlogArticle.query_article_by_id(article_id)
    article["content"] = markdown(article["content"])

    result["article"] = article
    result["user_info"] = request.META["user_info"]

    return render(request, "article/detail.html", result)
