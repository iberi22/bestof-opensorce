"""
Firebase Firestore integration for persisting processed repositories.

This module handles:
- Storing processed repository metadata
- Checking for duplicate processing
- Tracking video generation status
"""

import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64


class FirebaseStore:
    """
    Manages persistence of repository data using Firebase Firestore.

    Supports two initialization modes:
    1. Service account JSON file path
    2. Base64-encoded credentials (for CI/CD)
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Firebase connection.

        Args:
            credentials_path: Path to service account JSON or base64-encoded credentials.
                            If None, reads from FIREBASE_CREDENTIALS env var.

        Raises:
            ValueError: If credentials are not provided or invalid.
        """
        self.logger = logging.getLogger(__name__)

        # Get credentials from parameter or environment
        creds_source = credentials_path or os.getenv("FIREBASE_CREDENTIALS")

        if not creds_source:
            raise ValueError(
                "Firebase credentials required. Set FIREBASE_CREDENTIALS env var "
                "or pass credentials_path parameter."
            )

        # Initialize Firebase Admin SDK
        try:
            if not firebase_admin._apps:
                cred = self._load_credentials(creds_source)
                firebase_admin.initialize_app(cred)
                self.logger.info("Firebase Admin SDK initialized successfully")

            self.db = firestore.client()
            self.collection = self.db.collection('processed_repos')

        except Exception as e:
            self.logger.error(f"Failed to initialize Firebase: {e}")
            raise

    def _load_credentials(self, creds_source: str) -> credentials.Certificate:
        """
        Load Firebase credentials from file path or base64 string.

        Args:
            creds_source: File path or base64-encoded JSON credentials.

        Returns:
            Firebase Certificate object.
        """
        # Try as file path first
        if os.path.isfile(creds_source):
            self.logger.info(f"Loading credentials from file: {creds_source}")
            return credentials.Certificate(creds_source)

        # Try as base64-encoded JSON
        try:
            decoded = base64.b64decode(creds_source)
            creds_dict = json.loads(decoded)
            self.logger.info("Loading credentials from base64-encoded string")
            return credentials.Certificate(creds_dict)
        except Exception as e:
            self.logger.error(f"Failed to decode base64 credentials: {e}")
            raise ValueError(
                "FIREBASE_CREDENTIALS must be a valid file path or base64-encoded JSON"
            )

    def is_processed(self, repo_full_name: str) -> bool:
        """
        Check if a repository has already been processed.

        Args:
            repo_full_name: Full repository name (e.g., "owner/repo").

        Returns:
            True if repository exists in database, False otherwise.
        """
        try:
            doc = self.collection.document(repo_full_name).get()
            exists = doc.exists

            if exists:
                self.logger.info(f"Repository {repo_full_name} already processed")

            return exists

        except Exception as e:
            self.logger.error(f"Error checking if repo is processed: {e}")
            # Fail-safe: return False to allow processing
            return False

    def save_repo(
        self,
        repo_full_name: str,
        repo_data: Dict[str, Any],
        status: str = "pending"
    ) -> bool:
        """
        Save repository metadata to Firestore.

        Args:
            repo_full_name: Full repository name (e.g., "owner/repo").
            repo_data: Dictionary containing repository metadata.
            status: Processing status (pending, processing, completed, failed).

        Returns:
            True if save successful, False otherwise.
        """
        try:
            doc_data = {
                "repo_name": repo_full_name,
                "description": repo_data.get("description", ""),
                "stars": repo_data.get("stargazers_count", 0),
                "language": repo_data.get("language", "Unknown"),
                "status": status,
                "created_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "url": repo_data.get("html_url", ""),
            }

            self.collection.document(repo_full_name).set(doc_data)
            self.logger.info(f"Saved repository {repo_full_name} with status: {status}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving repository {repo_full_name}: {e}")
            return False

    def update_status(
        self,
        repo_full_name: str,
        status: str,
        video_url: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Update processing status of a repository.

        Args:
            repo_full_name: Full repository name.
            status: New status (processing, completed, failed).
            video_url: Optional YouTube video URL if completed.
            error_message: Optional error message if failed.

        Returns:
            True if update successful, False otherwise.
        """
        try:
            update_data = {
                "status": status,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }

            if video_url:
                update_data["video_url"] = video_url

            if error_message:
                update_data["error_message"] = error_message

            self.collection.document(repo_full_name).update(update_data)
            self.logger.info(f"Updated {repo_full_name} status to: {status}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating status for {repo_full_name}: {e}")
            return False

    def get_repo(self, repo_full_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve repository data from Firestore.

        Args:
            repo_full_name: Full repository name.

        Returns:
            Dictionary with repository data or None if not found.
        """
        try:
            doc = self.collection.document(repo_full_name).get()

            if doc.exists:
                return doc.to_dict()

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving repository {repo_full_name}: {e}")
            return None

    def get_recent_repos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recently processed repositories.

        Args:
            limit: Maximum number of repositories to return.

        Returns:
            List of repository dictionaries.
        """
        try:
            docs = (
                self.collection
                .order_by("created_at", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream()
            )

            repos = [doc.to_dict() for doc in docs]
            self.logger.info(f"Retrieved {len(repos)} recent repositories")
            return repos

        except Exception as e:
            self.logger.error(f"Error retrieving recent repos: {e}")
            return []
