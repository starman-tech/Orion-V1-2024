#Finish

import os
import vosk
from a_config import current_tts_lang

LANG_MODELS = {
    'fr': 'vosk-model-small-fr-0.22',
    'en': 'vosk-model-small-en-us-0.15',
    'es': 'vosk-model-small-es-0.42',
    'it': 'vosk-model-small-it-0.22',
    'de': 'vosk-model-small-de-0.15'
}

project_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_dir, 'models', 'vosk-model-small-fr-0.22')
model = vosk.Model(model_path)

def load_model(lang):
    """Charge le modèle de la langue spécifiée."""
    global model, current_tts_lang
    current_tts_lang = lang
    from a_stt import listen
    if lang in LANG_MODELS:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(project_dir, 'models', LANG_MODELS[lang])
        model = vosk.Model(model_path)
    else:
        raise ValueError(f"Unsupported language '{lang}'. Supported languages are: {', '.join(LANG_MODELS.keys())}")

