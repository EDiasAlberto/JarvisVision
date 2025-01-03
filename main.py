from dotenv import load_dotenv
from os import getenv
from voice import Voice 
from gpt import GPT 
from computer import Computer 
from openai import OpenAI
from webserver import SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer

IMG_REQ_KEYSTRING = "IMAGE_REQUIRED"
SCREEN_REQ_KEYSTRING = "SCREENSHOT_REQUIRED"
CODE_SEG_KEYSTRING = "CODE_SEGMENT"
END_CONV_KEYSTRING = "END_CONV"

class Jarvis:

    def __init__(self, isSilent):
        load_dotenv()
        self.AIClient = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.voice = Voice(self.AIClient)
        self.pc = Computer()
        self.gpt = GPT(self.AIClient, IMG_REQ_KEYSTRING, CODE_SEG_KEYSTRING, SCREEN_REQ_KEYSTRING, END_CONV_KEYSTRING)
        self.silentMode = isSilent


    def handleImageRequirement(self):
        image = self.pc.takePhoto()
        res = self.gpt.sendImg(image)
        self.voice.tts(res)

    def handleScreenRequirement(self):
        image = self.pc.takeScreenshot()
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
        if self.silentMode:
            recogText = input("What would you like to ask?")
        else:
            recogText = self.voice.stt()
        print("Asking GPT")
        self.voice.tts("Hang on I'm thinking...")
        response = self.gpt.askGPT(recogText)
        print("Handling Response")
        if response.lower() == IMG_REQ_KEYSTRING.lower():
            self.handleImageRequirement()
        elif response.lower() == SCREEN_REQ_KEYSTRING.lower():
            self.handleScreenRequirement()
        elif CODE_SEG_KEYSTRING.lower() in response.lower():
            self.handleCodeSegment(response)
        elif END_CONV_KEYSTRING.lower() in response.lower():
            self.voice.tts(response.split(END_CONV_KEYSTRING)[1])
            return False
        else:
            self.voice.tts(response)
        print("Done with request 1!")
        return True

if __name__=="__main__":
    
    isSilent = input("Would you like to run without Speech Recog? (y/n)\t").lower() == "y"
    
    assistant = Jarvis(isSilent)


# Define the main function to start the server
    server_address = ('', 8080)
    # Use a lambda to pass custom attributes to the handler
    httpd = HTTPServer(
        server_address, 
        lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, jarvis=assistant, **kwargs)
    )
    print("Server is running on port 8080...")
    httpd.serve_forever()


