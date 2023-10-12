import openai
from dotenv import load_dotenv, find_dotenv
from data.clean import Dataset
from typing import List
import os

load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatInterface:
    def __init__(self):
        self.data = Dataset()
        self.data = self.data.data.head(100)
        self.chat_history = [
            {"role": "system", "content": "You are an AI playing a word game."},
            {"role": "user", "content": self.create_prompt()},
        ]

    def create_prompt(self) -> str:
        # Define the prompt
        return f"""
        You as the AI are playing a word game that is all about finding connections between words. The game starts with 16 words on the board and your 
        job will be to respond with four words that are connected. The four sets for four are not connected in any way. Once a set of four is correctly identified 
        the words in that set are not used again. Feedback will be provided on your responses to help you improve. 1. Correct, 2. One away 
        (correct except for one word), or 3. Incorrect.
        After each feedback you will be able to respond with four words again.
        The game will end after incorrect guesses of four words. 

        Below is provides examples of the correct categories and word sets indexed by the date. Each date is the set of 16 words.
        {self.data.to_string()}

        Once the game starts you will be given the 16 words and then you will be able to respond with four words.
        Remember you are the AI and you are playing the game.
        """

    def chat(self, message: str) -> None:
        self.chat_history.append({"role": "user", "content": message})

        completion = openai.ChatCompletion.create(
            model="gpt-4", messages=self.chat_history
        )
        print(completion.choices[0].message)
        self.chat_history.append(completion.choices[0].message)

        return completion.choices[0].message

    def start_game(self, words: List[str]):
        self.chat_history.append(
            {
                "role": "user",
                "content": f"This is the start of the game, here are the words: {words}. Please respond with four words.",
            }
        )

        while True:
            message = input("Enter your response: ")
            self.chat_history.append({"role": "user", "content": message})
            resp = self.chat(message)


if __name__ == "__main__":
    words = [
        "CAN",
        "BUTCHER",
        "ACTION",
        "LEAD",
        "PRIME",
        "CUT",
        "WAX",
        "MAY",
        "TOILET",
        "TOP",
        "MIGHT",
        "CAMERA",
        "HEAD",
        "LIGHTS",
        "SCRAP",
        "COULD",
    ]
    chat = ChatInterface()
    chat.start_game(words)
