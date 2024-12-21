from openai import OpenAI

from dotenv import load_dotenv
from os import getenv
from base64 import b64encode


class GPT:
    def __init__(self, api_key, IMG_REQ_KEYSTRING):
        self.messages = []
        self.client = OpenAI(api_key=api_key) 

        setupContext = [
            "You are a helpful AI assistant. Refer to the user as Sir. Your purpose is to aid in project guidance or programming help.",
            f"If a request that I make to you requires an image (for example, I ask you about something on my desk) then respond with just '{IMG_REQ_KEYSTRING}'. The subsequent message will then contain the relevant image.",
            #"If a request that I make to you requires some code (for example I ask you how to program a snippet) then respond with just 'CODE_REQUIRED'. The subsequent message will then contain the relevant code."
        ]

        for input in setupContext:
            self.createMessage(input, "system")
        self.maxTokens = 2000

    def createMessage(self, content, role="user"):
        newMsg = {"role": role, "content": content}
        self.messages.append(newMsg)

    def sendMessageHistory(self):
        response = self.client.chat.completions.create(model = "gpt-4o-mini",
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
