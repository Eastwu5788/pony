from django.db import models


class Image(models.Model):

    share_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    image_o = models.CharField()
    image_a = models.CharField()
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    file_name = models.CharField()
    file_ext = models.CharField()
    mime_type = models.CharField()
    file_size = models.IntegerField()
    hash_key = models.CharField()
    status = models.IntegerField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    @staticmethod
    def query_image_by_id(image_id=0):
        try:
            image = Image.objects.get(id=image_id)
            return Image.format_signal_image(image)
        except Image.DoesNotExist:
            return dict()

    @staticmethod
    def format_signal_image(image, full_info=False):
        result = dict()

        if not image:
            return result

        result["image_o"] = "/static/uploads/image/"+image.image_a
        result["image_a"] = "/static/uploads/image/"+image.image_a
        result["image_width"] = image.image_width
        result["image_height"] = image.image_height

        if full_info:
            result["hash_key"] = image.hash_key

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "image"
