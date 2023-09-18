import inspect
import click
import requests
import subprocess
import os
from tabulate import tabulate
from time import sleep
from yaspin import yaspin
import importlib.resources
import re
import zipfile
import urllib.parse
import shutil
from textbase.utils.logs import fetch_and_display_logs
from importlib.resources import files

CLOUD_URL = "https://us-east1-chat-agents.cloudfunctions.net/deploy-from-cli"
UPLOAD_URL = "https://us-east1-chat-agents.cloudfunctions.net/upload-file"

@click.group()
def cli():
    pass

@cli.command()
@click.option("--project_name", prompt="What do you want to name your project", required=True)
def init(project_name):
    """
    Initialize a new project with a basic template setup.
    """
    # Define the path to the new project directory
    project_dir = os.path.join(os.getcwd(), project_name)

    # Check if the directory already exists
    if os.path.exists(project_dir):
        click.secho(f"Error: Directory '{project_name}' already exists.", fg="red")
        return

    # Create the new project directory
    os.makedirs(project_dir)

    # Copy the contents of the template directory to the new project directory
    template_dir = files('textbase').joinpath('template')
    for item in template_dir.iterdir():
        s = str(item)
        d = os.path.join(project_dir, os.path.basename(s))
        if item.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    click.secho(f"Project '{project_name}' has been initialized!", fg="green")
    

@cli.command()
@click.option("--path", prompt="Path to the main.py file", required=True)
@click.option("--port", prompt="Enter port", required=False, default=8080)
def test(path, port):
    # Check if the file exists
    if not os.path.exists(path):
        click.secho("Incorrect main.py path.", fg='red')
        return

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Check if 'on_message' exists and is a function
    if "on_message" in dir(module) and inspect.isfunction(getattr(module, "on_message")):
        click.secho("The function 'on_message' exists in the specified main.py file.", fg='yellow')
    else:
        click.secho("The function 'on_message' does not exist in the specified main.py file.", fg='red')
        return
    server_path = importlib.resources.files('textbase').joinpath('utils', 'server.py')
    try:
        if os.name == 'posix':
            process_local_ui = subprocess.Popen(f'python3 {server_path}', shell=True)
        else:
            process_local_ui = subprocess.Popen(f'python {server_path}', shell=True)

        process_gcp = subprocess.Popen(f'functions_framework --target=on_message --source={path} --debug --port={port}',
                     shell=True,
                     stdin=subprocess.PIPE)

        # Print the Bot UI Url
        encoded_api_url = urllib.parse.quote(f"http://localhost:{port}", safe='')
        click.secho(f"Server URL: http://localhost:4000/?API_URL={encoded_api_url}", fg='cyan', bold=True)
        process_local_ui.communicate()
        process_gcp.communicate()  # Wait for the process to finish
    except KeyboardInterrupt:
        process_gcp.kill()  # Stop the process when Ctrl+C is pressed
        process_local_ui.kill()
        click.secho("Server stopped.", fg='red')

#################################################################################################################
def files_exist(path):
    if not os.path.exists(os.path.join(path, "main.py")):
        click.echo(click.style(f"Error: main.py not found in {path} directory.", fg='red'))
        return False
    if not os.path.exists(os.path.join(path, "requirements.txt")):
        click.echo(click.style(f"Error: requirements.txt not found in {path} directory.", fg='red'))
        return False
    return True

def check_requirement(requirements_path):
    try:
        with open(requirements_path, 'r') as file:
            requirements = file.readlines()
        for requirement in requirements:
            if 'textbase-client' in requirement:
                click.echo(click.style("textbase-client is in requirements.txt", fg='green'))
                return True
        click.echo(click.style("textbase-client is not in requirements.txt. Aborting..", fg='red'))
        return False
    except FileNotFoundError:
        click.echo(click.style("requirements.txt file not found", fg='red'))
        return False

@cli.command()
@click.option("--path", prompt="Path to the directory containing main.py and requirements.txt file", default=os.getcwd())
def compress(path):
    click.echo(click.style("Creating zip file for deployment", fg='green'))

    OUTPUT_ZIP_FILENAME = 'deploy.zip'
    OUTPUT_ZIP_PATH = os.path.join(os.getcwd(), OUTPUT_ZIP_FILENAME)
    REQUIREMENTS_FILE_PATH = os.path.join(path, 'requirements.txt')

    if files_exist(path) and check_requirement(REQUIREMENTS_FILE_PATH):
        with zipfile.ZipFile(OUTPUT_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(path):
                for file in files:
                    # skip the zip file itself when zipping it
                    if file == OUTPUT_ZIP_FILENAME:
                        continue
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, path))
        click.echo(click.style(f"Files have been zipped to {OUTPUT_ZIP_FILENAME}", fg='green'))

#################################################################################################################
def validate_bot_name(ctx, param, value):
    pattern = r'^[a-z0-9_-]+$'
    if not re.match(pattern, value):
        error_message = click.style('Bot name can only contain lowercase alphanumeric characters, hyphens, and underscores.', fg='red')
        raise click.BadParameter(error_message)
    return value


