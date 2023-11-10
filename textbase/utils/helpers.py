import click
import os
import re

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

def validate_bot_name(ctx, param, value):
    pattern = r'^[a-z0-9_-]+$'
    if not re.match(pattern, value):
        error_message = click.style('Bot name can only contain lowercase alphanumeric characters, hyphens, and underscores.', fg='red')
        raise click.BadParameter(error_message)
    return value
