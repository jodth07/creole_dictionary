
from definition import DefinitionFetcher

import re
import random
from typing import List

class ChatProcessor:
    def __init__(self, definition_fetcher: DefinitionFetcher):
        self.definition_fetcher = definition_fetcher

    @staticmethod
    def extract_words(text: str) -> List[str]:
        patterns = [
            r"kisa\s+(\w+)\s+vle\s+di",
            r"kisa\s+yon\s+(\w+)\s+ye",
            r"kisa\s+(\w+)\s+ye",
            r"ki\s+siyifikasyon\s+(\w+)",
            r"sa\s+vle\s+di\s+(\w+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return [match.group(1)]
        return re.findall(r"\b\w+\b", text.lower())

    @staticmethod
    def format_reply(word: str, definition: str, source: str) -> str:
        formats = [
            f"Mo '{word}' vle di '{definition}'. (Sous: {source})",
            f"Bon kesyon! Mo '{word}' vle di '{definition}'. Sa soti nan {source}.",
            f"Ah, '{word}'? Sa fasil! Li vle di '{definition}'. (Sous: {source})"
        ]
        return random.choice(formats)

    def process_message(self, message: str) -> dict:
        words = self.extract_words(message)
        seen = set()
        definitions = []

        for word in words:
            if word not in seen:
                defn, source = self.definition_fetcher.get_definition(word)
                if defn:
                    definitions.append({"word": word, "definition": defn, "source": source})
                seen.add(word)

        if not definitions:
            return {"reply": "Mwen pa jwenn okenn definisyon.", "definitions": []}

        reply = "\n".join([
            self.format_reply(d['word'], d['definition'], d['source'])
            for d in definitions
        ])
        return {"reply": reply, "definitions": definitions}

