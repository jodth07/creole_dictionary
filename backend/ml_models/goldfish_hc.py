import json
from typing import Optional
from datasets import load_dataset
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    Trainer, TrainingArguments
)
import torch


class GoldfishCreoleTrainer:
    def __init__(
            self,
            model_name: str = "goldfish-models/hat_latn_100mb",
            dataset_path: str = "resources/train.txt",
            output_dir: str = "./goldfish-creole-finetuned",
            max_length: int = 128,
            device: Optional[str] = None
    ):
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.output_dir = output_dir
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = self.get_device(device)
        self.model.to(self.device)
        self.tokenized_dataset = None

    @staticmethod
    def get_device(device: Optional[str]):
        if device is not None:
            if torch.cuda.is_available():
                return "cuda"
            elif torch.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return device

    ### --- STEP 1: Data Cleaning ---
    def clean_json_dictionary(self, json_file: str) -> None:
        with open(json_file, "r", encoding="utf-8") as infile:
            entries = json.load(infile)

        with open(self.dataset_path, "w", encoding="utf-8") as outfile:
            for entry in entries:
                word = entry.get("word", "").strip()
                definition = entry.get("definition", "").strip()
                if word and definition:
                    outfile.write(f"Mo: {word}\nDefinisyon: {definition}\n\n")

        print(f"✅ Cleaned data written to {self.dataset_path}")

    ### --- STEP 2: Load and Tokenize ---
    def load_and_tokenize(self):
        raw_dataset = load_dataset("text", data_files={"train": self.dataset_path})

        def tokenize_function(example):
            tokenized = self.tokenizer(
                example["text"],
                truncation=True,
                padding="max_length",
                max_length=self.max_length
            )
            tokenized["labels"] = tokenized["input_ids"].copy()
            return tokenized

        self.tokenized_dataset = raw_dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=["text"]
        )
        self.tokenized_dataset.set_format("torch")
        print("✅ Tokenized and formatted dataset")

    ### --- STEP 3: Fine-Tuning ---
    def train(self, num_train_epochs: int = 5, batch_size: int = 8):
        if not self.tokenized_dataset:
            raise RuntimeError("Tokenized dataset not prepared. Run `load_and_tokenize()` first.")

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=batch_size,
            warmup_steps=10,
            learning_rate=5e-5,
            weight_decay=0.01,
            logging_steps=10,
            eval_strategy="no",
            save_strategy="epoch"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.tokenized_dataset["train"]
        )

        trainer.train()
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        print(f"✅ Model fine-tuned and saved to {self.output_dir}")

    ### --- STEP 4: Load Fine-Tuned Model ---
    def load_finetuned_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.output_dir)
        self.model = AutoModelForCausalLM.from_pretrained(self.output_dir)
        self.model.to(self.device)
        print(f"✅ Fine-tuned model loaded from {self.output_dir}")

    ### --- STEP 5: Generate Text from Prompt ---
    def generate_definition(self, word: str, max_length: int = 50, num_return_sequences: int = 3):
        prompt = f"Mo: {word}\nDefinisyon:"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            num_return_sequences=num_return_sequences
        )

        results = [
            self.tokenizer.decode(output, skip_special_tokens=True)
            for output in outputs
        ]

        print("📝 Generated Definitions:")
        for i, text in enumerate(results):
            print(f"{i + 1}. {text.strip()}")
        return results


def main():
    trainer = GoldfishCreoleTrainer()

    # Step 1: Clean raw dictionary JSON into text format
    dictionary_js_path = "resources/haitian_creole_monolingual_dictionary.json"
    trainer.clean_json_dictionary(dictionary_js_path)

    # Step 2: Load and tokenize the cleaned data
    trainer.load_and_tokenize()

    # Step 3: Train the model
    trainer.train(num_train_epochs=5)

    # (Optional) Reload the fine-tuned model later
    trainer.load_finetuned_model()

    # Step 4: Generate definition for a new word
    trainer.generate_definition("abònman")

if __name__ == "__main__":
    main()
