# Integrating Langchain with Hugging Face Models

This guide explains how to integrate Langchain with models from the Hugging Face Hub, enabling controlled and interactive AI-based conversations.

## Instructions:

### Step 1: Get Hugging Face API Key##

1. Create an account on Hugging Face.
2. Click on the profile icon at the top right corner of the page.
3. Go to "Settings."
4. Navigate to the "Access Tokens" tab.
5. Click "Create New Token" and enter any name for the token.
6. Copy the generated token.
### Step 2: Installation

Install Langchain via pip:

```bash
Copy code
pip install langchain

```
### Step 3: Configuration

#### Environment Variable:

Set up your Hugging Face API key as an environment variable using the token you obtained in Step 1.


## Class Definition

The LangchainHuggingFace class in models.py constructs the Langchain pipleline, and retrieves the bot's response using generate method.

## Main Interaction
In the on_message function of your main.py file, determine the system prompt(SYSTEM_PROMPT) that will be used for the prompt template.

You can use the following code snippet to call the generate method:

```python
bot_response = models.LangchainHuggingFace.generate(<parameters>
)
```

The parameters are:

    (message_history: list[Message],
    system_prompt: str,
    model: typing.Optional[str] = "databricks/dolly-v2-3b",
    max_tokens: typing.Optional[int] = 20,
    temperature: typing.Optional[float] = 0.3,
    min_tokens: typing.Optional[int] = None,
    top_k: typing.Optional[int] = 50)


#### Note: You can pass any model path from the Hugging Face Hub in the model argument.

## Usage

With everything set up, you can now use the generate method to interact with the Hugging Face models.

## Additional Configuration

You can customize the behavior by adjusting parameters such as max_tokens, temperature, etc. These can be added as arguments to the generate method and passed to the Hugging Face Hub instance.

## Conclusion

By following these steps, you can integrate Langchain with models from the Hugging Face Hub to create intelligent and interactive chatbots. Make sure to customize the prompt templates and parameters according to your specific use case and application requirements.