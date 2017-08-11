import hashlib
import time
from datetime import date

from PIL import Image

from django.shortcuts import render

from pony.settings import *
from app.models.blog.image import Image as ImageModel


def upload_handler(request):
    if request.method == 'GET':
        return render(request, "upload/upload.html")
    else:
        upload_image = UploadImage(request)
        upload_image.save()
        return render(request, "upload/upload.html", {"image": upload_image})


def generate_image_file():
    """
    生成图片存储文件
    按照年/月/日/xxx.jpg分类
    """
    today = date.today()
    path = "upload/%d/%02d/%02d/" % (today.year, today.month, today.day)
    full_path = os.path.join(UPLOAD_IMAGE_PATH, path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return path


def hash_image(image):
    if not image:
        return ""
    md5obj = hashlib.md5()
    md5obj.update(image)
    return md5obj.hexdigest()


class UploadImage(object):
    """
    图片上传模块封装
    """
    def __init__(self, request):
        self.request = request
        self.images = self.pre_upload()

    def save(self):
        image_info_list = []
        for item in self.images:
            image_info_list.append(UploadImage.save_image(item))
        return image_info_list

    @staticmethod
    def save_image(image_info):
        full_o_path = os.path.join(UPLOAD_IMAGE_PATH, image_info["image_o"])
        full_a_path = os.path.join(UPLOAD_IMAGE_PATH, image_info["image_a"])

        image_info["pil_image"].save(full_o_path, "jpeg", quality=90)
        thumb_image = image_info["pil_image"].copy()
        thumb_image.thumbnail((100, 100))
        thumb_image.save(full_a_path, "jpeg", quality=90)

        image = ImageModel()
        image.image_o = image_info["image_o"]
        image.image_a = image_info["image_a"]
        image.image_width = image_info["width"]
        image.image_height = image_info["height"]
        image.file_name = image_info["hash_key"]
        image.file_ext = "jpg"
        image.mime_type = image_info["mime_type"]
        image.file_size = image_info["file_size"]
        image.hash_key = image_info["hash_key"]
        image.status = 1
        image.save()
        return image

    @staticmethod
    def save_image_file(path, image):
        pass

    def pre_upload(self):
        image_info_list = []
        ori_image = self.request.FILES.get("image")
        if ori_image:
            image_info_list.append(UploadImage.format_image(ori_image))
        return image_info_list

    @staticmethod
    def format_image(image):

        result = dict()
        result["ori_image"] = image
        result["hash_key"] = hash_image(image.read())

        pil_image = Image.open(image)
        result["pil_image"] = pil_image
        result["width"] = pil_image.width
        result["height"] = pil_image.height
        result["image_o"] = UploadImage.generate_image_file_name(result["hash_key"], 'o')
        result["image_a"] = UploadImage.generate_image_file_name(result["hash_key"], 'a')
        result["mime_type"] = pil_image.mode
        result["file_size"] = image.size

        return result

    @staticmethod
    def generate_image_file_name(hash_key, size='o'):
        """
        生成唯一的图片名称
        """
        ori_key = hash_key + "_" + size + "_" + str(time.time())
        img_name = hashlib.md5(ori_key.encode("utf8")).hexdigest()+".jpg"
        return generate_image_file()+img_name

