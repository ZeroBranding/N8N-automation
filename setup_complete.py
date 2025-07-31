#!/usr/bin/env python3
"""
Komplettes Setup-Skript für kostenlose Social Media & E-Mail Automation
Installiert alle Abhängigkeiten und konfiguriert die Umgebung
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Führt einen Befehl aus und zeigt den Status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} erfolgreich")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei {description}: {e}")
        print(f"Fehlerausgabe: {e.stderr}")
        return False

def check_python_version():
    """Prüft die Python-Version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 oder höher wird benötigt")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} gefunden")
    return True

def install_dependencies():
    """Installiert Python-Abhängigkeiten"""
    return run_command("pip install -r requirements.txt", "Python-Abhängigkeiten installieren")

def install_chrome_driver():
    """Installiert Chrome Driver"""
    system = platform.system().lower()
    
    if system == "linux":
        # Chrome installieren
        run_command("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -", 
                   "Google Chrome Signing Key hinzufügen")
        run_command("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list", 
                   "Chrome Repository hinzufügen")
        run_command("sudo apt-get update", "Paketliste aktualisieren")
        run_command("sudo apt-get install -y google-chrome-stable", "Google Chrome installieren")
        
        # Chrome Driver installieren
        run_command("wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip", 
                   "Chrome Driver herunterladen")
        run_command("unzip /tmp/chromedriver.zip -d /tmp/", "Chrome Driver entpacken")
        run_command("sudo mv /tmp/chromedriver /usr/local/bin/", "Chrome Driver installieren")
        run_command("sudo chmod +x /usr/local/bin/chromedriver", "Chrome Driver ausführbar machen")
        
    elif system == "darwin":  # macOS
        run_command("brew install --cask google-chrome", "Google Chrome installieren")
        run_command("brew install chromedriver", "Chrome Driver installieren")
        
    elif system == "windows":
        print("⚠️  Für Windows bitte Chrome und Chrome Driver manuell installieren")
        print("   Chrome: https://www.google.com/chrome/")
        print("   Chrome Driver: https://chromedriver.chromium.org/")
        return True
    
    return True

def create_env_file():
    """Erstellt eine .env Datei mit allen benötigten API-Keys"""
    env_content = """# Kostenlose API-Keys für Social Media Automation
# Alle diese Services bieten kostenlose Tiers an

# ElevenLabs - Text zu Sprache (kostenlos: 10.000 Zeichen/Monat)
# https://elevenlabs.io/
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# D-ID - Avatar Video Generation (kostenlos: 20 Credits/Monat)
# https://www.d-id.com/
DID_API_KEY=your_did_api_key_here

# Unsplash - Kostenlose Fotos (kostenlos: 50 Requests/Stunde)
# https://unsplash.com/developers
UNSPLASH_API_KEY=your_unsplash_api_key_here

# Remove.bg - Hintergrund entfernen (kostenlos: 50 Bilder/Monat)
# https://www.remove.bg/api
REMOVEBG_API_KEY=your_removebg_api_key_here

# Cloudinary - Bild/Video Hosting (kostenlos: 25 Credits/Monat)
# https://cloudinary.com/
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# Social Media Login-Daten (normale Login-Daten, keine API-Keys)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

TIKTOK_USERNAME=your_tiktok_username
TIKTOK_PASSWORD=your_tiktok_password

YOUTUBE_EMAIL=your_youtube_email
YOUTUBE_PASSWORD=your_youtube_password

# Telegram Bot Token
# https://t.me/botfather
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# E-Mail Login-Daten (für Gmail App-Passwort verwenden)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env Datei erstellt")
    print("⚠️  Bitte füllen Sie die API-Keys in der .env Datei aus")

def create_config():
    """Erstellt eine Beispiel-Konfiguration"""
    config_content = """# Komplette kostenlose Social Media & E-Mail Automation
# Diese Datei enthält Ihre Login-Daten (verschlüsselt)

