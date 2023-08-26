import functions_framework

@functions_framework.http
def bot():
    def bot_message(func):
        def bot_function(*args):
            request = args[0]
            post_body = request.json
            history_messages = post_body['data']['message_history']
            state = post_body['data']['state']

            if not isinstance(history_messages, list):
                return 'Error in processing', 402

            resp = func(history_messages, state)

            history_messages.append({
                "role": "assistant",
                "content": resp["response"]["data"]["messages"]
            })

            return {
                "message_history": history_messages,
                "state": resp["response"]["data"]["state"],
                "new_message": resp["response"]["data"]["messages"]
            }
        return bot_function
    return bot_message