from dotenv import load_dotenv
from os import getenv
from voice import Voice 
from gpt import GPT 
from computer import Computer 

IMG_REQ_KEYSTRING = "IMAGE_REQUIRED"

class Jarvis:

    def __init__(self):
        load_dotenv()
        self.voice = Voice()
        self.pc = Computer()
        self.gpt = GPT(getenv("OPENAI_API_KEY"), IMG_REQ_KEYSTRING)


    def handleImageRequirement(self):
        image = self.pc.takePhoto()
        res = self.gpt.sendImg(image)
        self.voice.tts(res)

    def mainLoop(self):
        #get mic audio
        #send mic audio to gpt
        #handle response
        # TODO: Implement code clipboard handling

        recogText = self.voice.getMicAudio()
        response = self.gpt.askGPT(recogText)
        if response.lower() == IMG_REQ_KEYSTRING:
            self.handleImageRequirement()
        else:
            self.voice.tts(response)

