import mistune
import json
from django.http import HttpResponse
from app.modules.common.util_struct import *


def apply_markdown(request):
    result = base_result()

    ori_str = request.POST.get("ori_str", None)
    if ori_str:
        result["code"] = 200
        result["data"] = markdown_engin(ori_str)
    else:
        result["code"] = 500

    return HttpResponse(json.dumps(result))


def markdown_engin(ori_str=""):
    renderer = mistune.Renderer(hard_wrap=True, parse_inline_html=True)
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(ori_str)