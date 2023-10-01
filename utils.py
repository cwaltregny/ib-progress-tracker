import os
import requests
from github import Github
import pandas as pd

# Function to load data
def load_data(student_initials):
    GITHUB_REPO = 'cwaltregny/ib-progress-tracker'  
    BASE_URL = f'https://raw.githubusercontent.com/{GITHUB_REPO}/main/data/'
    try:
        response = requests.get(f"{BASE_URL}{student_initials}.csv")
        data = pd.read_csv(response.text.splitlines())
        return data
    except:
        return None


# Function to save data to GitHub
def save_to_github(data, student_initials, token):
    GITHUB_REPO = 'cwaltregny/ib-progress-tracker' 
    g = Github(token)
    repo = g.get_repo(GITHUB_REPO)
    contents = data.to_csv(index=False)
    file_path = f"{student_initials}.csv"
    try:
        repo_file = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update {student_initials}.csv", contents, repo_file.sha)
    except:
        repo.create_file(file_path, f"Create {student_initials}.csv", contents)