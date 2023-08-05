## Introduction

This framework is a tool that allows developers to create their own chatbot with minimal coding within minutes.

The framework simplifies the chatbot development process by providing a selection of pre-built chatbots that include, all models provided by OpenAI API, all models provided by HuggingFace API, BotLibre API as well as all models provided by HuggingFace python library.

## Getting started

Follow the installation steps given in the `readme.md` If you wish to use the OpenAI API or the HuggingFace API, you will need an API key. For Botlibre API you would require Application and Instance ID

**To get OpenAI API key, follow these steps**:
1. Go to the OpenAI website at https://openai.com/ and sign up for an account or log in with your existing account.
2. Click on your profile icon at the top-right corner of the page and select “View API Keys”.
3. Click on “Create New Secret Key” to generate a new API key. You can also view, copy, or delete your existing keys from this page.
4. Copy the API key and store it in a secure location. You will need it to authenticate your requests to the OpenAI API.

**To get a Hugging Face API key, follow these steps**:
1. Go to the Hugging Face website at https://huggingface.co/ and sign up for an account or log in with your existing account.
2. Click on your profile icon at the top-right corner of the page and select “Settings”.
3. Click on the “API tokens” tab and click on “Create an API token”.
4. Enter a name for your token and click on “Create”. You can also view, copy, or delete your existing tokens from this page.
5. Copy the API token and store it in a secure location. You will need it to authenticate your requests to the Hugging Face API.

**To get a Botlibre API application id and instance, follow these steps**:
1. Create account on https://www.botlibre.com and log in
2. Open https://www.botlibre.com/api-test.jsp and choose JSON chat API
3. Note application ID and instance

## Chatbot selection

The list of examples are found in the `examples` folder
You can choose any one of them and edit your `main.py` file

You can change the model in case of OpenAI, HuggingFace and Transformers. You can do that by passing the `model_name` parameter for HuggingFace and HuggingFace and `model` parameter for OpenAI in the `models.api_name.generate` functions in the `main.py` file

## Chatbot customization

You can customize the chosen chatbot by making changes in the `models.py` file. Refer to OpenAI and HuggingFace documentation for more information.