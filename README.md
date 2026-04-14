# PostSync 🚀
**AI-Powered Social Media Agency Workflows**

PostSync is the core automation engine for accelerating multi-platform social media distribution. Instead of wasting 20+ hours a week managing individual apps, write a single core thought, and let our custom AI instantly tailor, optimize, and natively publish it identically across Twitter/X, Instagram, LinkedIn, and Facebook at the same time.

---

## ✨ Features
- **Intelligent Platform Tailoring**: Powered by Google's massive `gemini-2.5-flash` model. Our prompt engineering pipeline automatically restricts Twitter length under 240 chars, inflates LinkedIn with professional metrics, and injects Instagram with heavy engaging hashtags.
- **Preview & Polish UI**: A beautifully custom-designed, glassmorphism React interface that lets you dynamically preview all AI-generated content cards sequentially. You can click to edit any mistakes manually before approving the ultimate upload!
- **Universal Media Proxy (FreeImage.host)**: Seamlessly upload local `.png`/`.jpg` images natively targeting Instagram. PostSync bypasses strict API boundaries using an ingenious shadow-proxy to generate clean public URLs that the social networks ingest smoothly!
- **Bring Your Own Key (BYOK) Compliance**: Authenticates natively through your specific X (Twitter) Developer Portal configurations to prevent legacy API suspensions. 

---

## 🏗️ Architecture Stack
- **Frontend Panel**: React 18 / Vanilla Component CSS (`npm run dev`)
- **Backend API Server**: Python FastAPI (`uvicorn main:app --reload`)
- **AI Synthesis**: Google `google-genai` SDK
- **Cross-Platform Delivery Engine**: Ayrshare API

---

## ⚙️ Getting Started

### 1. Requirements
Ensure your machine is running Python 3.9+ and Node.js v18+. You must generate two specific keys to run this successfully:
1. **Google Gemini API Key** (for creating the captions)
2. **Ayrshare Developer Key** (for distributing the captions)

### 2. Environment Setup

*Backend Configuration*:
Create a `.env` file directly inside the root `PostSync` repository. Insert your generated keys below:
```env
GEMINI_API_KEY="your_google_ai_key"
AYRSHARE_API_KEY="your_ayrshare_developer_key"

# REQUIRED specifically for Twitter/X integration only
TWITTER_API_KEY="your_twitter_api_key_from_x_portal"
TWITTER_API_SECRET="your_twitter_api_secret_from_x_portal"
```

### 3. Server Launch Instructions

First, boot up the local Python **Backend**:
```bash
# Set up isolated VENV
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install strict dependencies 
pip install -r requirements.txt

# Ignite FastAPI engine
uvicorn main:app --reload
```
*(Leave this terminal window running in the background).*

Next, boot up the React **Frontend** UI:
```bash
# Open a NEW independent terminal window
cd frontend
npm install
npm run dev
```

Navigate your browser to `http://localhost:5173`. 
Select your platforms, write your hook, upload a picture, and click **Generate**!

---

## 🛑 Troubleshooting Common API Errors
- **Failed to Generate Previews**: Your terminal dropped out of `(venv)`. Stop the uvicorn process, reactivate `.\venv\Scripts\activate`, and run it again to restore the namespace path.
- **Twitter Error 419**: You didn't add the `TWITTER_API_KEY` to your `.env` file. X Developer profiles strictly require "BYOK" authentication. 
- **Instagram Error 147/136**: You did not upload a valid 1:1 local image file. Instagram actively blocks pure-text payloads. 
