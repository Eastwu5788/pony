from django.db import models
from app.models.account.info import UserInfo


class UserAccount(models.Model):

    user_name = models.CharField(default='')
    mobile = models.CharField(default='')
    email = models.CharField(default='')
    password = models.CharField(default='')
    type = models.IntegerField(default=0)
    open_id = models.CharField(default='')
    banned = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    @staticmethod
    def query_account_by_email(email):
        account = UserAccount.objects.get(email=email)
        return account

    @staticmethod
    def query_user_by_id(user_id=0, cache=True):
        return UserAccount.objects.get(id=user_id)

    @staticmethod
    def query_format_user(user_id=0, cache=True):
        user = UserAccount.objects.get(id=user_id)
        return UserAccount.format_user(user)

    @staticmethod
    def format_user(user):
        result = UserInfo.query_format_info_by_user_id(user.id)
        return result

    class Meta:
        app_label = "b_account"
        db_table = "user_account"
