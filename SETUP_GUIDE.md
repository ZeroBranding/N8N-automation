# 🚀 Komplettes Setup Guide - Schritt für Schritt

## 📋 Voraussetzungen
- Linux/Mac/Windows mit Python 3.8+
- n8n installiert (kostenlos)
- Google Chrome Browser

---

## 🔧 Schritt 1: Repository Setup

```bash
# 1. Repository klonen oder Dateien herunterladen
cd /workspace

# 2. Überprüfen Sie, dass alle Dateien vorhanden sind
ls -la
```

**Erwartete Dateien:**
- `web_automation_extended.py`
- `n8n_complete_free_template.json`
- `setup_complete.py`
- `requirements.txt`
- `config.py`

---

## 🐍 Schritt 2: Python Setup

```bash
# 1. Python-Version prüfen
python3 --version

# 2. Falls Python 3.8+ nicht installiert ist:
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip

# macOS:
brew install python3

# Windows:
# Laden Sie Python von python.org herunter
```

---

## ⚙️ Schritt 3: Automatisches Setup ausführen

```bash
# 1. Setup-Skript ausführen
python3 setup_complete.py
```

**Was passiert:**
- ✅ Python-Abhängigkeiten werden installiert
- ✅ Chrome und Chrome Driver werden installiert
- ✅ .env Datei wird erstellt
- ✅ Start-Skript wird erstellt
- ✅ Anleitungen werden erstellt

---

## 🔑 Schritt 4: Kostenlose API-Keys besorgen

### 4.1 ElevenLabs (Text zu Sprache)
```bash
# 1. Gehen Sie zu: https://elevenlabs.io/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 4.2 D-ID (Avatar Videos)
```bash
# 1. Gehen Sie zu: https://www.d-id.com/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 4.3 Unsplash (Fotos)
```bash
# 1. Gehen Sie zu: https://unsplash.com/developers
# 2. Registrieren Sie sich als Developer
# 3. Erstellen Sie eine neue App
# 4. Kopieren Sie den Access Key
```

### 4.4 Remove.bg (Hintergrund entfernen)
```bash
# 1. Gehen Sie zu: https://www.remove.bg/api
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 4.5 Cloudinary (Bild/Video Hosting)
```bash
# 1. Gehen Sie zu: https://cloudinary.com/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu Dashboard
# 4. Kopieren Sie Cloud Name, API Key und Secret
```

---

## 📝 Schritt 5: .env Datei konfigurieren

```bash
# 1. .env Datei öffnen
nano .env

# 2. Alle API-Keys eintragen:
```

```env
# Kostenlose API-Keys
ELEVENLABS_API_KEY=your_elevenlabs_key_here
DID_API_KEY=your_did_key_here
UNSPLASH_API_KEY=your_unsplash_key_here
REMOVEBG_API_KEY=your_removebg_key_here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# Social Media Login-Daten (normale Login-Daten)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
TIKTOK_USERNAME=your_tiktok_username
TIKTOK_PASSWORD=your_tiktok_password
YOUTUBE_EMAIL=your_youtube_email
YOUTUBE_PASSWORD=your_youtube_password

# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# E-Mail Login-Daten
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

```bash
# 3. Speichern und schließen (Ctrl+X, Y, Enter)
```

---

## 🤖 Schritt 6: Telegram Bot erstellen

```bash
# 1. Gehen Sie zu: https://t.me/botfather
# 2. Senden Sie: /newbot
# 3. Folgen Sie den Anweisungen:
#    - Bot Name eingeben
#    - Bot Username eingeben (muss mit 'bot' enden)
# 4. Kopieren Sie den Bot Token
# 5. Token in .env Datei eintragen
```

**Beispiel:**
```
Bot Name: My Automation Bot
Bot Username: my_automation_bot
Bot Token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

---

## 📧 Schritt 7: Gmail App-Passwort erstellen (für E-Mail)

```bash
# 1. Gehen Sie zu: https://myaccount.google.com/
# 2. Sicherheit → 2-Schritt-Verifizierung aktivieren
# 3. App-Passwörter → App auswählen → Andere
# 4. Name eingeben: "n8n Automation"
# 5. App-Passwort kopieren
# 6. In .env Datei eintragen
```

---

## 🚀 Schritt 8: API starten

```bash
# 1. API starten
./start.sh

# 2. Überprüfen Sie, dass die API läuft
curl http://localhost:5000/health
```

**Erwartete Ausgabe:**
```json
{"status": "healthy", "message": "Extended Web Automation API läuft"}
```

---

## 🔧 Schritt 9: n8n installieren und starten

### 9.1 n8n installieren
```bash
# Option 1: Mit npm (empfohlen)
npm install n8n -g

# Option 2: Mit Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Option 3: Mit Docker Compose
wget https://raw.githubusercontent.com/n8n-io/n8n/master/docker/compose/withPostgres/package.json
docker-compose up -d
```

### 9.2 n8n starten
```bash
# n8n starten
n8n

