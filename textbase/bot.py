import functions_framework

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

            history_messages.append({
                "role": "assistant",
                "content": resp["response"]["data"]["messages"]
            })

            return {
                "message_history": history_messages,
                "state": resp["response"]["data"]["state"],
                "new_message": resp["response"]["data"]["messages"]
            }, resp['status_code'], headers
        return bot_function
    return bot_message