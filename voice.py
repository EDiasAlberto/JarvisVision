from gtts import gTTS 
from os import system
from dotenv import load_dotenv
import speech_recognition as sr 


class Voice:
    
    def __init__(self):
        self.lang = "en"
        self.slow = False
        self.outputFile = "text.mp3"
        self.audioRecog = sr.Recognizer()
        self.micIndex = 1

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
        ttsObj = gTTS(text=string, lang=self.lang, slow=self.slow)
        ttsObj.save(self.outputFile)
        system(f"afplay {self.outputFile}")

    def stt(self):
        audio = self.getMicAudio()
        try:
            print(f"OpenAI Whisper API thinks you said {self.audioRecog.recognize_openai(audio)}")
        except sr.RequestError as e:
            print("BIG ERROR")


if __name__=="__main__":
    load_dotenv()
    client = Voice()
    client.tts("This should be read out loud!")

    client.stt()

