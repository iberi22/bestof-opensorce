"""
Blog Manager for Git operations.

Handles branch creation, commits, and pull requests for blog posts.
"""

import logging
import subprocess
from typing import List, Optional, Dict, Any
from pathlib import Path
import requests
import os


class BlogManager:
    """
    Manages Git operations for the blog.

    Handles:
    - Creating branches for new posts
    - Committing files
    - Creating pull requests
    - Auto-merging (if checks pass)
    """

    def __init__(self, repo_path: str = ".", github_token: Optional[str] = None):
        """
        Initialize BlogManager.

        Args:
            repo_path: Path to the Git repository.
            github_token: GitHub personal access token for API operations.
        """
        self.logger = logging.getLogger(__name__)
        self.repo_path = Path(repo_path)
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

        if not self.github_token:
            self.logger.warning("No GitHub token provided. PR creation will not work.")

    def create_branch(self, branch_name: str) -> bool:
        """
        Create a new Git branch.

        Args:
            branch_name: Name of the branch to create.

        Returns:
            True if successful, False otherwise.
        """
        try:
            # Ensure we're on main/master
            self._run_git_command(["checkout", "main"])

            # Pull latest changes
            self._run_git_command(["pull", "origin", "main"])

            # Create and checkout new branch
            self._run_git_command(["checkout", "-b", branch_name])

            self.logger.info(f"Created branch: {branch_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create branch: {e}")
            return False

    def commit_files(self, files: List[str], message: str) -> bool:
        """
        Commit files to the current branch.

        Args:
            files: List of file paths to commit.
            message: Commit message.

        Returns:
            True if successful, False otherwise.
        """
        try:
            # Add files
            for file in files:
                self._run_git_command(["add", file])

            # Commit
            self._run_git_command(["commit", "-m", message])

            self.logger.info(f"Committed {len(files)} files: {message}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to commit files: {e}")
            return False

    def push_branch(self, branch_name: str) -> bool:
        """
        Push branch to remote.

        Args:
            branch_name: Name of the branch to push.

        Returns:
            True if successful, False otherwise.
        """
        try:
            self._run_git_command(["push", "-u", "origin", branch_name])

            self.logger.info(f"Pushed branch: {branch_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to push branch: {e}")
            return False

    def create_pull_request(
        self,
        branch_name: str,
        title: str,
        body: str,
        repo_owner: str,
        repo_name: str
    ) -> Optional[str]:
        """
        Create a pull request via GitHub API.

        Args:
            branch_name: Source branch name.
            title: PR title.
            body: PR description.
            repo_owner: Repository owner (username or org).
            repo_name: Repository name.

        Returns:
            PR URL if successful, None otherwise.
        """
        if not self.github_token:
            self.logger.error("GitHub token required for PR creation")
            return None

        try:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"

            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            data = {
                "title": title,
                "body": body,
                "head": branch_name,
                "base": "main"
            }

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            pr_data = response.json()
            pr_url = pr_data.get("html_url")

            self.logger.info(f"Created PR: {pr_url}")
            return pr_url

        except Exception as e:
            self.logger.error(f"Failed to create PR: {e}")
            return None

    def auto_merge(
        self,
        pr_number: int,
        repo_owner: str,
        repo_name: str
    ) -> bool:
        """
        Auto-merge a pull request if checks pass.

        Args:
            pr_number: Pull request number.
            repo_owner: Repository owner.
            repo_name: Repository name.

        Returns:
            True if merged, False otherwise.
        """
        if not self.github_token:
            self.logger.error("GitHub token required for auto-merge")
            return False

        try:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/merge"

            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            data = {
                "commit_title": "Auto-merge blog post",
                "merge_method": "squash"
            }

            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()

            self.logger.info(f"Auto-merged PR #{pr_number}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to auto-merge: {e}")
            return False

    def _run_git_command(self, args: List[str]) -> str:
        """
        Run a Git command.

        Args:
            args: Git command arguments.

        Returns:
            Command output.

        Raises:
            subprocess.CalledProcessError: If command fails.
        """
        cmd = ["git"] + args
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def get_current_branch(self) -> str:
        """
        Get the name of the current Git branch.

        Returns:
            Branch name.
        """
        return self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

    def branch_exists(self, branch_name: str) -> bool:
        """
        Check if a branch exists.

        Args:
            branch_name: Branch name to check.

        Returns:
            True if exists, False otherwise.
        """
        try:
            self._run_git_command(["rev-parse", "--verify", branch_name])
            return True
        except subprocess.CalledProcessError:
            return False
