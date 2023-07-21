registered_chatbots = {}
    
def register(name):
    """
    The `register` function is a decorator that adds a chatbot function to the `registered_chatbots`
    dictionary with a given name.
    
    :param name: The name parameter is a string that represents the name of the chatbot
    :return: The decorator function is being returned.
    """
    def decorator(func):
        registered_chatbots[name] = func
        return func
    return decorator
