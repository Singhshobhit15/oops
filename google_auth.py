# google_auth.py
import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists('token_calendar.pkl'):
        with open('token_calendar.pkl', 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_calendar.pkl', 'wb') as f:
            pickle.dump(creds, f)

    return build('calendar', 'v3', credentials=creds)

# if __name__ == "__main__":
#     get_calendar_service()
