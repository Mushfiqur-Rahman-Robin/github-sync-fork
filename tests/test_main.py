import unittest
from unittest.mock import patch, MagicMock
import src.main as main

class TestSyncAllForks(unittest.TestCase):

    @patch("src.main.requests.post")
    @patch("src.main.Github")
    def test_sync_all_forks_success_and_failure(self, mock_github_class, mock_post):
        fake_token = "fake_token"

        # Mock Github instance and user repos
        mock_github = MagicMock()
        mock_user = MagicMock()
        mock_repo_fork = MagicMock()
        mock_repo_nonfork = MagicMock()

        # Fork repo with parent (should be processed)
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

        # Simulate a successful sync response
        def post_side_effect(url, headers, json):
            mock_resp = MagicMock()
            if "forked_repo" in url:
                mock_resp.status_code = 200
                mock_resp.json.return_value = {"message": "Up to date"}
            else:
                mock_resp.status_code = 400
                mock_resp.json.return_value = {"message": "Error"}
            return mock_resp

        mock_post.side_effect = post_side_effect

        # Call function
        results = main.sync_all_forks(fake_token)

        # Assertions
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["repo"], "user/forked_repo")
        self.assertEqual(results[0]["status"], "synced")
        self.assertIn("Up to date", results[0]["message"])

if __name__ == "__main__":
    unittest.main()
