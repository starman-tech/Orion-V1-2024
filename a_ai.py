from datetime import datetime
from a_config import client, openai_client, current_ai_engine, chat_history, discussion
import base64

def encode_image_to_data_url(image_path):
    """Encode l'image locale en data URL."""
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        mime_type = "image/png"  # Assurez-vous que le type MIME correspond à votre image (png, jpeg, etc.)
        return f"data:{mime_type};base64,{base64_image}"

def send_image_to_model(image_path,prompt):
    """Envoie une image locale au modèle sous forme de data URL."""
    image_data_url = encode_image_to_data_url(image_path)
    
    completion = client.chat.completions.create(
        model="llava-v1.5-7b-4096-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    transcription = completion.choices[0].message.content
    chat_history.append({"role": "assistant", "content": transcription})
    return transcription

def switch_ai_engine():
    """Bascule entre les moteurs AI"""
    from a_config import ai_engines
    global current_ai_engine
    current_index = ai_engines.index(current_ai_engine)
    current_ai_engine = ai_engines[(current_index + 1) % len(ai_engines)]
    print(f"Moteur AI changé en : {current_ai_engine}")

def get_response(user_input): 
    """Ajoute le timestamp au message de l'utilisateur et renvoie la réponse de l'IA"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_input_with_time = f"[{current_time}] {user_input}"

    chat_history.append({"role": "user", "content": user_input_with_time})

    if "gpt-4" in current_ai_engine:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history,
        ).choices[0].message.content
    else:
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model=current_ai_engine,
        )
        response = chat_completion.choices[0].message.content

    chat_history.append({"role": "assistant", "content": response})
    return response

def get_response_from_Codeur(Codeur_input): 
    """Ajoute le timestamp au message de l'utilisateur et renvoie la réponse de l'IA"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Codeur_input_with_time = f"[{current_time}] {Codeur_input}"

    discussion.append({"role": "user", "content": Codeur_input_with_time})
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=discussion,
    ).choices[0].message.content

    discussion.append({"role": "assistant", "content": response})
    print(response)
    return response

def get_response_from_Al(Al_input): 
    """Ajoute le timestamp au message de l'utilisateur et renvoie la réponse de l'IA"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Al_input_with_time = f"[{current_time}] {Al_input}"

    chat_history.append({"role": "user", "content": Al_input_with_time})
    if "gpt-4" in current_ai_engine:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history,
        ).choices[0].message.content
    else:
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model=current_ai_engine,
        )
        response = chat_completion.choices[0].message.content

    chat_history.append({"role": "assistant", "content": response})
    print(response)
    return response
    