import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text
import time
import click
from yaspin import yaspin

def fetch_and_display_logs(cloud_url, headers, params):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Timestamp")
    table.add_column("Severity")
    table.add_column("Summary")

    while True:
        with yaspin(text="Logs...", color="yellow") as spinner:
            response = requests.get(cloud_url, headers=headers, params=params)

            if response.ok:
                response_data = response.json()
                data = response_data.get('data')
                if data is not None:
                    logs = data.get('logs')
                    if logs:
                        for log in logs:
                            severity_color = 'blue' if log['severity'].lower() in ['notice', 'info', 'debug'] else 'red' if log['severity'].lower() in ['alert', 'critical', 'error'] else 'yellow'
                            
                            table.add_row(log['timestamp'], Text(log['severity'], style=severity_color), Text(log.get('text', ''), style=severity_color))
                            
                        console.clear()
                        console.print(table)
                    # Update the params for the next request
                    params['pageToken'] = data.get('nextPageToken')
                    params['startTime'] = data.get('startTime')
                else:
                    click.echo(click.style("No logs found in the response.", fg='yellow'))
            else:
                click.echo(click.style("Failed to retrieve logs.", fg='red'))

            # Poll the endpoint every 3 seconds
            time.sleep(3)