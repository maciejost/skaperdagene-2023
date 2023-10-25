import os
import openai
import random
openai.api_key = "API-nøkkelen er i chatten"

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

def getName():
	# Få svar fra "rfid"
	# Sjekk om "rfid" er i people
	# Hvis ja, returner navn
	return "Robbin"


def fetchGreeting(name):
	prompt = random.choice(prompts) + name + "."
	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "user", "content": prompt},
		]
	)
	return completion.choices[0].message.content


print(fetchGreeting(getName()))