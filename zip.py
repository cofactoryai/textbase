import zipfile
import os

# Define the names of the files to be zipped
files_to_zip = ['requirements.txt', 'main.py']

# Define the name of the output zip file as "deploy.zip"
output_zip_filename = 'deploy.zip'

# Create a ZipFile object in write mode
with zipfile.ZipFile(output_zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_to_zip in files_to_zip:
        # Check if the file exists in the current directory
        if os.path.exists(file_to_zip):
            # Add the file to the zip archive
            zipf.write(file_to_zip, os.path.basename(file_to_zip))
        else:
            print(f"Warning: {file_to_zip} not found in the current directory.")

print(f"Files {', '.join(files_to_zip)} have been zipped to {output_zip_filename}")
