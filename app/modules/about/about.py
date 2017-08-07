from django.shortcuts import render


def about_index_handler(request):
    return render(request, "about/about.html")
