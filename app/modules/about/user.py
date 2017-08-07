from django.shortcuts import render
from app.modules.common.auth import login_required
from app.models.blog.article import BlogArticle
from app.models.account.info import UserInfo


@login_required
def user_info_handler(request):
    user = request.META["user_info"]

    result = dict()
    result["user_info"] = UserInfo.query_format_info_by_user_id(user.id)
    result["article_list"] = BlogArticle.query_articles_by_user(user.id)

    for article in result["article_list"]:
        if len(article["content"]) > 200:
            article["content"] = article["content"][:200]

    return render(request, "about/user.html", result)
