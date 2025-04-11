from transformers import pipeline

# Load translation models
print("Loading models...")
nllb_translation = pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M",
    src_lang="eng_Latn",
    tgt_lang="hat_Latn",
)
# m2m100_translation = pipeline("translation", model="facebook/m2m100_418M", src_lang="en", tgt_lang="hat")
# marianmt_translation = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ht")

# Sample sentences – add or modify as needed
sample_sentences = [
    "The weather is nice today, isn't it?",
    "I am learning Haitian Creole to connect with my roots.",
    "Where is the nearest hospital?",
    "A Large Language Model (LLM) is a type of artificial intelligence that can generate human-like text and understand natural language, trained on vast amounts of text data to predict the next word in a sequence.",
    "Agentic AI refers to AI systems that can act autonomously, adapt in real-time, and solve multi-step problems based on context and objectives, going beyond simple question-answering or content generation.",
]


# Function to translate all sentences using each model
def translate_all(models, sentences):
    translations = {}
    for model_name, model in models.items():
        print(f"Translating with {model_name}...")
        translated = []
        for sentence in sentences:
            result = model(sentence)[0]["translation_text"]
            translated.append(result)
        translations[model_name] = translated
    return translations


# Register models
models = {
    "NLLB-200": nllb_translation,
    # "M2M-100": m2m100_translation,
    # "MarianMT": marianmt_translation,
}

# Perform translations
translations = translate_all(models, sample_sentences)

# Display results side-by-side
for i, sentence in enumerate(sample_sentences):
    print(f"\n====================\nOriginal: {sentence}\n")
    for model in models.keys():
        print(f"{model} → {translations[model][i]}")
