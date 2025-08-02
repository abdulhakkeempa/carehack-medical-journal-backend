import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

import os
import json
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Specify the path to the audio file
# filename =  "audio.mp3" # Replace with your audio file!

def whisper_transcribe(file):
    # with open(filename, "rb") as file:
        # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
        file=file, # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        #   prompt="Specify context or spelling",  # Optional
        #   response_format="verbose_json",  # Optional
        #   timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
        language="en",  # Optional
        temperature=0.0  # Optional
    )

    return transcription.text

# print(whisper_transcribe(filename))

    # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
# print(json.dumps(transcription, indent=2, default=str))
# def recognize_from_microphone():
#      # This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
#      # Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
#     speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), endpoint=os.environ.get('AZURE_SPEECH_REGION'))
#     speech_config.speech_recognition_language="en-US"

#     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

#     print("Speak into your microphone.")
#     speech_recognition_result = speech_recognizer.recognize_once_async().get()

#     if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         print("Recognized: {}".format(speech_recognition_result.text))
#     elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
#         print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
#     elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = speech_recognition_result.cancellation_details
#         print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print("Error details: {}".format(cancellation_details.error_details))
#             print("Did you set the speech resource key and endpoint values?")

# recognize_from_microphone()