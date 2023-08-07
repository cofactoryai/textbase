## Introduction

This framework is a tool that allows developers to create their own chatbot with minimal coding within minutes.

The framework simplifies the chatbot development process by providing a selection of pre-built chatbots that include, all models provided by OpenAI API, all models provided by HuggingFace API, BotLibre API as well as all models provided by HuggingFace python library.

## Getting started with transformers library

Follow the installation steps given in the `readme.md`. No API key is needed for transformers library but you might need to install dependencies using following commands.

```bash
poetry add transformers
poetry add torch
poetry install
```

## Chatbot selection

You can change the model by passing the `model_name` variable in `on_message` function in the `main.py` file

## Chatbot customization

You can customize the chosen chatbot by making changes in the `on_message` function. Refer to [transformers](https://huggingface.co/docs/transformers/index) documentation for more information.