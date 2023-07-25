# textbase_cli.py
import os
import sys
import click
import importlib.util
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def test(filename):
    try:
        # Start the FastAPI server in a separate process with hot reload
        my_env = os.environ.copy()
        my_env['FILE_PATH'] = filename
        logging.info(my_env['FILE_PATH'])
        p = subprocess.Popen(['uvicorn', 'textbase.backend:app', '--reload', '--host', '0.0.0.0', '--port', '4000'], env=my_env)

        # Import the module containing the decorated function
        module_name = filename[:-3] if filename.endswith('.py') else filename
        module = importlib.import_module(module_name)

        if hasattr(module, 'on_message'):
            print("Chatbot is running. Visit http://localhost:4000/ in your web browser to interact.")
            p.wait()
        else:
            print("Error: 'on_message' function not found in the file.")
    
    except Exception as e:
        # Log the exception or print a custom error message
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    cli()
