from datasets import load_dataset
import pandas as pd
import os

languages = {
    "hau": "Hausa",
    "ibo": "Igbo",
    "pcm": "Pidgin",
    "yor": "Yoruba"
}

os.makedirs("data/raw", exist_ok=True)

for code, name in languages.items():
    dataset = load_dataset("masakhane/masakhanews", code)
    df = dataset["train"].to_pandas()
    df.to_csv(f"data/raw/{name.lower()}_news.csv", index=False)
    print(f"Saved {name}: {len(df)} articles → data/raw/{name.lower()}_news.csv")