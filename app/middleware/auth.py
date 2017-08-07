from app.models.account.token import AccessToken
from app.models.account.account import UserAccount


class AuthMiddleware(object):
    """
    授权中间件
    1、渲染View之前将Session中的access_token转换成user_info
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 调用View之前
        token = request.session.get("access_token")
        if not token:
            request.META["user_info"] = None
        else:
            access_token = AccessToken.query_token(token)
            if not access_token:
                request.META["user_info"] = None
            else:
                user_info = UserAccount.query_user_by_id(access_token.user_id)
                request.META["user_info"] = user_info

        response = self.get_response(request)
        # 调用View之后

        return response
