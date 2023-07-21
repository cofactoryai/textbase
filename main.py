# main.py

from textbase.chatbot import registered_chatbots

def main():
    print("Welcome to the Chatbot!")
    print("Type 'exit' to end the conversation.")

    # Find the registered class with the name 'cologne-chatbot'
    chatbot_class = registered_chatbots.get('cologne-chatbot')

    if chatbot_class:
        chatbot = chatbot_class('cologne-chatbot')  # Pass the name 'cologne-chatbot' when creating the instance
        print("Registered Chatbots:")
        for name in registered_chatbots:
            print("-", name)
    else:
        print("Chatbot 'cologne-chatbot' not found. Exiting.")
        return

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        response = chatbot.process_message(user_input)
        print(response)

if __name__ == "__main__":
    main()
