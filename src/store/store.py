import sys 
import os
from dotenv import load_dotenv
import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
from decouple import config

load_dotenv()
work_dir = os.getenv('WORK_DIR')

sys.path.append(work_dir)

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = service_account.Credentials.from_service_account_file(config('SERVICE_ACCOUNT_FILE'), scopes=SCOPES)
    return creds

def upload_file(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': "merged_data.csv",
        'parents': [config('PARENT_FOLDER_ID')],
        'mimeType': 'text/csv'
    }

    media = MediaInMemoryUpload(file_path, mimetype='text/csv')

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        print("File uploaded successful")
    except Exception as e:
        print("Error:", e)
