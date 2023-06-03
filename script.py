from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)


def retrieve_emails(service, user_id, label_ids=[], max_results=40):
    results = service.users().messages().list(
        userId=user_id, labelIds=label_ids, maxResults=max_results).execute()
    messages = results.get('messages', [])
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            print(msg['snippet'])

retrieve_emails(service, 'joshisuryansh2005@gmail.com', label_ids=['INBOX'], max_results=20)

