#!/usr/bin/env python3
"""
Google OAuth Setup for Frankie
Run this once to authorize Google Sheets access.
"""

import os
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser
import threading

# Check for required packages
try:
    from google_auth_oauthlib.flow import Flow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    print("Missing packages. Run:")
    print("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    exit(1)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.readonly'
]

CREDENTIALS_DIR = Path(__file__).parent.parent / 'credentials'
CLIENT_SECRET = CREDENTIALS_DIR / 'google_oauth.json'
TOKEN_FILE = CREDENTIALS_DIR / 'token.json'

# Store the auth code from callback
auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    """Handle the OAuth callback."""

    def do_GET(self):
        global auth_code
        query = parse_qs(urlparse(self.path).query)

        if 'code' in query:
            auth_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Authorization Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                </body></html>
            ''')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error = query.get('error', ['Unknown error'])[0]
            self.wfile.write(f'<html><body><h1>Error: {error}</h1></body></html>'.encode())

    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

def authenticate():
    """Run OAuth flow and save token."""
    global auth_code
    creds = None

    # Load existing token if available
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...\n")

            # Use localhost redirect (no trailing slash — must match Google Console exactly)
            redirect_uri = 'http://localhost:8085'

            flow = Flow.from_client_secrets_file(
                str(CLIENT_SECRET),
                scopes=SCOPES,
                redirect_uri=redirect_uri
            )

            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )

            print("=" * 60)
            print("STEP 1: Copy this URL and open it in your browser:\n")
            print(auth_url)
            print("\n" + "=" * 60)
            print("\nSTEP 2: Sign in with humanledai@gmail.com")
            print("STEP 3: After approval, you'll be redirected.")
            print("\nWaiting for authorization...\n")

            # Start local server to catch the callback
            server = HTTPServer(('localhost', 8085), OAuthHandler)
            server.timeout = 300  # 5 minute timeout

            # Try to open browser (may not work in WSL)
            try:
                webbrowser.open(auth_url)
            except:
                pass

            # Wait for callback
            while auth_code is None:
                server.handle_request()

            server.server_close()

            # Exchange code for token
            flow.fetch_token(code=auth_code)
            creds = flow.credentials

        # Save token for future use
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print(f"\nToken saved to {TOKEN_FILE}")

    return creds

def test_sheets_access():
    """Test access to the tracking spreadsheet."""
    creds = authenticate()

    # Load sheet ID from env
    from dotenv import load_dotenv
    load_dotenv(CREDENTIALS_DIR / '.env')
    sheet_id = os.getenv('GOOGLE_SHEET_ID', '1_RfKelGdoc2teeAluqKJ1aYhXLBT-IwBCLeCYDy_CHI')

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Get spreadsheet metadata
        result = sheet.get(spreadsheetId=sheet_id).execute()
        print(f"\nConnected to: {result['properties']['title']}")
        print(f"Sheets: {[s['properties']['title'] for s in result['sheets']]}")
        print("\nGoogle Sheets access working!")
        return True
    except Exception as e:
        print(f"Error accessing sheet: {e}")
        return False

if __name__ == '__main__':
    print("=== Google OAuth Setup ===\n")
    test_sheets_access()
