from openai import OpenAI

from dotenv import load_dotenv
from os import getenv

setupContext = [
    "You are a helpful AI assistant. Refer to the user as Sir. Your purpose is to aid in project guidance or programming help.",
    "If a request that I make to you requires an image (for example, I ask you about something on my desk) then respond with just 'IMAGE_REQUIRED'. The subsequent message will then contain the relevant image.",
    #"If a request that I make to you requires some code (for example I ask you how to program a snippet) then respond with just 'CODE_REQUIRED'. The subsequent message will then contain the relevant code."
]

class GPT:
    def __init__(self, api_key):
        self.messages = []
        self.client = OpenAI(api_key=api_key) 
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


if __name__=="__main__":
    load_dotenv()
    key = getenv("OPENAI_API_KEY")
    client = GPT(key)

    client.askGPT("Hey, what is your purpose?")
    client.askGPT("Cool, how would you write a HTTP request in Python?")
    client.askGPT("What was my first message to you?")

