import os
import requests
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("Set GITHUB_TOKEN with write access to forks")

def sync_all_forks():
    gh = Github(GITHUB_TOKEN)
    me = gh.get_user()
    results = []
    for repo in me.get_repos():
        if not repo.fork or not repo.parent:
            continue
        print(f"Accessing repository: {repo.full_name}")
        owner, name = repo.full_name.split("/")
        branch = repo.default_branch
        url = f"https://api.github.com/repos/{owner}/{name}/merge-upstream"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        resp = requests.post(url, headers=headers, json={"branch": branch})
        if resp.status_code == 200:
            msg = resp.json().get("message", "")
            results.append({"repo": repo.full_name, "status": "synced", "message": msg})
        else:
            results.append({
                "repo": repo.full_name,
                "status": "failed",
                "code": resp.status_code,
                "error": resp.json().get("message", resp.text)
            })
    return results

if __name__ == "__main__":
    sync_results = sync_all_forks()
    for res in sync_results:
        print(res)
