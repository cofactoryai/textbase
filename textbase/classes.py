from textbase.helpers import convert_img_to_url
from PIL.Image import Image as PILImageClass
import os

class Image:
    def __init__(self, url="", pil_image="", path=""):
        if pil_image:
            if url:
                raise TypeError("Only url OR pil_image can be given.")
            if not isinstance(pil_image, PILImageClass):
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
