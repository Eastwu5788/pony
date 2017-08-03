from django.db import models


class UserInfo(models.Model):

    user_id = models.IntegerField()
    role_id = models.IntegerField()
    nick_name = models.CharField()
    gender = models.IntegerField()
    avatar = models.IntegerField()
    status = models.IntegerField()
    created_time = models.CharField()
    updated_time = models.CharField()

    class Meta:
        app_label = "b_account"
        db_table = "user_info"
