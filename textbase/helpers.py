import requests
from PIL.Image import Image as PILImageClass
from io import BytesIO

URL = "https://us-central1-chat-agents.cloudfunctions.net/upload-multimedia"


def upload_file(file_path: str, file_type: str) -> str:
    with open(file_path, 'rb') as _file:
        _file = {
            'file': _file
        }
        data = {
            'parent_path': 'bot',
            'file_type': file_type
        }

        response = requests.post(URL, files=_file, data=data)

        if 'error' in response.json():
            return f'Error: {response.json()["error"]}'
        else:
            return response.json()['url']


def convert_img_to_url(image_file_path: str="", pil_image: PILImageClass=None) -> str:
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
            'file_type': 'images',
            'file_extension': img_format.lower()
        }

        response = requests.post(URL, files=img_file, data=data)

        if 'error' in response.json():
            return f'Error: {response.json()["error"]}'
        else:
            return response.json()['url']
    else:
        response = upload_file(image_file_path, 'images')
        return response


def convert_video_to_url(video_file_path: str="") -> str:
    response = upload_file(video_file_path, 'videos')
    return response

def convert_audio_to_url(audio_file_path: str="") -> str:
    response = upload_file(audio_file_path, 'audios')
    return response

def convert_file_to_url(file_path: str="") -> str:
    response = upload_file(file_path, 'files')
    return response
