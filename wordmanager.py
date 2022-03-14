import requests
import random
import string

# API http://www.datamuse.com/api/
# wildcard patterns: https://www.onelook.com/?c=faq#patterns


class WordManager:
    """ Handles calls to the DataMuse words API """
    def __init__(self):
        self.request_path = "https://api.datamuse.com/words"

    @staticmethod
    def parse_words(json_words):
        """ parse list of words out of the JSON data """
        words = []
        for entry in json_words:
            words.append(entry['word'])
        return words

    def get_random_word(self):
        """ uses API calls to return a random five-letter word """
        word = ""
        while len(word) == 0:
            # selecting one random letter for the random word returns less obscure words
            pattern = f"{random.choice(string.ascii_uppercase)}????"
            response = requests.get(f"{self.request_path}?sp=//{pattern}")
            if response.status_code == 200:
                if len(response.json()):
                    word = random.choice(WordManager.parse_words(response.json())).upper()
            else:
                print(response.status_code)
                return False
        return word

    def is_word(self, word):
        """ returns true if word is in the API dictionary, false otherwise """
        response = requests.get(f"{self.request_path}?sp={word}")
        if response.status_code == 200:
            if len(response.json()):
                words = WordManager.parse_words(response.json())
                if word.lower() in words:
                    return True
        return False

