import requests
import os
import json


def get_commits_by_user(username, token):
    base_url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'}
    params = {
        # 'sort': 'updated', 'direction': 'desc',
        # "page":1
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(
            f"Error: Unable to fetch repositories. Status code: {response.status_code}")
        return None

    repositories = response.json()
    json.dump(repositories, open("repos.json", 'w', encoding="UTF-8"))

    recent_commits = []
    for repo in repositories:
        repo_name = repo['name']
        commits_url = f'https://api.github.com/repos/{username}/{repo_name}/commits'

        response = requests.get(commits_url, headers=headers)
        print(f"Repository: {repo_name}, Status code: {response.status_code}")

        if response.status_code != 200:
            continue

        commits = response.json()
        recent_commits.extend(commits)

    recent_commits.sort(key=lambda x: x["commit"]["committer"]["date"])
    return recent_commits


if __name__ == "__main__":
    # TODO: load username, token from .env
    if not os.path.exists("out.json"):
        commits_json = get_commits_by_user(username, token)
        json.dump(commits_json, open("out.json", 'w', encoding="UTF-8"))

    commits_json = json.load(open("out.json", 'r', encoding="UTF-8"))
    commits_json.sort(key=lambda x: x["commit"]["committer"]["date"])
    if commits_json:
        for commit in commits_json[-5:]:
            print(commit["commit"]["committer"]["date"])
            print(commit["commit"]["message"])
            print(commit["html_url"])
            print()
