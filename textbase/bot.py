import functions_framework
from textbase.classes import Image

@functions_framework.http
def bot():
    def bot_message(func):
        def bot_function(*args):
            request = args[0]
            if request.method == 'OPTIONS':
                # Allows GET requests from any origin with the Content-Type
                # header and caches preflight response for an 3600s
                headers = {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Max-Age': '3600'
                }

                return ('', 204, headers)

            # Set CORS headers for the main request
            headers = {
                'Access-Control-Allow-Origin': '*'
            }

            post_body = request.json
            history_messages = post_body['data']['message_history']
            state = post_body['data']['state']

            if not isinstance(history_messages, list):
                return 'Error in processing', 402, headers

            resp = func(history_messages, state)

            content = []

            if "errors" in resp:
                return {
                    "message_history": history_messages,
                    "state": resp["state"],
                    "new_message": []
                }, 500, headers

            for message in resp["messages"]:
                if isinstance(message, str):
                    content.append({
                        "data_type": "STRING",
                        "value": message
                    })
                elif isinstance(message, Image):
                    if message.url:
                        content.append({
                            "data_type": "IMAGE_URL",
                            "value": message.url
                        })
                    elif message.pil_image:
                        message.upload_pil_to_bucket()
                        content.append({
                            "data_type": "IMAGE_URL",
                            "value": message.url
                        })

            history_messages.append({
                "role": "assistant",
                "content": content
            })

            return {
                "message_history": history_messages,
                "state": resp["state"],
                "new_message": content
            }, 200, headers
        return bot_function
    return bot_message