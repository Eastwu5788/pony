from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponseRedirect

from app.models.account.account import UserAccount
from app.modules.common.secret import *
from app.models.account.info import UserInfo
from app.models.account.token import AccessToken


def register_handler(request):
    if request.method == "GET":
        return render(request, "auth/register/register.html")

    # TODO: 封装参数校验方法
    nick_name = request.POST.get("nick_name")
    email = request.POST.get("email")
    password = request.POST.get("pass_word")

    # TODO:检查参数合法性

    # 检查通过 注册用户
    register_new_account(nick_name, email, password)

    # TODO：发送邮箱验证邮件

    return HttpResponseRedirect("/auth/login/")


def register_new_account(nick_name, email, password):

    with transaction.atomic():
        # 用户账户注册
        account = UserAccount()

        account.user_name = email
        account.email = email
        account.password = get_secret_password(password)
        account.type = 0
        account.banned = 1
        # 未激活
        account.status = 0
        account.save()

        user_info = UserInfo()
        user_info.user_id = account.id
        user_info.nick_name = nick_name
        user_info.gender = 0
        user_info.avatar = 0
        user_info.status = 1
        user_info.save()

        token = AccessToken.create_new_toke(user_info.user_id)

    result = {
        "account": account,
        "user_info": user_info,
        "token": token
    }

    return result



