import os
import platform
from typing import Union
import requests
import json

import openai
from dotenv import load_dotenv, find_dotenv

import personalities, prompts
# from tts import synthesize_speech

load_dotenv(find_dotenv())

from google.cloud import texttospeech
from playsound import playsound

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="no-NO", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)


openai.api_key = os.environ.get("OPENAI_API_KEY")

available_zones = [
    {"name": "Kontor A", "temperature": 19},
    {"name": "Kontor B", "temperature": 21},
    {"name": "Kontor C", "temperature": 23},
    {"name": "Kontor D", "temperature": 17},
    {"name": "Kontor E", "temperature": 22},
]


class User:
    def __init__(
        self,
        name: str,
        rfid: str,
        previous_conversation: bool,
        preferred_personality: Union[personalities.Personality, None] = None
    ):
        self.name = name
        self.rfid = rfid
        self.previous_conversation = previous_conversation
        if preferred_personality is None:
            self.preferred_personality = personalities.Personality.DEFAULT
        else:
            self.preferred_personality = preferred_personality


class RobBin:
    IDLE = 1
    MOVING = 2
    BUSY = 3
    TALKING = 4
    OFF = -1
    ESP32_URL = "http://4.3.2.1"

    def __init__(self):
        self._send_state(self.IDLE)
        self.busy = False
        self.current_user = None
        self.conversation = []

    def _send_state(self, state: int, on: bool = True, retries: int = 10):
        attempt = 0
        while True:
            r = requests.post(
                f"{self.ESP32_URL}/json/state",
                data=json.dumps({"on": on, "ps": str(state)})
            )
            if r.status_code == 200:
                break
            else:
                attempt += 1

            if attempt >= retries:
                break

    def _add_user_prompt(self, prompt: str):
        self.conversation.append(
            {"role": "user", "content": prompt}
        )
    
    def _get_response(self):
        message = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.conversation
        )
        content = message.choices[0].message.content
        self.conversation.append(
            {"role": "assistant", "content": content}
        )
        return content

    def run(self, user: User, zone: dict[str, str]):
        # runs when a users requests RobBin
        self.busy = True
        self._send_state(self.BUSY)
        self.current_user = user
        persona = personalities.get_persona(user.preferred_personality)
        self.conversation = [{"role": "system", "content": persona}]
        
        greeting = self.greet_user()
        self.play_message(greeting)

        feedback = self.give_feedback()
        self.play_message(feedback)

        goodbye = self.say_goodbye(zone=zone)
        self.play_message(goodbye)
        self._send_state(self.MOVING)

        
    def greet_user(self):
        assert self.current_user is not None

        if not self.current_user.previous_conversation:
            self._add_user_prompt(prompts.introduction(self.current_user.name))
            response = self._get_response()
        else:
            self._add_user_prompt(prompts.hello(self.current_user.name))
            response = self._get_response()

        return response


    def give_feedback(self):
        assert self.current_user is not None

        self._add_user_prompt(prompts.feedback(self.current_user.name))
        response = self._get_response()

        return response


    def say_goodbye(self, zone: dict[str, str]):
        assert self.current_user is not None

        self._add_user_prompt(prompts.goodbye_and_suggestion(self.current_user.name, zone, available_zones))
        response = self._get_response()

        return response

    def get_mp3(self, content) -> str:
        synthesis_input = texttospeech.SynthesisInput(text=content)
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        print("")
        # todo: call to synthesize_speech

    def play_message(self, content):
        self._send_state(self.TALKING)
        mp3_path = self.get_mp3(content)
        print(content)
        print("\n")
        self._send_state(self.IDLE)
        # if platform.system() == "Darwin":
        #     # mac
        #     os.system("afplay " + mp3_path)
        # else:
        #     # linux
        #     os.system("mpg123 " + mp3_path)

users = [
    User("Maciej", "1234567890", True, personalities.Personality.POETIC),
    User("Harald", "4234234", False, personalities.Personality.POLITE),
    User("Karolina", "343558", False, personalities.Personality.FUNNY),
    User("Mathias", "378756746", True, personalities.Personality.SASSY),
    User("Torbjørn", "46732", False, personalities.Personality.POETIC),
    User("Ragna", "457658583", True, personalities.Personality.POLITE),
    User("Sindre", "23945875", True, personalities.Personality.TERSE),
]
if __name__ == "__main__":
    bot = RobBin()
    bot.run(users[3], zone={"name": "Kontor A", "temperature": "19"})