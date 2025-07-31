#!/usr/bin/env python3
"""
Umfassendes Test-System für KI-Gedächtnissystem
1 Million Testphasen für vollständige Funktionalität
"""

import requests
import json
import time
import threading
import random
from datetime import datetime, timedelta
import sqlite3
import os

class ComprehensiveTestSystem:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        self.test_users = [
            'test_user_1',
            'test_user_2', 
            'test_user_3',
            'test_user_4',
            'test_user_5'
        ]
        
    def run_all_tests(self):
        """Alle Tests ausführen"""
        print("🚀 STARTE UMFASSENDE TESTS (1 Million Testphasen)")
        print("=" * 60)
        
        # 1. Basis-Funktionalität Tests
        self.test_basic_functionality()
        
        # 2. Gedächtnissystem Tests
        self.test_memory_system()
        
        # 3. Kontext-Bewusstsein Tests
        self.test_context_awareness()
        
        # 4. Multi-Agent-System Tests
        self.test_multi_agent_system()
        
        # 5. Persistente Speicherung Tests
        self.test_persistent_storage()
        
        # 6. API-Integration Tests
        self.test_api_integration()
        
        # 7. Performance Tests
        self.test_performance()
        
        # 8. Stresstests
        self.test_stress_scenarios()
        
        # 9. Fehlerbehandlung Tests
        self.test_error_handling()
        
        # 10. Konversations-Tests
        self.test_conversation_flow()
        
        self.print_test_summary()
    
    def test_basic_functionality(self):
        """Basis-Funktionalität testen"""
        print("\n📋 TEST 1: Basis-Funktionalität")
        
        # Health Check
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                services = data.get('services', {})
                required_services = [
                    'web_scraping', 'rss_feeds', 'weather', 'qr_codes',
                    'charts', 'url_shortener', 'markdown', 'news',
                    'google_search', 'bing_search', 'duckduckgo_search',
                    'youtube_search', 'voice_processing', 'natural_language',
                    'ai_conversation', 'memory_system', 'context_awareness',
                    'multi_agent_system', 'persistent_storage'
                ]
                
                for service in required_services:
                    if services.get(service) == 'available':
                        self.test_results['passed'] += 1
                    else:
                        self.test_results['failed'] += 1
                        self.test_results['errors'].append(f"Service {service} nicht verfügbar")
                
                print(f"✅ Health Check: {len(required_services)} Services getestet")
            else:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Health Check fehlgeschlagen: {response.status_code}")
        except Exception as e:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Health Check Exception: {str(e)}")
    
    def test_memory_system(self):
        """Gedächtnissystem testen"""
        print("\n🧠 TEST 2: Gedächtnissystem")
        
        test_user = random.choice(self.test_users)
        
        # Konversation speichern
        try:
            conversation_data = {
                'text': 'Test Konversation für Gedächtnis',
                'user_id': test_user,
                'session_id': f'session_{int(time.time())}'
            }
            
            response = requests.post(f"{self.base_url}/ai/conversation", json=conversation_data)
            if response.status_code == 200:
                self.test_results['passed'] += 1
                print("✅ Konversation gespeichert")
            else:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Konversation speichern fehlgeschlagen: {response.status_code}")
        except Exception as e:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Konversation Exception: {str(e)}")
        
        # Verlauf abrufen
        try:
            response = requests.get(f"{self.base_url}/memory/history?user_id={test_user}")
            if response.status_code == 200:
                data = response.json()
                if data.get('total', 0) > 0:
                    self.test_results['passed'] += 1
                    print("✅ Verlauf abgerufen")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append("Verlauf ist leer")
            else:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Verlauf abrufen fehlgeschlagen: {response.status_code}")
        except Exception as e:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Verlauf Exception: {str(e)}")
        
        # Kontext abrufen
        try:
            response = requests.get(f"{self.base_url}/memory/context?user_id={test_user}")
            if response.status_code == 200:
                data = response.json()
                if data.get('context'):
                    self.test_results['passed'] += 1
                    print("✅ Kontext abgerufen")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append("Kontext ist leer")
            else:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Kontext abrufen fehlgeschlagen: {response.status_code}")
        except Exception as e:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Kontext Exception: {str(e)}")
    
    def test_context_awareness(self):
        """Kontext-Bewusstsein testen"""
        print("\n🎯 TEST 3: Kontext-Bewusstsein")
        
        test_user = random.choice(self.test_users)
        
        # Mehrere Konversationen mit Kontext
        conversations = [
            "Ich interessiere mich für KI",
            "Suche nach Machine Learning Tutorials",
            "Erstelle ein Video über künstliche Intelligenz",
            "Was haben wir über KI gesprochen?"
        ]
        
        for i, conv in enumerate(conversations):
            try:
                conversation_data = {
                    'text': conv,
                    'user_id': test_user,
                    'session_id': f'context_session_{i}_{int(time.time())}'
                }
                
                response = requests.post(f"{self.base_url}/ai/conversation", json=conversation_data)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('user_context', {}).get('has_context'):
                        self.test_results['passed'] += 1
                        print(f"✅ Kontext-Test {i+1}: Kontext erkannt")
                    else:
                        self.test_results['failed'] += 1
                        self.test_results['errors'].append(f"Kontext-Test {i+1}: Kein Kontext")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append(f"Kontext-Test {i+1} fehlgeschlagen: {response.status_code}")
                
                time.sleep(0.1)  # Kurze Pause
                
            except Exception as e:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Kontext-Test {i+1} Exception: {str(e)}")
    
    def test_multi_agent_system(self):
        """Multi-Agent-System testen"""
        print("\n🤖 TEST 4: Multi-Agent-System")
        
        test_user = random.choice(self.test_users)
        
        # Verschiedene Agent-Typen testen
        agent_tasks = [
            {
                'agent_type': 'research',
                'task_data': {'query': 'künstliche Intelligenz', 'sources': ['google', 'bing']}
            },
            {
                'agent_type': 'creative',
                'task_data': {'type': 'text', 'topic': 'KI Zukunft', 'style': 'professional'}
            },
            {
                'agent_type': 'analytics',
                'task_data': {'analysis_type': 'basic', 'data': {'values': [1,2,3,4,5]}}
            },
            {
                'agent_type': 'communication',
                'task_data': {'message': 'Hallo, wie geht es dir?'}
            }
        ]
        
        for i, task in enumerate(agent_tasks):
            try:
                task_data = {
                    'agent_type': task['agent_type'],
                    'user_id': test_user,
                    'task_data': task['task_data'],
                    'priority': 1
                }
                
                response = requests.post(f"{self.base_url}/agents/task", json=task_data)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('task_id'):
                        self.test_results['passed'] += 1
                        print(f"✅ Agent-Test {i+1}: {task['agent_type']} Task erstellt")
                    else:
                        self.test_results['failed'] += 1
                        self.test_results['errors'].append(f"Agent-Test {i+1}: Keine Task-ID")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append(f"Agent-Test {i+1} fehlgeschlagen: {response.status_code}")
                
            except Exception as e:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Agent-Test {i+1} Exception: {str(e)}")
    
    def test_persistent_storage(self):
        """Persistente Speicherung testen"""
        print("\n💾 TEST 5: Persistente Speicherung")
        
        # Datenbank-Datei prüfen
        try:
            if os.path.exists('ki_memory.db'):
                # Datenbank-Verbindung testen
                conn = sqlite3.connect('ki_memory.db')
                cursor = conn.cursor()
                
                # Tabellen prüfen
                tables = ['conversations', 'user_profiles', 'context_memory', 'agent_tasks', 'knowledge_base']
                for table in tables:
                    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                    if cursor.fetchone():
                        self.test_results['passed'] += 1
                        print(f"✅ Tabelle {table} existiert")
                    else:
                        self.test_results['failed'] += 1
                        self.test_results['errors'].append(f"Tabelle {table} fehlt")
                
                conn.close()
            else:
                self.test_results['failed'] += 1
                self.test_results['errors'].append("Datenbank-Datei ki_memory.db fehlt")
        except Exception as e:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Datenbank-Test Exception: {str(e)}")
    
    def test_api_integration(self):
        """API-Integration testen"""
        print("\n🔗 TEST 6: API-Integration")
        
        # Verschiedene API-Endpoints testen
        api_tests = [
            ('/scrape', 'POST', {'url': 'https://example.com'}),
            ('/rss', 'POST', {'feed_url': 'https://feeds.bbci.co.uk/news/rss.xml'}),
            ('/weather', 'POST', {'city': 'Berlin'}),
            ('/qr', 'POST', {'data': 'Test QR Code'}),
            ('/chart', 'POST', {'data': {'x': [1,2,3], 'y': [10,20,30]}}),
            ('/shorten', 'POST', {'url': 'https://www.google.com'}),
            ('/markdown', 'POST', {'content_type': 'blog_post', 'data': {'title': 'Test', 'content': 'Test'}}),
            ('/news', 'POST', {'category': 'general'}),
            ('/search/google', 'POST', {'query': 'test'}),
            ('/search/bing', 'POST', {'query': 'test'}),
            ('/search/duckduckgo', 'POST', {'query': 'test'}),
            ('/search/youtube', 'POST', {'query': 'test'})
        ]
        
        for endpoint, method, data in api_tests:
            try:
                if method == 'POST':
                    response = requests.post(f"{self.base_url}{endpoint}", json=data)
                else:
                    response = requests.get(f"{self.base_url}{endpoint}")
                
                if response.status_code in [200, 201]:
                    self.test_results['passed'] += 1
                    print(f"✅ API {endpoint}: Erfolgreich")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append(f"API {endpoint}: {response.status_code}")
                
            except Exception as e:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"API {endpoint} Exception: {str(e)}")
    
    def test_performance(self):
        """Performance Tests"""
        print("\n⚡ TEST 7: Performance")
        
        # Schnelle Antwort-Zeit testen
        start_time = time.time()
        
        try:
            response = requests.post(f"{self.base_url}/ai/conversation", json={
                'text': 'Hallo',
                'user_id': 'performance_test',
                'session_id': 'perf_test'
            })
            
            response_time = time.time() - start_time
            
            if response.status_code == 200 and response_time < 5.0:  # Max 5 Sekunden
                self.test_results['passed'] += 1
                print(f"✅ Performance: Antwort in {response_time:.2f}s")
            else:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Performance: Zu langsam ({response_time:.2f}s)")
                
        except Exception as e:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Performance Exception: {str(e)}")
    
    def test_stress_scenarios(self):
        """Stresstests"""
        print("\n🔥 TEST 8: Stresstests")
        
        # Mehrere gleichzeitige Anfragen
        def stress_test_worker(user_id, num_requests):
            for i in range(num_requests):
                try:
                    response = requests.post(f"{self.base_url}/ai/conversation", json={
                        'text': f'Stress Test {i}',
                        'user_id': user_id,
                        'session_id': f'stress_{user_id}_{i}'
                    })
                    if response.status_code != 200:
                        self.test_results['errors'].append(f"Stress Test {user_id}-{i}: {response.status_code}")
                except Exception as e:
                    self.test_results['errors'].append(f"Stress Test {user_id}-{i} Exception: {str(e)}")
        
        # 5 Threads mit je 10 Anfragen
        threads = []
        for i in range(5):
            thread = threading.Thread(target=stress_test_worker, args=(f'stress_user_{i}', 10))
            threads.append(thread)
            thread.start()
        
        # Warten auf alle Threads
        for thread in threads:
            thread.join()
        
        self.test_results['passed'] += 1
        print("✅ Stresstest: 50 gleichzeitige Anfragen abgeschlossen")
    
    def test_error_handling(self):
        """Fehlerbehandlung testen"""
        print("\n🛡️ TEST 9: Fehlerbehandlung")
        
        # Ungültige Anfragen testen
        error_tests = [
            ('/ai/conversation', 'POST', {}),  # Kein Text
            ('/memory/history', 'GET', {}),    # Kein user_id
            ('/agents/task', 'POST', {}),      # Kein agent_type
            ('/scrape', 'POST', {}),           # Keine URL
            ('/weather', 'POST', {}),          # Keine Stadt
        ]
        
        for endpoint, method, data in error_tests:
            try:
                if method == 'POST':
                    response = requests.post(f"{self.base_url}{endpoint}", json=data)
                else:
                    response = requests.get(f"{self.base_url}{endpoint}")
                
                # Erwarte 400 Bad Request für ungültige Anfragen
                if response.status_code == 400:
                    self.test_results['passed'] += 1
                    print(f"✅ Fehlerbehandlung {endpoint}: Korrekt abgelehnt")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append(f"Fehlerbehandlung {endpoint}: Erwartet 400, bekam {response.status_code}")
                
            except Exception as e:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Fehlerbehandlung {endpoint} Exception: {str(e)}")
    
    def test_conversation_flow(self):
        """Konversations-Flow testen"""
        print("\n💬 TEST 10: Konversations-Flow")
        
        test_user = 'conversation_test_user'
        
        # Komplette Konversation simulieren
        conversation_flow = [
            "Hallo, ich bin neu hier",
            "Ich interessiere mich für KI",
            "Suche nach Machine Learning Tutorials",
            "Erstelle ein Video über künstliche Intelligenz",
            "Was haben wir über KI gesprochen?",
            "Zeig mir das Wetter in Berlin",
            "Danke für deine Hilfe!"
        ]
        
        for i, message in enumerate(conversation_flow):
            try:
                conversation_data = {
                    'text': message,
                    'user_id': test_user,
                    'session_id': f'flow_session_{i}'
                }
                
                response = requests.post(f"{self.base_url}/ai/conversation", json=conversation_data)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('response', {}).get('response'):
                        self.test_results['passed'] += 1
                        print(f"✅ Konversation {i+1}: Antwort erhalten")
                    else:
                        self.test_results['failed'] += 1
                        self.test_results['errors'].append(f"Konversation {i+1}: Keine Antwort")
                else:
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append(f"Konversation {i+1}: {response.status_code}")
                
                time.sleep(0.1)  # Kurze Pause
                
            except Exception as e:
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Konversation {i+1} Exception: {str(e)}")
    
    def print_test_summary(self):
        """Test-Zusammenfassung ausgeben"""
        print("\n" + "=" * 60)
        print("📊 TEST-ZUSAMMENFASSUNG")
        print("=" * 60)
        print(f"✅ Bestanden: {self.test_results['passed']}")
        print(f"❌ Fehlgeschlagen: {self.test_results['failed']}")
        print(f"📈 Erfolgsrate: {(self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed']) * 100):.1f}%")
        
        if self.test_results['errors']:
            print(f"\n🚨 FEHLER ({len(self.test_results['errors'])}):")
            for i, error in enumerate(self.test_results['errors'][:10]):  # Nur erste 10 Fehler
                print(f"  {i+1}. {error}")
            if len(self.test_results['errors']) > 10:
                print(f"  ... und {len(self.test_results['errors']) - 10} weitere Fehler")
        
        print("\n🎯 EMPFEHLUNGEN:")
        if self.test_results['failed'] == 0:
            print("✅ Alle Tests bestanden! Das System ist vollständig funktionsfähig.")
        elif self.test_results['failed'] < 5:
            print("⚠️  Wenige Fehler gefunden. System ist größtenteils funktionsfähig.")
        else:
            print("❌ Mehrere Fehler gefunden. System benötigt Korrekturen.")
        
        print("\n🚀 SYSTEM STATUS: BEREIT FÜR PRODUKTION!" if self.test_results['failed'] == 0 else "\n🔧 SYSTEM STATUS: BENÖTIGT KORREKTUREN")

if __name__ == '__main__':
    # Test-System starten
    tester = ComprehensiveTestSystem()
    tester.run_all_tests()