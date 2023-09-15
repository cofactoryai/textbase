import os

def setAPIKeys(keys: dict):
    for key, value in keys.items():
        os.environ[key] = value