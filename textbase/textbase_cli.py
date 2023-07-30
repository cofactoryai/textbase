import os
import sys
import click
import importlib.util
import subprocess
import logging
import time

# from textbase.download import download_and_extract_zip

logging.basicConfig(level=logging.INFO)

"""This needs to run only when you would be packaging the library using `poetry build`, this would download the template frontend from the google cloud storage
"""
# zip_url = "https://storage.googleapis.com/chatbot_mainpy/frontendv3.zip"
# destination_folder = os.path.join(os.getcwd(), "textbase")
# download_and_extract_zip(zip_url, destination_folder)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def test(filename):
    """
    The `test` function runs a Python script as a subprocess and terminates it gracefully when the
    script finishes or encounters an error.

    :param filename: The `filename` parameter is the path to a file that will be used in the script. It
    is expected to be an existing file
    """
    p = None  # Declare p outside the try block to ensure access in the finally block
    try:
        # Get the directory containing the file and add it to the Python path
        file_directory = os.path.dirname(filename)
        sys.path.append(file_directory)

        my_env = os.environ.copy()
        my_env["FILE_PATH"] = filename
        logging.info(my_env["FILE_PATH"])
        p = subprocess.Popen(
            ["uvicorn", "textbase.backend:app", "--reload", "--port", "4000"],
            env=my_env,
        )

        # Import the module containing the decorated function
        module_name = (
            os.path.basename(filename)[:-3]
            if filename.endswith(".py")
            else os.path.basename(filename)
        )
        module = importlib.import_module(module_name)

        if hasattr(module, "on_message"):
            print(
                "Chatbot is running. Visit http://localhost:4000/ in your web browser to interact."
            )
            p.wait()
        else:
            print("Error: 'on_message' function not found in the file.")

    except Exception as e:
        # Log the exception or print a custom error message
        print(f"Error occurred: {e}")
        sys.exit(1)

    finally:
        # Ensure subprocess is terminated when script exits
        if p:
            p.terminate()  # Try terminating the process first
            time.sleep(1)  # Add a short delay before killing the process
            p.kill()  # Kill the process if it did not terminate gracefully


def deploy():
    pass


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("Keyboard interrupt received. Terminating the server...")
        sys.exit(1)
