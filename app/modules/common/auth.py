from django.http.response import HttpResponseRedirect


def login_required(func):
    def do_auth(*args, **kwargs):
        user_info = args[0].META["user_info"]
        if not user_info:
            return HttpResponseRedirect("/auth/login")
        return func(*args, **kwargs)
    return do_auth
