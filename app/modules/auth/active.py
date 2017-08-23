from django.shortcuts import redirect

from app.models.account.account import UserAccount
from app.models.account.token import AccessToken
from app.models.account.info import UserInfo
from app.modules.common.util_struct import *
from app.modules.common.secret import verify_password
from app.modules.common.easemob import register_ease_mob


def active_account_handler(request):
    token = request.GET.get("access_token")
    pass_port = request.GET.get("pass_port")

    try:
        access_token = AccessToken.objects.get(access_token=token)
        if not verify_password(access_token.access_token+access_token.salt, pass_port):
            return json_fail_response("无效的用户请求")

        if access_token.status == 0:
            return json_fail_response("token失效")

    except AccessToken.DoesNotExist:
        return json_fail_response("请求无效!")

    try:
        account = UserAccount.objects.get(id=access_token.user_id)
        if account.status == 1:
            return json_fail_response("当前用户已经激活")
    except UserAccount.DoesNotExist:
        return json_fail_response("激活用户不存在")

    account.status = 1
    account.save()

    # 注册环信
    user_info = UserInfo.query_format_info_by_user_id(account.id, use_cache=False)
    register_ease_mob(user_info['ease_mob'])

    return redirect("/auth/login")

