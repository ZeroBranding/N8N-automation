#!/usr/bin/env python3
"""
Setup-Skript für Social Media Automation
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

def create_config():
    """Erstellt eine Beispiel-Konfiguration"""
    config_content = """# Social Media Automation Konfiguration
# Diese Datei enthält Ihre Login-Daten (verschlüsselt)

# Beispiel für die Verwendung:
# python config.py
# 
# Dann in der Python-Konsole:
# from config import ConfigManager
# config = ConfigManager()
# config.save_credentials("instagram", "ihr_username", "ihr_password")
# config.save_credentials("tiktok", "ihr_username", "ihr_password")
"""
    
    with open("config.example.txt", "w") as f:
        f.write(config_content)
    
    print("✅ Beispiel-Konfiguration erstellt")

def create_start_script():
    """Erstellt ein Start-Skript"""
    script_content = """#!/bin/bash
# Start-Skript für Social Media Automation

echo "🚀 Starte Social Media Automation API..."
echo "📡 API läuft auf: http://localhost:5000"
echo "📋 Verfügbare Endpoints:"
echo "   - POST /login - Login zu Social Media Plattformen"
echo "   - GET /posts - Posts/Videos abrufen"
echo "   - POST /logout - Logout"
echo "   - GET /health - Health Check"
echo ""
echo "💡 Tipp: Importieren Sie die n8n_workflow.json in n8n"
echo ""

python3 web_automation.py
"""
    
    with open("start.sh", "w") as f:
        f.write(script_content)
    
    # Ausführbar machen
    os.chmod("start.sh", 0o755)
    print("✅ Start-Skript erstellt")

def main():
    """Hauptfunktion für das Setup"""
    print("🔧 Social Media Automation Setup")
    print("=" * 40)
    
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
    
    # Start-Skript erstellen
    create_start_script()
    
    print("\n🎉 Setup erfolgreich abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. Konfigurieren Sie Ihre Login-Daten:")
    print("   python3 config.py")
    print("2. Starten Sie die API:")
    print("   ./start.sh")
    print("3. Importieren Sie den n8n Workflow:")
    print("   n8n_workflow.json")
    print("\n🔗 API wird auf http://localhost:5000 verfügbar sein")

if __name__ == "__main__":
    main()