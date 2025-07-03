import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

MODEL_ID = os.getenv("BASE_MODEL", "microsoft/DialoGPT-small")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./finetuned-aviation")
MODEL_REPO = os.getenv("MODEL_REPO", "afscomercial/streamlit-chatbot-aviation")
MAX_LEN = 128
EPOCHS = int(os.getenv("EPOCHS", 1))

# Load custom aviation dataset
print("Loading dataset…")
train_ds = load_dataset("json", data_files="data/aviation_conversations.jsonl", split="train")

# Tokenizer & model
print("Loading base model…")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# Ensure the tokenizer has a pad token to avoid padding errors
if tokenizer.pad_token is None:
    # Re-use the EOS token as the padding token (common for causal language models like DialoGPT)
    tokenizer.pad_token = tokenizer.eos_token
    # Resize model embeddings in case a new token was added
    model.resize_token_embeddings(len(tokenizer))

def tokenize(batch):
    # Tokenize the input text and create labels that mirror the input_ids so the model can compute a loss
    tokens = tokenizer(batch["text"], truncation=True, max_length=MAX_LEN, padding="max_length")
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

train_tok = train_ds.map(tokenize, batched=True, remove_columns=["text"])

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=2,
    save_total_limit=1,
    logging_steps=10,
    push_to_hub=True,
    hub_model_id=MODEL_REPO,
)

trainer = Trainer(model=model, args=training_args, train_dataset=train_tok, tokenizer=tokenizer)
print("Starting training…")
trainer.train()
print("Pushing to Hub…")
trainer.push_to_hub()
print("Done!") 