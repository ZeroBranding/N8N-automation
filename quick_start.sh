#!/bin/bash

# 🚀 Quick Start Script für komplette Social Media & E-Mail Automation
# Führt das komplette Setup automatisch durch

echo "🎬 Komplette kostenlose Social Media & E-Mail Automation"
echo "=================================================="
echo ""

# Farben für bessere Lesbarkeit
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktion zum Anzeigen von Status
print_status() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Schritt 1: Python prüfen
print_status "Prüfe Python Installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION gefunden"
else
    print_error "Python 3 nicht gefunden. Bitte installieren Sie Python 3.8+"
    exit 1
fi

# Schritt 2: Setup ausführen
print_status "Führe automatisches Setup aus..."
if [ -f "setup_complete.py" ]; then
    python3 setup_complete.py
    if [ $? -eq 0 ]; then
        print_success "Setup erfolgreich abgeschlossen"
    else
        print_error "Setup fehlgeschlagen"
        exit 1
    fi
else
    print_error "setup_complete.py nicht gefunden"
    exit 1
fi

# Schritt 3: .env Datei prüfen
print_status "Prüfe .env Konfiguration..."
if [ -f ".env" ]; then
    print_success ".env Datei gefunden"
    
    # Prüfe ob API-Keys eingetragen sind
    if grep -q "your_" .env; then
        print_warning "API-Keys müssen noch in .env eingetragen werden"
        echo ""
        echo "📋 Bitte füllen Sie die .env Datei aus:"
        echo "   nano .env"
        echo ""
        echo "🔑 Kostenlose API-Keys bekommen Sie hier:"
        echo "   - ElevenLabs: https://elevenlabs.io/"
        echo "   - D-ID: https://www.d-id.com/"
        echo "   - Unsplash: https://unsplash.com/developers"
        echo "   - Remove.bg: https://www.remove.bg/api"
        echo "   - Cloudinary: https://cloudinary.com/"
        echo ""
        echo "🤖 Telegram Bot erstellen:"
        echo "   - Gehen Sie zu: https://t.me/botfather"
        echo "   - Senden Sie: /newbot"
        echo ""
        read -p "Drücken Sie Enter, wenn Sie die .env Datei ausgefüllt haben..."
    else
        print_success "API-Keys sind bereits konfiguriert"
    fi
else
    print_error ".env Datei nicht gefunden"
    exit 1
fi

# Schritt 4: API starten
print_status "Starte Web Automation API..."
if [ -f "start.sh" ]; then
    chmod +x start.sh
    ./start.sh &
    API_PID=$!
    
    # Warten bis API läuft
    sleep 5
    
    # API Status prüfen
    if curl -s http://localhost:5000/health > /dev/null; then
        print_success "API läuft auf http://localhost:5000"
    else
        print_error "API konnte nicht gestartet werden"
        exit 1
    fi
else
    print_error "start.sh nicht gefunden"
    exit 1
fi

# Schritt 5: n8n Installation prüfen
print_status "Prüfe n8n Installation..."
if command -v n8n &> /dev/null; then
    print_success "n8n ist installiert"
else
    print_warning "n8n ist nicht installiert"
    echo ""
    echo "🔧 n8n Installation:"
    echo "   npm install n8n -g"
    echo ""
    echo "   Oder mit Docker:"
    echo "   docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n"
    echo ""
    read -p "Drücken Sie Enter, wenn n8n installiert ist..."
fi

# Schritt 6: n8n starten
print_status "Starte n8n..."
if command -v n8n &> /dev/null; then
    echo ""
    echo "🚀 n8n wird gestartet..."
    echo "   n8n ist verfügbar unter: http://localhost:5678"
    echo ""
    echo "📥 Workflow importieren:"
    echo "   1. Öffnen Sie http://localhost:5678"
    echo "   2. Klicken Sie auf 'Import from file'"
    echo "   3. Wählen Sie: n8n_complete_free_template.json"
    echo ""
    echo "🤖 Telegram Bot konfigurieren:"
    echo "   1. Öffnen Sie den Telegram Trigger Node"
    echo "   2. Bot Token eingeben"
    echo "   3. Webhook URL kopieren"
    echo "   4. Bei BotFather registrieren: /setwebhook"
    echo ""
    
    # n8n im Hintergrund starten
    n8n start > n8n.log 2>&1 &
    N8N_PID=$!
    
    print_success "n8n gestartet (PID: $N8N_PID)"
else
    print_error "n8n konnte nicht gestartet werden"
fi

# Schritt 7: Finale Anweisungen
echo ""
echo "🎉 Setup abgeschlossen!"
echo "======================"
echo ""
echo "📋 Verfügbare Services:"
echo "   - Web API: http://localhost:5000"
echo "   - n8n: http://localhost:5678"
echo ""
echo "📱 Telegram Bot Befehle:"
echo "   /start - Willkommensnachricht"
echo "   /video [text] - Video mit Avatar generieren"
echo "   /photo [text] - Foto erstellen"
echo "   /upload_instagram [caption] - Zu Instagram hochladen"
echo "   /upload_tiktok [caption] - Zu TikTok hochladen"
echo "   /upload_youtube [title] [description] - Zu YouTube hochladen"
echo "   /email_setup [email] [password] - E-Mail einrichten"
echo "   /email_read - E-Mails lesen"
echo ""
echo "🔧 Nützliche Befehle:"
echo "   # API Status prüfen"
echo "   curl http://localhost:5000/health"
echo ""
echo "   # n8n Status prüfen"
echo "   curl http://localhost:5678/healthz"
echo ""
echo "   # Logs anzeigen"
echo "   tail -f n8n.log"
echo ""
echo "   # Services stoppen"
echo "   kill $API_PID $N8N_PID"
echo ""
echo "📚 Weitere Informationen:"
echo "   - SETUP_GUIDE.md - Detaillierte Anleitung"
echo "   - TELEGRAM_SETUP.md - Telegram Bot Setup"
echo "   - FREE_APIS_GUIDE.md - Kostenlose APIs"
echo ""
echo "🎯 Testen Sie jetzt Ihren Bot!"
echo "   Gehen Sie zu: https://t.me/your_bot_name"
echo "   Senden Sie: /start"
echo ""

# PIDs speichern für späteres Stoppen
echo $API_PID > .api_pid
echo $N8N_PID > .n8n_pid

print_success "Setup vollständig abgeschlossen! 🚀"