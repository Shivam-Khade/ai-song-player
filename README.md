# AI YouTube Music Automation System

This is a full-stack application that takes natural language music requests, validates them using Google Gemini AI, and plays them on YouTube automatically using Playwright.

## Prerequisites

- Node.js (v18+ recommended)
- Python (v3.10+ recommended)
- Google Gemini API Key

## Setup Instructions

### 1. Python Automation Setup

Open a terminal and run the following commands:

```bash
cd ai-yt-song/automation
pip install playwright google-generativeai python-dotenv
playwright install chrome
```

Configure your API Key:
1. Copy the `.env.example` to `.env` in the `automation` directory.
2. Edit `automation/.env` and add your Gemini API Key.

### 2. Backend Setup

Open a new terminal and run:

```bash
cd ai-yt-song/backend
npm install express cors dotenv
```

### 3. Frontend Setup

Open a third terminal and run:

```bash
cd ai-yt-song/frontend
# Create Vite React app structure if you haven't already
# npm create vite@latest . -- --template react
npm install axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Make sure your `tailwind.config.js` is set up properly:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

And your `src/index.css` has the Tailwind directives:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Running the Application

You need to run both the Backend and Frontend servers.

1. **Start the Backend:**
```bash
cd backend
npm start
```

2. **Start the Frontend:**
```bash
cd frontend
npm run dev
```

Open your browser to `http://localhost:5173` (or the port Vite provides) and enter a music request like "Play Bohemian Rhapsody by Queen".

## How it works

1. The React frontend sends your request to the Express backend.
2. The Express backend spawns the Python automation script.
3. The Python script uses Google Gemini to determine if your request is valid (music-related).
4. If invalid, the script returns `DECLINED`.
5. If valid, the script uses Playwright to open Chrome, search YouTube, and play the first result.
