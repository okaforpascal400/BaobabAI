import pandas as pd
import os
from tqdm import tqdm

def clean_text(text):
    if not isinstance(text, str):
        return None
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove very short texts
    if len(text) < 50:
        return None
    return text

languages = [
    "hausa", "igbo", "pidgin", "yoruba",
    "swahili", "amharic", "somali",
    "xhosa", "lingala", "luganda", "shona"
]

os.makedirs("data/cleaned", exist_ok=True)

total_before = 0
total_after = 0

for lang in tqdm(languages, desc="Cleaning"):
    path = f"data/raw/{lang}_news.csv"
    if not os.path.exists(path):
        print(f"⚠️  {lang}: file not found")
        continue

    df = pd.read_csv(path)
    before = len(df)
    total_before += before

    # Clean text column
    df["text"] = df["text"].apply(clean_text)
    df = df.dropna(subset=["text"])
    df = df.drop_duplicates(subset=["text"])

    after = len(df)
    total_after += after

    df.to_csv(f"data/cleaned/{lang}_clean.csv", index=False)
    print(f"✅ {lang}: {before} → {after} articles")

print(f"\n🌍 Total: {total_before} → {total_after} clean articles")