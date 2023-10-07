import requests
from PIL.Image import Image as PILImageClass
from io import BytesIO

URL = "https://us-central1-chat-agents.cloudfunctions.net/upload-multimedia"

def convert_img_to_url(image_file_path="", pil_image: PILImageClass=None) -> str:
    if pil_image:
        img_byte_arr = BytesIO()
        pil_image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        img_file = {
            'file': img_byte_arr
        }
        data = {
            'parent_path': 'bot'
        }
        response = requests.post(URL, files=img_file, data=data)
        if 'error' in response.json():
            return f'Error: {response.json()["error"]}'
        else:
            return response.json()['image_url']
    with open(image_file_path, 'rb') as img_file:
        img_file = {
            'file': img_file
        }
        data = {
            'parent_path': 'bot'
        }
        response = requests.post(URL, files=img_file, data=data)
    if 'error' in response.json():
        return f'Error: {response.json()["error"]}'
    else:
        return response.json()['image_url']