# Beispiel für die Verwendung:
# python config.py
# 
# Dann in der Python-Konsole:
# from config import ConfigManager
# config = ConfigManager()
# config.save_credentials("instagram", "ihr_username", "ihr_password")
# config.save_credentials("tiktok", "ihr_username", "ihr_password")
# config.save_credentials("youtube", "ihr_email", "ihr_password")

# Kostenlose API-Keys bekommen Sie hier:
# - ElevenLabs: https://elevenlabs.io/ (10.000 Zeichen/Monat kostenlos)
# - D-ID: https://www.d-id.com/ (20 Credits/Monat kostenlos)
# - Unsplash: https://unsplash.com/developers (50 Requests/Stunde kostenlos)
# - Remove.bg: https://www.remove.bg/api (50 Bilder/Monat kostenlos)
# - Cloudinary: https://cloudinary.com/ (25 Credits/Monat kostenlos)
"""
    
    with open("config.example.txt", "w") as f:
        f.write(config_content)
    
    print("✅ Beispiel-Konfiguration erstellt")

def create_start_script():
    """Erstellt ein Start-Skript"""
    script_content = """#!/bin/bash
# Start-Skript für komplette kostenlose Social Media & E-Mail Automation

echo "🚀 Starte komplette kostenlose Automation API..."
echo "📡 API läuft auf: http://localhost:5000"
echo ""
echo "📋 Verfügbare Endpoints:"
echo "   - POST /login - Login zu Social Media Plattformen"
echo "   - POST /upload - Upload zu Social Media"
echo "   - POST /email/setup - E-Mail Setup"
echo "   - GET /email/read - E-Mails lesen"
echo "   - POST /email/send - E-Mail senden"
echo "   - POST /email/auto-reply - Auto-Antworten"
echo "   - POST /logout - Logout"
echo "   - GET /health - Health Check"
echo ""
echo "💡 Tipp: Importieren Sie die n8n_complete_free_template.json in n8n"
echo ""

python3 web_automation_extended.py
"""
    
    with open("start.sh", "w") as f:
        f.write(script_content)
    
    # Ausführbar machen
    os.chmod("start.sh", 0o755)
    print("✅ Start-Skript erstellt")

def create_telegram_bot_guide():
    """Erstellt eine Anleitung für Telegram Bot Setup"""
    guide_content = """# Telegram Bot Setup Anleitung

## 1. Bot erstellen
1. Gehen Sie zu https://t.me/botfather
2. Senden Sie `/newbot`
3. Folgen Sie den Anweisungen
4. Kopieren Sie den Bot Token

## 2. Bot Token in .env Datei eintragen
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## 3. Bot zu n8n hinzufügen
1. Öffnen Sie n8n
2. Erstellen Sie einen neuen Workflow
3. Fügen Sie einen "Telegram Trigger" Node hinzu
4. Konfigurieren Sie den Bot Token
5. Importieren Sie n8n_complete_free_template.json

## 4. Verfügbare Befehle
- `/start` - Willkommensnachricht
- `/video [text]` - Video mit Avatar generieren
- `/photo [text]` - Foto erstellen
- `/upload_instagram [caption]` - Zu Instagram hochladen
- `/upload_tiktok [caption]` - Zu TikTok hochladen
- `/upload_youtube [title] [description]` - Zu YouTube hochladen
- `/email_setup [email] [password]` - E-Mail einrichten
- `/email_read` - E-Mails lesen

## 5. Beispiel
```
/video Hallo Welt! Das ist ein automatisch generiertes Video.
```
"""
    
    with open("TELEGRAM_SETUP.md", "w") as f:
        f.write(guide_content)
    
    print("✅ Telegram Bot Setup Anleitung erstellt")

def create_free_apis_guide():
    """Erstellt eine Anleitung für kostenlose APIs"""
    guide_content = """# Kostenlose APIs Anleitung

## 🆓 Alle APIs sind kostenlos verfügbar!

### 1. ElevenLabs - Text zu Sprache
- **URL**: https://elevenlabs.io/
- **Kostenlos**: 10.000 Zeichen/Monat
- **Setup**: 
  1. Registrieren Sie sich
  2. Gehen Sie zu API Keys
  3. Kopieren Sie den API Key
  4. Fügen Sie ihn in .env ein

