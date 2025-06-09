# GitHub Fork Sync Tool

A Python tool to automatically sync all your forked GitHub repositories with their upstream sources using the GitHub API's new "merge-upstream" endpoint. It keeps your forks up to date effortlessly by triggering merges on the default branch of each fork.

---

## Features

- Sync all forked repositories under your GitHub user automatically
- Uses GitHub Personal Access Token for authentication
- Handles success and failure responses per repository
- Simple CLI script with minimal dependencies

---

## Prerequisites

- Python 3.13+ (flexible with other versions as well)
- GitHub Personal Access Token (PAT) with `repo` permissions
- `uv` package manager installed

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Mushfiqur-Rahman-Robin/github-sync-fork.git
   cd github-sync-fork
   ```

2. **Create virtual environment**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies using uv**

   Dependencies are defined in `pyproject.toml`. To install them:

   ```bash
   uv sync
   ```

   This command reads from `pyproject.toml` and installs the exact versions specified.

4. **Set your GitHub token**

   Create a `.env` file in the root folder with:

   ```
   GITHUB_TOKEN=ghp_rest_of_the_personal_access_token_here
   ```

---

## Usage

Run the sync script from the root directory:

```bash
cd src/
uv run main.py
```

It will process all your forked repositories and attempt to sync each with its upstream repo.

---

## Testing

Run the test suite with uv:

```bash
cd src/
pytest test.py
```

---