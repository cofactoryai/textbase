import os
import http.server
import socketserver
from textbase.utils.download_build import download_and_extract_zip
import click

socketserver.TCPServer.allow_reuse_address=True

# URL of the zip file containing the dist folder
zip_url = "https://storage.googleapis.com/chatbot_mainpy/frontendUI.zip"

# Destination folder where the zip file will be extracted
destination_folder = os.path.join(os.getcwd(), "")

# Download and extract the zip file
download_and_extract_zip(zip_url, destination_folder)

# Port where the HTTP server will be running
PORT = 4000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = super().translate_path(path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(os.getcwd(), 'dist', relpath)
        return fullpath

Handler = MyHandler

# Change the current working directory to the destination folder
os.chdir(destination_folder)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()