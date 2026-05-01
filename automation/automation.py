import sys
import os
import asyncio
import google.generativeai as genai
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables from .env file located in the same directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path, override=True)

# Configure Google Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or not api_key.strip():
    # If no API key is provided, fail gracefully
    print("DECLINED (Missing API Key)", flush=True)
    sys.exit(1)
    
api_key = api_key.strip()

genai.configure(api_key=api_key)

# The strict system prompt to enforce validation rules
SYSTEM_PROMPT = """You are a strict music request validator.
Your job is to determine if the user's input is a music-related request (song, artist, album, genre, playlist).
If it IS music-related, return ONLY YouTube search keywords (e.g., "Arijit Singh hits" or "Bohemian Rhapsody Queen") without quotes, special characters, or explanations.
If it is NOT music-related (weather, news, general questions, random commands), return EXACTLY the string "DECLINED" with no punctuation.
"""

import datetime
import urllib.request
import json

def get_current_context():
    """Fetches current time, exact location, and weather to feed to the AI."""
    now = datetime.datetime.now()
    day_time = now.strftime("%A, %I:%M %p")
    
    weather = "Unknown weather"
    location = "Unknown location"
    
    try:
        # 1. Get exact location from IP using ip-api
        with urllib.request.urlopen("http://ip-api.com/json/", timeout=5) as response:
            data = json.loads(response.read().decode())
            lat = data.get('lat')
            lon = data.get('lon')
            city = data.get('city', 'your city')
            country = data.get('country', '')
            location = f"{city}, {country}".strip(', ')
            
        # 2. Get accurate weather from Open-Meteo using the lat/lon (No API Key Required!)
        if lat and lon:
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            with urllib.request.urlopen(weather_url, timeout=5) as w_response:
                w_data = json.loads(w_response.read().decode())
                temp = w_data['current_weather']['temperature']
                weathercode = w_data['current_weather']['weathercode']
                
                # Simple weather code mapping
                condition = "Clear"
                if weathercode in [1, 2, 3]: condition = "Partly cloudy"
                elif weathercode in [45, 48]: condition = "Foggy"
                elif weathercode in [51, 53, 55, 56, 57]: condition = "Drizzling"
                elif weathercode in [61, 63, 65, 66, 67]: condition = "Raining"
                elif weathercode in [71, 73, 75, 77, 85, 86]: condition = "Snowing"
                elif weathercode in [80, 81, 82]: condition = "Rain showers"
                elif weathercode in [95, 96, 99]: condition = "Thunderstorm"
                
                weather = f"{temp}°C and {condition}"
    except Exception as e:
        print(f"Weather/Location Fetch Error: {e}", file=sys.stderr)
        pass
    
    context_string = f"CURRENT REAL-WORLD CONTEXT: The user is located in {location}. It is {day_time}. The weather is {weather}."
    
    # Print it to the console so the user can see what was detected!
    print("=== Auto Vibe Context ===", file=sys.stderr)
    print(f"Location: {location}", file=sys.stderr)
    print(f"Day/Time: {day_time}", file=sys.stderr)
    print(f"Weather:  {weather}", file=sys.stderr)
    print("=========================", file=sys.stderr)
    
    return context_string

async def validate_query(query):
    """Uses Gemini API to validate and extract keywords from the natural language query."""
    try:
        context_string = get_current_context()
        # Append the context so Gemini knows the user's environment
        dynamic_prompt = SYSTEM_PROMPT + f"\n\n{context_string}\nIf the user asks for music based on weather/time/vibe, use this context to pick a highly fitting song or playlist."
        
        # We use gemini-2.5-flash
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=dynamic_prompt)
        response = await model.generate_content_async(query)
        result = response.text.strip()
        return result
    except Exception as e:
        # Log the actual error to stderr so the backend console can see it
        print(f"Gemini API Error: {str(e)}", file=sys.stderr)
        return "DECLINED"

async def play_on_youtube(keywords):
    """Uses Playwright to automate YouTube search and play the first video."""
    playwright = await async_playwright().start()
    
    # Use Chrome channel for better compatibility, headless=False to show browser
    browser = await playwright.chromium.launch(headless=False, channel="chrome")
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Navigate to YouTube
        print("Navigating to YouTube...", file=sys.stderr)
        await page.goto("https://www.youtube.com")
        
        # Wait for the search input field to be available
        print("Waiting for search box...", file=sys.stderr)
        search_selector = 'input[name="search_query"]'
        await page.wait_for_selector(search_selector, timeout=15000)
        
        # Fill the search field with the AI-generated keywords
        print("Filling search box...", file=sys.stderr)
        await page.fill(search_selector, keywords)
        
        # Press Enter to perform the search
        print("Pressing enter...", file=sys.stderr)
        await page.press(search_selector, "Enter")
        
        # Wait for the search results to load
        print("Waiting for results...", file=sys.stderr)
        await page.wait_for_selector("ytd-video-renderer", timeout=15000)
        
        # Find the first video title link and click it
        print("Clicking first video...", file=sys.stderr)
        videos = await page.query_selector_all("ytd-video-renderer a#video-title")
        if videos and len(videos) > 0:
            await videos[0].click()
            print("Video playing!", file=sys.stderr)
            
            # Wait briefly for the video player to initialize
            await page.wait_for_timeout(2000)
            
            # Press 'f' to make the video fullscreen
            print("Making video fullscreen...", file=sys.stderr)
            await page.keyboard.press("f")
            
            # Keep browser open and periodically check for "Skip Ad" buttons
            print("Watching for ads to skip...", file=sys.stderr)
            skip_selectors = [
                ".ytp-ad-skip-button",
                ".ytp-ad-skip-button-modern",
                ".ytp-skip-ad-button",
                ".ytp-ad-text.ytp-ad-skip-button-text"
            ]
            
            while True:
                for selector in skip_selectors:
                    try:
                        skip_btn = await page.query_selector(selector)
                        if skip_btn and await skip_btn.is_visible():
                            await skip_btn.click()
                            print("Ad skipped!", file=sys.stderr)
                            await page.wait_for_timeout(2000) # prevent rapid-fire clicking
                    except Exception:
                        pass
                
                # Check for ads every 2 seconds
                await page.wait_for_timeout(2000)
        else:
            print("No video results found.", file=sys.stderr)
            await browser.close()
            await playwright.stop()
            sys.exit(0)
    except Exception as e:
        # Handle timeout or selector failures gracefully
        print(f"Playwright Automation Error: {str(e)}", file=sys.stderr)
        await browser.close()
        await playwright.stop()
        sys.exit(1)

async def main():
    # Reject empty queries
    if len(sys.argv) < 2:
        print("DECLINED", flush=True)
        sys.exit(1)
        
    query = sys.argv[1]
    
    # 1. AI VALIDATION (The Gatekeeper)
    validation_result = await validate_query(query)
    
    if validation_result == "DECLINED" or not validation_result:
        # Output "DECLINED" exactly to stdout
        print("DECLINED", flush=True)
    else:
        # Output "VALIDATED: {keywords}" to stdout for the backend to see
        print(f"VALIDATED: {validation_result}", flush=True)
        
        # 2. BROWSER AUTOMATION
        await play_on_youtube(validation_result)

if __name__ == "__main__":
    asyncio.run(main())
