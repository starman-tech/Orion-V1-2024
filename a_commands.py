import re
import json
from a_tts import switch_tts_engine
from a_ai import switch_ai_engine, get_response_from_Al, send_image_to_model, get_response_from_Codeur
from a_tts import speak_in_chunks
from module_language import load_model
from module_google_search import get_website_text, google_search, format_results, google_first_link
from module_calendar_integration import add_event, delete_event, update_event, set_reminder
from module_screenshot import Picture
from module_mail import send_email, list_recent_emails, authenticate_gmail
from module_application_launcher import launcher
from module_injecteur import execute_code_with_dependencies,testr

def extract_commands(text):
    """Extrait toutes les commandes du texte sous forme de tuples (command_type, command, params)"""
    command_pattern = r'\["([^;]+)";"([^"]+)"\](?:;({.*?}))?'
    matches = re.findall(command_pattern, text)
    commands = [
        (match[0], match[1], json.loads(match[2]) if match[2] else None)
        for match in matches
    ]
    return commands

def execute_command(commands):
    """Exécute les commandes données"""
    for command_type, command, params in commands:
        if command_type == "notread":
            if command == "none":
                print('')

        if command_type == "gmail":
            if command == "send":
                send_email(params)
            elif command == "list":
                service = authenticate_gmail()
                list_recent_emails(service)

        elif command_type == "code" :
            if command == "new":
                code2 = params["thecode"]
                response = get_response_from_Codeur(code2)
                response2 = testr(response)
                execute_code_with_dependencies(response2)
                
        elif command_type == "open" :
            if command == "app" :
                launcher.search_and_open_app(params)
            if command == "web" :
                launcher.open_url_in_chrome(params)
            if command == "websearch" :
                open_link = google_first_link(params)
                launcher.open_url_in_chrome(open_link)

        elif command_type == "switch":
            if command == "tts":
                switch_tts_engine()
            elif command == "ai":
                switch_ai_engine()
                load_model("fr")
            elif command == "language":
                load_model(params['lang'])

        elif command_type == "calendar":
            if command == "add":
                add_event(params)
            elif command == "delete":
                delete_event(params)
            elif command == "update":
                update_event(params)
            elif command == "reminder":
                set_reminder(params)
            
        elif command_type == "web":
            if command == "search":
                results = google_search(params["query"])
                formatted_results = format_results(results)
                print(formatted_results)
                response = get_response_from_Al(formatted_results)
                print(f"Assistant1 : {response}")
                commands = extract_commands(response)
                if commands:
                    execute_command(commands)
                    for command_type, command, params in commands:
                        response = response.replace(f'["{command_type}";"{command}"]', '')
                        if params:
                            response = response.replace(f';{json.dumps(params)}', '')
                if response.strip():
                    speak_in_chunks(response)

            if command == "visit":
                url = params['url']
                website_text = get_website_text(url)
                response = get_response_from_Al(f"Text from {url}:\n{website_text}")
                print(f"Assistant2 : {response}")
                commands = extract_commands(response)
                if commands:
                    execute_command(commands)
                    for command_type, command, params in commands:
                        response = response.replace(f'["{command_type}";"{command}"]', '')
                        if params:
                            response = response.replace(f';{json.dumps(params)}', '')
                if response.strip():
                    speak_in_chunks(response)

        elif command_type == "image":
            if command == "capture":
                image_url = Picture.take_photo()
                transcription = send_image_to_model(image_url,params)
                response = get_response_from_Al(transcription)
                print(f"Assistant12 : {response}")
                speak_in_chunks(response)
            elif command == "screenshot":
                screenshot_url = Picture.take_screenshot()
                transcription = send_image_to_model(screenshot_url,params)
                print(f"Assistant12 : {transcription}")
                speak_in_chunks(transcription)
      
        else:
            print(f"Commande non reconnue : {command_type} - {command}")

        