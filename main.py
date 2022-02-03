from dotenv import load_dotenv
import os
import json
import requests
from github import Github
import csv

load_dotenv()


def repo_sizes():
    token = os.environ.get("api-token")
    base_url = os.environ.get("base_url")
    org = os.environ.get("organisation")
    header = {'Authorization': 'token ' + token}

    name = []
    size = []
    url = []
    created_date = []

    g = Github(base_url=base_url,
               login_or_token=token)

    for repo in g.get_organization(org).get_repos():
        response = requests.get(
            f"{base_url}/repos/{org}/{repo.name}", headers=header)
        json_object = json.loads(response.content)
        kb = json_object["size"]
        mb = int(kb) / 1024
        name.append(repo.name)
        size.append(round(mb, 2))
        url.append(json_object["html_url"])
        created_date.append(json_object["created_at"])
    return name, size, url, created_date


def output(name, size, url, date):
    repo_list = zip(name, size, url, date)
    with open('repo_list.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'size in mb', 'url', 'created date'])
        writer.writerows(repo_list)


def main():
    repo_name, repo_size, repo_url, repo_created_date = repo_sizes()
    output(repo_name, repo_size, repo_url, repo_created_date)


if __name__ == "__main__":
    main()
