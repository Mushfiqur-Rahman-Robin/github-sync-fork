import os
import requests
from github import Github
import click
import getpass

def sync_all_forks(github_token):
    gh = Github(github_token)
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
            "Authorization": f"Bearer {github_token}",
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

@click.command()
@click.pass_context
def sync_all_forks_cli(ctx):
    """Synchronizes all your forked repositories with their upstream counterparts."""
    click.echo("Please enter your GitHub Personal Access Token (PAT):")
    token = getpass.getpass()

    if not token:
        click.echo("Error: GitHub token cannot be empty.", err=True)
        ctx.exit(1)

    results = sync_all_forks(token)
    for res in results:
        if res["status"] == "synced":
            click.echo(f"Successfully synced {res['repo']}: {res['message']}")
        else:
            click.echo(f"Failed to sync {res['repo']}: {res.get('error', 'Unknown error')}", err=True)
