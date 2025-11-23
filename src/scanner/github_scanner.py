import requests
import datetime
import os
import logging

class GitHubScanner:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.api_url = "https://api.github.com"

    def scan_recent_repos(self, query="created:>2023-01-01", limit=10):
        # In a real scenario, we would calculate the timestamp for "last hour"
        # one_hour_ago = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat()
        # query = f"created:>{one_hour_ago} {query}"

        url = f"{self.api_url}/search/repositories?q={query}&sort=updated&order=desc&per_page={limit}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logging.error(f"Error searching repos: {response.text}")
            return []

        return response.json().get("items", [])

    def validate_repo(self, repo):
        # 1. Check for CI status
        if not self._check_ci_status(repo["full_name"]):
            return False

        # 2. Check for Description and Readme
        if not repo.get("description"):
            return False

        # 3. Check for Alpha/Test keywords (basic filter)
        keywords = ["alpha", "test", "demo", "example"]
        if any(k in repo["name"].lower() for k in keywords):
            # Allow beta if explicitly checked (logic to be improved)
            if "beta" not in repo["name"].lower():
                return False

        return True

    def _check_ci_status(self, repo_full_name):
        url = f"{self.api_url}/repos/{repo_full_name}/actions/runs?per_page=1"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            if runs:
                latest_run = runs[0]
                return latest_run["conclusion"] == "success"
        return False # Assume false if no runs or error, or make lenient
