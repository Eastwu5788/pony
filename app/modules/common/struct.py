import json
from django.http import HttpResponse
from app.modules.common.encoder import DateEncoder


def base_result():
    return {"code": 200, "message": None, "data": None}


def json_success_response(result=None):
    """
    请求成功的响应
    """
    _result = base_result()
    _result["message"] = "成功"
    _result["data"] = result
    return json_response(_result)


def json_fail_response(message="请求失败", code=500):
    """
    请求失败的响应
    """
    _result = base_result()
    _result["code"] = code
    _result["message"] = message
    return json_response(_result)


def json_response(result):
    """
    返回JSON响应
    """
    return HttpResponse(json.dumps(result, cls=DateEncoder))








def check_request_params(request, rules):

    rules_method = rules.get("method")
    if rules_method != request.method:
        return None

    if request.method == "GET":
        return check_get_params(request, rules)
    else:
        return check_post_params(request, rules)


def check_upload_params(params, rules):
    pass


def check_get_params(request, params):
    result = dict()

    for key, value in enumerate(params):
        upload_params = request.GET.get(key, None)
        check_upload_params(upload_params, value)

    return result


def check_post_params(request, params):
    pass
