import json
from a_stt import listen
from a_ai import get_response
from a_tts import speak_in_chunks
from a_commands import extract_commands, execute_command
from a_config import current_ai_engine, current_tts_engine, current_tts_lang,ai_engines

def main():
    developer_mode = True
    print(f"Paramètres actuels :\n"
      f"  TTS Engine : {current_tts_engine}\n"
      f"  AI Engine  : {current_ai_engine}\n"
      f"  TTS Langue : {current_tts_lang}\n"
      f"  AI Engines : {', '.join(ai_engines)}")
    print(f'')

    while True:
        if developer_mode:
            user_input = input("Entrez votre message : ").strip()
        else:
            user_input = listen()

        if user_input:
            response = get_response(user_input)
            print(f"Assistant : {response}")

            commands = extract_commands(response)
            if commands:
                execute_command(commands)
                for command_type, command, params in commands:
                    response = response.replace(f'["{command_type}";"{command}"]', '')
                    if params:
                        response = response.replace(f';{json.dumps(params)}', '')
            if response.strip():
                speak_in_chunks(response)
                    
main()