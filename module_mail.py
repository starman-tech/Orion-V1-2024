#Finish

import os
import base64
import pickle
import os.path
import google.auth
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from a_config import chat_history

project_dir = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.readonly']
json_folder = os.path.join(project_dir, 'json')
credentials_path = os.path.join(json_folder, 'credentials.json')
token_path = os.path.join(json_folder, 'token.json')

def authenticate_gmail():
    """Obtient le service du calendrier Google avec des informations d'identification"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if os.path.exists(token_path):
        with open(token_path, 'r') as token:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(to,subject,message_text):
    """Crée le contenu d'un email à envoyer."""
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    
    msg = MIMEText(message_text, 'plain')
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}

def send_email(mail_detail):
    """Envoie un email via l'API Gmail."""
    try:
        service = authenticate_gmail()
        message = create_message(mail_detail['to'], mail_detail['subject'], mail_detail['message_text'])
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f"Message sent successfully to {mail_detail['to']}")
        return sent_message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

def list_recent_emails(service, max_results=10):
    """Liste les adresses e-mails des expéditeurs des derniers messages de la boîte de réception"""
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        print('Aucun message trouvé.')
    else:
        print(f'{len(messages)} derniers messages trouvés :\n')

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
            headers = msg['payload']['headers']

            for header in headers:
                if header['name'] == 'From':
                    from_header = header['value']
                    email_match = re.search(r'<(.+?)>', from_header)
                    if email_match:
                        email = email_match.group(1)
                    else:
                        email = from_header 
                    chat_history.append({"role": "assistant", "content": f'Expéditeur: {email}'})
                    break

