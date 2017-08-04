from django.db import models
from app.models.blog.image import Image


class UserInfo(models.Model):

    user_id = models.IntegerField(default=0)
    role_id = models.IntegerField(default=0)
    nick_name = models.CharField(default='')
    gender = models.IntegerField(default=0)
    avatar = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    @staticmethod
    def query_format_info_by_user_id(user_id, cache=True):
        user_info = UserInfo.objects.get(user_id=user_id)
        return UserInfo.format_user_info(user_info)

    @staticmethod
    def format_user_info(user_info):
        result = dict()
        result["nick_name"] = user_info.nick_name
        result["gender"] = user_info.gender
        result["avatar"] = Image.query_image_by_id(user_info.avatar)
        return result

    class Meta:
        app_label = "b_account"
        db_table = "user_info"
