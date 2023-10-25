"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech


client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="no-NO", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

def synthesize_speech (text):
	print("Henter lydfil")
	synthesis_input = texttospeech.SynthesisInput(text=text)

	response = client.synthesize_speech(
		input=synthesis_input, voice=voice, audio_config=audio_config
	)

	with open("output.mp3", "wb") as out:
		# Write the response to the output file.
		out.write(response.audio_content)
		print('Lydfil lagret i "output.mp3"')
