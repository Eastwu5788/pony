from django.shortcuts import render
from app.modules.common.struct import *


def life_index_handler(request):
    result = base_result()
    data = dict()

    data["section_info"] = "3"

    result["data"] = data
    return render(request, "life/life.html", result)
