from typing import Optional
import json

import nltk

class DictionaryLoader:
    def __init__(self, path: Optional[str] = None):
        self.path = path or "../resources/haitian_creole_monolingual_dictionary.json"
        self.dictionary = self.load_dictionary()
        nltk.download("wordnet")

    def load_dictionary(self):
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {item["word"]: item["definition"] for item in data}

    def get_definition(self, word: str) -> Optional[str]:
        return self.dictionary.get(word)