import pandas as pd
import os
import json
from tqdm import tqdm

folders = ["data/raw", "data/expansion"]
all_docs = []

print("📂 Loading all data sources...")

for folder in folders:
    if not os.path.exists(folder):
        continue
    for f in os.listdir(folder):
        if f.endswith(".csv"):
            try:
                df = pd.read_csv(f"{folder}/{f}")
                if "text" in df.columns:
                    df["source_file"] = f
                    all_docs.append(df[["text", "source_file"] + 
                        [c for c in ["language", "headline", "category"] 
                         if c in df.columns]])
            except Exception as e:
                print(f"⚠️  {f}: {str(e)[:50]}")

# Merge everything
merged = pd.concat(all_docs, ignore_index=True)
print(f"\n✅ Total documents loaded: {len(merged)}")

# Clean
merged["text"] = merged["text"].astype(str)
merged = merged[merged["text"].str.len() > 100]
merged = merged.drop_duplicates(subset=["text"])
print(f"✅ After cleaning: {len(merged)} documents")

# Generate training pairs
os.makedirs("data/training", exist_ok=True)
training_pairs = []

for _, row in tqdm(merged.iterrows(), total=len(merged), desc="Generating pairs"):
    text = row["text"]
    lang = row.get("language", "African")

    # Pair 1 — Summarization
    training_pairs.append({
        "instruction": f"Summarize the following {lang} text in one sentence.",
        "input": text[:800],
        "output": row["headline"] if "headline" in row and pd.notna(row.get("headline")) else text[:100]
    })

    # Pair 2 — Language identification
    training_pairs.append({
        "instruction": "What language is this text written in?",
        "input": text[:200],
        "output": str(lang)
    })

    # Pair 3 — Comprehension
    training_pairs.append({
        "instruction": "What is the main topic of this text?",
        "input": text[:500],
        "output": row["category"] if "category" in row and pd.notna(row.get("category")) else "African news and information"
    })

print(f"\n✅ Total training pairs: {len(training_pairs)}")

# Save
output_path = "data/training/baobabai_v2_training.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for pair in training_pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"✅ Saved to {output_path}")
print(f"\n🌍 BaobabAI v0.2 training data ready!")