import os
import logging
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    def __init__(self, client_secret_file, token_file="token.pickle"):
        self.client_secret_file = client_secret_file
        self.token_file = token_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.youtube = self._authenticate()

    def _authenticate(self):
        credentials = None

        # Load existing credentials
        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                credentials = pickle.load(token)

        # Refresh or create new credentials
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                logging.info("Refreshing access token...")
                credentials.refresh(Request())
            else:
                logging.info("Fetching new tokens (User Interaction Required)...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, self.scopes
                )
                credentials = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_file, "wb") as token:
                pickle.dump(credentials, token)

        return build("youtube", "v3", credentials=credentials)

    def upload_video(self, video_path, title, description, tags=None, category_id="28", privacy_status="private"):
        if not os.path.exists(video_path):
            logging.error(f"Video file not found: {video_path}")
            return False

        if tags is None:
            tags = []

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        logging.info(f"Uploading {video_path} to YouTube...")

        try:
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logging.info(f"Uploaded {int(status.progress() * 100)}%")

            logging.info(f"Upload Complete! Video ID: {response.get('id')}")
            return True

        except Exception as e:
            logging.error(f"An error occurred during upload: {e}")
            return False
