from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from app.models.account.account import UserAccount
from app.modules.common.secret import *
from app.models.account.token import AccessToken


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
