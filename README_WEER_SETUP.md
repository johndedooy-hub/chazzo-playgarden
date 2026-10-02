# NOS Weer Scraper & TTS Automation

## Wat doet dit?

Dit systeem:
1. **Haalt weergegevens op** van nos.nl/weer (automatisch)
2. **Reinigt de tekst** (verwijdert fouten, rare tekens, HTML)
3. **Voegt intro en outro toe** ("Welkom bij het weer" + "dit was het weer")
4. **Zet alles om in audio** via OpenAI (professionele stem)
5. **Slaat het op** in je GitHub repo

Alles automatisch, zonder handwerk.

## Stap 1: OpenAI API Key instellen

1. Ga naar: https://github.com/johndedooy-hub/chazzo-playgarden/settings/secrets/actions
2. Klik op "New repository secret"
3. Naam: `OPENAI_API_KEY`
4. Waarde: Jouw OpenAI API key (van https://platform.openai.com/api-keys)
5. Klik "Add secret"

**Klaar!** De workflow kan nu starten.

## Stap 2: Automatisering activeren

De workflow draait automatisch op:
- **6:00 uur** (ochtend)
- **12:00 uur** (middag)
- **18:00 uur** (avond)

Of start handmatig:
1. Ga naar Actions tab in je repo
2. Selecteer "NOS Weer Scraper & TTS"
3. Klik "Run workflow"

## Stap 3: Audio beluisteren

Na elke run vindt je de audio hier:
`audio_output/weer.mp3`

## Aanpassingen (eenvoudig)

Open `scripts/weer_tts.py` en wijzig:

### Andere stem:
```python
voice="nova"  # Kies: nova, echo, alloy, fable, onyx, shimmer
```

### Andere intro/outro:
```python
intro = "Goedemorgen, hier is het weerbericht"
outro = "Tot ziens"
```

### Sneller/langzamer:
```python
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input=text,
    speed=1.2  # 0.25 tot 4.0
)
```

### Andere model (sneller, goedkoper):
```python
model="tts-1"  # In plaats van tts-1-hd
```

## Bestanden

```
.github/workflows/weer-scraper-tts.yml    ← Automation (GitHub Actions)
scripts/weer_tts.py                        ← Python script (logic)
audio_output/weer.mp3                      ← Output (gegenereerd)
README.md                                  ← Dit bestand
```

## Problemen?

**Script runt niet:**
- Check of OPENAI_API_KEY is ingesteld (Settings > Secrets)
- Check of de API key geldig is

**Audio klinkt vreemd:**
- Probeer een andere `voice` (nova, echo, alloy, etc.)
- Probeer `speed=0.9` of `speed=1.1`

**Weertext is onvolledig:**
- Nos.nl kan de HTML structuur wijzigen
- Het script probeert automatisch aan te passen
- Stuur me een issue met de foutmelding

## Kosten

- OpenAI TTS: ~$0.015 per minuut audio
- 3x per dag = ~$1.35/maand (zeer goedkoop)
- GitHub Actions: Gratis (unlimited voor public repos)
