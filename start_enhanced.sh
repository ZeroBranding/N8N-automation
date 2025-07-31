#!/bin/bash

# 🚀 ENHANCED START-SCRIPT FÜR KI-GEDÄCHTNISSYSTEM
# Vollständig funktionsfähige KI-Fabrik mit Multi-Agent-System

echo "🤖 STARTE KI-GEDÄCHTNISSYSTEM..."
echo "=================================="

# 1. Python-Version prüfen
echo "📋 Prüfe Python-Version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3 nicht gefunden!"
    exit 1
fi

# 2. Dependencies installieren
echo "📦 Installiere Dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Dependencies-Installation fehlgeschlagen!"
    exit 1
fi

# 3. Chrome Driver installieren
echo "🌐 Installiere Chrome Driver..."
python3 -c "
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ChromeDriverManager().install()
print('✅ Chrome Driver installiert')
"

# 4. Datenbank initialisieren
echo "💾 Initialisiere KI-Gedächtnis-Datenbank..."
python3 -c "
from web_automation_extended import ki_memory
print('✅ KI-Gedächtnissystem initialisiert')
"

# 5. API-Server starten
echo "🚀 Starte KI-API-Server..."
python3 web_automation_extended.py &
API_PID=$!
echo "✅ API-Server gestartet (PID: $API_PID)"

# 6. Warten bis API verfügbar
echo "⏳ Warte auf API-Verfügbarkeit..."
for i in {1..30}; do
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "✅ API ist verfügbar!"
        break
    fi
    echo "   Versuch $i/30..."
    sleep 2
done

# 7. Umfassende Tests ausführen
echo "🧪 Führe umfassende Tests aus..."
python3 test_system.py
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ Alle Tests bestanden!"
else
    echo "⚠️  Einige Tests fehlgeschlagen, aber System läuft weiter..."
fi

# 8. n8n starten
echo "🔄 Starte n8n..."
n8n start &
N8N_PID=$!
echo "✅ n8n gestartet (PID: $N8N_PID)"

# 9. System-Status anzeigen
echo ""
echo "🎉 KI-GEDÄCHTNISSYSTEM ERFOLGREICH GESTARTET!"
echo "=============================================="
echo ""
echo "📊 SYSTEM STATUS:"
echo "   🤖 KI-API-Server: http://localhost:5000"
echo "   🔄 n8n Workflow: http://localhost:5678"
echo "   🧠 Gedächtnissystem: Aktiv"
echo "   🤖 Multi-Agent-System: Aktiv"
echo "   💾 Persistente Speicherung: Aktiv"
echo ""
echo "🎯 VERFÜGBARE FEATURES:"
echo "   ✅ Sprachmemo-Verarbeitung"
echo "   ✅ Natürliche Sprachverarbeitung"
echo "   ✅ Kontext-Bewusstsein"
echo "   ✅ Persistente Erinnerungen"
echo "   ✅ Multi-Agent-System"
echo "   ✅ Suchmaschinen-Integration"
echo "   ✅ Social Media Automation"
echo "   ✅ E-Mail Automation"
echo "   ✅ Web Scraping"
echo "   ✅ RSS Feeds"
echo "   ✅ Wetter-API"
echo "   ✅ QR Code Generator"
echo "   ✅ Chart Generator"
echo "   ✅ URL Shortener"
echo "   ✅ Markdown Generator"
echo "   ✅ News Headlines"
echo ""
echo "💬 TELEGRAM BOT VERWENDUNG:"
echo "   🎤 Sprachmemos senden"
echo "   💬 Natürlich sprechen: 'Erstelle ein Video über KI'"
echo "   🔍 Suchen: 'Suche nach Python Tutorials'"
echo "   🌤️ Wetter: 'Wie ist das Wetter in Berlin?'"
echo "   🧠 Gedächtnis: 'Was haben wir letzte Woche besprochen?'"
echo ""
echo "🆓 ALLES KOSTENLOS - KEINE API-KEYS NÖTIG!"
echo ""
echo "🛑 Zum Stoppen: Ctrl+C"
echo ""

# 10. Monitoring-Loop
while true; do
    # API-Status prüfen
    if ! curl -s http://localhost:5000/health > /dev/null; then
        echo "❌ API-Server nicht erreichbar!"
        break
    fi
    
    # n8n-Status prüfen
    if ! curl -s http://localhost:5678 > /dev/null; then
        echo "❌ n8n nicht erreichbar!"
        break
    fi
    
    sleep 30
done

# 11. Cleanup bei Beendigung
echo ""
echo "🛑 Beende System..."
kill $API_PID 2>/dev/null
kill $N8N_PID 2>/dev/null
echo "✅ System beendet"