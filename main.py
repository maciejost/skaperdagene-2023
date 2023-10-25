import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import openai
import random

from tts import synthesize_speech

openai.api_key = os.environ.get("OPENAI_API_KEY")

prompts = [
	"Gi meg et kort vers på seks linjer som rimer om hvor kul en person er, personen heter ",
	"Gi meg en haiku om hvor fantastisk en person er, personen heter ",
]

people = [
	{
		"name": "Maciej",
		"rfid": "1234567890"
	},
	{
		"name": "Ragna",
		"rfid": "0987654321"
	},
	{
		"name": "Sindre",
		"rfid": "1234567890"
	},
	{
		"name": "Mathias",
		"rfid": "0987654321"
	},
	{
		"name": "Karolina",
		"rfid": "1234567890"
	},
	{
		"name": "Torbjørn",
		"rfid": "0987654321"
	},
	{
		"name": "Harald",
		"rfid": "1234567890"
	}
]

def get_name():
	print("--- Henter navn ---")
	# Få svar fra "rfid"
	# Sjekk om "rfid" er i people
	# Hvis ja, returner navn
	return "RobBin"


def fetch_greeting(name):
	print("--- Henter hilsen fra OpenAI ---")
	prompt = random.choice(prompts) + name + "."
	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "user", "content": prompt},
		]
	)
	return completion.choices[0].message.content

def main():
	synthesize_speech(fetch_greeting(get_name()))

# Måle hvor lang tid det tar å kjøre alt
import time
start_time = time.time()
main()
print("--- Det hele tok %s sekunder ---" % (time.time() - start_time))