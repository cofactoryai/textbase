import os
from PIL.Image import Image as PILImageClass
from textbase.helpers import convert_img_to_url,\
    convert_video_to_url,\
    convert_audio_to_url,\
    convert_file_to_url


def check_parameters(*args):
    if sum(bool(p) for p in args[0]) > 1:
        raise TypeError("Only one parameter can be given.")


class Image:
    def __init__(self, url="", pil_image="", path=""):
        # list(locals().values())[1:] is the list of arguments except the 'self' argument
        check_parameters(list(locals().values())[1:])

        if pil_image and not isinstance(pil_image, PILImageClass):
            raise TypeError("Not a valid PIL image.")

        self.url = url
        self.pil_image = pil_image

        if path and not os.path.exists(path):
            raise FileNotFoundError("The given path doesn't exist.")

        self.path = path

    def upload_pil_to_bucket(self):
        self.url = convert_img_to_url(pil_image=self.pil_image)

    def upload_file_to_bucket(self):
        self.url = convert_img_to_url(image_file_path=self.path)


class Media:
    def __init__(self, url="", path=""):
        # list(locals().values())[1:] is the list of arguments except the 'self' argument
        check_parameters(list(locals().values())[1:])

        self.url = url

        if path and not os.path.exists(path):
            raise FileNotFoundError("The given path doesn't exist.")

        self.path = path

    def upload_file_to_bucket(self, convert_func):
        self.url = convert_func(self.path)


class Video(Media):
    def upload_file_to_bucket(self):
        super().upload_file_to_bucket(convert_video_to_url)


class Audio(Media):
    def upload_file_to_bucket(self):
        super().upload_file_to_bucket(convert_audio_to_url)


class File(Media):
    def upload_file_to_bucket(self):
        super().upload_file_to_bucket(convert_file_to_url)
