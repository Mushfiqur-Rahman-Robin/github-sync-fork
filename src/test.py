import unittest
from unittest.mock import patch, MagicMock
import main

class TestSyncAllForks(unittest.TestCase):

    @patch("main.requests.post")
    @patch("main.Github")
    @patch("main.os.getenv")
    def test_sync_all_forks_success_and_failure(self, mock_getenv, mock_github_class, mock_post):
        # Setup mock environment variable
        mock_getenv.return_value = "fake_token"

        # Mock Github instance and user repos
        mock_github = MagicMock()
        mock_user = MagicMock()
        mock_repo_fork = MagicMock()
        mock_repo_nonfork = MagicMock()

        # Fork repo with parent (should attempt sync)
        mock_repo_fork.fork = True
        mock_repo_fork.parent = True
        mock_repo_fork.full_name = "user/forked_repo"
        mock_repo_fork.default_branch = "main"

        # Non-fork repo (should be skipped)
        mock_repo_nonfork.fork = False
        mock_repo_nonfork.parent = None
        mock_repo_nonfork.full_name = "user/nonforked_repo"

        mock_user.get_repos.return_value = [mock_repo_fork, mock_repo_nonfork]
        mock_github.get_user.return_value = mock_user
        mock_github_class.return_value = mock_github

        # Mock requests.post to simulate a successful sync and a failed sync
        def post_side_effect(url, headers, json):
            if "forked_repo" in url:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {"message": "Up to date"}
                return mock_resp
            else:
                mock_resp = MagicMock()
                mock_resp.status_code = 400
                mock_resp.json.return_value = {"message": "Error"}
                return mock_resp

        mock_post.side_effect = post_side_effect

        results = main.sync_all_forks()

        # It should only process the forked repo, skipping non-fork
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["repo"], "user/forked_repo")
        self.assertEqual(results[0]["status"], "synced")
        self.assertIn("Up to date", results[0]["message"])

if __name__ == "__main__":
    unittest.main()
