import os
import sys
import click
import importlib.util
import subprocess
import logging
import time  # Import the time module

logging.basicConfig(level=logging.INFO)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def test(filename):
    process = None  # Declare process outside the try block to ensure access in the finally block
    try:
        # Get the directory containing the file and add it to the Python path
        file_directory = os.path.dirname(filename)
        sys.path.append(file_directory)

        my_env = os.environ.copy()
        my_env['FILE_PATH'] = filename
        logging.info(my_env['FILE_PATH'])
        process = subprocess.Popen(['uvicorn', 'textbase.backend:app', '--reload', '--host', '0.0.0.0', '--port', '4000'], env=my_env)

        # Import the module containing the decorated function
        module_name = os.path.basename(filename)[:-3] if filename.endswith('.py') else os.path.basename(filename)
        module = importlib.import_module(module_name)

        if hasattr(module, 'on_message'):
            print("Chatbot is running. Visit http://localhost:4000/ in your web browser to interact.")
            process.wait()
        else:
            print("Error: 'on_message' function not found in the file.")

    except Exception as e:
        # Log the exception or print a custom error message
        print(f"Error occurred: {e}")
        sys.exit(1)

    finally:
        # Ensure subprocess is terminated when script exits
        if process:
            process.terminate()  # Try terminating the process first
            time.sleep(1)  # Add a short delay before killing the process
            process.kill()  # Kill the process if it did not terminate gracefully

def deploy():
    pass

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("Keyboard interrupt received. Terminating the server...")
        sys.exit(1)
