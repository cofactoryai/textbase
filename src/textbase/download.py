import os
import zipfile
import requests

def download_and_extract_zip(zip_url, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Download the zip file
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_file_path = os.path.join(destination_folder, "frontend.zip")
        with open(zip_file_path, 'wb') as f:
            f.write(response.content)

        # Extract the contents of the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

        # Remove the zip file after extraction
        os.remove(zip_file_path)

        print("Zip file downloaded and extracted successfully.")
    else:
        print("Failed to download the zip file.")
