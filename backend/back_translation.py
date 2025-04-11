from typing import Optional

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import nltk
import json

nltk.download("wordnet")
from nltk.corpus import wordnet as wn


# Load NLLB model and tokenizer
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Language codes
lang_ht = "hat_Latn"
lang_en = "eng_Latn"

translation_en_ht = pipeline(
    "translation",
    model=model,
    tokenizer=tokenizer,
    src_lang=lang_en,
    tgt_lang=lang_ht,
    max_length=400,
)

translation_ht_en = pipeline(
    "translation",
    model=model,
    tokenizer=tokenizer,
    src_lang=lang_ht,
    tgt_lang=lang_en,
    max_length=400,
)


def load_dictionary(creole_dict_path: Optional[str] = None):
    if not creole_dict_path:
        creole_dict_path = "../resources/haitian_creole_monolingual_dictionary.json"
    with open(creole_dict_path, "r", encoding="utf-8") as file:
        return json.load(file)


def word_def_dictionary(dictionary_list: Optional[list] = None):
    if dictionary_list is None:
        dictionary_list = load_dictionary()
    return {
        dictionary["word"]: dictionary["definition"] for dictionary in dictionary_list
    }


pre_loaded_dictionary = word_def_dictionary


def translate_ht_en(text) -> str:
    return translation_ht_en(text)[0]["translation_text"]


def translate_en_ht(text) -> str:
    return translation_en_ht(text)[0]["translation_text"]


def get_english_definition(word_en):
    synsets = wn.synsets(word_en, pos=wn.NOUN)
    if not synsets:
        synsets = wn.synsets(word_en)

    if synsets:
        return synsets[0].definition()
    return None


def get_creole_definition(word_ht, creole_dict=None):

    if creole_dict is None:
        creole_dict = pre_loaded_dictionary()
    if word_ht in creole_dict:
        return creole_dict[word_ht], "from_local_dict"
    else:
        word_en = translate_ht_en(word_ht)
        def_en = get_english_definition(word_en)
        if not def_en:
            return None, "missing_definition"
        def_ht = translate_en_ht(def_en)
        return def_ht, "back_translated"
