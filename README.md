# 🎵 AI YouTube Music Automation System 🤖

Welcome to the **AI YouTube Music Automation System**! This full-stack application takes natural language music requests, validates them using Google's powerful Gemini AI, and automatically plays the perfect matching song on YouTube using Playwright. 

Plus, with the new **Auto Vibe 🌤️** feature, the AI detects your real-world location, time, and weather to pick the absolute best track for your current mood!

---

## ✨ Features

- 🧠 **AI-Powered Validation:** Uses Google Gemini 2.5 Flash to ensure only music-related queries are processed.
- 🌤️ **Auto Vibe Mode:** Context-aware! The app automatically finds your exact location, time, and real-time weather, feeding it to the AI to pick the perfect song.
- 🎬 **Automated Playwright:** Automatically opens YouTube, types your query, clicks the top result, and presses `f` to enter full-screen mode.
- ⏩ **Auto Ad-Skipping:** Runs a background loop to automatically detect and click YouTube's "Skip Ad" buttons so your music isn't interrupted.
- 💅 **Premium UI:** A beautiful, responsive frosted-glass UI with animated mesh gradients built with React and custom Vanilla CSS.

---

## 🛠️ Prerequisites

Make sure you have the following installed:
- **Node.js** (v18+ recommended) 🟢
- **Python** (v3.10+ recommended) 🐍
- **Google Gemini API Key** 🔑 ([Get one here](https://aistudio.google.com/app/apikey))

---

## 🚀 Setup Instructions

### 1️⃣ Python Automation Setup

Open your terminal and run the following commands to install the Python dependencies and Playwright browsers:

```bash
cd automation
pip install playwright google-generativeai python-dotenv
playwright install chrome
```

**Configure your API Key:**
1. Rename `.env.example` to `.env` inside the `automation` directory.
2. Edit `.env` and paste your Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```

### 2️⃣ Backend Setup

Open a new terminal window and set up the Node.js Express server:

```bash
cd backend
npm install
```

### 3️⃣ Frontend Setup

Open a third terminal window for the React frontend:

```bash
cd frontend
npm install
```

*(Note: This project uses beautiful, custom Vanilla CSS for a premium design—no complex CSS frameworks required!)*

---

## 🎮 Running the Application

You need to run both the Backend and Frontend servers simultaneously to use the app.

1. **Start the Backend:** 🖥️
   ```bash
   cd backend
   npm start
   ```

2. **Start the Frontend:** 🌐
   ```bash
   cd frontend
   npm run dev
   ```

Open your browser to the URL provided by Vite (usually `http://localhost:5173`). 

---

## 🤔 How it works

1. 📝 **Request:** The React frontend sends your natural language request to the Express backend.
2. 🕵️‍♂️ **Execution:** The Express backend securely spawns the Python automation script.
3. 🌡️ **Context:** Python detects your IP, location, and real-time weather using Open-Meteo.
4. 🤖 **AI Magic:** Google Gemini validates the request and generates precise YouTube search keywords (or picks a song based on your current Vibe).
5. 📺 **Playback:** Playwright automatically opens Chrome, searches YouTube, clicks the first result, enters full screen, and actively skips any ads!
