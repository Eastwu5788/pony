from django.db import models


class Video(models.Model):

    share_id = models.IntegerField()
    video_url = models.CharField()
    video_width = models.IntegerField()
    video_height = models.IntegerField()
    screen_shot = models.CharField()
    playing_time = models.IntegerField()
    file_name = models.CharField()
    file_size = models.IntegerField()
    file_ext = models.CharField()
    mime_type = models.CharField()
    hash_key = models.CharField()
    bitrate_mode = models.CharField()
    status = models.IntegerField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    class Meta:
        app_label = "b_blog"
        db_table = "video"
