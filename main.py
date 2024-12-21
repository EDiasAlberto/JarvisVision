from dotenv import load_dotenv
from os import getenv
from voice import Voice 
from gpt import GPT 
from computer import Computer 
from openai import OpenAI

IMG_REQ_KEYSTRING = "IMAGE_REQUIRED"

class Jarvis:

    def __init__(self):
        load_dotenv()
        self.AIClient = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.voice = Voice(self.AIClient)
        self.pc = Computer()
        self.gpt = GPT(self.AIClient, IMG_REQ_KEYSTRING)


    def handleImageRequirement(self):
        image = self.pc.takePhoto()
        res = self.gpt.sendImg(image)
        self.voice.tts(res)

    def mainLoop(self):
        #get mic audio
        #send mic audio to gpt
        #handle response
        # TODO: Implement code clipboard handling

        recogText = self.voice.stt()
        print("Asking GPT")
        self.voice.tts("Hang on I'm thinking...")
        response = self.gpt.askGPT(recogText)
        print("Handling Response")
        if response.lower() == IMG_REQ_KEYSTRING.lower():
            self.handleImageRequirement()
        else:
            self.voice.tts(response)
        print("Done with request 1!")

if __name__=="__main__":
    assistant = Jarvis()

    while True:
        assistant.mainLoop()
