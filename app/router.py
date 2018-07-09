from django.conf.urls import url

from app.modules.about.about import about_index_handler
from app.modules.about.set import user_setting_handler
from app.modules.about.user import *
from app.modules.article.comment import *
from app.modules.article.detail import article_detail_handler
from app.modules.article.edit import change_article_status_handler
from app.modules.article.edit import delete_article_handler
from app.modules.article.edit import edit_article_handler as edit_article
from app.modules.article.like import like_edit_handler
from app.modules.article.reply import *
from app.modules.auth.active import active_account_handler
from app.modules.auth.login import login_api_handler
from app.modules.auth.login import login_handler
from app.modules.auth.logout import logout_api_handler
from app.modules.auth.logout import logout_handler
from app.modules.auth.register import check_register_email
from app.modules.auth.register import register_handler
from app.modules.common.markdown import apply_markdown
from app.modules.common.upload import upload_handler
from app.modules.im.chat import *
from app.modules.index.index import index_handler
from app.modules.manage.admin import manage_handler
from app.modules.manage.edit import edit_article_handler
from app.modules.manage.recommend import home_recommend_handler
from app.modules.manage.recommend import remove_home_recommend_handler
from app.modules.relation.follow import *
from app.modules.skill.skill import technology_handler

app_name = 'pony'

urlpatterns = [
    # === Auth ===
    url(r"^auth/login", login_handler),
    url(r"^auth/logout", logout_handler),
    url(r"^auth/register", register_handler),
    url(r"^auth/active", active_account_handler),
    url(r"^auth/api/login", login_api_handler),
    url(r"^auth/api/logout", logout_api_handler),
    url(r"^auth/api/checkemail", check_register_email),

    # === Article ===
    url(r"^article/detail/(\w+)", article_detail_handler),
    url(r"^article/status", change_article_status_handler),
    url(r"^article/edit", edit_article),
    url(r"^article/like", like_edit_handler),                   # api:article/like 编辑点赞状态
    url(r"^article/comment/add", comment_add_handler),          # api:article/comment/add 评论
    url(r"^article/comment/like", comment_like_edit_handler),   # api:article/comment/like 评论点赞状态编辑
    url(r"^article/comment/reply", comment_reply_handler),      # api:article/comment/reply 评论回复

    # === Upload ===
    url(r"^upload/", upload_handler),

    # === MarkDown ===
    url(r"^markdown", apply_markdown),

    # === Tech ===
    url(r"^skill/", technology_handler),

    # === Chat ===
    url(r"^chat/", chat_module_handler),

    # === About ===
    url(r"^about/", about_index_handler),
    url(r"^user/info/(\w+)", user_info_handler),
    url(r"^user/api/info", user_info_api_handler),
    url(r"^user/api/search", user_search_api),
    url(r"^user/api/easemob", user_info_api_by_ease_mob_handler),
    url(r"^user/setting", user_setting_handler),
    url(r"^user/api/follow", change_follow_status_handler),
    url(r"^user/follower/(\w+)", follower_list_handler),
    url(r"^user/following/(\w+)", following_list_handler),

    # === Manage ===
    url(r"^manage/edit/(\w+)", edit_article_handler),
    url(r"^manage/article/remove", delete_article_handler),
    url(r"^manage/recommend/remove", remove_home_recommend_handler),
    url(r"^manage/recommend", home_recommend_handler),
    url(r"^manage$", manage_handler),

    # === Index(首页必须放在最后一个) ===
    url(r'index', index_handler),
    url(r'', index_handler),
]
