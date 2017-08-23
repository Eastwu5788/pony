from django.shortcuts import render
from app.modules.common.util_struct import *


def technology_handler(request):
    result = base_result()
    data = dict()

    data["section_info"] = "2"

    result["data"] = data
    return render(request, "technology/skill.html", result)
