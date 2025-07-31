# 🎬 Komplette kostenlose Social Media & E-Mail Automation

Eine vollständige Lösung für n8n mit kostenlosen Tools für Video-Generierung, Foto-Erstellung, Social Media Uploads und E-Mail-Automatisierung - **alles ohne API-Keys, nur mit normalen Login-Daten!**

## 🎯 Was Sie bekommen

### 📹 **Video & Foto Generation**
- **Avatar Videos**: Mit D-ID (20 Credits/Monat kostenlos)
- **Text zu Sprache**: Mit ElevenLabs (10.000 Zeichen/Monat kostenlos)
- **Fotos erstellen**: Mit Unsplash (50 Requests/Stunde kostenlos)
- **Hintergrund entfernen**: Mit Remove.bg (50 Bilder/Monat kostenlos)

### 📤 **Social Media Uploads**
- **Instagram**: Fotos/Videos mit Caption hochladen
- **TikTok**: Videos mit Caption hochladen
- **YouTube**: Videos mit Titel und Beschreibung hochladen
- **Keine API-Keys**: Nur normale Login-Daten erforderlich

### 📧 **E-Mail Automation**
- **E-Mails lesen**: IMAP Integration
- **E-Mails senden**: SMTP Integration
- **Auto-Antworten**: Basierend auf Keywords
- **Anhänge**: Bilder und Videos anhängen

### 🤖 **Telegram Bot Integration**
- **Einfache Befehle**: `/video`, `/photo`, `/upload_instagram`, etc.
- **Sofortige Antworten**: Direkt in Telegram
- **Automatische Verarbeitung**: Vollständig automatisiert

## 🆓 **Alle Tools sind kostenlos!**

| Service | Kostenlos | Link |
|---------|-----------|------|
| ElevenLabs | 10.000 Zeichen/Monat | https://elevenlabs.io/ |
| D-ID | 20 Credits/Monat | https://www.d-id.com/ |
| Unsplash | 50 Requests/Stunde | https://unsplash.com/developers |
| Remove.bg | 50 Bilder/Monat | https://www.remove.bg/api |
| Cloudinary | 25 Credits/Monat | https://cloudinary.com/ |

## 🚀 **Schnellstart**

### 1. Setup ausführen
```bash
python3 setup_complete.py
```

### 2. Kostenlose API-Keys besorgen
- ElevenLabs: https://elevenlabs.io/
- D-ID: https://www.d-id.com/
- Unsplash: https://unsplash.com/developers
- Remove.bg: https://www.remove.bg/api
- Cloudinary: https://cloudinary.com/

### 3. API-Keys in .env eintragen
```bash
nano .env
```

### 4. Telegram Bot erstellen
- Gehen Sie zu https://t.me/botfather
- Erstellen Sie einen neuen Bot
- Token in .env eintragen

### 5. API starten
```bash
./start.sh
```

### 6. n8n Workflow importieren
Importieren Sie `n8n_complete_free_template.json` in n8n.

## 📋 **Verfügbare Telegram Befehle**

### 🎬 Video & Foto Generation
```
/video Hallo Welt! Das ist ein automatisch generiertes Video.
/photo Natur Landschaft
/avatar Mein Avatar
```

### 📤 Social Media Uploads
```
/upload_instagram Mein tolles Video mit Caption
/upload_tiktok TikTok Video mit Hashtags
/upload_youtube Mein YouTube Video Das ist die Beschreibung
```

### 📧 E-Mail Automation
```
/email_setup email@example.com password
/email_read
/email_send recipient@example.com Betreff Nachrichtentext
/email_auto_reply support,help Hallo {sender_name}, danke für Ihre Nachricht zu {original_subject}
```

## 🔧 **Technische Details**

### Architektur
```
Telegram Bot → n8n Workflow → HTTP API → Web Automation → Social Media/E-Mail
```

### Komponenten
- **web_automation_extended.py**: Erweiterte API mit allen Funktionen
- **n8n_complete_free_template.json**: Kompletter n8n Workflow
- **setup_complete.py**: Automatisches Setup-Skript
- **config.py**: Sichere Credential-Verwaltung

### API Endpoints
- `POST /login` - Login zu Social Media Plattformen
- `POST /upload` - Upload zu Social Media
- `POST /email/setup` - E-Mail Setup
- `GET /email/read` - E-Mails lesen
- `POST /email/send` - E-Mail senden
- `POST /email/auto-reply` - Auto-Antworten
- `POST /logout` - Logout
- `GET /health` - Health Check

## 🔒 **Sicherheit**

- **Verschlüsselte Speicherung**: Login-Daten werden mit Fernet verschlüsselt
- **Session-Management**: Automatisches Logout nach Verwendung
- **Headless Mode**: Browser läuft im Hintergrund
- **Keine API-Keys für Social Media**: Nur normale Login-Daten
- **Kostenlose APIs**: Alle Tools bieten kostenlose Tiers

