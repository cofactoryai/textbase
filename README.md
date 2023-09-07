<p align="center">
  <picture>
    <img alt="Textbase python library" src="assets/logo.svg" width="352" height="59" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<p align="center">
    <a href="https://docs.textbase.ai">
        <img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/transformers/index.svg?down_color=red&down_message=offline&up_message=online">
    </a>
</p>

<h3 align="center">
    <p>✨ Textbase is a framework for building chatbots using NLP and ML. ✨</p>
</h3>

<h3 align="center">
    <a href="https://textbase.ai"><img src="assets/banner.png"></a>
</h3>

Just implement the `on_message` function in `main.py` and Textbase will take care of the rest :)

Since it is just Python you can use whatever models, libraries, vector databases and APIs you want.

Coming soon:
- [x] [PyPI package](https://pypi.org/project/textbase-client/)
- [x] Easy web deployment via [textbase-client deploy](docs/docs/deployment/deploy-from-cli.md)
- [ ] SMS integration
- [ ] Native integration of other models (Claude, Llama, ...)

![Demo Deploy GIF](assets/textbase-deploy.gif)

## Installation
Make sure you have `python version >=3.9.0`, it's always good to follow the [docs](https://docs.textbase.ai/get-started/installation) 👈🏻
### 1. Through pip
```bash
pip install textbase-client
```

### 2. Local installation
Clone the repository and install the dependencies using [Poetry](https://python-poetry.org/) (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

For proper details see [here]()

```bash
git clone https://github.com/cofactoryai/textbase
cd textbase
poetry shell
poetry install
```

## Start development server

> If you're using the default template, **remember to set the OpenAI API key** in `main.py`.

Run the following command:
- if installed locally
    ```bash
    poetry run python textbase/textbase_cli.py test
    ```
- if installed through pip
    ```bash
    textbase-client test
    ```
Response:
```bash
Path to the main.py file: examples/openai-bot/main.py # You can create a main.py by yourself and add that path here. NOTE: The path should not be in quotes
```
Now go to the link in blue color which is shown on the CLI and you will be able to chat with your bot!
![Local UI](assets/test_command.png)

### `Other commands have been mentioned in the documentation website.` [Have a look](https://docs.textbase.ai/usage) 😃!


## Contributions

Contributions are welcome! Please open an issue or create a pull request.
