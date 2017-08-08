from app.modules.common.struct import *
from app.modules.common.auth import login_required


def logout_handler(request):
    pass


@login_required
def logout_api_handler(request):
    if request.method == "GET":
        return json_fail_response("不支持GET请求")

    request.session["access_token"] = None
    return json_success_response()

