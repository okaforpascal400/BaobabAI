from datasets import load_dataset
import pandas as pd
import os

nigerian_languages = {
    "hau": "Hausa",
    "ibo": "Igbo",
    "pcm": "Pidgin",
    "yor": "Yoruba"
}

african_languages = {
    "swa": "Swahili",
    "xho": "Xhosa",
    "amh": "Amharic",
    "som": "Somali",
    "lin": "Lingala",
    "lug": "Luganda"
}

os.makedirs("data/raw", exist_ok=True)

all_languages = {**nigerian_languages, **african_languages}

for code, name in all_languages.items():
    filepath = f"data/raw/{name.lower()}_news.csv"
    
    # Skip if already downloaded
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        print(f"⏭️  {name}: already saved ({len(df)} articles)")
        continue
    
    try:
        dataset = load_dataset("masakhane/masakhanews", code)
        df = dataset["train"].to_pandas()
        df["language"] = name
        df["language_code"] = code
        df.to_csv(filepath, index=False)
        print(f"✅ {name}: {len(df)} articles saved")
    except Exception as e:
        print(f"⚠️  {name}: skipped — {str(e)[:60]}")