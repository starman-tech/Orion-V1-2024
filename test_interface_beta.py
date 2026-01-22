import tkinter as tk
from tkinter import ttk
import json
from a_stt import listen
from a_ai import get_response
from a_tts import speak_in_chunks
from a_commands import extract_commands, execute_command
from a_config import current_ai_engine, current_tts_engine, current_tts_lang, ai_engines

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat IA")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.is_dark_mode = False
        self.is_collapsed = False
        self.is_voice_mode = False               

        self.light_theme = {
            "bg": "#f5f5f5",
            "fg": "#000",
            "msg_user_bg": "#d1e7dd",
            "msg_ia_bg": "#f8d7da",
            "entry_bg": "#ffffff",
            "entry_fg": "#000"
        }
        self.dark_theme = {
            "bg": "#2c2c2c",
            "fg": "#fff",
            "msg_user_bg": "#3c6e71",
            "msg_ia_bg": "#353535",
            "entry_bg": "#333333",
            "entry_fg": "#fff"
        }
        self.theme = self.light_theme

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.chat_frame = tk.Canvas(self.main_frame, bg=self.theme["bg"], highlightthickness=0)
        self.chat_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.chat_frame.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.chat_frame.configure(yscrollcommand=self.scrollbar.set)

        self.chat_content = tk.Frame(self.chat_frame, bg=self.theme["bg"])
        self.chat_frame.create_window((0, 0), window=self.chat_content, anchor="nw")

        self.chat_content.bind("<Configure>", lambda e: self.chat_frame.configure(scrollregion=self.chat_frame.bbox("all")))

        self.entry_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        self.entry_frame.pack(fill="x", pady=5)

        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(self.entry_frame, textvariable=self.message_var, font=("Arial", 12))
        self.message_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.buttons_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        self.buttons_frame.pack(side="bottom", fill="x", pady=5)

        self.toggle_size_button = ttk.Button(self.buttons_frame, text="⛶ Réduire", command=self.toggle_window_size)
        self.toggle_size_button.pack(side="left", padx=5)

        self.settings_button = ttk.Button(self.buttons_frame, text="⚙️ Paramètres", command=self.open_settings)
        self.settings_button.pack(side="left", padx=5)

        self.theme_button = ttk.Button(self.buttons_frame, text="Mode Sombre", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=5)

        self.voice_button = ttk.Button(self.buttons_frame, text="🎤 Activer Vocal", command=self.toggle_voice_mode)
        self.voice_button.pack(side="right", padx=5)

        self.transparency_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        self.transparency_frame.pack(side="bottom", fill="x", pady=5)

        tk.Label(self.transparency_frame, text="Transparence", bg=self.theme["bg"], fg=self.theme["fg"]).pack(side="left", padx=10)
        self.transparency_slider = ttk.Scale(self.transparency_frame, from_=0.5, to=1.0, value=1.0, orient="horizontal",
                                             command=self.set_transparency)
        self.transparency_slider.pack(side="left", fill="x", expand=True, padx=10)

        self.add_message(f"Bienvenue dans l'assistant vocal. TTS : {current_tts_engine}, AI : {current_ai_engine}.", "ia")


    def toggle_window_size(self):
        """Basculer entre mode réduit et normal."""
        if self.is_collapsed:
            self.root.geometry("600x400")
            self.toggle_size_button.pack(side="left", padx=5)
            self.settings_button.pack(side="left", padx=5)
            self.theme_button.pack(side="right", padx=5)
            self.voice_button.pack(side="right", padx=5)
            self.toggle_size_button.config(text="⛶ Réduire")
        else:
            self.root.geometry("200x100")
            for widget in self.buttons_frame.winfo_children():
                widget.pack_forget()

            ttk.Button(self.buttons_frame, text="🔼", command=self.toggle_window_size).pack(side="left", padx=5)
            ttk.Button(self.buttons_frame, text="🎤", command=self.toggle_voice_mode).pack(side="left", padx=5)
            ttk.Button(self.buttons_frame, text="⚙️", command=self.open_settings).pack(side="left", padx=5)

        self.is_collapsed = not self.is_collapsed

    def toggle_theme(self):
        """Basculer entre clair et sombre."""
        self.is_dark_mode = not self.is_dark_mode
        self.theme = self.dark_theme if self.is_dark_mode else self.light_theme
        self.theme_button.config(text="Mode Clair" if self.is_dark_mode else "Mode Sombre")

        self.main_frame.config(bg=self.theme["bg"])
        self.chat_frame.config(bg=self.theme["bg"])
        self.chat_content.config(bg=self.theme["bg"])
        self.entry_frame.config(bg=self.theme["bg"])
        self.message_entry.config(background=self.theme["entry_bg"], foreground=self.theme["entry_bg"])
        self.buttons_frame.config(bg=self.theme["bg"])
        self.transparency_frame.config(bg=self.theme["bg"])

    def open_settings(self):
        """Afficher une fenêtre de paramètres."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Paramètres")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)

        tk.Label(settings_window, text="Paramètres", font=("Arial", 14)).pack(pady=10)
        ttk.Label(settings_window, text="Options disponibles ici...").pack(pady=10)

        ttk.Button(settings_window, text="Fermer", command=settings_window.destroy).pack(pady=10)

    def toggle_voice_mode(self):
        """Activer/Désactiver le mode vocal."""
        self.is_voice_mode = not self.is_voice_mode
        state = "activé" if self.is_voice_mode else "désactivé"
        self.voice_button.config(text=f"🎤 {'Désactiver' if self.is_voice_mode else 'Activer'} Vocal")
        self.add_message(f"Mode vocal {state}.", "ia")


    def set_transparency(self, value):
        """Régler la transparence de la fenêtre."""
        self.root.attributes("-alpha", float(value))

    def send_message(self, event=None):
        """Envoyer un message."""
        if self.is_voice_mode:
            user_input = listen()
        else:
            user_input = self.message_var.get()

        if user_input.strip():
            self.add_message(user_input, "user")
            self.message_var.set("")

            response = get_response(user_input)
            commands = extract_commands(response)

            if commands:
                execute_command(commands)
                for command_type, command, params in commands:
                    response = response.replace(f'["{command_type}";"{command}"]', '')
                    if params:
                        response = response.replace(f';{json.dumps(params)}', '')

            if response.strip():
                self.add_message(response, "ia")
                speak_in_chunks(response)

    def add_message(self, text, sender):
        """Ajouter un message au chat."""
        bg_color = self.theme["msg_user_bg"] if sender == "user" else self.theme["msg_ia_bg"]
        anchor = "e" if sender == "user" else "w"
        side = "right" if sender == "user" else "left"
        avatar = "👤" if sender == "user" else "🤖"

        message_frame = tk.Frame(self.chat_content, bg=self.theme["bg"])
        message_frame.pack(fill="x", padx=5, pady=2, anchor=anchor)

        avatar_label = tk.Label(message_frame, text=avatar, bg=self.theme["bg"], font=("Arial", 14))
        avatar_label.pack(side=side, padx=5)

        message_label = tk.Label(
            message_frame,
            text=text,
            bg=bg_color,
            fg=self.theme["fg"],
            font=("Arial", 12),
            wraplength=400,
            justify="left",
            padx=10,
            pady=5,
            relief="solid",
            bd=1
        )
        message_label.pack(side=side, padx=5)

        self.chat_frame.update_idletasks()
        self.chat_frame.yview_moveto(1)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
