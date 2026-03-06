import pandas as pd
import json
import os
from tqdm import tqdm

languages = [
    "hausa", "igbo", "pidgin", "yoruba",
    "swahili", "amharic", "somali",
    "xhosa", "lingala", "luganda", "shona"
]

os.makedirs("data/training", exist_ok=True)

training_data = []

for lang in tqdm(languages, desc="Formatting"):
    path = f"data/cleaned/{lang}_clean.csv"
    if not os.path.exists(path):
        print(f"⚠️  {lang}: not found")
        continue

    df = pd.read_csv(path)

    for _, row in df.iterrows():
        # Format 1 — Summarization
        training_data.append({
            "instruction": f"Summarize this {lang} news article",
            "input": row["text"],
            "output": row["headline"]
        })

        # Format 2 — Classification
        training_data.append({
            "instruction": f"What category does this {lang} article belong to?",
            "input": row["text"],
            "output": row["category"]
        })

    print(f"✅ {lang}: {len(df) * 2} training pairs created")

# Save as JSONL
output_path = "data/training/baobabai_training.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for item in training_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"\n🌍 Total training pairs: {len(training_data)}")
print(f"✅ Saved to {output_path}")