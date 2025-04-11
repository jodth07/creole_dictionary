from image_lookup import ImageFetcher
from definition import DefinitionFetcher

import re
import random
from typing import List, Optional


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
                    definition = {"word": word, "definition": defn, "source": source}
                    definitions.append(definition)
                seen.add(word)

        if not definitions:
            return {"reply": "Mwen pa jwenn okenn definisyon.", "definitions": []}

        reply = "\n".join([
            self.format_reply(d['word'], d['definition'], d['source'])
            for d in definitions
        ])
        return {"reply": reply, "definitions": definitions}

    def detect_translation_request(self, message: str) -> Optional[dict]:
        """Detects if the message is asking for a translation and returns a Definition-style dict if so."""
        msg = message.strip().lower()

        creole_to_english_patterns = [
            r"(kisa|ki)\s+'?(\w+)'?\s+(vle di|vle di an angle|vle di an anglè)",
            r"tradui\s+'?(\w+)'?\s+an\s+(angle|anglè)",
            r"what\s+is\s+'?(\w+)'?\s+in\s+english"
        ]

        english_to_creole_patterns = [
            r"translate\s+'?(\w+)'?\s+to\s+creole",
            r"what\s+is\s+'?(\w+)'?\s+in\s+creole",
            r"tradui\s+'?(\w+)'?\s+an\s+krey[oò]l"
        ]

        definitions = []
        for pattern in creole_to_english_patterns:
            match = re.search(pattern, msg)
            if match:
                word = match.group(2)
                translated = self.definition_fetcher.translator.ht_to_en(word)
                definitions.append({
                    "word": word,
                    "definition": translated,
                    "source": "translation_ht_to_en"
                })
                reply = "\n".join([
                    self.format_reply(d['word'], d['definition'], d['source'])
                    for d in definitions
                ])
                return {"reply": reply, "definitions": definitions}

        for pattern in english_to_creole_patterns:
            match = re.search(pattern, msg)
            if match:
                word = match.group(1)
                translated = self.definition_fetcher.translator.en_to_ht(word)
                definitions.append({
                    "word": word,
                    "definition": translated,
                    "source": "translation_en_to_ht"
                })

                reply = "\n".join([
                    self.format_reply(d['word'], d['definition'], d['source'])
                    for d in definitions
                ])
                return {"reply": reply, "definitions": definitions}

        return None

