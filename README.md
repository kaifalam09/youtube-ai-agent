# YouTube AI Agent 🎬🤖

Ek chat-driven agent jo:
1. Script/topic se short video generate karta hai (max 50 seconds)
2. AI se title + description likhta hai
3. Seedha aapke YouTube channel pe upload karta hai (official YouTube Data API v3)
4. Chat commands se control hota hai

100% legal automation — YouTube ka apna official API use hota hai, jo creators/tools normally isi tarah use karte hain.

---

## 📦 Setup

### 1. Repo clone karo
```bash
git clone <your-repo-url>
cd youtube-ai-agent
pip install -r requirements.txt
```

### 2. FFmpeg install karo (video rendering ke liye)
- Windows: https://ffmpeg.org/download.html se download karke PATH mein add karo
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### 3. YouTube API credentials lo (free)
1. https://console.cloud.google.com pe jao
2. Naya project banao
3. "YouTube Data API v3" enable karo
4. "OAuth consent screen" setup karo (External, apna email daal do)
5. "Credentials" → "Create Credentials" → "OAuth client ID" → Type: **Desktop app**
6. `client_secret.json` download karke isi folder mein daal do

### 4. Anthropic API key (title/description generation ke liye)
1. https://console.anthropic.com pe account banao
2. API key generate karo
3. `.env` file banao (`.env.example` copy karke):
```
ANTHROPIC_API_KEY=your_key_here
```

### 5. Chalao
```bash
python main.py
```

Pehli baar chalane pe browser khulega — apne Google/YouTube account se login + permission do. Uske baad `token.json` save ho jayega, dobara login nahi mangega.

---

## 💬 Kaise use karein (Chat commands)

```
> generate video: "5 amazing facts about space" 
> upload last video
> generate and upload: "morning motivation quote"
> set title: My Custom Title
> exit
```

---

## 📁 Project Structure

```
youtube-ai-agent/
├── main.py                 # Chat loop / entry point
├── agent.py                 # Command parser + orchestration
├── video_generator.py       # TTS + video creation (max 50s)
├── youtube_uploader.py      # YouTube Data API upload
├── content_writer.py        # AI title/description generator
├── config.py                 # Settings + env loading
├── requirements.txt
├── .env.example
└── output/                   # Generated videos land here
```

## ⚠️ Important Limits
- Video duration hard-capped at 50 seconds (config.py mein `MAX_VIDEO_SECONDS`)
- YouTube API has daily upload quota (default ~6 uploads/day per project on free tier) — apne Cloud Console quota page pe check kar sakte ho
- Ye tool sirf **apne khud ke channel** pe upload karne ke liye hai — kisi aur ke account ya paywall/subscription bypass ke liye NAHI hai
