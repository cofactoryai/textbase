---
sidebar_position: 1
---

# Installation

## [Video guide](https://youtu.be/pcw7G3S7FGw) (for Windows and Ubuntu >19.04):

1. Make sure to upgrade your Python version to >= 3.8.1 and add it to your `PATH`.
2. Now, you need to [install](https://python-poetry.org/docs/#installation) `Poetry`, which is a python dependency manager which makes your life easier. It really does.

## Ubuntu (≤19.04):

1. Follow this [guide](https://gist.github.com/basaks/652eea861a143a9b3d11805c96273488) to install Python version 3.9.
2. Install pip using:
    ```bash
    sudo apt install python-pip
    ```
3. Install poetry using:
    ```bash
    pip install poetry
    ```
4. Add it to your path using:
    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```
5. `poetry config virtualenvs.in-project true` in the VS Code terminal inside the folder where you have cloned textbase repo so that you can select the default Python interpreter in VS Code to the one Poetry installed.
6. ```bash
    cd textbase-framework
    poetry shell
    ```
    This will make a new virtual Python environment inside the current directory and then you can select the default python interpreter to be the one in the `.venv` folder.
7. `poetry install` to install all the required dependencies.