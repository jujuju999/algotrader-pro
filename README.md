# AlgoTrader Pro — Cloud Deployment

## Was ist das?
Vollständiges Trading-System das 24/7 in der Cloud läuft:
- Echte Finnhub Live-Daten (WebSocket + REST)
- 7-Strategie Trading Engine
- 🧠 KI-Lernfunktion (Reinforcement Learning)
- Premium Web-Dashboard

## Railway.app Deployment (kostenlos, 5 Minuten)

### Schritt 1: GitHub Account
1. https://github.com → kostenlosen Account erstellen

### Schritt 2: Diesen Ordner hochladen
1. https://github.com/new → Neues Repository: "algotrader-pro"
2. "uploading an existing file" klicken
3. ALLE Dateien aus diesem Ordner hochladen
4. "Commit changes" klicken

### Schritt 3: Railway verbinden
1. https://railway.app → "Start a New Project"
2. "Deploy from GitHub repo" → dein Repository auswählen
3. Railway erkennt Python automatisch
4. Umgebungsvariable setzen:
   - Key: FINNHUB_KEY
   - Value: d6s6mg1r01qqlgbk3hhgd6s6mg1r01qqlgbk3hi0
5. Deploy klicken!

### Schritt 4: Website öffnen
Railway gibt dir eine URL wie:
https://algotrader-pro-production.up.railway.app

Diese URL im Browser öffnen = dein Live-Dashboard!

## Was die KI macht
Nach jedem Trade lernt der Bot:
- Welche Strategie den Trade ausgelöst hat
- Ob der Trade profitabel war
- Gewichte werden angepasst (gute Strategien → höheres Gewicht)
- Lernrate sinkt über Zeit (stabiler mit mehr Erfahrung)

## Finnhub API Key
Key: d6s6mg1r01qqlgbk3hhgd6s6mg1r01qqlgbk3hi0
Kostenloser Plan: 60 API calls/minute, WebSocket inklusive
