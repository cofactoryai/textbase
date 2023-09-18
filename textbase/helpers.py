import requests

URL = "https://us-central1-chat-agents.cloudfunctions.net/upload-multimedia"

def convert_img_to_url(image_file_path) -> str:
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
