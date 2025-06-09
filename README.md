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

- Python 3.13+
- GitHub Personal Access Token (PAT) with `repo` scope.
- `uv` Python package manager installed (see [uv installation](https://github.com/astral-sh/uv#installation)).

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

---

## Usage

After installation, you can run the tool directly from your terminal:

```bash
github-sync-fork
```

The tool will then securely prompt you to enter your GitHub Personal Access Token (PAT). Input your token and press Enter to proceed.

It will process all your forked repositories and attempt to sync each with its upstream repo, printing the status of each operation.

---

## Testing

To run the test suite, navigate to the project root directory and use pytest:

```bash
pytest src/test.py
```

This will execute the tests defined in `src/test.py`.

---