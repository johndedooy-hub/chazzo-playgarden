#!/usr/bin/env python3
import os
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from pathlib import Path

# Config
OUTPUT_DIR = Path("audio_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Init OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def scrape_weer():
    """Scrape weer van nos.nl"""
    url = "https://nos.nl/weer"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Zoek de weer paragraph - flexibel voor class wijzigingen
    paragraph = soup.find('p', class_=re.compile(r'.*Paragraph.*'))
    
    if not paragraph:
        print("Paragraph niet gevonden, probeer alternatief...")
        # Fallback: zoek alle p tags met weer content
        for p in soup.find_all('p'):
            text = p.get_text()
            if 'vannacht' in text.lower() or 'graden' in text.lower():
                paragraph = p
                break
    
    if not paragraph:
        print("Geen weer tekst gevonden")
        return None
    
    weer_text = paragraph.get_text()
    return weer_text

def clean_text(text):
    """Clean en normaliseer tekst"""
    # HTML entities
    text = text.replace('&#39;', "'")
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    # Extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Verwijder vreemde tekens maar hou interpunctie
    text = re.sub(r'[^\w\s.,!?\'"\-—]', '', text)
    
    return text

def create_audio_text(weer_text):
    """Combineer intro, weer en outro"""
    intro = "Welkom bij het weer."
    outro = "Dit was het weer."
    
    full_text = f"{intro} {weer_text} {outro}"
    return full_text

def generate_tts(text, output_file):
    """Generate TTS audio met OpenAI"""
    try:
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="nl",
            input=text,
            speed=1.0
        )
        
        response.stream_to_file(output_file)
        print(f"Audio saved: {output_file}")
        return True
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return False

def main():
    print("🌤️ Starten weer scrape + TTS...")
    
    # Scrape
    weer_raw = scrape_weer()
    if not weer_raw:
        print("Scrape failed")
        return
    
    # Clean
    weer_clean = clean_text(weer_raw)
    print(f"Weer text: {weer_clean[:100]}...")
    
    # Create full text
    full_text = create_audio_text(weer_clean)
    print(f"Volledige tekst: {full_text[:100]}...")
    
    # Generate audio
    output_file = OUTPUT_DIR / "weer.mp3"
    if generate_tts(full_text, str(output_file)):
        print("✅ Klaar")
    else:
        print("❌ TTS error")

if __name__ == "__main__":
    main()
