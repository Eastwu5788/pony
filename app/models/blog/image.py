import os

from django.db import models
from django.core.cache import cache
import django.utils.timezone as timezone
from pony.settings import IMAGE_HOST

CACHE_KEY_ID = "Pony:Image:CacheId:"
CACHE_TIME = 60*60*24


class Image(models.Model):

    share_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    image_o = models.CharField(default='')
    image_a = models.CharField(default='')
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)
    file_name = models.CharField(default='')
    file_ext = models.CharField(default='')
    mime_type = models.CharField(default='')
    file_size = models.IntegerField(default=0)
    hash_key = models.CharField(default='')
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_image_by_id(image_id=0, use_cache=True):
        key = CACHE_KEY_ID+str(image_id)
        #if use_cache:
        #    image = cache.get(key)
        #    if image:
        #        return image

        try:
            image = Image.objects.get(id=image_id)
            image = Image.format_signal_image(image)
            cache.set(key, image, CACHE_TIME)
            return image
        except Image.DoesNotExist:
            return dict()

    @staticmethod
    def format_signal_image(image, full_info=False):
        result = dict()

        if not image:
            return result

        result["image_o"] = os.path.join(IMAGE_HOST, image.image_o)
        result["image_a"] = os.path.join(IMAGE_HOST, image.image_a)
        result["image_width"] = image.image_width
        result["image_height"] = image.image_height

        if full_info:
            result["hash_key"] = image.hash_key

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "image"
