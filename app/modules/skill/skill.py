from django.shortcuts import render
from app.modules.common.struct import BASE_RESULT


def technology_handler(request):
    result = BASE_RESULT
    data = dict()

    data["section_info"] = "2"

    result["data"] = data
    return render(request, "technology/skill.html", result)
