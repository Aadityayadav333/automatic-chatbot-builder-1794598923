
import os
import time

from utils.github_utils import (
    create_github_repo,
    commit_and_push_changes
)
from utils.load_env import load_env_file


class DeploymentAgent:

    def __init__(self):

        # Load environment variables
        env_vars = load_env_file() or {}

        # Get GitHub token
        self.github_token = (
            env_vars.get("GITHUB_TOKEN")
            or os.getenv("GITHUB_TOKEN")
        )

        if not self.github_token:
            raise ValueError(
                "Missing GITHUB_TOKEN. Please configure it in .env"
            )

        # Make token available to helper functions
        os.environ["GITHUB_TOKEN"] = self.github_token

        # Generate repository name
        ts = int(time.time())
        self.repo_name = f"automatic-chatbot-builder-{ts}"

        self.github_repo_url = None

    def deploy_now(self) -> str:

        # 1. Create GitHub repository
        print("[1/2] Creating GitHub repository...")

        self.github_repo_url = create_github_repo(
            self.repo_name
        )

        print("[SUCCESS] GitHub repository created.")

        # 2. Push project files
        print("[2/2] Pushing project files to GitHub...")

        commit_and_push_changes(
            self.github_repo_url,
            self.repo_name
        )

        print("[SUCCESS] Code pushed to GitHub.")

        return self.github_repo_url
