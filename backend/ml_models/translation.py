
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

nltk.download("wordnet")


class Translator:
    def __init__(self):
        model_name = "facebook/nllb-200-distilled-600M"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.lang_ht = "hat_Latn"
        self.lang_en = "eng_Latn"
        self.translation_en_ht = pipeline("translation", model=self.model, tokenizer=self.tokenizer,
                                          src_lang=self.lang_en, tgt_lang=self.lang_ht, max_length=400)
        self.translation_ht_en = pipeline("translation", model=self.model, tokenizer=self.tokenizer,
                                          src_lang=self.lang_ht, tgt_lang=self.lang_en, max_length=400)

    def ht_to_en(self, text: str) -> str:
        return self.translation_ht_en(text)[0]["translation_text"]

    def en_to_ht(self, text: str) -> str:
        return self.translation_en_ht(text)[0]["translation_text"]
