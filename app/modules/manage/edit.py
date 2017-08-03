from django.shortcuts import render


def edit_article_handler(request):
    """
    编辑文章 处理模块
    """

    return render(request, "manage/edit.html", None)
