
def base_result():
    return {"code": 200, "message": None, "data": None}


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