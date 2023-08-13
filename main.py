import streamlit as st
from textbase.message import Message
from textbase import models
from textbase.chains import ConversationChain
from textbase.chains.conversation.memory import ConversationEntityMemory
from textbase.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Set Streamlit page configuration
st.set_page_config(page_title='🧠MemoryBot🤖', layout='wide')

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""

# Define function to get user input
def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                               placeholder="Your AI assistant here! Ask me anything ...",
                               label_visibility='hidden')
    return input_text

# Define function to start a new chat
def new_chat():
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""

# Set up Streamlit app layout
st.title("🤖 Chat Bot with 🧠")
st.subheader("Powered by 🦜 Textbase + OpenAI + Streamlit")

# Create an OpenAI instance
models.OpenAI.api_key = "YOUR_OPENAI_API_KEY"
openai_instance = models.OpenAI()

# Define the chatbot logic
def chatbot_logic(message_history: List[Message]):
    # Implement your chatbot's logic here
    # For example:
    user_input = message_history[-1].content
    bot_response = openai_instance.generate_response(user_input)
    return bot_response

# Set up the Streamlit app
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

user_input = get_text()

if user_input:
    # Create a ConversationEntityMemory object
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=openai_instance, k=5)

    # Create the ConversationChain object
    conversation_chain = ConversationChain(
        llm=openai_instance,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
    )

    # Generate bot response using the ConversationChain
    bot_response = conversation_chain.run(user_input)

    # Store conversation history
    st.session_state.past.append(user_input)
    st.session_state.generated.append(bot_response)

# Display the conversation history
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i], icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")

    # Download button for conversation history
    download_str = "\n".join([f"User: {user}\nBot: {bot}" for user, bot in zip(st.session_state["past"], st.session_state["generated"])])
    if download_str:
        st.download_button('Download Conversation', download_str)

# Run the Streamlit app
if __name__ == "__main__":
    st.sidebar.warning("Please provide your OpenAI API key in the code.")