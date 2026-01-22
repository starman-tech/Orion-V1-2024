#Finish

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
from a_config import chat_history

project_dir = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.readonly']
json_folder = os.path.join(project_dir, 'json')
credentials_path = os.path.join(json_folder, 'credentials.json')
token_path = os.path.join(json_folder, 'token.json')

def get_calendar_service():
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

    
    return build('calendar', 'v3', credentials=creds)

calendar_service = get_calendar_service()

def add_event(event_details):
    """Ajoute un événement au calendrier"""
    event = {
        'summary': event_details['summary'],
        'start': {
            'dateTime': event_details['start'],
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': event_details['end'],
            'timeZone': 'Europe/Paris',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    event = calendar_service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
    chat_history.append({"role": "evenement", "content": f"Evenement Créé : Titre:{event_details['summary']}; ID:{event.get('id')}"})

def delete_event(event_id):
    """Supprime un événement du calendrier"""
    try:
        calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()
        print("Event deleted.")
    except HttpError as error:
        print(f"An error occurred: {error}")
    
    chat_history.append({"role": "evenement", "content": f"Evenement Supprimé : ID: {event_id}"})

def update_event(event_id, event_details):
    """Met à jour un événement dans le calendrier"""
    event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
    event['summary'] = event_details.get('summary', event['summary'])
    event['start']['dateTime'] = event_details.get('start', event['start']['dateTime'])
    event['end']['dateTime'] = event_details.get('end', event['end']['dateTime'])
    updated_event = calendar_service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    print(f"Event updated: {updated_event.get('htmlLink')}")

def set_reminder(event_id, reminder_time):
    """Définit un rappel pour un événement"""
    event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
    event['reminders'] = {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': reminder_time},
            {'method': 'popup', 'minutes': reminder_time},
        ],
    }
    updated_event = calendar_service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    print(f"Reminder set for event: {updated_event.get('htmlLink')}")
