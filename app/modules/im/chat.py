from django.shortcuts import render
from app.modules.common.auth import login_required
from app.modules.relation.follow import format_relation_users
from app.models.account.account import UserInfo
from app.models.account.follow import UserFollow


@login_required
def chat_module_handler(request):
    contact = request.GET.get("contact", None)
    result = dict()
    result["user_info"] = UserInfo.query_format_info_by_user_id(request.META["user_info"].id)
    if contact:
        result["contact"] = UserInfo.query_format_info_by_ease_mob(contact)

    follow_list = UserFollow.query_user_relation_list(request.META["user_info"].id, True)
    result["follow_list"] = format_relation_users(follow_list, True, request.META["user_info"].id)
    return render(request, "chat/chat.html", result)

