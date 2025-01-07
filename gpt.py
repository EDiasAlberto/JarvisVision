from openai import OpenAI

from dotenv import load_dotenv
from os import getenv
from base64 import b64encode


class GPT:
    def __init__(self, client, IMG_REQ_KEYSTRING, CODE_SEG_KEYSTRING, SCREEN_REQ_KEYSTRING, END_CONV_KEYSTRING):
        self.messages = []
        self.client = client
        self.gptModel = "gpt-4o-mini"

        setupContext = [
            "Your name is Jarvis. You are a helpful AI assistant. Your purpose is to aid in project guidance or programming help.",
            f"If a request that I make to you requires an image of something around me (for example, I ask you about something on my desk) then respond with just '{IMG_REQ_KEYSTRING}'. The subsequent message will then contain the relevant image.",
            f"If I ask you to describe something but it is not in reference to a specific occurrence of that thing around me, then just describe a generic version. If I specify that I want you to talk about an occurrence of that item that is around me (e.g. 'this apple' or 'this chair'), then follow the normal rules for requiring an image, else just describe a generic version.",
            f"If a request that I make to you involves responding with some code, then please put the entirety of the snippet of code at the end of the message. Please prefix the code snippet with '\n{CODE_SEG_KEYSTRING}\n'. The formatting should be such that you have a description of the code and/or how it works, followed by a notice that the code has been copied to my clipboard, followed by a line that says '{CODE_SEG_KEYSTRING}' and then the code itself, and then the end of the message. There should be no actual text following the code segment. There should also be no code prior to {CODE_SEG_KEYSTRING}.",
            f"If I say that I am done or say goodbye in some way, simply return a message with {END_CONV_KEYSTRING} followed by a goodbye message. There should be no text before {END_CONV_KEYSTRING}. You should also never end a message with just {END_CONV_KEYSTRING}.",
            f"If I make a request that references something on my screen, and you need to see it, then respond with just '{SCREEN_REQ_KEYSTRING}'. The subsequent message will then contain the relevant screenshot."
        ]

        for input in setupContext:
            self.createMessage(input, "system")
        self.maxTokens = 2000

    def createMessage(self, content, role="user"):
        newMsg = {"role": role, "content": content}
        self.messages.append(newMsg)

    def sendMessageHistory(self):
        response = self.client.chat.completions.create(model = self.gptModel,
        messages = self.messages,
        max_tokens = self.maxTokens)

        gptResponse = response.choices[0].message.content
        print(f"Response: {gptResponse}")

        self.messages.append({"role": "assistant", "content": gptResponse})
        return gptResponse

    def askGPT(self, message):
        self.createMessage(message)
        response = self.sendMessageHistory()
        return response

    def sendImg(self, imgData):
        imgMsg = {"role": "user", "content": [
            {
                "type": "text",
                "text": "Here is the associated image for the previous request",
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{imgData}"}
            }
        ]}
        self.messages.append(imgMsg)
        response = self.sendMessageHistory()
        return response


if __name__=="__main__":
    load_dotenv()
    key = getenv("OPENAI_API_KEY")
    client = GPT(key)

    #client.askGPT("Hey, what is your purpose?")
    #client.askGPT("Cool, how would you write a HTTP request in Python?")
    #client.askGPT("What was my first message to you?")
    client.askGPT("Please describe the image im sending to you")
    b64Img = 0
    with open("forest.jpg", "rb") as image:
        b64Img = b64encode(image.read()).decode("utf-8")
    client.sendImg(b64Img)
