from django.db import models
from app.modules.common.secret import get_seed


class AccessToken(models.Model):

    user_id = models.IntegerField(default=0)
    access_token = models.CharField(default='')
    salt = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    @staticmethod
    def query_token_by_user_id(user_id):
        return AccessToken.objects.order_by("-id").filter(status=1).get(user_id=user_id)

    @staticmethod
    def query_token(token):
        return AccessToken.objects.order_by("-id").filter(status=1).get(access_token=token)

    @staticmethod
    def create_new_toke(user_id):
        token = AccessToken()
        token.user_id = user_id
        token.access_token = get_seed(str(user_id))
        token.salt = get_seed(str(user_id), 10)
        token.status = 1
        token.save()
        return token

    class Meta:
        app_label = "b_account"
        db_table = "user_access_token"
