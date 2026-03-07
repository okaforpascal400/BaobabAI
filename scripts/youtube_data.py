import subprocess
import json
import pandas as pd
import os
import time
from youtube_transcript_api import YouTubeTranscriptApi

os.makedirs("data/youtube", exist_ok=True)

# Real BBC Africa YouTube channel IDs
channels = {
    "pidgin": "UCU8UBCRMxuSk1RHcMSR-FFA",
    "hausa": "UCHqYcMTFR3I4DYKqIkdkEhg",
    "yoruba": "UCNNqGdOW4URXkJxXSbBrODg",
    "swahili": "UCWMhDpPNFVcCWGCBFJm4UFw",
    "igbo": "UCg8VRMiPLvkFpfwF5FeOBJg",
}

ytt_api = YouTubeTranscriptApi()
all_data = []

for lang, channel_id in channels.items():
    print(f"\n🎬 Fetching {lang} videos from BBC...")
    
    # Get video IDs from channel using yt-dlp
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "id",
        "--playlist-end", "10",
        f"https://www.youtube.com/channel/{channel_id}/videos"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        video_ids = [v.strip() for v in result.stdout.strip().split("\n") if v.strip()]
        print(f"  Found {len(video_ids)} videos")
        
        lang_data = []
        for video_id in video_ids[:5]:
            try:
                transcript = ytt_api.fetch(video_id)
                text = " ".join([t.text for t in transcript])
                if len(text) > 100:
                    lang_data.append({
                        "language": lang,
                        "video_id": video_id,
                        "text": text,
                        "source": "youtube_bbc"
                    })
                    print(f"  ✅ {video_id}: {len(text)} chars")
            except Exception as e:
                print(f"  ⚠️  {video_id}: no transcript")
            time.sleep(1)

        if lang_data:
            df = pd.DataFrame(lang_data)
            df.to_csv(f"data/youtube/{lang}_youtube.csv", index=False)
            all_data.extend(lang_data)

    except Exception as e:
        print(f"  ❌ {lang}: {str(e)[:60]}")

print(f"\n✅ Total YouTube transcripts: {len(all_data)}")