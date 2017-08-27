from app.modules.common.auth import login_required
from app.modules.common.util_struct import *

from app.models.account.follow import UserFollow
from app.models.account.info import UserInfo

@login_required
def change_follow_status_handler(request):
    login_user = request.META["user_info"]
    status = request.POST.get("status")
    user_id = request.POST.get("user")

    if user_id == login_user.id:
        return json_fail_response("您不能关注或取消关注您自己")

    if int(status) not in [1, 2]:
        return json_fail_response("参数错误!")

    if int(status) == 1:
        return cancel_follow(user_id, login_user.id)
    else:
        return add_follow(user_id, login_user.id)


def cancel_follow(user_id, login_user):
    relation = UserFollow.query_user_relation(login_user, user_id)
    if relation == 0 or relation == 2:
        return json_fail_response("您当前尚未关注对方")

    UserFollow.objects.filter(user_id=login_user, follow_user=user_id, status=1).update(status=0)

    refresh_cache(user_id, login_user)

    return json_success_response("取消关注成功")


def add_follow(user_id, login_user):
    relation = UserFollow.query_user_relation(login_user, user_id)
    if relation == 1 or relation == 3:
        return json_fail_response("您当前已经关注了对方")

    follow = UserFollow(user_id=login_user, follow_user=user_id, status=1)
    follow.save()

    refresh_cache(user_id, login_user)

    return json_success_response("关注对方成功")


def refresh_cache(user_id, login_user):
    UserFollow.query_user_meta_count(user_id, is_follow=False, use_cache=False)
    UserFollow.query_user_meta_count(login_user, is_follow=True, use_cache=False)
    UserInfo.query_format_info_by_user_id(user_id, use_cache=False)
    UserInfo.query_format_info_by_user_id(login_user, use_cache=False)
