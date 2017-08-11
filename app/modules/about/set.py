from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from app.modules.common.auth import login_required
from app.models.account.info import UserInfo
from app.models.account.account import UserAccount
from app.modules.common.upload import UploadImage


@login_required
def user_setting_handler(request):
    user_account = request.META["user_info"]
    user_info = UserInfo.query_format_info_by_user_id(user_account.id)
    if request.method == "GET":
        data = dict()
        user_info["email"] = UserAccount.query_user_by_id(user_account.id).email
        data["user_info"] = user_info
        return render(request, "about/setting.html", data)

    # 获取头像
    avatar = UploadImage(request)
    image_list = avatar.save()

    nick_name = request.POST.get("nick_name")
    gender = request.POST.get("gender")

    user = UserInfo.objects.get(user_id=user_account.id)
    user.gender = gender
    if nick_name != user_info["nick_name"]:
        user.nick_name = nick_name
    if len(image_list) > 0:
        user.avatar = image_list[0].id
    user.save()

    # 刷新缓存
    UserInfo.query_format_info_by_user_id(user_account.id, False)

    return HttpResponseRedirect("/user/info/" + str(user_account.id))