@cli.command()
@click.option("--path", prompt="Path to the zip folder", required=True)
@click.option("--bot_name", prompt="Name of the bot", required=True, callback=validate_bot_name)
@click.option("--api_key", prompt="Textbase API Key", required=True)
@click.option("--show_logs", is_flag=True, default=True, help="Fetch show_logs after deployment")
def deploy(path, bot_name, api_key, show_logs):
    click.echo(click.style(f"Deploying bot '{bot_name}' with zip folder from path: {path}", fg='yellow'))

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    files = {
        "file": open(path, "rb"),
    }

    data = {
        "botName": bot_name
    }

    with yaspin(text="Uploading...", color="yellow") as spinner:
        response = requests.post(
            UPLOAD_URL,
            headers=headers,
            data=data,
            files=files
        )

    if response.ok:
        click.echo(click.style("Upload completed successfully! ✅", fg='green'))
        response_data = response.json()
        error = response_data.get('error')
        data = response_data.get('data')
        if not error and data:
            message = data.get('message')
            # Parse the message to extract bot ID and URL
            parts = message.split('. ')
            bot_id = parts[1].split(' ')[-1]
            url = parts[2].split(' ')[-1]
            # Create a list of dictionaries for tabulate
            data_list = [{'Status': parts[0], 'Bot ID': bot_id, 'URL': url}]
            table = tabulate(data_list, headers="keys", tablefmt="pretty")
            click.echo(click.style("Deployment details:", fg='blue'))
            click.echo(table)
        else:
            click.echo(click.style("Something went wrong! ❌", fg='red'))
            click.echo(response.text)
    else:
        click.echo(click.style("Something went wrong! ❌", fg='red'))
        click.echo(response.text)

    # Piping logs in the cli in real-time
    if show_logs:
        click.echo(click.style(f"Fetching logs for bot '{bot_name}'...", fg='green'))

        cloud_url = f"{CLOUD_URL}/logs"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "botName": bot_name,
            "pageToken": None
        }

        fetch_and_display_logs(cloud_url=cloud_url,
                           headers=headers,
                           params=params)
#################################################################################################################

@cli.command()
@click.option("--bot_id", prompt="Id of the bot", required=True)
@click.option("--api_key", prompt="Textbase API Key", required=True)
def health(bot_id, api_key):
    click.echo(click.style(f"Checking health of bot '{bot_id}' with API key: {api_key}", fg='green'))

    # the user would get the bot_id from the GET /list and use it here
    cloud_url = f"{CLOUD_URL}/bot-health"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "botId": bot_id
    }

    response = requests.get(cloud_url, headers=headers, params=params)

    if response.ok:
        response_data = response.json()
        data = response_data.get('data')
        if data is not None:
            # Convert the data dictionary to a list of dictionaries for tabulate
            data_list = [data]
            table = tabulate(data_list, headers="keys", tablefmt="pretty")
            click.echo(click.style("Bot status:", fg='green'))
            click.echo(table)
        else:
            click.echo(click.style("Status information not found in the response.", fg='red'))
            click.echo(response_data)
    else:
        click.echo(click.style("Failed to retrieve bot status.", fg='red'))


@cli.command()
@click.option("--api_key", prompt="Textbase API Key", required=True)
def list(api_key):
    click.echo(click.style("Getting the list of bots...", fg='green'))

    cloud_url = f"{CLOUD_URL}/list"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(
        cloud_url,
        headers=headers
    )

    if response.ok:
        data = response.json().get('data', [])
        if data:
            # Reorder the dictionaries in the data list
            reordered_data = [{'id': d['id'], 'name': d['name'], 'url': d['url']} for d in data]
            table = tabulate(reordered_data, headers="keys", tablefmt="pretty")
            click.echo(click.style("List of bots:", fg='blue'))
            print(table)
        else:
            click.echo(click.style("No bots found.", fg='yellow'))
    else:
        click.echo(click.style("Something went wrong!", fg='red'))


@cli.command()
@click.option("--bot_id", prompt="Id of the bot", required=True)
@click.option("--api_key", prompt="Textbase API Key", required=True)
def delete(bot_id, api_key):
    click.echo(click.style(f"Deleting bot '{bot_id}'...", fg='red'))

    cloud_url = f"{CLOUD_URL}/delete"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "botId": bot_id
    }

    with click.progressbar(length=100, label='Deleting...') as bar:
        for i in range(100):
            sleep(0.02)  # simulate deletion progress
            bar.update(1)

    response = requests.post(
        cloud_url,
        json=data,
        headers=headers
    )

    if response.ok:
        click.echo(click.style(f"Bot '{bot_id}' deleted successfully!", fg='green'))
        response_data = response.json()
        if response_data:
            # Convert the data dictionary to a list of dictionaries for tabulate
            data_list = [response_data]
            table = tabulate(data_list, headers="keys", tablefmt="pretty")
            click.echo(table)
        else:
            click.echo("No data found in the response.")
    else:
        click.echo(click.style("Something went wrong!", fg='red'))


@cli.command()
@click.option("--bot_name", prompt="Name of the bot", required=True)
@click.option("--api_key", prompt="Textbase API Key", required=True)
@click.option("--start_time", prompt="Logs for previous ___ minutes", required=False, default=5)
def logs(bot_name, api_key, start_time):
    click.echo(click.style(f"Fetching logs for bot '{bot_name}'...", fg='green'))

    cloud_url = f"{CLOUD_URL}/logs"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "botName": bot_name,
        "startTime": start_time,
        "pageToken": None
    }

    fetch_and_display_logs(cloud_url=cloud_url, 
                           headers=headers, 
                           params=params)    
    
    
@cli.command()
@click.option("--bot_name", prompt="Name of the bot", required=True)
@click.option("--api_key", prompt="Textbase API Key", required=True)
def download(bot_name, api_key):
    cloud_url = f"{CLOUD_URL}/downloadZip"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {"botName": bot_name}
    response = requests.get(cloud_url, 
                            headers=headers, 
                            params=params, 
                            stream=True)

    if response.status_code == 200:
        with open(f"{bot_name}.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    else:
        click.echo(click.style(f"Error: {response.status_code}, {response.text}", fg="red"))

if __name__ == "__main__":
    cli()

