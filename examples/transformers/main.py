import textbase
from textbase.message import Message
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    model_name="microsoft/DialoGPT-small"

    # generate a bot response
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    input_ids = tokenizer.encode(message_history[-1].content + tokenizer.eos_token, return_tensors="pt")

    chat_history_ids = model.generate(
        input_ids,
        max_length=1000,
        do_sample=True,
        top_p=0.95,
        top_k=0,
        temperature=0.75,
        pad_token_id=tokenizer.eos_token_id
    )
    output = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return output