# Oder im Hintergrund
n8n start
```

**n8n ist dann verfügbar unter:** http://localhost:5678

---

## 📥 Schritt 10: n8n Workflow importieren

### 10.1 n8n öffnen
```bash
# 1. Browser öffnen
# 2. Gehen Sie zu: http://localhost:5678
# 3. Erstellen Sie ein Konto oder melden Sie sich an
```

### 10.2 Workflow importieren
```bash
# 1. Klicken Sie auf "Import from file"
# 2. Wählen Sie: n8n_complete_free_template.json
# 3. Klicken Sie auf "Import"
```

### 10.3 Workflow konfigurieren
```bash
# 1. Telegram Trigger Node öffnen
# 2. Bot Token eingeben (aus .env Datei)
# 3. Webhook URL kopieren
# 4. Webhook URL bei BotFather registrieren
```

---

## 🔗 Schritt 11: Telegram Webhook registrieren

```bash
# 1. Webhook URL aus n8n kopieren
# Beispiel: https://your-domain.com/webhook/telegram-bot

# 2. Bei BotFather registrieren:
# Gehen Sie zu: https://t.me/botfather
# Senden Sie: /setwebhook
# URL eingeben: https://your-domain.com/webhook/telegram-bot
```

---

## ✅ Schritt 12: Testen

### 12.1 Telegram Bot testen
```bash
# 1. Gehen Sie zu Ihrem Bot: https://t.me/your_bot_name
# 2. Senden Sie: /start
# 3. Sie sollten eine Willkommensnachricht erhalten
```

### 12.2 Video generieren testen
```bash
# 1. Senden Sie: /video Hallo Welt!
# 2. Warten Sie auf die Verarbeitung
# 3. Sie sollten ein Video erhalten
```

### 12.3 Foto erstellen testen
```bash
# 1. Senden Sie: /photo Natur
# 2. Sie sollten ein Foto erhalten
```

---

## 🔧 Schritt 13: Troubleshooting

### Häufige Probleme:

**1. API startet nicht**
```bash
# Port prüfen
netstat -tlnp | grep 5000

# Falls Port belegt:
sudo lsof -i :5000
sudo kill -9 <PID>
```

**2. Chrome Driver Fehler**
```bash
# Chrome Driver neu installieren
sudo rm /usr/local/bin/chromedriver
python3 setup_complete.py
```

**3. n8n nicht erreichbar**
```bash
# Port prüfen
netstat -tlnp | grep 5678

# n8n neu starten
n8n start
```

**4. Telegram Bot nicht erreichbar**
```bash
# Bot Token prüfen
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# Webhook Status prüfen
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

---

## 📋 Schritt 14: Vollständige Konfiguration

### 14.1 Alle Umgebungsvariablen prüfen
```bash
# .env Datei überprüfen
cat .env

# Alle Variablen sollten ausgefüllt sein:
# - API Keys (alle 5 Services)
# - Social Media Login-Daten
# - Telegram Bot Token
# - E-Mail Login-Daten
```

### 14.2 Services testen
```bash
# 1. API Health Check
curl http://localhost:5000/health

# 2. n8n Health Check
curl http://localhost:5678/healthz

# 3. Telegram Bot Test
# Senden Sie /start an Ihren Bot
```

---

## 🎉 Schritt 15: Vollständiger Test

### 15.1 Kompletter Workflow Test
```bash
# 1. Video generieren und hochladen
/video Test Video für Instagram

# 2. Foto erstellen
/photo Landschaft

# 3. E-Mail Setup
/email_setup your_email@gmail.com your_app_password

# 4. E-Mails lesen
/email_read
```

### 15.2 Erwartete Ergebnisse:
- ✅ Video wird generiert und an Telegram gesendet
- ✅ Foto wird erstellt und an Telegram gesendet
- ✅ E-Mail Setup erfolgreich
- ✅ E-Mails werden gelesen und angezeigt

---

## 📚 Nächste Schritte

### Automatisierung erweitern:
```bash
# 1. Weitere Social Media Plattformen hinzufügen
# 2. E-Mail Auto-Antworten konfigurieren
# 3. Zeitgesteuerte Automatisierungen erstellen
# 4. Benutzerdefinierte Befehle hinzufügen
```

### Monitoring:
```bash
# 1. Logs überwachen
tail -f /var/log/automation.log

# 2. API Status prüfen
curl http://localhost:5000/health

# 3. n8n Workflows überwachen
# Gehen Sie zu: http://localhost:5678
```

---

## 🆘 Support

### Bei Problemen:
1. **Logs prüfen**: `tail -f /var/log/automation.log`
2. **API Status**: `curl http://localhost:5000/health`
3. **n8n Status**: `curl http://localhost:5678/healthz`
4. **Telegram Bot**: Testen Sie mit `/start`

### Nützliche Befehle:
```bash
# Alle Services neu starten
./start.sh

# n8n neu starten
n8n start

# API neu starten
python3 web_automation_extended.py

# Logs anzeigen
tail -f /var/log/automation.log
```

---

## 🎯 Zusammenfassung

Nach diesem Setup haben Sie:
- ✅ Komplette kostenlose Automation
- ✅ Video & Foto Generation
- ✅ Social Media Uploads (ohne API-Keys)
- ✅ E-Mail Automation
- ✅ Telegram Bot Integration
- ✅ n8n Workflow Integration

**Ihre Automation ist jetzt vollständig einsatzbereit!** 🚀