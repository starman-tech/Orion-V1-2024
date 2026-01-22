import io
import re
import threading
from gtts import gTTS
from queue import Queue
from pydub import AudioSegment
from pydub.playback import play
from a_config import current_tts_engine, openai_client

def speak_chunk(chunk, queue):
    """Convertit un morceau de texte en parole et le joue immédiatement"""
    from module_language import current_tts_lang
    audio_segment = None
    if current_tts_engine == "openai":
        print(f"Conversion de la phrase avec OpenAI TTS : {chunk}")
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=chunk
        )
        audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    else:
        tts = gTTS(text=chunk, lang=current_tts_lang) 
        with io.BytesIO() as f:
            tts.write_to_fp(f)
            f.seek(0)
            audio_segment = AudioSegment.from_file(f, format="mp3")
    
    queue.put(audio_segment)

def split_text_into_sentences(text):
    """Divise le texte en phrases"""
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences

def switch_tts_engine():
    """Bascule entre les moteurs TTS OpenAI et gTTS"""
    global current_tts_engine
    current_tts_engine = "gtts" if current_tts_engine == "openai" else "openai"
    print(f"Moteur TTS changé en : {current_tts_engine}")

def play_audio(queue):
    """Lit l'audio depuis la queue"""
    while True:
        audio_segment = queue.get()
        if audio_segment is None:
            break
        play(audio_segment)

def speak_in_chunks(text):
    """Convertit le texte en phrases en parole et les joue séquentiellement"""
    sentences = split_text_into_sentences(text)
    queue = Queue()

    play_thread = threading.Thread(target=play_audio, args=(queue,))
    play_thread.start()

    for sentence in sentences:
        speak_chunk(sentence, queue)

    queue.put(None)
    play_thread.join()
