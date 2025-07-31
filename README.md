# Social Media Automation ohne API-Keys

Eine einfache Lösung für n8n, die normale Login-Daten anstatt API-Keys verwendet, um mit Social Media Plattformen wie Instagram und TikTok zu arbeiten.

## 🎯 Problem gelöst

- **Keine API-Keys erforderlich**: Verwenden Sie Ihre normalen Login-Daten
- **Einfache Integration**: Direkte Anbindung an n8n über HTTP-API
- **Sichere Speicherung**: Login-Daten werden verschlüsselt gespeichert
- **Web Scraping**: Funktioniert auch ohne offizielle APIs

## 🚀 Schnellstart

### 1. Setup ausführen
```bash
python3 setup.py
```

### 2. Login-Daten konfigurieren
```bash
python3 -c "
from config import ConfigManager
config = ConfigManager()
config.save_credentials('instagram', 'ihr_username', 'ihr_password')
config.save_credentials('tiktok', 'ihr_username', 'ihr_password')
"
```

### 3. API starten
```bash
./start.sh
```

### 4. n8n Workflow importieren
Importieren Sie die `n8n_workflow.json` Datei in n8n.

## 📋 Features

### Unterstützte Plattformen
- ✅ Instagram
- ✅ TikTok
- 🔄 Weitere Plattformen können einfach hinzugefügt werden

### Verfügbare Aktionen
- **Login**: Anmeldung mit normalen Credentials
- **Posts abrufen**: Bilder/Videos von Profilen holen
- **Daten verarbeiten**: Strukturierte Ausgabe für n8n
- **Automatischer Logout**: Sichere Session-Verwaltung

## 🔧 Technische Details

### Architektur
```
n8n Workflow → HTTP API → Web Automation → Social Media Plattformen
```

### Komponenten
- **web_automation.py**: Haupt-API mit Selenium WebDriver
- **config.py**: Sichere Credential-Verwaltung
- **n8n_workflow.json**: Fertiger n8n Workflow
- **setup.py**: Automatisches Setup-Skript

### API Endpoints
- `POST /login` - Login zu Social Media Plattformen
- `GET /posts` - Posts/Videos abrufen
- `POST /logout` - Logout und Session beenden
- `GET /health` - Health Check

## 🔒 Sicherheit

- **Verschlüsselte Speicherung**: Login-Daten werden mit Fernet verschlüsselt
- **Session-Management**: Automatisches Logout nach Verwendung
- **Headless Mode**: Browser läuft im Hintergrund
- **Keine API-Keys**: Keine sensiblen API-Schlüssel erforderlich

## 📖 Verwendung

### Beispiel: Instagram Posts abrufen
```python
import requests

# Login
login_response = requests.post('http://localhost:5000/login', json={
    'platform': 'instagram',
    'username': 'ihr_username',
    'password': 'ihr_password'
})

# Posts abrufen
posts_response = requests.get('http://localhost:5000/posts', params={
    'platform': 'instagram',
    'username': 'target_user',
    'count': 10
})

# Logout
requests.post('http://localhost:5000/logout')
```

### n8n Integration
1. Importieren Sie `n8n_workflow.json` in n8n
2. Passen Sie die Login-Daten im Workflow an
3. Workflow ausführen

## 🛠️ Installation

### Voraussetzungen
- Python 3.8+
- Google Chrome
- n8n (optional, für Workflow-Integration)

### Automatische Installation
```bash
# Repository klonen
git clone <repository-url>
cd N8N-automation

# Setup ausführen
python3 setup.py
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

## 🔧 Konfiguration

### Login-Daten speichern
```python
from config import ConfigManager

config = ConfigManager()
config.save_credentials("instagram", "ihr_username", "ihr_password")
config.save_credentials("tiktok", "ihr_username", "ihr_password")
```

### Login-Daten laden
```python
username, password = config.load_credentials("instagram")
```

### Plattformen auflisten
```python
platforms = config.list_platforms()
print(platforms)  # ['instagram', 'tiktok']
```

## 🐛 Troubleshooting

### Häufige Probleme

**Chrome Driver Fehler**
```bash
# Chrome Driver neu installieren
sudo rm /usr/local/bin/chromedriver
# Dann setup.py erneut ausführen
```

**Login Fehler**
- Überprüfen Sie Ihre Login-Daten
- Stellen Sie sicher, dass 2FA deaktiviert ist
- Versuchen Sie es mit einem anderen Browser-Profil

**API nicht erreichbar**
```bash
# Port prüfen
netstat -tlnp | grep 5000

# Firewall-Einstellungen prüfen
sudo ufw allow 5000
```

## 📝 Logs

Logs werden automatisch in der Konsole ausgegeben:
```
INFO:__main__:Chrome Driver erfolgreich gestartet
INFO:__main__:Instagram Login erfolgreich
INFO:__main__:10 Posts abgerufen
```

## 🤝 Beitragen

1. Fork erstellen
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE` Datei für Details.

## ⚠️ Haftungsausschluss

Diese Software ist für Bildungs- und Entwicklungszwecke gedacht. Bitte beachten Sie die Nutzungsbedingungen der jeweiligen Social Media Plattformen. Die Verwendung von Web Scraping kann gegen die Terms of Service verstoßen.

## 🆘 Support

Bei Problemen oder Fragen:
1. Issues auf GitHub erstellen
2. Logs bereitstellen
3. System-Informationen angeben (OS, Python-Version, etc.)