### 2. D-ID - Avatar Video Generation
- **URL**: https://www.d-id.com/
- **Kostenlos**: 20 Credits/Monat
- **Setup**:
  1. Registrieren Sie sich
  2. Gehen Sie zu API Keys
  3. Kopieren Sie den API Key
  4. Fügen Sie ihn in .env ein

### 3. Unsplash - Kostenlose Fotos
- **URL**: https://unsplash.com/developers
- **Kostenlos**: 50 Requests/Stunde
- **Setup**:
  1. Registrieren Sie sich als Developer
  2. Erstellen Sie eine App
  3. Kopieren Sie den Access Key
  4. Fügen Sie ihn in .env ein

### 4. Remove.bg - Hintergrund entfernen
- **URL**: https://www.remove.bg/api
- **Kostenlos**: 50 Bilder/Monat
- **Setup**:
  1. Registrieren Sie sich
  2. Gehen Sie zu API Keys
  3. Kopieren Sie den API Key
  4. Fügen Sie ihn in .env ein

### 5. Cloudinary - Bild/Video Hosting
- **URL**: https://cloudinary.com/
- **Kostenlos**: 25 Credits/Monat
- **Setup**:
  1. Registrieren Sie sich
  2. Gehen Sie zu Dashboard
  3. Kopieren Sie Cloud Name, API Key und Secret
  4. Fügen Sie sie in .env ein

## 🔑 .env Datei Beispiel
```
ELEVENLABS_API_KEY=your_key_here
DID_API_KEY=your_key_here
UNSPLASH_API_KEY=your_key_here
REMOVEBG_API_KEY=your_key_here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## ⚠️ Wichtige Hinweise
- Alle APIs bieten kostenlose Tiers an
- Keine Kreditkarte erforderlich
- Einfache Registrierung
- Sofort verfügbar
"""
    
    with open("FREE_APIS_GUIDE.md", "w") as f:
        f.write(guide_content)
    
    print("✅ Kostenlose APIs Anleitung erstellt")

def main():
    """Hauptfunktion für das Setup"""
    print("🔧 Komplette kostenlose Social Media & E-Mail Automation Setup")
    print("=" * 60)
    
    # Python-Version prüfen
    if not check_python_version():
        sys.exit(1)
    
    # Abhängigkeiten installieren
    if not install_dependencies():
        print("❌ Setup fehlgeschlagen - Abhängigkeiten konnten nicht installiert werden")
        sys.exit(1)
    
    # Chrome Driver installieren
    if not install_chrome_driver():
        print("❌ Setup fehlgeschlagen - Chrome Driver konnte nicht installiert werden")
        sys.exit(1)
    
    # Konfiguration erstellen
    create_config()
    create_env_file()
    create_start_script()
    create_telegram_bot_guide()
    create_free_apis_guide()
    
    print("\n🎉 Setup erfolgreich abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. Kostenlose API-Keys besorgen:")
    print("   - ElevenLabs: https://elevenlabs.io/")
    print("   - D-ID: https://www.d-id.com/")
    print("   - Unsplash: https://unsplash.com/developers")
    print("   - Remove.bg: https://www.remove.bg/api")
    print("   - Cloudinary: https://cloudinary.com/")
    print("")
    print("2. API-Keys in .env Datei eintragen")
    print("")
    print("3. Telegram Bot erstellen:")
    print("   - Gehen Sie zu https://t.me/botfather")
    print("   - Erstellen Sie einen neuen Bot")
    print("   - Token in .env eintragen")
    print("")
    print("4. API starten:")
    print("   ./start.sh")
    print("")
    print("5. n8n Workflow importieren:")
    print("   n8n_complete_free_template.json")
    print("")
    print("🔗 API wird auf http://localhost:5000 verfügbar sein")
    print("")
    print("📚 Weitere Informationen:")
    print("   - TELEGRAM_SETUP.md - Telegram Bot Setup")
    print("   - FREE_APIS_GUIDE.md - Kostenlose APIs Anleitung")

if __name__ == "__main__":
    main()