from os import system, getenv
from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr

class Voice:
    
    def __init__(self, openAIClient):
        self.lang = "en"
        self.slow = False
        self.outputFile = "text.mp3"
        self.audioRecog = sr.Recognizer()
        self.micIndex = 1
        self.client = openAIClient
        self.isEnabled = True

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False

    def list_microphones(self):
        mics = sr.Microphone.list_microphone_names()
        print("Available microphones:")
        for index, mic_name in enumerate(mics):
            print(f"{index}: {mic_name}")
        return mic_list

    def getMicAudio(self):
        with sr.Microphone(device_index = self.micIndex) as mic:
            print("Accepting input!")
            audio = self.audioRecog.listen(mic)
        return audio


    def tts(self, string):
        if not self.isEnabled:
            return
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=string
        )
        response.stream_to_file(self.outputFile)
        system(f"afplay {self.outputFile}")

    def stt(self):
        audio = self.getMicAudio()
        recogText = self.audioRecog.recognize_openai(audio)
        try:
            print(f"OpenAI Whisper API thinks you said {recogText}")
            return recogText
        except sr.RequestError as e:
            print("BIG ERROR")


if __name__=="__main__":
    load_dotenv()
    AIClient = OpenAI(api_key=getenv("OPENAI_API_KEY"))
    client = Voice(AIClient)
    client.list_microphones()
    client.tts("This should be read out loud!")

    client.stt()

