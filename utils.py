import os
from github import Github
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Function to load data
def load_data(student_initials):
    GITHUB_REPO = 'cwaltregny/ib-progress-tracker'  
    BASE_URL = f'https://raw.githubusercontent.com/{GITHUB_REPO}/main/data/'
    try:
        data = pd.read_csv(f"{BASE_URL}{student_initials}.csv")
        return data
    except:
        return None

def initialize_data(data, SUBJECTS_TOPICS):
    if data is None:
        progress = {subject: 0 for subject in SUBJECTS_TOPICS}
        confidence = {subject: [0]*len(SUBJECTS_TOPICS.values()) for subject in SUBJECTS_TOPICS}  # default to 50%
    else:
        progress = {row['Subject']: row['Progress'] for _, row in data.iterrows()}
        confidence = {row['Subject']: row['Confidence'] for _, row in data.iterrows()}
    return progress, confidence
    
# Function to save data to GitHub
def save_data_github(data, student_initials, token):
    GITHUB_REPO = 'cwaltregny/ib-progress-tracker' 
    g = Github(token)
    repo = g.get_repo(GITHUB_REPO)
    contents = data.to_csv(index=False)
    file_path = f"data/{student_initials}.csv"
    try:
        repo_file = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update {student_initials}.csv", contents, repo_file.sha)
    except:
        repo.create_file(file_path, f"Create {student_initials}.csv", contents)


# Function to save data to GitHub
def save_plot_github(file_path, token):
    GITHUB_REPO = 'cwaltregny/ib-progress-tracker' 
    g = Github(token)
    repo = g.get_repo(GITHUB_REPO)
    with open(file_path, 'rb') as file:
        file_content = file.read()
    try:
        repo_file = repo.get_contents(file_path)
        repo.update_file(file_path, f"Updated plot", file_content, repo_file.sha)
    except:
        repo.create_file(file_path, f"Create plot", file_content)