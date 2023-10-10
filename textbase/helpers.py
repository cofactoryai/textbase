import requests
from PIL.Image import Image as PILImageClass
from io import BytesIO

URL = "https://us-central1-chat-agents.cloudfunctions.net/upload-multimedia"

def convert_img_to_url(image_file_path="", pil_image: PILImageClass=None) -> str:
    if pil_image:
        # convert PIL object to a byte array
        img_byte_arr = BytesIO()
        img_format = pil_image.format
        pil_image.save(img_byte_arr, img_format)
        img_byte_arr = img_byte_arr.getvalue()

        img_file = {
            'file': img_byte_arr
        }
        data = {
            'parent_path': 'bot',
            'file_extension': img_format.lower()
        }

        response = requests.post(URL, files=img_file, data=data)

        if 'error' in response.json():
            return f'Error: {response.json()["error"]}'
        else:
            return response.json()['image_url']
    else:
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
