from django.http.response import HttpResponseRedirect
from app.models.account.info import UserInfo


def login_required(func):
    """
    检查用户当前是否登录
    """
    def do_auth(*args, **kwargs):
        user_info = args[0].META["user_info"]
        if not user_info:
            return HttpResponseRedirect("/auth/login")
        return func(*args, **kwargs)
    return do_auth


def manager_required(func):
    """
    检查当前登录用户是否具有管理员权限
    如果没有管理员权限，则重定向到首页
    """
    def auth_check(*args, **kwargs):
        account = args[0].META["user_info"]
        try:
            user_info = UserInfo.objects.filter(user_id=account.id, status=1).get()
            if user_info.role_id != 9:
                return HttpResponseRedirect("/index")
        except UserInfo.DoesNotExist:
            return HttpResponseRedirect("/index")
        return func(*args, **kwargs)
    return auth_check
