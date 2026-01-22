<p align="center">
  <img src="https://raw.githubusercontent.com/starman-tech/Orion-V1-2024/orion.png" width="760"/>
</p>

<h1 align="center">🌌 ORION V1</h1>

<p align="center">
  <b>Hybrid AI Assistant Prototype</b><br/>
  <i>Local-first voice assistant combining STT, LLM and TTS with system automation.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Type-Research%20Prototype-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/AI-STT%20%7C%20LLM%20%7C%20TTS-purple?style=for-the-badge">
</p>

<p align="center">
  <a href="https://discord.gg/nZtKJJtsyA">
    <img src="https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  </a>
</p>

<hr style="border:1px solid #333"/>

<p align="center">
  ⚡ <b>Experimental Jarvis-like assistant for offline/online AI research</b> ⚡  
</p>

---

# Orion-V1-2024


> Remarque : ce projet est un prototype personnel de type "Jarvis" écrit en Python, créé il y a ~2–3 ans. Beaucoup de techniques et d'API sont aujourd'hui datées ou fragiles, mais le code sert de base d'apprentissage pour bâtir un assistant hybride (STT + LLM + TTS) hors-ligne/en-ligne.

---

## 🏅 Badges

[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg?style=flat-square)](https://github.com/starman-tech/Orion-V1-2024/releases)

---
## Enoncé du problème
Construire un assistant vocal local qui :
- Écoute l'utilisateur (STT),
- Envoie du texte à un moteur IA (clients Groq / OpenAI dans ce prototype),
- Extrait des commandes structurées renvoyées par l'IA,
- Exécute des actions système utiles (ouvrir applis/URLs, calendrier, Gmail, maps, capture image/screenshot),
- Répond à voix (TTS).

Ce dépôt assemble des composants open-source : STT (Vosk), TTS (gTTS ou OpenAI), clients IA (Groq/OpenAI), et des modules d'intégration système.

---

## Ce qui fonctionne (aujourd'hui)
- STT hors-ligne avec Vosk (modèles fournis dans models/ pour fr/en/es/it/de).
- TTS via gTTS (par défaut). Option OpenAI TTS si activée et configurée.
- Boucle conversationnelle de base : a_main.py (entrée -> get_response -> extract_commands -> execute -> speak).
- Changement de langue : module_language.load_model(lang).
- Parsing et exécution de commandes JSON-like (a_commands.py) : switch, gmail, calendar, websearch/open, image capture/screenshot, open app.
- Modules utilitaires inclus : module_google_search, module_mail, module_application_launcher, module_maps, module_screenshot/picture, module_injecteur (dangerux).
- Modèles Vosk "small" embarqués pour usage hors-ligne.

---

## Ce qui est obsolète, fragile ou dangereux
- Appels Groq/OpenAI et noms de modèles (ex. "llama3-*", "gpt-4o") datent d'expérimentations : vérifiez et adaptez aux APIs actuelles.
- module_google_search scrappe google.com en HTML : fragile et susceptible de violer les ToS.
- module_application_launcher repose sur des hypothèses OS et chemins codés — peut nécessiter adaptation par OS.
- module_injecteur installe des paquets et exécute du code généré automatiquement — extrêmement dangereux. Ne l'activez pas sur une machine exposée.
- L'intégration calendrier / certaines fonctions peuvent être incomplètes selon l'état du dépôt.

---

## Démarrage rapide (exécution locale)

1. Cloner le dépôt :
   git clone https://github.com/starman-tech/Orion-V1-2024.git
   cd Orion-V1-2024

2. Créer et activer un environnement virtuel Python :
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows (PowerShell: .\venv\Scripts\Activate.ps1)

3. Installer dépendances Python :
   pip install -r txt/requirements.txt

   Dépendances système supplémentaires :
   - ffmpeg (nécessaire pour pydub)
     - Debian/Ubuntu: sudo apt-get install ffmpeg
     - macOS (Homebrew): brew install ffmpeg
     - Windows: installer ffmpeg et ajouter au PATH
   - Pilotes audio OS pour sounddevice

4. Configuration des clés API (recommandé : variables d'environnement)
   - Éditez a_config.py pour qu'il lise les variables d'environnement (exemples ci-dessous),
     ou exportez les variables dans votre shell :
     - export OPENAI_API_KEY="sk_..."
     - export GROQ_API_KEY="..."

   Exemple minimal recommandé (modifier a_config.py pour lire os.environ) :
   ```python
   import os
   from openai import OpenAI
   from groq import Groq

   openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
   client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
   ```

   - Pour Gmail : placez credentials.json dans module_mail/json/ et laissez le flux OAuth créer token.json lors du premier lancement.

5. Mode développeur (entrée texte) :
   python a_main.py
   - a_main démarre en developer_mode = True (entrée texte).
   - Pour utiliser la reconnaissance vocale, passez developer_mode = False et veillez aux permissions micro.

6. Utilisation :
   - Tapez (ou dites) une requête ; l'assistant renvoie une réponse parlée si TTS actif et tente d'exécuter les commandes trouvées.

---

## Configuration (fichiers et variables clés)

Fichier principal de configuration : a_config.py

Variables importantes (à adapter / déplacer en variables d'environnement) :
- openai_client / client : clients OpenAI et Groq (injectez vos clés via os.environ).
- current_tts_engine : "gtts" (par défaut) ou "openai".
- current_ai_engine : moteur courant (ex. "llama3-70b-8192"); valeur initiale fournie dans a_config.py.
- current_tts_lang : langue TTS par défaut (ex. "fr").
- ai_engines : liste de moteurs disponibles (utilisée par switch_ai_engine).

Langues supportées : 'fr', 'en', 'es', 'it', 'de' via module_language.load_model(lang).

Gmail : module_mail s'attend à module_mail/json/credentials.json pour OAuth et écrit token.json à côté.

---

## Commandes et exemples

Les réponses IA peuvent contenir des tokens de commande encodés sous forme JSON-like :
Format détecté :
  ["command_type";"command"];{optional_params}

Exemples courants :
- Changer TTS :
  ["switch";"tts"]
- Changer d'IA :
  ["switch";"ai"]
- Changer de langue :
  ["switch";"language"];{"lang":"en"}
- Ouvrir une application :
  ["open";"app"];{"appname":"Visual Studio Code"}
- Ouvrir un site (ou chercher et ouvrir) :
  ["open";"websearch"];{"sitename":"github.com"}
  ["open";"web"];{"url":"https://example.com"}
- Envoyer un mail :
  ["gmail";"send"];{"to":"alice@example.com","subject":"Hello","message_text":"Texte"}
- Recherche Web (scraping, fragile) :
  ["web";"search"];{"query":"météo Paris"}
- Prendre photo/screenshot :
  ["image";"capture"];{"prompt":"Décris ce que tu vois"}
  ["image";"screenshot"];{"prompt":"Décris l'écran"}

Le parsing est fait par a_commands.extract_commands et l'exécution dans execute_command. Les tokens sont retirés de la réponse parlée par a_main après exécution.

---

## Architecture et composants (aperçu technique)

Composants principaux :
- a_main.py : boucle principale (mode texte/voix).
- STT : a_stt.py + module_language.py
  - Vosk (modèles dans models/) + sounddevice.
  - module_language.load_model(lang) charge le modèle Vosk correspondant (mise à jour runtime).
- IA : a_ai.py
  - Wrapper client Groq (client.chat.completions.create) et fallback OpenAI (openai_client.chat.completions.create).
  - Fonctions de conversation et d'envoi d'images au modèle (encodage base64).
- Parsing & exécution : a_commands.py
  - extract_commands(text) : regex sur le pattern JSON-like.
  - execute_command(commands) : mapping vers modules (mail, maps, apps, image, calendar, switch, code).
- TTS : a_tts.py
  - gTTS + pydub (par défaut).
  - Option OpenAI TTS si configurée.
  - speak_in_chunks découpe en phrases et joue séquentiellement.
- Modules d'intégration :
  - module_application_launcher : détection applications et ouverture (Windows/macOS/Linux).
  - module_google_search : scraping Google et récupération texte de pages (fragile).
  - module_mail : auth Gmail, envoi et listing.
  - module_maps : recherche locale via geopy + routage OSRM.
  - module_screenshot / Picture : capture écran / photo (plateforme dépendante).
  - module_injecteur : installe dépendances et exécute code généré (dangereux).

---

## Description des datasets inclus
Ce dépôt ne contient pas de jeux de données d'entraînement LLM. Il inclut uniquement des modèles Vosk pré-entraînés (petits) pour STT :
- vosk-model-small-fr-0.22
- vosk-model-small-en-us-0.15
- vosk-model-small-es-0.42
- vosk-model-small-it-0.22
- vosk-model-small-de-0.15

Aucun poids LLM ni données de fine-tuning ne sont fournis ici.

---

## Dépendances (exactes du fichier txt/requirements.txt)
- gtts==2.3.2
- openai==0.27.0
- pydub==0.25.1
- vosk==0.3.45
- google-api-python-client==2.89.0
- google-auth==2.20.0
- google-auth-httplib2==0.1.0
- google-auth-oauthlib==1.0.0
- sounddevice==0.4.6
- requests==2.31.0
- httplib2==0.22.0
- numpy==1.24.4
- pytz==2023.3
- regex==2023.6.3
- groq==0.6.0

Notes :
- Certaines versions et APIs (openai/groq) ont pu changer depuis la création du projet — vérifiez la compatibilité avant mise en production.
- Installez ffmpeg pour pydub.

---

## Récapitulatif des fonctions principales (description courte par fonction / méthode)
Ci-dessous des explications courtes et pratiques pour chaque fonction/méthode clé (basées sur le code fourni).

- a_main.main()
  - Boucle principale : lecture entrée (texte ou micro), obtention réponse via get_response, extraction/exécution commandes, et TTS via speak_in_chunks.

- a_stt.listen()
  - Ouvre un flux audio avec sounddevice (16 kHz) et Vosk pour retourner la première transcription reconnue.

- module_language.load_model(lang)
  - Charge le modèle Vosk correspondant à la langue demandée et met à jour current_tts_lang. Lève ValueError si langue non supportée.

- a_ai.get_response(user_input)
  - Ajoute un timestamp au message, l'ajoute à chat_history, appelle le client IA (Groq par défaut, OpenAI si "gpt-4" détecté) et retourne la réponse. Met la réponse dans chat_history.

- a_ai.send_image_to_model(image_path, prompt)
  - Encode l'image locale en data URL (base64) et envoie un message multimodal au modèle via client.chat.completions.create; retourne la transcription/résultat.

- a_ai.switch_ai_engine()
  - Parcourt ai_engines (depuis a_config) et bascule sur l'entrée suivante (rotatif).

- a_ai.get_response_from_Codeur(...) et get_response_from_Al(...)
  - Variantes pour envoyer des messages à des "sous-discussions" (discussion/chat_history distincts) en utilisant openai_client.

- a_tts.speak_in_chunks(text)
  - Découpe le texte en phrases, convertit chaque phrase en audio (gTTS ou OpenAI TTS si activé) puis joue séquentiellement via pydub.

- a_tts.switch_tts_engine()
  - Bascule entre "gtts" et "openai" (variable globale current_tts_engine).

- a_commands.extract_commands(text)
  - Extrait toutes les commandes selon le pattern regex '\["([^;]+)";"([^"]+)"\](?:;({.*?}))?' et retourne une liste de tuples (type, command, params).

- a_commands.execute_command(commands)
  - Itère les commandes et appelle les modules appropriés : Gmail (send/list), open/app/web/websearch, switch (tts/ai/language), calendar (add/delete/update/reminder), web search/visit (module_google_search + get_response_from_Al), image capture/screenshot (Picture + send_image_to_model), code (module_injecteur + get_response_from_Codeur) — attention aux fonctions dangereuses.

- module_application_launcher.AppLauncher
  - Détecte applications selon OS et propose search_and_open_app(search_name) (recherche floue) et open_url_in_chrome(url). Méthodes internes pour exécution cross-OS.

- module_google_search.google_search(query)
  - Scrappe les résultats Google et retourne une liste de dicts {link, title, description, position}. Fragile.

- module_google_search.get_website_text(url)
  - Récupère tout le texte d'une page via requests + BeautifulSoup.

- module_google_search.google_first_link(query)
  - Renvoie le premier lien d'une recherche Google (fragile).

- module_maps.LocalSearch.find_nearby_places(query, location, ...)
  - Recherche des lieux/localisation via geopy.Nominatim et filtre par distance. get_route start/destination via OSRM.

- module_mail.authenticate_gmail()
  - Gère le flux OAuth (credentials.json -> token.json) et retourne un service Gmail (googleapiclient).

- module_mail.create_message / send_email / list_recent_emails(service)
  - Création et envoi de message MIME, listing des derniers messages (ajoute expéditeur au chat_history).

- module_injecteur.install_missing_dependencies(code)
  - Analyse imports et tente d'installer les libs manquantes via pip (danger : installation non contrôlée).

- module_injecteur.execute_code_with_dependencies(code)
  - Installe dépendances détectées, écrit un temp_script.py et l'exécute, puis supprime le fichier (DANGEREUX).

- module_injecteur.generate_code / testr
  - Utilitaires pour écrire du code et nettoyer une chaîne (usage interne au flux "code" du prototype).

---

## Résultats et métriques recommandées
Ce prototype n'inclut pas d'évaluations formelles. Recommandations pour évaluer localement :
- STT : mesurer le Word Error Rate (WER) sur un petit jeu de test enregistré (même acoustique/conditions).
- Parsing de commandes : construire un jeu de paires (utterance -> token attendu) et mesurer précision/rappel de a_commands.extract_commands.
- Latence : mesurer temps total micro -> réponse parlée (STT + AI + TTS) sur votre configuration matérielle.
- TTS : test subjectif (écoute) ; gTTS intelligible mais basique.

---


## Dépannage rapide
- Erreur Vosk ModelNotFound : vérifiez que les dossiers modèles sont dans models/ et que module_language.LANG_MODELS pointe vers les bons noms.
- Microphone non détecté : vérifier sounddevice list, permissions et pilotes.
- pydub / ffmpeg error : installer ffmpeg et l'ajouter au PATH.
- Erreurs Google API : vérifier module_mail/json/credentials.json et supprimer token.json pour réauthentifier.
- Erreurs OpenAI/Groq : vérifiez variables d'environnement et compatibilités des versions clients.

---

## Points incomplets / à vérifier dans le code source
- module_application_launcher fait des hypothèses (nom Chrome, chemins Windows). Tester et ajuster selon votre OS.
- module_google_search dépend du HTML de Google — préférer APIs officielles.

---

## Licence & statut
- Prototype personnel — code fourni "as-is".
- Archivage du projet : ce dépôt est archivé depuis 2023.

---
