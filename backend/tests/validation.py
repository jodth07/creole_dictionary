# Existing dictionary
from backend.back_translation import get_creole_definition

creole_dict = {"liv": "Objè ki gen plizyè paj, kote ou ka li enfòmasyon oswa istwa."}

# Test words
all_words = ["liv", "boul", "pen"]


if __name__ == "__main__":
    # Test on sample words
    for word in all_words:
        definition, source = get_creole_definition(word, creole_dict)
        print(f"Word: {word}\nDefinition: {definition}\nSource: {source}\n")
