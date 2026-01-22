import json
import vosk
import sounddevice as sd

#vosk.SetLogLevel(-1)  # Désactive les logs

def listen():
    """Écoute l'utilisateur et retourne la transcription"""
    print("Dites quelque chose...")
    from module_language import model
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1) as stream:
        recognizer = vosk.KaldiRecognizer(model, 16000)
        recognizer.Reset()
        while True:
            data, _ = stream.read(4000)
            if recognizer.AcceptWaveform(bytes(data)):
                result = recognizer.Result()
                result_json = json.loads(result)
                text = result_json.get('text', '')
                print(f"Vous avez dit : {text}")
                return text
