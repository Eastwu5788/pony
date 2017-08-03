from django.db import models


class UserAccount(models.Model):

    user_name = models.CharField()
    mobile = models.CharField()
    email = models.CharField()
    password = models.CharField()
    type = models.IntegerField()
    open_id = models.CharField()
    banned = models.IntegerField()
    status = models.IntegerField()
    created_time = models.CharField()
    updated_time = models.CharField()

    @staticmethod
    def query_user_by_id(user_id=0, cache=True):
        pass

    class Meta:
        app_label = "b_account"
        db_table = "user_account"
