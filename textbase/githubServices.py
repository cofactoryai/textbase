import os
import requests

def read_github_file():
    api_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_github_commits():
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file_path}"
    response = requests.get(api_url)

    if response.status_code == 200:
        commits = response.json()
        if len(commits) > 0:
            last_commit_hash = commits[0]["sha"]
            return last_commit_hash
        else:
            return None
    else:
        return None
        # do error handling

repo_owner = os.getenv("repo_owner")
repo_name  = os.getenv("repo_name")
file_path  = os.getenv("file_path")




