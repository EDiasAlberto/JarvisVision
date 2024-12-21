from dotenv import load_dotenv
from os import getenv
from voice import Voice 
from gpt import GPT 
from computer import Computer 
from openai import OpenAI

IMG_REQ_KEYSTRING = "IMAGE_REQUIRED"
CODE_SEG_KEYSTRING = "CODE_SEGMENT"

class Jarvis:

    def __init__(self):
        load_dotenv()
        self.AIClient = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.voice = Voice(self.AIClient)
        self.pc = Computer()
        self.gpt = GPT(self.AIClient, IMG_REQ_KEYSTRING, CODE_SEG_KEYSTRING)


    def handleImageRequirement(self):
        image = self.pc.takePhoto()
        res = self.gpt.sendImg(image)
        self.voice.tts(res)

    def handleCodeSegment(self, res):
        #prevent excessively long tts when code segment
        #split at code segment
        explanation, code = res.split(CODE_SEG_KEYSTRING)
        self.pc.copy(code)
        self.voice.tts(explanation)

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
        if CODE_SEG_KEYSTRING.lower() in response.lower():
            self.handleCodeSegment(response)
        else:
            self.voice.tts(response)
        print("Done with request 1!")

if __name__=="__main__":
    assistant = Jarvis()

    assistant.mainLoop()
