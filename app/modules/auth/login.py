from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from app.models.account.account import UserAccount
from app.modules.common.secret import *
from app.models.account.token import AccessToken
from app.modules.common.struct import *


def login_handler(request):
    if request.method == "GET":
        return render(request, "auth/login/login.html")

    email = request.POST.get("email")
    pass_word = request.POST.get("pass_word")

    # TODO: email 和 password 合法性校验

    account = UserAccount.query_account_by_email(email)
    if not verify_password(pass_word, account.password):
        return render(request, "auth/login/login.html")

    # token处理
    token = AccessToken.query_token_by_user_id(account.id)
    if not token:
        AccessToken.create_new_toke(account.id)

    request.session["access_token"] = token.access_token
    return HttpResponseRedirect("/index/")


def login_api_handler(request):
    """
    登录api处理
    """
    if request.method == "GET":
        return json_fail_response("get request is not supported!")

    email = request.POST.get("email")
    pass_word = request.POST.get("pass_word")

    try:
        account = UserAccount.objects.get(email=email)
        # 1、密码检测
        if not verify_password(pass_word, account.password):
            return json_fail_response("请检查您的登录账户或密码!")
        # 2、激活状态检测
        if account.status == 0:
            return json_fail_response("当前账户未激活!")
        # 3、封号检测
        if account.banned == 0:
            return json_fail_response("对不起，当前登录账户已被封禁!")

        # token处理
        token = AccessToken.query_token_by_user_id(account.id)
        if not token:
            AccessToken.create_new_toke(account.id)
        # 返回token给前端
        request.session["access_token"] = token.access_token
        return json_success_response(token.access_token)

    except UserAccount.DoesNotExist:
        return json_fail_response("当前用户不存在!")
