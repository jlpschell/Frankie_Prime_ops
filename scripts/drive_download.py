#!/usr/bin/env python3
"""Download files from Google Drive"""

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

CREDS_PATH = "/home/plotting1/frankie-bot/workspace/credentials/token.json"
DOWNLOAD_DIR = "/home/plotting1/frankie-bot/workspace/drive_sync"

def get_service():
    with open(CREDS_PATH, 'r') as f:
        token_data = json.load(f)
    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data['refresh_token'],
        token_uri=token_data['token_uri'],
        client_id=token_data['client_id'],
        client_secret=token_data['client_secret'],
        scopes=token_data['scopes']
    )
    return build('drive', 'v3', credentials=creds)

def download_file(service, file_id, file_name, mime_type, dest_dir):
    """Download a single file"""
    file_path = os.path.join(dest_dir, file_name)
    os.makedirs(dest_dir, exist_ok=True)

    export_types = {
        'application/vnd.google-apps.document': ('text/plain', '.txt'),
        'application/vnd.google-apps.spreadsheet': ('text/csv', '.csv'),
    }

    try:
        if mime_type in export_types:
            export_mime, ext = export_types[mime_type]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            file_path += ext
        else:
            request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  Progress: {int(status.progress() * 100)}%")

        with open(file_path, 'wb') as f:
            f.write(fh.getvalue())

        size_mb = len(fh.getvalue()) / (1024 * 1024)
        print(f"  Downloaded: {file_path} ({size_mb:.2f} MB)")
        return file_path
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    service = get_service()

    # Create directories
    takeout_dir = os.path.join(DOWNLOAD_DIR, "takeout")
    ghl_dir = os.path.join(DOWNLOAD_DIR, "ghl")
    notebooklm_dir = os.path.join(DOWNLOAD_DIR, "notebooklm")

    # Download Takeout zips
    print("=== Downloading Takeout ZIPs ===")
    query = "name contains 'takeout' and mimeType = 'application/x-zip'"
    results = service.files().list(q=query, fields="files(id, name, mimeType, size)").execute()
    for f in results.get('files', []):
        print(f"\nDownloading: {f['name']} ({int(f.get('size', 0))/(1024*1024):.1f} MB)")
        download_file(service, f['id'], f['name'], f['mimeType'], takeout_dir)

    # Download GHL docs
    print("\n=== Downloading GoHighLevel docs ===")
    ghl_files = [
        ("HumanLedAI_GHL account details", "application/vnd.google-apps.document"),
        ("Go high level", "application/vnd.google-apps.document"),
        ("GoHighLevel Onboarding Walkthrough.pdf", "application/pdf"),
        ("Copy of Voicemail + SMS", "application/vnd.google-apps.document"),
    ]

    for name, expected_mime in ghl_files:
        query = f"name = '{name}'"
        results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        files = results.get('files', [])
        if files:
            f = files[0]
            print(f"\nDownloading: {f['name']}")
            download_file(service, f['id'], f['name'], f['mimeType'], ghl_dir)

    # Download NotebookLM docs
    print("\n=== Downloading NotebookLM docs ===")
    query = "name contains 'notebook' or name contains 'NotebookLM'"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    for f in results.get('files', []):
        print(f"\nDownloading: {f['name']}")
        download_file(service, f['id'], f['name'], f['mimeType'], notebooklm_dir)

    print("\n=== Done ===")

if __name__ == "__main__":
    main()
