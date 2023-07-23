class ChatbotRegistry:
    _registry = {}

    @classmethod
    def register(cls, bot_name):
        def decorator(func):
            cls._registry[bot_name] = func
            return func
        return decorator

    @classmethod
    def get_bot(cls, bot_name):
        return cls._registry.get(bot_name, None)

registry = ChatbotRegistry()

def chatbot(bot_name):
    return registry.register(bot_name)


