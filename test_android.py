from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.slider import Slider
import json
from a_stt import listen
from a_ai import get_response
from a_tts import speak_in_chunks
from a_commands import extract_commands, execute_command

class ChatApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Zone des messages
        self.chat_scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_content = BoxLayout(size_hint_y=None, orientation="vertical")
        self.chat_content.bind(minimum_height=self.chat_content.setter('height'))
        self.chat_scroll.add_widget(self.chat_content)
        self.add_widget(self.chat_scroll)

        # Zone de saisie
        self.input_box = BoxLayout(size_hint=(1, 0.1), orientation="horizontal")
        self.text_input = TextInput(hint_text="Tapez votre message ici...", size_hint=(0.8, 1))
        self.send_button = Button(text="Envoyer", size_hint=(0.2, 1), on_press=self.send_message)
        self.input_box.add_widget(self.text_input)
        self.input_box.add_widget(self.send_button)
        self.add_widget(self.input_box)

        # Slider de transparence (optionnel pour desktop)
        self.slider_box = BoxLayout(size_hint=(1, 0.1), orientation="horizontal")
        self.slider_label = Label(text="Transparence :", size_hint=(0.3, 1))
        self.transparency_slider = Slider(min=0.5, max=1.0, value=1.0, size_hint=(0.7, 1))
        self.slider_box.add_widget(self.slider_label)
        self.slider_box.add_widget(self.transparency_slider)
        self.add_widget(self.slider_box)

    def add_message(self, text, sender):
        """Afficher un message dans l'interface."""
        color = [0.6, 0.8, 0.6, 1] if sender == "user" else [1, 0.7, 0.7, 1]
        label = Label(
            text=f"[{sender}] {text}",
            size_hint_y=None,
            height=40,
            halign="left",
            color=color,
            text_size=(self.width, None)
        )
        self.chat_content.add_widget(label)
        self.chat_scroll.scroll_to(label)

    def send_message(self, instance):
        """Envoyer un message et obtenir une réponse."""
        user_input = self.text_input.text.strip()
        if user_input:
            self.add_message(user_input, "user")
            self.text_input.text = ""

            # Obtenir une réponse de l'IA
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

class ChatAppKivy(App):
    def build(self):
        return ChatApp()

if __name__ == "__main__":
    ChatAppKivy().run()
