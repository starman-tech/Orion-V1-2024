#Finish

import os
import platform
import subprocess
from difflib import get_close_matches

class AppLauncher:
    def __init__(self):
        """
        Initialise le module en détectant l'OS et charge les applications disponibles.
        """
        self.os_name = platform.system()
        self.applications = self._get_applications()

    def _is_utility_app(self, app_name):
        """
        Vérifie si une application est un utilitaire utilisateur.
        Args:
            app_name (str): Nom de l'application.
        Returns:
            bool: True si l'application est un utilitaire utilisateur, False sinon.
        """
        system_apps_keywords = [
            "cinnamon", "gnome", "kde", "system", "settings", "config", 
            "xterm", "shell", "terminal", "cmd", "bash", "powershell",
            "diagnostic", "update", "setup", "control panel", "explorer"
        ]
        app_name_lower = app_name.lower()
        return not any(keyword in app_name_lower for keyword in system_apps_keywords)

    def _get_applications(self):
        """
        Recherche les applications disponibles sur le système.
        Returns:
            dict: Dictionnaire contenant les noms et chemins des applications.
        """
        applications = {}

        if self.os_name == "Windows":
            start_menu_paths = [
                r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
                os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
            ]
            for path in start_menu_paths:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(".lnk"):
                            app_name = file[:-4]
                            if self._is_utility_app(app_name):
                                full_path = os.path.join(root, file)
                                applications[app_name] = full_path

        elif self.os_name == "macOS":
            app_paths = ["/Applications", os.path.expanduser("~/Applications")]
            for path in app_paths:
                for root, dirs, files in os.walk(path):
                    for dir_name in dirs:
                        if dir_name.endswith(".app"):
                            app_name = dir_name[:-4]
                            if self._is_utility_app(app_name):
                                full_path = os.path.join(root, dir_name)
                                applications[app_name] = full_path

        elif self.os_name == "Linux":
            desktop_paths = ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]
            for path in desktop_paths:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(".desktop"):
                            app_name = file[:-8]
                            if self._is_utility_app(app_name):
                                full_path = os.path.join(root, file)
                                applications[app_name] = full_path

        return applications

    def _execute_application(self, app_path):
        """
        Ouvre l'application en fonction de l'OS, avec redirection de la sortie.
        Args:
            app_path (str): Chemin complet de l'application.
        """
        try:
            if self.os_name == "Windows":
                subprocess.Popen(
                    ["cmd", "/c", app_path],
                    shell=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif self.os_name == "macOS":
                subprocess.Popen(
                    ["open", app_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif self.os_name == "Linux":
                if app_path.endswith(".desktop"):
                    with open(app_path, "r") as f:
                        for line in f:
                            if line.startswith("Exec="):
                                command = line.split("=", 1)[1].strip().split(" ")[0]
                                subprocess.Popen(
                                    [command],
                                    stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                )
                                return
                else:
                    subprocess.Popen(
                        ["xdg-open", app_path],
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
        except Exception as e:
            print(f"Erreur lors de l'ouverture de l'application : {e}")

    def search_and_open_app(self, search_name, similarity_threshold=0.5):
        """
        Recherche et ouvre une application par son nom, en utilisant la correspondance floue.
        Args:
            search_name (str): Nom (ou partie du nom) de l'application à rechercher.
            similarity_threshold (float): Seuil de similarité minimale pour accepter une correspondance (entre 0 et 1).
        """
        matching_apps = get_close_matches(
            search_name["appname"].lower(), 
            [name.lower() for name in self.applications.keys()], 
            n=5, 
            cutoff=similarity_threshold
        )

        if not matching_apps:
            print(f"Aucune application trouvée contenant un nom proche de : {search_name["appname"]}")
            return
        
        print(f"Applications trouvées pour '{search_name["appname"]}':")
        for match in matching_apps:
            app_name = next((key for key in self.applications if key.lower() == match), None)
            if app_name:
                print(f"- {app_name}")

        best_match = matching_apps[0]
        app_path = self.applications.get(best_match)
        if app_path:
            self._execute_application(app_path)

    def open_url_in_chrome(self, url):
        """
        Ouvre un lien dans Google Chrome sans afficher de messages.
        Args:
            url (dict): Contient le lien à ouvrir (par exemple, {"sitename": "https://example.com"}).
        """
        try:
            if self.os_name == "Windows":
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen(
                    [chrome_path, url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )
            elif self.os_name == "macOS":
                subprocess.Popen(
                    ["open", "-a", "Google Chrome", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )
            elif self.os_name == "Linux":
                subprocess.Popen(
                    ["google-chrome", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )
        except Exception as e:
            print(f"Erreur lors de l'ouverture du lien : {e}")

launcher = AppLauncher()
