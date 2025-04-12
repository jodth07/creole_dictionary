from nltk.corpus import wordnet as wn
from typing import Optional

from loader import DictionaryLoader
from ml_models.translation import Translator


class DefinitionFetcher:
    def __init__(self, dictionary_loader: DictionaryLoader, translator: Translator):
        self.dictionary_loader = dictionary_loader
        self.translator = translator

    def get_definition(self, word_ht: str) -> (Optional[str], str):
        local_def = self.dictionary_loader.get_definition(word_ht)
        if local_def:
            return local_def, "from_local_dict"

        word_en = self.translator.ht_to_en(word_ht)
        synsets = wn.synsets(word_en, pos=wn.NOUN) or wn.synsets(word_en)
        if not synsets:
            return None, "missing_definition"
        def_en = synsets[0].definition()
        def_ht = self.translator.en_to_ht(def_en)
        return def_ht, "back_translated"
