import openai
from dotenv import load_dotenv, find_dotenv
from data.clean import Dataset
from typing import List
from termcolor import colored
import os

load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatInterface:
    def __init__(self):
        self.data = Dataset()
        self.data = self.data.data.head(20)
        self.chat_history = [
            {"role": "system", "content": "You are an AI playing a word game."},
            {"role": "user", "content": self.create_prompt()},
        ]

    def create_prompt(self) -> str:
        # Define the prompt
        return f"""
        You as the AI are playing a word game that is all about finding connections between words. The game starts with 16 words on the board and your 
        job will be to respond with four sets of four words that are connected. The four sets for four are not connected in any way, although some words may fall into multiple categories. 
        It is your job to disambiguate the words and find the correct set of four. You will be given 16 words and then you will respond with the four collections of four words and the assumed category, 
        in addition to which set should be judged in this round. Use the following format:
        "
        set1: [word1, word2, word3, word4] is [category]
        set2: [word1, word2, word3, word4] is [category]
        set3: [word1, word2, word3, word4] is [category]
        set4: [word1, word2, word3, word4] is [category]
        Sumbit [setN] for judging.
        Each word can only be used once. A human user will submit your answers one set at a time to a judge. After each set submission, you will be given feedback on the correctness of only that set. 
        Feeback will come in 3 options:

        1. correct: all four words are in the correct set, do not change this set
        2. 1 away: three of the words are in the correct set, but one is not.
        3. incorrect: two or more words are not in the correct set.
        
        After this feedback you will reconsider your categorizations and return four sets of words again. This process will repeat until you have found the correct set of four words.
        If you are told that a set is correct, do not change that set. Those words are now off the table. The game ends when you have four incorrect or 1 away guesses, so be smart with your turns.

        Below is provides examples of the correct categories and word sets indexed by the date. Each date is the set of 16 words.
        {self.data.to_string()}

        Once the game starts you will be given the 16 words and then you will be able to respond with the four sets.
        Remember you are the AI and you are playing the game.
        """

    def chat(self, message: str) -> None:
        self.chat_history.append({"role": "user", "content": message})

        completion = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo", messages=self.chat_history
            model="gpt-4",
            messages=self.chat_history,
        )
        print(completion.choices[0].message["content"])
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
            message = input(colored("chat>", "green"))
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
    words = [
        "NOSE",
        "CROWN",
        "SWORD",
        "MASK",
        "DIAL",
        "FAUCET",
        "TIARA",
        "HAND",
        "BLOCK",
        "MASCARA",
        "HIDE",
        "LASSO",
        "CANDIDATE",
        "SHIELD",
        "STRAP",
        "COVER",
    ]
    chat = ChatInterface()
    chat.start_game(words)
