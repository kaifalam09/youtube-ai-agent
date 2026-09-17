"""
Uploads a video to the authenticated user's own YouTube channel
using the official YouTube Data API v3.

Requires client_secret.json (from Google Cloud Console) in the project root.
On first run, opens a browser for OAuth consent; saves token.json for reuse.
"""
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import config


def _get_credentials():
    creds = None
    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            config.TOKEN_FILE, config.YOUTUBE_SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(config.CLIENT_SECRET_FILE):
                raise FileNotFoundError(
                    "client_secret.json not found. Download it from "
                    "Google Cloud Console (OAuth client, Desktop app type) "
                    "and place it in the project root. See README.md."
                )
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                config.CLIENT_SECRET_FILE, config.YOUTUBE_SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(config.TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    privacy_status: str = "private",
    category_id: str = "22",
) -> str:
    """
    Uploads video_path to the user's own channel.
    privacy_status: 'private', 'unlisted', or 'public'. Defaults to
    'private' so nothing goes live by accident — change it explicitly
    when you're ready to publish.
    Returns the uploaded video's URL.
    """
    creds = _get_credentials()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = googleapiclient.http.MediaFileUpload(
        video_path, chunksize=-1, resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    return f"https://youtu.be/{video_id}"
