from django.conf.urls import url

from app.modules.index.index import index_handler
from app.modules.auth.login import login_handler
from app.modules.auth.logout import logout_handler
from app.modules.auth.register import register_handler

from app.modules.skill.skill import technology_handler

from app.modules.life.life import life_index_handler

from app.modules.about.about import about_index_handler

from app.modules.article.detail import article_detail_handler

from app.modules.common.upload import upload_handler

from app.modules.manage.admin import manage_handler
from app.modules.manage.edit import edit_article_handler

urlpatterns = [
    # === Auth ===
    url(r"^auth/login/", login_handler),
    url(r"^auth/logout/", logout_handler),
    url(r"^auth/register/", register_handler),

    # === Article ===
    url(r"^article/detail/(\w+)", article_detail_handler),

    # === Upload ===
    url(r"^upload/", upload_handler),

    # === Tech ===
    url(r"^skill/", technology_handler),

    # === Lift ===
    url(r"^life/", life_index_handler),

    # === About ===
    url(r"^about/", about_index_handler),

    # === Manage ===
    url(r"^manage$", manage_handler),
    url(r"^manage/edit$", edit_article_handler),

    # === Index(首页必须放在最后一个) ===
    url(r'', index_handler),
]
