from textbase.helpers import convert_img_to_url
from PIL.Image import Image as PILImageClass

class Image:
    def __init__(self, url="", pil_image=""):
        if url and pil_image:
            raise TypeError("Only url OR pil_image can be given.")
        if not isinstance(pil_image, PILImageClass):
            raise TypeError("Not a valid PIL image.")

        self.url = url
        self.pil_image = pil_image

    def upload_pil_to_bucket(self):
        self.url = convert_img_to_url(pil_image=self.pil_image)