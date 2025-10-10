# 🧾 Monospace Caption Bot

A professional Telegram bot that converts file captions into monospace (code block) text and sends them back — supports multi-file albums.

## 🚀 Features
- Converts captions to Telegram monospace MarkdownV2 format  
- Supports documents, photos, videos, audio  
- Handles multi-file (media group) messages  
- Clean modular code structure  
- Logging & environment configuration  

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/monospace-bot.git
cd monospace-bot
```

### 2. Create a `.env` file
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the bot
```bash
python run.py
```

## 🧩 Example
Send any file (or media album) with a caption:

**Input:**
```
Here is your document
```

**Output caption:**
```
`Here is your document`
```

## 🛠️ Tech Stack
- Pyrogram
- Python 3.8+
- dotenv for config management

## 📄 License
MIT © 2025 YourName