## 📖 **Beispiel Workflow**

### 1. Video generieren und hochladen
```
/video Hallo Welt! → Text zu Sprache → Avatar Video → Instagram Upload
```

### 2. Foto erstellen und teilen
```
/photo Natur → Unsplash API → Hintergrund entfernen → TikTok Upload
```

### 3. E-Mail Automation
```
/email_setup → E-Mails lesen → Auto-Antworten → Benachrichtigung
```

## 🛠️ **Installation**

### Voraussetzungen
- Python 3.8+
- Google Chrome
- n8n (optional, für Workflow-Integration)
- Telegram Bot (kostenlos)

### Automatische Installation
```bash
# Repository klonen
git clone <repository-url>
cd N8N-automation

# Setup ausführen
python3 setup_complete.py
```

### Manuelle Installation
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Chrome Driver installieren (Linux)
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip -d /tmp/
sudo mv /tmp/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

## 🔧 **Konfiguration**

### .env Datei Beispiel
```env
# Kostenlose API-Keys
ELEVENLABS_API_KEY=your_key_here
DID_API_KEY=your_key_here
UNSPLASH_API_KEY=your_key_here
REMOVEBG_API_KEY=your_key_here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Social Media Login-Daten (normale Login-Daten)
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
TIKTOK_USERNAME=your_username
TIKTOK_PASSWORD=your_password
YOUTUBE_EMAIL=your_email
YOUTUBE_PASSWORD=your_password

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token

# E-Mail
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Login-Daten speichern
```python
from config import ConfigManager

config = ConfigManager()
config.save_credentials("instagram", "ihr_username", "ihr_password")
config.save_credentials("tiktok", "ihr_username", "ihr_password")
config.save_credentials("youtube", "ihr_email", "ihr_password")
```

## 🐛 **Troubleshooting**

### Häufige Probleme

**Chrome Driver Fehler**
```bash
# Chrome Driver neu installieren
sudo rm /usr/local/bin/chromedriver
# Dann setup_complete.py erneut ausführen
```

**API-Keys nicht funktionieren**
- Überprüfen Sie die kostenlosen Limits
- Stellen Sie sicher, dass die Keys korrekt sind
- Prüfen Sie die .env Datei

**Telegram Bot nicht erreichbar**
- Überprüfen Sie den Bot Token
- Stellen Sie sicher, dass der Bot aktiv ist
- Testen Sie mit `/start`

**E-Mail Setup Fehler**
- Verwenden Sie App-Passwörter für Gmail
- Aktivieren Sie 2FA und erstellen Sie ein App-Passwort
- Überprüfen Sie IMAP/SMTP Einstellungen

## 📝 **Logs**

Logs werden automatisch in der Konsole ausgegeben:
```
INFO:__main__:Chrome Driver erfolgreich gestartet
INFO:__main__:Instagram Login erfolgreich
INFO:__main__:Video erfolgreich generiert
INFO:__main__:Upload zu Instagram erfolgreich
INFO:__main__:E-Mail erfolgreich gesendet
```

## 📚 **Weitere Informationen**

- **TELEGRAM_SETUP.md**: Detaillierte Telegram Bot Anleitung
- **FREE_APIS_GUIDE.md**: Kostenlose APIs Setup Guide
- **config.example.txt**: Konfigurationsbeispiele

## 🤝 **Beitragen**

1. Fork erstellen
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📄 **Lizenz**

Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE` Datei für Details.

## ⚠️ **Haftungsausschluss**

Diese Software ist für Bildungs- und Entwicklungszwecke gedacht. Bitte beachten Sie die Nutzungsbedingungen der jeweiligen Plattformen. Die Verwendung von Web Scraping kann gegen die Terms of Service verstoßen.

## 🆘 **Support**

Bei Problemen oder Fragen:
1. Issues auf GitHub erstellen
2. Logs bereitstellen
3. System-Informationen angeben (OS, Python-Version, etc.)
4. Überprüfen Sie die kostenlosen API-Limits

## 🎉 **Fazit**

Sie haben jetzt eine **komplette kostenlose Automation-Lösung** mit:
- ✅ Video-Generierung mit Avatar
- ✅ Foto-Erstellung und Bearbeitung
- ✅ Social Media Uploads (Instagram, TikTok, YouTube)
- ✅ E-Mail-Automatisierung
- ✅ Telegram Bot Integration
- ✅ Alles ohne API-Keys für Social Media
- ✅ Alle Tools kostenlos verfügbar
- ✅ Einfache n8n Integration

**Starten Sie jetzt und automatisieren Sie Ihre Social Media Präsenz!** 🚀