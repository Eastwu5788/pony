from django.shortcuts import render
from app.modules.common.struct import BASE_RESULT


def life_index_handler(request):
    result = BASE_RESULT
    data = dict()

    data["section_info"] = "3"

    result["data"] = data
    return render(request, "life/life.html", result)
