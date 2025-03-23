import requests
import os
from flask import jsonify

# Load GitHub API Token (if using authentication)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "github-stats-service",
}

# Add Authorization if a token is available
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def get_github_user_stats(username):
    """Fetch GitHub user stats including repos, followers, following, etc."""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    data = response.json()
    
    # Extracting necessary stats
    user_stats = {
        "username": data.get("login"),
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "avatar_url": data.get("avatar_url"),
        "bio": data.get("bio"),
        "location": data.get("location"),
    }
    
    return user_stats


def get_starred_repos(username):
    """Fetch the number of repositories a user has starred."""
    url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None
    
    # GitHub paginates this, so count all entries
    return len(response.json())


def get_user_organizations(username):
    """Fetch the organizations a user belongs to."""
    url = f"https://api.github.com/users/{username}/orgs"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None
    
    orgs = [org["login"] for org in response.json()]
    return orgs
