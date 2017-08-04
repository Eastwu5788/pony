from django.conf.urls import url

from app.modules.index.index import index_handler

from app.modules.auth.login import login_handler
from app.modules.auth.logout import logout_handler
from app.modules.auth.register import register_handler

from app.modules.skill.skill import technology_handler

from app.modules.life.life import life_index_handler

from app.modules.about.about import about_index_handler

from app.modules.article.detail import article_detail_handler
from app.modules.article.edit import edit_article_handler as edit_article
from app.modules.article.edit import change_article_status_handler

from app.modules.common.upload import upload_handler
from app.modules.common.markdown import apply_markdown

from app.modules.manage.admin import manage_handler
from app.modules.manage.edit import edit_article_handler
from app.modules.manage.recommend import home_recommend_handler
from app.modules.manage.recommend import remove_home_recommend_handler


urlpatterns = [
    # === Auth ===
    url(r"^auth/login/", login_handler),
    url(r"^auth/logout/", logout_handler),
    url(r"^auth/register", register_handler),

    # === Article ===
    url(r"^article/detail/(\w+)", article_detail_handler),
    url(r"^article/status", change_article_status_handler),
    url(r"^article/edit", edit_article),

    # === Upload ===
    url(r"^upload/", upload_handler),

    # === MarkDown ===
    url(r"^markdown", apply_markdown),

    # === Tech ===
    url(r"^skill/", technology_handler),

    # === Lift ===
    url(r"^life/", life_index_handler),

    # === About ===
    url(r"^about/", about_index_handler),

    # === Manage ===
    url(r"^manage/edit/(\w+)", edit_article_handler),
    url(r"^manage/recommend/remove", remove_home_recommend_handler),
    url(r"^manage/recommend", home_recommend_handler),
    url(r"^manage$", manage_handler),

    # === Index(首页必须放在最后一个) ===
    url(r'/index/', index_handler),
    url(r'', index_handler),
]
