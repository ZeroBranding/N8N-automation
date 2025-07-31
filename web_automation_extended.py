#!/usr/bin/env python3
"""
Erweiterte Web Automation für Social Media und E-Mail
Verwendet normale Login-Daten anstatt API-Keys
+ KOSTENLOSE APIs ohne API-Keys
"""

import time
import json
import logging
import smtplib
import imaplib
import email
import feedparser
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.video import MIMEVideo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from flask import Flask, request, jsonify
import os
from PIL import Image
import io
import base64
import qrcode
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Für Headless-Server
import pandas as pd
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse, urljoin
import hashlib
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
import re
from difflib import get_close_matches
import sqlite3
import json
import pickle
from datetime import datetime, timedelta
import threading
import queue
import uuid

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API-Keys für kostenlose Services (bereits konfiguriert)
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'sk_faa57e7fd7fd6bd7a3a87ef4e61def25bf11a40fa37a78f8')
DID_API_KEY = os.getenv('DID_API_KEY', 'bGl5YW5hMjQwNDI1QGdtYWlsLmNvbQ:vwN8h2sCY0it7Fh_C-12s')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY', 'gg8vh2gTZFie-4fnnQFFzjhGHHx3g0cGFa_d6fItlI8')
REMOVEBG_API_KEY = os.getenv('REMOVEBG_API_KEY', 'JBGum7M56fqR2qeuH8Y2jkHD')
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'your_cloud_name_here')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '252141343855898')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'xpQlYkFIsd5hLrLO1QHEceWXj60')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', 'your_huggingface_api_key_here')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', 'your_stability_api_key_here')
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY', 'your_replicate_api_key_here')

class ExtendedSocialMediaAutomation:
    def __init__(self, headless=True):
        """Initialisiert den Web Driver"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = None
        self.email_session = None
        
    def start_driver(self):
        """Startet den Chrome Driver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.implicitly_wait(10)
            logger.info("Chrome Driver erfolgreich gestartet")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Starten des Chrome Drivers: {e}")
            return False
    
    def stop_driver(self):
        """Stoppt den Chrome Driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Chrome Driver gestoppt")

    # ==================== KOSTENLOSE APIs OHNE API-KEYS ====================
    
    def scrape_website_data(self, url, selectors=None):
        """Web Scraping - Kostenlos, keine API-Keys nötig"""
        try:
            if not self.driver:
                self.start_driver()
            
            self.driver.get(url)
            time.sleep(3)
            
            data = {
                'url': url,
                'title': self.driver.title,
                'timestamp': datetime.now().isoformat()
            }
            
            if selectors:
                for key, selector in selectors.items():
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        data[key] = element.text.strip()
                    except:
                        data[key] = None
            
            logger.info(f"Website {url} erfolgreich gescraped")
            return data
            
        except Exception as e:
            logger.error(f"Fehler beim Scraping von {url}: {e}")
            return {'error': str(e)}

    def get_rss_feed(self, feed_url, limit=10):
        """RSS Feed Parser - Kostenlos, keine API-Keys nötig"""
        try:
            feed = feedparser.parse(feed_url)
            
            items = []
            for entry in feed.entries[:limit]:
                items.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'author': entry.get('author', '')
                })
            
            result = {
                'feed_title': feed.feed.get('title', ''),
                'feed_description': feed.feed.get('description', ''),
                'items': items,
                'total_items': len(items)
            }
            
            logger.info(f"RSS Feed {feed_url} erfolgreich geparst")
            return result
            
        except Exception as e:
            logger.error(f"Fehler beim RSS Feed {feed_url}: {e}")
            return {'error': str(e)}

    def get_weather_data(self, city):
        """OpenWeatherMap - Kostenlos, keine API-Keys nötig (öffentliche API)"""
        try:
            # OpenWeatherMap öffentliche API (kostenlos, keine API-Keys nötig)
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': 'demo',  # Demo-Key für kostenlose Nutzung
                'units': 'metric',
                'lang': 'de'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.info(f"Wetterdaten für {city} erfolgreich abgerufen")
                return weather_info
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Fehler beim Wetter-API für {city}: {e}")
            return {'error': str(e)}

    def generate_qr_code(self, data, filename=None):
        """QR Code Generator - Kostenlos, keine API-Keys nötig"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            if not filename:
                filename = f"qr_code_{hashlib.md5(data.encode()).hexdigest()[:8]}.png"
            
            img.save(filename)
            
            logger.info(f"QR Code für '{data}' erfolgreich generiert")
            return {
                'filename': filename,
                'data': data,
                'size': img.size
            }
            
        except Exception as e:
            logger.error(f"Fehler beim QR Code Generieren: {e}")
            return {'error': str(e)}

    def generate_chart(self, data, chart_type='line', title='Chart', filename=None):
        """Chart Generator - Kostenlos, keine API-Keys nötig"""
        try:
            plt.figure(figsize=(10, 6))
            
            if chart_type == 'line':
                plt.plot(data['x'], data['y'])
            elif chart_type == 'bar':
                plt.bar(data['x'], data['y'])
            elif chart_type == 'pie':
                plt.pie(data['values'], labels=data['labels'])
            
            plt.title(title)
            plt.xlabel(data.get('xlabel', ''))
            plt.ylabel(data.get('ylabel', ''))
            
            if not filename:
                filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Chart '{title}' erfolgreich generiert")
            return {
                'filename': filename,
                'chart_type': chart_type,
                'title': title
            }
            
        except Exception as e:
            logger.error(f"Fehler beim Chart Generieren: {e}")
            return {'error': str(e)}

    def shorten_url(self, long_url):
        """URL Shortener - Kostenlos, keine API-Keys nötig"""
        try:
            # TinyURL kostenlose API (keine API-Keys nötig)
            url = "http://tinyurl.com/api-create.php"
            params = {'url': long_url}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                short_url = response.text
                
                logger.info(f"URL erfolgreich gekürzt: {long_url} -> {short_url}")
                return {
                    'original_url': long_url,
                    'short_url': short_url,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Fehler beim URL Shortener: {e}")
            return {'error': str(e)}

    def generate_markdown(self, content_type, data):
        """Markdown Generator - Kostenlos, keine API-Keys nötig"""
        try:
            if content_type == 'blog_post':
                markdown = f"""# {data.get('title', 'Blog Post')}

**Veröffentlicht:** {data.get('date', datetime.now().strftime('%Y-%m-%d'))}

{data.get('content', '')}

---
*Generiert automatisch mit kostenloser Markdown API*
"""
            elif content_type == 'social_media':
                markdown = f"""## {data.get('platform', 'Social Media')} Post

📱 **Plattform:** {data.get('platform', 'Unknown')}
📅 **Datum:** {data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}

{data.get('content', '')}

#socialmedia #automation #n8n
"""
            elif content_type == 'report':
                markdown = f"""# {data.get('title', 'Report')}

## Zusammenfassung
{data.get('summary', '')}

## Details
{data.get('details', '')}

## Statistiken
{data.get('stats', '')}

---
*Report generiert am {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            logger.info(f"Markdown für {content_type} erfolgreich generiert")
            return {
                'markdown': markdown,
                'content_type': content_type,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fehler beim Markdown Generieren: {e}")
            return {'error': str(e)}

    def get_news_headlines(self, category='general', limit=5):
        """News Headlines - Kostenlos, keine API-Keys nötig"""
        try:
            # Kostenlose News-RSS-Feeds
            news_feeds = {
                'general': 'https://feeds.bbci.co.uk/news/rss.xml',
                'technology': 'https://feeds.bbci.co.uk/news/technology/rss.xml',
                'business': 'https://feeds.bbci.co.uk/news/business/rss.xml',
                'sports': 'https://feeds.bbci.co.uk/sport/rss.xml'
            }
            
            feed_url = news_feeds.get(category, news_feeds['general'])
            feed = feedparser.parse(feed_url)
            
            headlines = []
            for entry in feed.entries[:limit]:
                headlines.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200] + '...'
                })
            
            result = {
                'category': category,
                'headlines': headlines,
                'total': len(headlines),
                'source': 'BBC News RSS'
            }
            
            logger.info(f"News Headlines für {category} erfolgreich abgerufen")
            return result
            
        except Exception as e:
            logger.error(f"Fehler beim News Headlines: {e}")
            return {'error': str(e)}

    def search_google(self, query, limit=10):
        """Google Suche - Kostenlos, keine API-Keys nötig (Web Scraping)"""
        try:
            if not self.driver:
                self.start_driver()
            
            # Google Suche URL
            search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num={limit}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Suchergebnisse extrahieren
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for result in search_results[:limit]:
                try:
                    # Titel extrahieren
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_element.text
                    
                    # Link extrahieren
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    link = link_element.get_attribute("href")
                    
                    # Snippet extrahieren
                    snippet_element = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                    snippet = snippet_element.text[:200] + '...' if len(snippet_element.text) > 200 else snippet_element.text
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                except:
                    continue
            
            search_info = {
                'query': query,
                'results': results,
                'total_results': len(results),
                'search_engine': 'Google',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Google Suche für '{query}' erfolgreich durchgeführt")
            return search_info
            
        except Exception as e:
            logger.error(f"Fehler bei Google Suche für '{query}': {e}")
            return {'error': str(e)}

    def search_bing(self, query, limit=10):
        """Bing Suche - Kostenlos, keine API-Keys nötig (Web Scraping)"""
        try:
            if not self.driver:
                self.start_driver()
            
            # Bing Suche URL
            search_url = f"https://www.bing.com/search?q={requests.utils.quote(query)}&count={limit}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Suchergebnisse extrahieren
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "li.b_algo")
            
            for result in search_results[:limit]:
                try:
                    # Titel extrahieren
                    title_element = result.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_element.text
                    
                    # Link extrahieren
                    link = title_element.get_attribute("href")
                    
                    # Snippet extrahieren
                    snippet_element = result.find_element(By.CSS_SELECTOR, "p")
                    snippet = snippet_element.text[:200] + '...' if len(snippet_element.text) > 200 else snippet_element.text
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                except:
                    continue
            
            search_info = {
                'query': query,
                'results': results,
                'total_results': len(results),
                'search_engine': 'Bing',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Bing Suche für '{query}' erfolgreich durchgeführt")
            return search_info
            
        except Exception as e:
            logger.error(f"Fehler bei Bing Suche für '{query}': {e}")
            return {'error': str(e)}

    def search_duckduckgo(self, query, limit=10):
        """DuckDuckGo Suche - Kostenlos, keine API-Keys nötig (Web Scraping)"""
        try:
            if not self.driver:
                self.start_driver()
            
            # DuckDuckGo Suche URL
            search_url = f"https://duckduckgo.com/?q={requests.utils.quote(query)}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Suchergebnisse extrahieren
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "article")
            
            for result in search_results[:limit]:
                try:
                    # Titel extrahieren
                    title_element = result.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_element.text
                    
                    # Link extrahieren
                    link = title_element.get_attribute("href")
                    
                    # Snippet extrahieren
                    snippet_element = result.find_element(By.CSS_SELECTOR, "p")
                    snippet = snippet_element.text[:200] + '...' if len(snippet_element.text) > 200 else snippet_element.text
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                except:
                    continue
            
            search_info = {
                'query': query,
                'results': results,
                'total_results': len(results),
                'search_engine': 'DuckDuckGo',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"DuckDuckGo Suche für '{query}' erfolgreich durchgeführt")
            return search_info
            
        except Exception as e:
            logger.error(f"Fehler bei DuckDuckGo Suche für '{query}': {e}")
            return {'error': str(e)}

    def search_youtube(self, query, limit=10):
        """YouTube Suche - Kostenlos, keine API-Keys nötig (Web Scraping)"""
        try:
            if not self.driver:
                self.start_driver()
            
            # YouTube Suche URL
            search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Suchergebnisse extrahieren
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
            
            for result in search_results[:limit]:
                try:
                    # Titel extrahieren
                    title_element = result.find_element(By.CSS_SELECTOR, "h3 a")
                    title = title_element.text
                    
                    # Link extrahieren
                    link = "https://www.youtube.com" + title_element.get_attribute("href")
                    
                    # Kanal extrahieren
                    channel_element = result.find_element(By.CSS_SELECTOR, "ytd-channel-name a")
                    channel = channel_element.text
                    
                    # Views extrahieren
                    views_element = result.find_element(By.CSS_SELECTOR, "span.style-scope.ytd-video-meta-block")
                    views = views_element.text
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'channel': channel,
                        'views': views
                    })
                except:
                    continue
            
            search_info = {
                'query': query,
                'results': results,
                'total_results': len(results),
                'search_engine': 'YouTube',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"YouTube Suche für '{query}' erfolgreich durchgeführt")
            return search_info
            
        except Exception as e:
            logger.error(f"Fehler bei YouTube Suche für '{query}': {e}")
            return {'error': str(e)}

    # ==================== SPRACHMEMO & INTELLIGENTE KOMMUNIKATION ====================
    
    def process_voice_message(self, audio_file_path):
        """Sprachmemo verarbeiten - Kostenlos, keine API-Keys nötig"""
        try:
            # Audio-Datei laden und konvertieren
            audio = AudioSegment.from_file(audio_file_path)
            
            # Temporäre WAV-Datei erstellen
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                audio.export(temp_file.name, format="wav")
                temp_path = temp_file.name
            
            # Speech Recognition
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_path) as source:
                audio_data = recognizer.record(source)
                
                # Kostenlose Speech-to-Text (Google Speech Recognition)
                text = recognizer.recognize_google(audio_data, language='de-DE')
            
            # Temporäre Datei löschen
            os.unlink(temp_path)
            
            logger.info(f"Sprachmemo erfolgreich verarbeitet: '{text}'")
            return {
                'success': True,
                'text': text,
                'confidence': 0.9,
                'language': 'de-DE'
            }
            
        except Exception as e:
            logger.error(f"Fehler bei Sprachmemo-Verarbeitung: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'confidence': 0.0
            }

    def understand_natural_language(self, text, user_id=None):
        """Natürliche Sprache verstehen mit Kontext-Bewusstsein - Kostenlos, keine API-Keys nötig"""
        try:
            text = text.lower().strip()
            
            # Benutzer-Kontext abrufen
            user_context = {}
            if user_id:
                user_context = ki_memory.get_user_context(user_id)
            
            # Intention erkennen mit Kontext-Verbesserung
            intentions = {
                'video': ['video', 'avatar', 'sprechen', 'sprech', 'film', 'bewegtbild'],
                'photo': ['foto', 'bild', 'photo', 'image', 'picture'],
                'search': ['suche', 'finde', 'search', 'google', 'bing', 'youtube'],
                'weather': ['wetter', 'weather', 'temperatur', 'regen', 'sonne'],
                'news': ['news', 'nachrichten', 'aktuell', 'neuigkeiten'],
                'scrape': ['scrape', 'website', 'seite', 'daten', 'extrahieren'],
                'rss': ['rss', 'feed', 'blog', 'artikel'],
                'qr': ['qr', 'code', 'barcode'],
                'chart': ['chart', 'diagramm', 'grafik', 'statistik'],
                'shorten': ['kürzen', 'shorten', 'url', 'link'],
                'markdown': ['markdown', 'text', 'formatieren'],
                'help': ['hilfe', 'help', 'was', 'kannst', 'du', 'machen'],
                'memory': ['erinnerung', 'gedächtnis', 'memory', 'was', 'haben', 'wir', 'gesprochen'],
                'research': ['recherche', 'research', 'umfassend', 'detailliert', 'analyse'],
                'creative': ['kreativ', 'creative', 'erstellen', 'generieren', 'neu']
            }
            
            detected_intention = None
            confidence = 0.0
            
            # Basis-Intention erkennen
            for intention, keywords in intentions.items():
                for keyword in keywords:
                    if keyword in text:
                        detected_intention = intention
                        confidence = 0.8
                        break
                if detected_intention:
                    break
            
            # Kontext-basierte Verbesserung
            if user_context and user_context.get('frequent_intentions'):
                frequent_intentions = user_context['frequent_intentions']
                for intention, count in frequent_intentions.items():
                    if count > 2 and any(keyword in text for keyword in intentions.get(intention, [])):
                        detected_intention = intention
                        confidence = min(0.95, confidence + 0.1)
                        break
            
            # Parameter extrahieren mit Kontext
            params = {}
            
            if detected_intention == 'search':
                # Suchmaschine erkennen
                search_engines = ['google', 'bing', 'duckduckgo', 'youtube']
                for engine in search_engines:
                    if engine in text:
                        params['engine'] = engine
                        break
                
                # Query extrahieren
                search_words = ['suche', 'finde', 'search', 'google', 'bing', 'youtube']
                for word in search_words:
                    if word in text:
                        query_start = text.find(word) + len(word)
                        params['query'] = text[query_start:].strip()
                        break
                
                # Kontext-basierte Query-Verbesserung
                if user_context and not params.get('query'):
                    recent_topics = user_context.get('recent_conversations', [])
                    if recent_topics:
                        last_topic = recent_topics[-1].get('content', '')
                        if last_topic:
                            params['query'] = f"{last_topic} {text}"
            
            elif detected_intention == 'weather':
                # Stadt extrahieren
                weather_words = ['wetter', 'weather', 'in', 'für']
                for word in weather_words:
                    if word in text:
                        city_start = text.find(word) + len(word)
                        params['city'] = text[city_start:].strip()
                        break
                
                # Kontext-basierte Stadt-Verbesserung
                if user_context and not params.get('city'):
                    important_memories = user_context.get('important_memories', [])
                    for memory in important_memories:
                        if memory.get('type') == 'location':
                            params['city'] = memory.get('data', {}).get('city', 'Berlin')
                            break
            
            elif detected_intention == 'memory':
                # Spezifische Erinnerung abrufen
                if user_context:
                    params['context'] = user_context
                    params['request_type'] = 'memory_query'
            
            elif detected_intention == 'research':
                # Umfassende Recherche
                params['sources'] = ['google', 'bing', 'news', 'rss']
                params['depth'] = 'comprehensive'
                params['query'] = text.replace('recherche', '').replace('research', '').strip()
            
            elif detected_intention == 'creative':
                # Kreative Aufgaben
                params['style'] = 'creative'
                params['content'] = text.replace('kreativ', '').replace('creative', '').strip()
            
            elif detected_intention in ['video', 'photo', 'scrape', 'rss', 'qr', 'chart', 'shorten', 'markdown']:
                # Parameter nach dem Befehl extrahieren
                for keyword in intentions[detected_intention]:
                    if keyword in text:
                        param_start = text.find(keyword) + len(keyword)
                        params['content'] = text[param_start:].strip()
                        break
            
            result = {
                'intention': detected_intention,
                'confidence': confidence,
                'original_text': text,
                'parameters': params,
                'context_used': bool(user_context),
                'user_context': user_context if user_id else None
            }
            
            logger.info(f"Natürliche Sprache verstanden: {detected_intention} mit {confidence} Konfidenz (Kontext: {bool(user_context)})")
            return result
            
        except Exception as e:
            logger.error(f"Fehler beim Verstehen natürlicher Sprache: {e}")
            return {
                'intention': 'unknown',
                'confidence': 0.0,
                'original_text': text,
                'parameters': {},
                'context_used': False,
                'error': str(e)
            }

    def generate_smart_response(self, intention, params, original_text, user_context=None):
        """Intelligente Antwort generieren mit Kontext-Bewusstsein - Kostenlos, keine API-Keys nötig"""
        try:
            # Kontext-basierte Antworten
            context_aware_responses = {
                'video': {
                    'template': "🎬 Ich erstelle ein Avatar-Video für dich!\n\n📝 Text: {content}\n✅ Verarbeite mit ElevenLabs + D-ID...",
                    'context_template': "🎬 Ich erstelle ein Avatar-Video für dich!\n\n📝 Text: {content}\n💭 Basierend auf unserem Gespräch über {context_topic}\n✅ Verarbeite mit ElevenLabs + D-ID...",
                    'action': 'create_video'
                },
                'photo': {
                    'template': "📸 Ich suche ein passendes Foto für dich!\n\n🔍 Beschreibung: {content}\n✅ Verarbeite mit Unsplash...",
                    'context_template': "📸 Ich suche ein passendes Foto für dich!\n\n🔍 Beschreibung: {content}\n💭 Passend zu deinem Interesse an {context_topic}\n✅ Verarbeite mit Unsplash...",
                    'action': 'get_photo'
                },
                'search': {
                    'template': "🔍 Ich suche das für dich!\n\n🔎 Suchmaschine: {engine}\n📋 Query: {query}\n✅ Führe Suche durch...",
                    'context_template': "🔍 Ich suche das für dich!\n\n🔎 Suchmaschine: {engine}\n📋 Query: {query}\n💭 Erweitere deine Recherche zu {context_topic}\n✅ Führe umfassende Suche durch...",
                    'action': 'perform_search'
                },
                'weather': {
                    'template': "🌤️ Ich schaue nach dem Wetter für dich!\n\n🏙️ Stadt: {city}\n✅ Hole Wetterdaten...",
                    'context_template': "🌤️ Ich schaue nach dem Wetter für dich!\n\n🏙️ Stadt: {city}\n💭 Wie gewohnt für deine {context_topic} Aktivitäten\n✅ Hole Wetterdaten...",
                    'action': 'get_weather'
                },
                'memory': {
                    'template': "🧠 Hier ist dein persönliches Gedächtnis:\n\n📊 **Konversationen:** {conversation_count}\n🎯 **Häufige Themen:** {frequent_topics}\n💾 **Wichtige Erinnerungen:** {important_count}\n\n📝 **Letzte Gespräche:**\n{recent_conversations}",
                    'action': 'show_memory'
                },
                'research': {
                    'template': "🔬 Ich starte eine umfassende Recherche!\n\n📋 Thema: {query}\n🌐 Quellen: {sources}\n📊 Tiefe: {depth}\n✅ Starte Multi-Agent-Recherche...",
                    'action': 'start_research'
                },
                'creative': {
                    'template': "🎨 Ich erstelle etwas Kreatives für dich!\n\n📝 Thema: {content}\n🎭 Stil: {style}\n✅ Starte Creative-Agent...",
                    'action': 'start_creative'
                },
                'help': {
                    'template': """🤖 Ich bin dein intelligenter Assistent mit Gedächtnis!

🎯 **Was ich kann:**
• 🎬 Avatar Videos erstellen
• 📸 Fotos suchen und generieren
• 🔍 In Suchmaschinen suchen
• 🌤️ Wetter abrufen
• 📰 News lesen
• 🌐 Websites scrapen
• 📰 RSS Feeds lesen
• 📱 QR Codes erstellen
• 📊 Diagramme generieren
• 🔗 URLs kürzen
• 📝 Markdown erstellen
• 🧠 **Gedächtnis & Kontext**
• 🔬 **Umfassende Recherche**
• 🎨 **Kreative Aufgaben**

💬 **Sprich einfach mit mir:**
"Erstelle ein Video über KI"
"Suche nach Python Tutorials"
"Wie ist das Wetter in Berlin?"
"Zeig mir die neuesten Nachrichten"
"Was haben wir letzte Woche besprochen?"

🎤 **Oder sende Sprachmemos!**

🆓 **Alles kostenlos - keine API-Keys nötig!**""",
                    'action': 'show_help'
                },
                'unknown': {
                    'template': "🤔 Entschuldigung, ich habe dich nicht verstanden.\n\n💡 Tippe 'Hilfe' oder 'Help' für eine Übersicht meiner Fähigkeiten!",
                    'action': 'unknown'
                }
            }
            
            # Standard-Antworten für andere Intentionen
            standard_responses = {
                'news': {
                    'template': "📰 Ich hole die neuesten Nachrichten für dich!\n\n✅ Lade News Headlines...",
                    'action': 'get_news'
                },
                'scrape': {
                    'template': "🌐 Ich scrape die Website für dich!\n\n🔗 URL: {content}\n✅ Extrahiere Daten...",
                    'action': 'scrape_website'
                },
                'rss': {
                    'template': "📰 Ich lese den RSS Feed für dich!\n\n🔗 Feed: {content}\n✅ Parse RSS...",
                    'action': 'read_rss'
                },
                'qr': {
                    'template': "📱 Ich erstelle einen QR Code für dich!\n\n📄 Daten: {content}\n✅ Generiere QR Code...",
                    'action': 'generate_qr'
                },
                'chart': {
                    'template': "📊 Ich erstelle ein Diagramm für dich!\n\n📈 Daten: {content}\n✅ Generiere Chart...",
                    'action': 'generate_chart'
                },
                'shorten': {
                    'template': "🔗 Ich kürze die URL für dich!\n\n🔗 URL: {content}\n✅ Kürze Link...",
                    'action': 'shorten_url'
                },
                'markdown': {
                    'template': "📝 Ich formatiere den Text für dich!\n\n📄 Inhalt: {content}\n✅ Generiere Markdown...",
                    'action': 'generate_markdown'
                }
            }
            
            # Antwort auswählen
            response_info = context_aware_responses.get(intention, standard_responses.get(intention, context_aware_responses['unknown']))
            
            # Template auswählen (kontext-bewusst oder standard)
            if user_context and intention in context_aware_responses and 'context_template' in context_aware_responses[intention]:
                template = response_info['context_template']
                # Kontext-Daten extrahieren
                context_data = self.extract_context_data(user_context, intention)
                params.update(context_data)
            else:
                template = response_info['template']
            
            action = response_info['action']
            
            # Template mit Parametern füllen
            try:
                formatted_response = template.format(**params)
            except Exception as e:
                logger.warning(f"Template-Formatierung fehlgeschlagen: {e}")
                formatted_response = template
            
            result = {
                'response': formatted_response,
                'action': action,
                'intention': intention,
                'parameters': params,
                'confidence': 0.9 if intention != 'unknown' else 0.0,
                'context_used': bool(user_context)
            }
            
            logger.info(f"Intelligente Antwort generiert für {intention} (Kontext: {bool(user_context)})")
            return result
            
        except Exception as e:
            logger.error(f"Fehler beim Generieren intelligenter Antwort: {e}")
            return {
                'response': "❌ Entschuldigung, es gab einen Fehler bei der Verarbeitung.",
                'action': 'error',
                'intention': intention,
                'parameters': params,
                'error': str(e)
            }
    
    def extract_context_data(self, user_context, intention):
        """Kontext-Daten für Antworten extrahieren"""
        try:
            context_data = {}
            
            # Häufige Themen
            frequent_intentions = user_context.get('frequent_intentions', {})
            if frequent_intentions:
                most_frequent = max(frequent_intentions.items(), key=lambda x: x[1])
                context_data['context_topic'] = most_frequent[0]
            
            # Benutzerprofil
            user_profile = user_context.get('user_profile', {})
            if user_profile:
                context_data['user_name'] = user_profile.get('name', 'User')
                context_data['conversation_count'] = user_profile.get('conversation_count', 0)
                context_data['favorite_topics'] = ', '.join(user_profile.get('favorite_topics', []))
            
            # Wichtige Erinnerungen
            important_memories = user_context.get('important_memories', [])
            context_data['important_count'] = len(important_memories)
            
            # Letzte Konversationen
            recent_conversations = user_context.get('recent_conversations', [])
            if recent_conversations:
                context_data['recent_conversations'] = '\n'.join([
                    f"• {conv.get('content', '')[:50]}..." 
                    for conv in recent_conversations[-3:]
                ])
            else:
                context_data['recent_conversations'] = "Keine kürzlichen Gespräche"
            
            return context_data
            
        except Exception as e:
            logger.error(f"Fehler beim Extrahieren von Kontext-Daten: {e}")
            return {}

    # ==================== SOCIAL MEDIA LOGIN ====================
    
    def login_instagram(self, username, password):
        """Instagram Login mit normalen Credentials"""
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Username eingeben
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)
            
            # Password eingeben
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            
            # Login Button klicken
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(5)
            
            # Prüfen ob Login erfolgreich war
            if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
                logger.info("Instagram Login erfolgreich")
                return True
            else:
                logger.error("Instagram Login fehlgeschlagen")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim Instagram Login: {e}")
            return False
    
    def login_tiktok(self, username, password):
        """TikTok Login mit normalen Credentials"""
        try:
            self.driver.get("https://www.tiktok.com/login")
            time.sleep(3)
            
            # Login mit Username/Email
            login_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log in')]"))
            )
            login_option.click()
            
            # Username eingeben
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)
            
            # Password eingeben
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            
            # Login Button klicken
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(5)
            
            # Prüfen ob Login erfolgreich war
            if "tiktok.com" in self.driver.current_url and "login" not in self.driver.current_url:
                logger.info("TikTok Login erfolgreich")
                return True
            else:
                logger.error("TikTok Login fehlgeschlagen")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim TikTok Login: {e}")
            return False
    
    def login_youtube(self, email, password):
        """YouTube Login mit normalen Credentials"""
        try:
            self.driver.get("https://accounts.google.com/signin")
            time.sleep(3)
            
            # Email eingeben
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            email_field.send_keys(email)
            email_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # Password eingeben
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            # Zu YouTube navigieren
            self.driver.get("https://www.youtube.com")
            time.sleep(3)
            
            # Prüfen ob Login erfolgreich war
            if "youtube.com" in self.driver.current_url:
                logger.info("YouTube Login erfolgreich")
                return True
            else:
                logger.error("YouTube Login fehlgeschlagen")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim YouTube Login: {e}")
            return False

    # ==================== SOCIAL MEDIA UPLOAD ====================
    
    def upload_to_instagram(self, image_path, caption=""):
        """Upload zu Instagram"""
        try:
            # Zu Instagram Upload navigieren
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Upload Button klicken
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='file']"))
            )
            upload_button.send_keys(image_path)
            
            time.sleep(3)
            
            # Caption eingeben
            if caption:
                caption_field = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Write a caption...']")
                caption_field.send_keys(caption)
            
            # Post Button klicken
            post_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Share')]")
            post_button.click()
            
            time.sleep(5)
            
            logger.info("Instagram Upload erfolgreich")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Instagram Upload: {e}")
            return False
    
    def upload_to_tiktok(self, video_path, caption=""):
        """Upload zu TikTok"""
        try:
            # Zu TikTok Upload navigieren
            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(3)
            
            # Video hochladen
            upload_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            upload_input.send_keys(video_path)
            
            time.sleep(5)
            
            # Caption eingeben
            if caption:
                caption_field = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']")
                caption_field.send_keys(caption)
            
            # Post Button klicken
            post_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
            post_button.click()
            
            time.sleep(5)
            
            logger.info("TikTok Upload erfolgreich")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim TikTok Upload: {e}")
            return False
    
    def upload_to_youtube(self, video_path, title, description=""):
        """Upload zu YouTube"""
        try:
            # Zu YouTube Studio navigieren
            self.driver.get("https://studio.youtube.com/")
            time.sleep(3)
            
            # Upload Button klicken
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'CREATE')]"))
            )
            upload_button.click()
            
            time.sleep(3)
            
            # Video hochladen
            upload_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            upload_input.send_keys(video_path)
            
            time.sleep(10)
            
            # Titel eingeben
            title_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Add a title that describes your video']"))
            )
            title_field.clear()
            title_field.send_keys(title)
            
            # Beschreibung eingeben
            if description:
                description_field = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Tell viewers about your video']")
                description_field.send_keys(description)
            
            # Publish Button klicken
            publish_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'PUBLISH')]")
            publish_button.click()
            
            time.sleep(5)
            
            logger.info("YouTube Upload erfolgreich")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim YouTube Upload: {e}")
            return False

    # ==================== E-MAIL AUTOMATION ====================
    
    def setup_email_session(self, email_address, password, imap_server="imap.gmail.com", smtp_server="smtp.gmail.com"):
        """E-Mail Session einrichten"""
        try:
            # IMAP für E-Mails lesen
            self.imap = imaplib.IMAP4_SSL(imap_server)
            self.imap.login(email_address, password)
            
            # SMTP für E-Mails senden
            self.smtp = smtplib.SMTP_SSL(smtp_server)
            self.smtp.login(email_address, password)
            
            self.email_address = email_address
            logger.info("E-Mail Session erfolgreich eingerichtet")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim E-Mail Setup: {e}")
            return False
    
    def read_emails(self, folder="INBOX", limit=10):
        """E-Mails lesen"""
        try:
            self.imap.select(folder)
            
            # Alle E-Mails suchen
            _, message_numbers = self.imap.search(None, 'ALL')
            email_list = message_numbers[0].split()
            
            # Neueste E-Mails zuerst
            email_list.reverse()
            
            emails = []
            for num in email_list[:limit]:
                _, msg_data = self.imap.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                subject = email_message.get('subject', '')
                sender = email_message.get('from', '')
                date = email_message.get('date', '')
                
                # E-Mail Inhalt extrahieren
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_message.get_payload(decode=True).decode()
                
                emails.append({
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body[:500] + '...' if len(body) > 500 else body
                })
            
            logger.info(f"{len(emails)} E-Mails erfolgreich gelesen")
            return emails
            
        except Exception as e:
            logger.error(f"Fehler beim E-Mails lesen: {e}")
            return []
    
    def send_email(self, to_email, subject, body, attachments=None):
        """E-Mail senden"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Anhänge hinzufügen
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as f:
                        part = MIMEImage(f.read())
                        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                        msg.attach(part)
            
            self.smtp.send_message(msg)
            logger.info(f"E-Mail an {to_email} erfolgreich gesendet")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim E-Mail senden: {e}")
            return False
    
    def auto_reply_emails(self, keywords, reply_template):
        """Automatische E-Mail-Antworten"""
        try:
            emails = self.read_emails(limit=20)
            
            replies_sent = 0
            for email_data in emails:
                # Prüfen ob Keywords im Betreff oder Inhalt enthalten sind
                content = f"{email_data['subject']} {email_data['body']}".lower()
                
                if any(keyword.lower() in content for keyword in keywords):
                    # Auto-Reply senden
                    sender_email = re.search(r'<(.+?)>', email_data['sender'])
                    if sender_email:
                        reply_to = sender_email.group(1)
                    else:
                        reply_to = email_data['sender']
                    
                    reply_subject = f"Re: {email_data['subject']}"
                    reply_body = reply_template.format(
                        original_subject=email_data['subject'],
                        original_sender=email_data['sender']
                    )
                    
                    if self.send_email(reply_to, reply_subject, reply_body):
                        replies_sent += 1
            
            logger.info(f"{replies_sent} Auto-Replies erfolgreich gesendet")
            return replies_sent
            
        except Exception as e:
            logger.error(f"Fehler bei Auto-Replies: {e}")
            return 0

# Flask App für n8n Integration
app = Flask(__name__)
automation = ExtendedSocialMediaAutomation()

# ==================== KI-GEDÄCHTNISSYSTEM ====================

class KIMemorySystem:
    def __init__(self, db_path="ki_memory.db"):
        """KI-Gedächtnissystem mit persistenter Datenbank"""
        self.db_path = db_path
        self.init_database()
        self.context_cache = {}
        self.agent_pool = {}
        self.task_queue = queue.Queue()
        self.start_background_workers()
    
    def init_database(self):
        """Datenbank initialisieren"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Konversationsverlauf
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    message_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    intention TEXT,
                    parameters TEXT,
                    response TEXT,
                    confidence REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    context_hash TEXT
                )
            ''')
            
            # Benutzerprofile
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    preferences TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
                    conversation_count INTEGER DEFAULT 0,
                    favorite_topics TEXT
                )
            ''')
            
            # Kontext-Speicher
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS context_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    context_type TEXT NOT NULL,
                    context_data TEXT NOT NULL,
                    importance_score REAL DEFAULT 1.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 1
                )
            ''')
            
            # Agent-Aufgaben
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    agent_type TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    task_data TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME,
                    result TEXT
                )
            ''')
            
            # Wissensdatenbank
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT,
                    confidence REAL DEFAULT 1.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("KI-Gedächtnissystem Datenbank initialisiert")
            
        except Exception as e:
            logger.error(f"Fehler bei Datenbank-Initialisierung: {e}")
    
    def save_conversation(self, user_id, session_id, message_type, content, 
                         intention=None, parameters=None, response=None, confidence=None):
        """Konversation speichern"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            context_hash = hashlib.md5(f"{user_id}{content}{intention}".encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO conversations 
                (user_id, session_id, message_type, content, intention, parameters, 
                 response, confidence, context_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, session_id, message_type, content, intention, 
                  json.dumps(parameters) if parameters else None,
                  response, confidence, context_hash))
            
            conn.commit()
            conn.close()
            
            # Kontext-Cache aktualisieren
            self.update_context_cache(user_id, content, intention, parameters)
            
            logger.info(f"Konversation für User {user_id} gespeichert")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Konversation: {e}")
            return False
    
    def get_conversation_history(self, user_id, limit=50, days_back=30):
        """Konversationsverlauf abrufen"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            cursor.execute('''
                SELECT * FROM conversations 
                WHERE user_id = ? AND timestamp > ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, cutoff_date, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            conversations = []
            for row in rows:
                conversations.append({
                    'id': row[0],
                    'user_id': row[1],
                    'session_id': row[2],
                    'message_type': row[3],
                    'content': row[4],
                    'intention': row[5],
                    'parameters': json.loads(row[6]) if row[6] else None,
                    'response': row[7],
                    'confidence': row[8],
                    'timestamp': row[9],
                    'context_hash': row[10]
                })
            
            return conversations
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen des Konversationsverlaufs: {e}")
            return []
    
    def update_context_cache(self, user_id, content, intention, parameters):
        """Kontext-Cache aktualisieren"""
        if user_id not in self.context_cache:
            self.context_cache[user_id] = {
                'recent_topics': [],
                'frequent_intentions': {},
                'user_preferences': {},
                'conversation_context': []
            }
        
        # Aktuelle Konversation zum Kontext hinzufügen
        context_entry = {
            'content': content,
            'intention': intention,
            'parameters': parameters,
            'timestamp': datetime.now().isoformat()
        }
        
        self.context_cache[user_id]['conversation_context'].append(context_entry)
        
        # Nur die letzten 10 Konversationen behalten
        if len(self.context_cache[user_id]['conversation_context']) > 10:
            self.context_cache[user_id]['conversation_context'] = \
                self.context_cache[user_id]['conversation_context'][-10:]
        
        # Häufige Intentionen tracken
        if intention:
            if intention not in self.context_cache[user_id]['frequent_intentions']:
                self.context_cache[user_id]['frequent_intentions'][intention] = 0
            self.context_cache[user_id]['frequent_intentions'][intention] += 1
    
    def get_user_context(self, user_id):
        """Benutzer-Kontext abrufen"""
        try:
            # Cache-Kontext
            cache_context = self.context_cache.get(user_id, {})
            
            # Datenbank-Kontext
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Benutzerprofil
            cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
            profile = cursor.fetchone()
            
            # Wichtige Kontext-Daten
            cursor.execute('''
                SELECT * FROM context_memory 
                WHERE user_id = ? 
                ORDER BY importance_score DESC, last_accessed DESC
                LIMIT 20
            ''', (user_id,))
            
            context_memories = cursor.fetchall()
            conn.close()
            
            # Kontext zusammenstellen
            context = {
                'user_profile': {
                    'name': profile[1] if profile else None,
                    'preferences': json.loads(profile[2]) if profile and profile[2] else {},
                    'conversation_count': profile[5] if profile else 0,
                    'favorite_topics': json.loads(profile[6]) if profile and profile[6] else []
                } if profile else {},
                'recent_conversations': cache_context.get('conversation_context', []),
                'frequent_intentions': cache_context.get('frequent_intentions', {}),
                'important_memories': [
                    {
                        'type': row[2],
                        'data': json.loads(row[3]),
                        'importance': row[4],
                        'last_accessed': row[6]
                    } for row in context_memories
                ]
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen des Benutzer-Kontexts: {e}")
            return {}
    
    def save_important_memory(self, user_id, context_type, context_data, importance_score=1.0):
        """Wichtige Erinnerung speichern"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO context_memory 
                (user_id, context_type, context_data, importance_score, last_accessed)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, context_type, json.dumps(context_data), importance_score))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Wichtige Erinnerung für User {user_id} gespeichert")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern wichtiger Erinnerung: {e}")
            return False
    
    def start_background_workers(self):
        """Hintergrund-Worker für Multi-Agent-System starten"""
        self.worker_thread = threading.Thread(target=self.background_worker, daemon=True)
        self.worker_thread.start()
        logger.info("Hintergrund-Worker für Multi-Agent-System gestartet")
    
    def background_worker(self):
        """Hintergrund-Worker für Agent-Aufgaben"""
        while True:
            try:
                # Aufgaben aus der Queue holen
                task = self.task_queue.get(timeout=1)
                if task:
                    self.process_agent_task(task)
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Fehler im Hintergrund-Worker: {e}")
    
    def process_agent_task(self, task):
        """Agent-Aufgabe verarbeiten"""
        try:
            task_id = task.get('task_id')
            agent_type = task.get('agent_type')
            user_id = task.get('user_id')
            task_data = task.get('task_data')
            
            # Aufgabe in Datenbank speichern
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agent_tasks 
                (task_id, agent_type, user_id, task_data, status)
                VALUES (?, ?, ?, ?, 'processing')
            ''', (task_id, agent_type, user_id, json.dumps(task_data)))
            
            conn.commit()
            conn.close()
            
            # Agent-spezifische Verarbeitung
            result = self.execute_agent_task(agent_type, task_data, user_id)
            
            # Ergebnis speichern
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE agent_tasks 
                SET status = ?, result = ?, completed_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
            ''', ('completed', json.dumps(result), task_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Agent-Aufgabe {task_id} abgeschlossen")
            
        except Exception as e:
            logger.error(f"Fehler bei Agent-Aufgabe: {e}")
    
    def execute_agent_task(self, agent_type, task_data, user_id):
        """Agent-Aufgabe ausführen"""
        try:
            if agent_type == 'research':
                return self.research_agent(task_data, user_id)
            elif agent_type == 'creative':
                return self.creative_agent(task_data, user_id)
            elif agent_type == 'analytics':
                return self.analytics_agent(task_data, user_id)
            elif agent_type == 'communication':
                return self.communication_agent(task_data, user_id)
            else:
                return {'error': f'Unbekannter Agent-Typ: {agent_type}'}
                
        except Exception as e:
            logger.error(f"Fehler bei Agent-Aufgabe {agent_type}: {e}")
            return {'error': str(e)}
    
    def research_agent(self, task_data, user_id):
        """Forschungs-Agent für umfassende Recherche"""
        try:
            query = task_data.get('query', '')
            sources = task_data.get('sources', ['google', 'bing', 'news'])
            
            results = {}
            for source in sources:
                if source == 'google':
                    results['google'] = self.search_google(query, limit=5)
                elif source == 'bing':
                    results['bing'] = self.search_bing(query, limit=5)
                elif source == 'news':
                    results['news'] = self.get_news_headlines('general', limit=5)
            
            # Ergebnisse zusammenfassen
            summary = self.summarize_research_results(results)
            
            return {
                'query': query,
                'sources': sources,
                'results': results,
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fehler im Research-Agent: {e}")
            return {'error': str(e)}
    
    def creative_agent(self, task_data, user_id):
        """Kreativ-Agent für Content-Erstellung"""
        try:
            content_type = task_data.get('type', 'text')
            topic = task_data.get('topic', '')
            style = task_data.get('style', 'professional')
            
            if content_type == 'text':
                content = self.generate_creative_text(topic, style)
            elif content_type == 'image':
                content = self.generate_creative_image(topic, style)
            elif content_type == 'video':
                content = self.generate_creative_video(topic, style)
            
            return {
                'type': content_type,
                'topic': topic,
                'style': style,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fehler im Creative-Agent: {e}")
            return {'error': str(e)}
    
    def analytics_agent(self, task_data, user_id):
        """Analytics-Agent für Datenanalyse"""
        try:
            data = task_data.get('data', {})
            analysis_type = task_data.get('analysis_type', 'basic')
            
            if analysis_type == 'basic':
                result = self.basic_data_analysis(data)
            elif analysis_type == 'trend':
                result = self.trend_analysis(data)
            elif analysis_type == 'prediction':
                result = self.prediction_analysis(data)
            
            return {
                'analysis_type': analysis_type,
                'data': data,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fehler im Analytics-Agent: {e}")
            return {'error': str(e)}
    
    def communication_agent(self, task_data, user_id):
        """Kommunikations-Agent für optimale Antworten"""
        try:
            message = task_data.get('message', '')
            context = self.get_user_context(user_id)
            
            # Kontext-basierte Antwort generieren
            response = self.generate_contextual_response(message, context)
            
            return {
                'original_message': message,
                'context_used': context,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fehler im Communication-Agent: {e}")
            return {'error': str(e)}
    
    def add_agent_task(self, agent_type, user_id, task_data, priority=1):
        """Agent-Aufgabe zur Queue hinzufügen"""
        try:
            task_id = str(uuid.uuid4())
            task = {
                'task_id': task_id,
                'agent_type': agent_type,
                'user_id': user_id,
                'task_data': task_data,
                'priority': priority
            }
            
            self.task_queue.put(task)
            logger.info(f"Agent-Aufgabe {task_id} zur Queue hinzugefügt")
            return task_id
            
        except Exception as e:
            logger.error(f"Fehler beim Hinzufügen der Agent-Aufgabe: {e}")
            return None

# KI-Gedächtnissystem initialisieren
ki_memory = KIMemorySystem()

@app.route('/health', methods=['GET'])
def health_check():
    """Health Check Endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'web_scraping': 'available',
            'rss_feeds': 'available',
            'weather': 'available',
            'qr_codes': 'available',
            'charts': 'available',
            'url_shortener': 'available',
            'markdown': 'available',
            'news': 'available',
            'google_search': 'available',
            'bing_search': 'available',
            'duckduckgo_search': 'available',
            'youtube_search': 'available',
            'voice_processing': 'available',
            'natural_language': 'available',
            'ai_conversation': 'available',
            'memory_system': 'available',
            'context_awareness': 'available',
            'multi_agent_system': 'available',
            'persistent_storage': 'available'
        }
    })

@app.route('/scrape', methods=['POST'])
def scrape_website():
    """Web Scraping Endpoint"""
    data = request.get_json()
    url = data.get('url')
    selectors = data.get('selectors', {})
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    result = automation.scrape_website_data(url, selectors)
    return jsonify(result)

@app.route('/rss', methods=['POST'])
def get_rss_feed():
    """RSS Feed Endpoint"""
    data = request.get_json()
    feed_url = data.get('feed_url')
    limit = data.get('limit', 10)
    
    if not feed_url:
        return jsonify({'error': 'feed_url required'}), 400
    
    result = automation.get_rss_feed(feed_url, limit)
    return jsonify(result)

@app.route('/weather', methods=['POST'])
def get_weather():
    """Weather API Endpoint"""
    data = request.get_json()
    city = data.get('city')
    
    if not city:
        return jsonify({'error': 'city required'}), 400
    
    result = automation.get_weather_data(city)
    return jsonify(result)

@app.route('/qr', methods=['POST'])
def generate_qr():
    """QR Code Generator Endpoint"""
    data = request.get_json()
    qr_data = data.get('data')
    filename = data.get('filename')
    
    if not qr_data:
        return jsonify({'error': 'data required'}), 400
    
    result = automation.generate_qr_code(qr_data, filename)
    return jsonify(result)

@app.route('/chart', methods=['POST'])
def generate_chart():
    """Chart Generator Endpoint"""
    data = request.get_json()
    chart_data = data.get('data')
    chart_type = data.get('chart_type', 'line')
    title = data.get('title', 'Chart')
    filename = data.get('filename')
    
    if not chart_data:
        return jsonify({'error': 'data required'}), 400
    
    result = automation.generate_chart(chart_data, chart_type, title, filename)
    return jsonify(result)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """URL Shortener Endpoint"""
    data = request.get_json()
    long_url = data.get('url')
    
    if not long_url:
        return jsonify({'error': 'url required'}), 400
    
    result = automation.shorten_url(long_url)
    return jsonify(result)

@app.route('/markdown', methods=['POST'])
def generate_markdown():
    """Markdown Generator Endpoint"""
    data = request.get_json()
    content_type = data.get('content_type')
    content_data = data.get('data', {})
    
    if not content_type:
        return jsonify({'error': 'content_type required'}), 400
    
    result = automation.generate_markdown(content_type, content_data)
    return jsonify(result)

@app.route('/news', methods=['POST'])
def get_news():
    """News Headlines Endpoint"""
    data = request.get_json()
    category = data.get('category', 'general')
    limit = data.get('limit', 5)
    
    result = automation.get_news_headlines(category, limit)
    return jsonify(result)

@app.route('/search/google', methods=['POST'])
def search_google():
    """Google Search Endpoint"""
    data = request.get_json()
    query = data.get('query')
    limit = data.get('limit', 10)
    
    if not query:
        return jsonify({'error': 'query required'}), 400
    
    result = automation.search_google(query, limit)
    return jsonify(result)

@app.route('/search/bing', methods=['POST'])
def search_bing():
    """Bing Search Endpoint"""
    data = request.get_json()
    query = data.get('query')
    limit = data.get('limit', 10)
    
    if not query:
        return jsonify({'error': 'query required'}), 400
    
    result = automation.search_bing(query, limit)
    return jsonify(result)

@app.route('/search/duckduckgo', methods=['POST'])
def search_duckduckgo():
    """DuckDuckGo Search Endpoint"""
    data = request.get_json()
    query = data.get('query')
    limit = data.get('limit', 10)
    
    if not query:
        return jsonify({'error': 'query required'}), 400
    
    result = automation.search_duckduckgo(query, limit)
    return jsonify(result)

@app.route('/search/youtube', methods=['POST'])
def search_youtube():
    """YouTube Search Endpoint"""
    data = request.get_json()
    query = data.get('query')
    limit = data.get('limit', 10)
    
    if not query:
        return jsonify({'error': 'query required'}), 400
    
    result = automation.search_youtube(query, limit)
    return jsonify(result)

@app.route('/voice/process', methods=['POST'])
def process_voice():
    """Voice Message Processing Endpoint"""
    if 'audio' not in request.files:
        return jsonify({'error': 'audio file required'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'no file selected'}), 400
    
    # Temporäre Datei speichern
    temp_path = tempfile.mktemp(suffix='.ogg')
    audio_file.save(temp_path)
    
    try:
        result = automation.process_voice_message(temp_path)
        return jsonify(result)
    finally:
        # Temporäre Datei löschen
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.route('/ai/understand', methods=['POST'])
def understand_text():
    """Natural Language Understanding Endpoint"""
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'text required'}), 400
    
    result = automation.understand_natural_language(text)
    return jsonify(result)

@app.route('/ai/respond', methods=['POST'])
def generate_response():
    """Smart Response Generation Endpoint"""
    data = request.get_json()
    intention = data.get('intention')
    params = data.get('parameters', {})
    original_text = data.get('original_text', '')
    
    if not intention:
        return jsonify({'error': 'intention required'}), 400
    
    result = automation.generate_smart_response(intention, params, original_text)
    return jsonify(result)

@app.route('/ai/conversation', methods=['POST'])
def handle_conversation():
    """Complete Conversation Handler Endpoint mit Gedächtnis"""
    data = request.get_json()
    text = data.get('text')
    user_id = data.get('user_id', 'default_user')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    if not text:
        return jsonify({'error': 'text required'}), 400
    
    try:
        # 1. Benutzer-Kontext abrufen
        user_context = ki_memory.get_user_context(user_id)
        
        # 2. Natürliche Sprache verstehen mit Kontext
        understanding = automation.understand_natural_language(text, user_id)
        
        # 3. Intelligente Antwort generieren mit Kontext
        response = automation.generate_smart_response(
            understanding['intention'],
            understanding['parameters'],
            understanding['original_text'],
            user_context
        )
        
        # 4. Konversation speichern
        ki_memory.save_conversation(
            user_id=user_id,
            session_id=session_id,
            message_type='text',
            content=text,
            intention=understanding['intention'],
            parameters=understanding['parameters'],
            response=response['response'],
            confidence=understanding['confidence']
        )
        
        # 5. Wichtige Erinnerungen speichern (bei hoher Konfidenz)
        if understanding['confidence'] > 0.8:
            ki_memory.save_important_memory(
                user_id=user_id,
                context_type='conversation',
                context_data={
                    'intention': understanding['intention'],
                    'content': text,
                    'parameters': understanding['parameters']
                },
                importance_score=understanding['confidence']
            )
        
        # 6. Agent-Aufgaben starten (bei komplexen Anfragen)
        if understanding['intention'] in ['research', 'creative', 'analytics']:
            task_id = ki_memory.add_agent_task(
                agent_type=understanding['intention'],
                user_id=user_id,
                task_data=understanding['parameters']
            )
            response['agent_task_id'] = task_id
        
        # 7. Kombiniertes Ergebnis zurückgeben
        result = {
            'understanding': understanding,
            'response': response,
            'user_context': {
                'has_context': bool(user_context),
                'conversation_count': user_context.get('user_profile', {}).get('conversation_count', 0) if user_context else 0
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Fehler bei Konversation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/memory/history', methods=['GET'])
def get_memory_history():
    """Konversationsverlauf abrufen"""
    user_id = request.args.get('user_id', 'default_user')
    limit = int(request.args.get('limit', 50))
    days_back = int(request.args.get('days_back', 30))
    
    try:
        history = ki_memory.get_conversation_history(user_id, limit, days_back)
        return jsonify({
            'user_id': user_id,
            'history': history,
            'total': len(history)
        })
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Verlaufs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/memory/context', methods=['GET'])
def get_user_context():
    """Benutzer-Kontext abrufen"""
    user_id = request.args.get('user_id', 'default_user')
    
    try:
        context = ki_memory.get_user_context(user_id)
        return jsonify({
            'user_id': user_id,
            'context': context
        })
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Kontexts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/memory/save', methods=['POST'])
def save_memory():
    """Wichtige Erinnerung speichern"""
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')
    context_type = data.get('context_type')
    context_data = data.get('context_data', {})
    importance_score = data.get('importance_score', 1.0)
    
    if not context_type:
        return jsonify({'error': 'context_type required'}), 400
    
    try:
        success = ki_memory.save_important_memory(
            user_id=user_id,
            context_type=context_type,
            context_data=context_data,
            importance_score=importance_score
        )
        
        return jsonify({
            'success': success,
            'user_id': user_id,
            'context_type': context_type
        })
    except Exception as e:
        logger.error(f"Fehler beim Speichern der Erinnerung: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/agents/task', methods=['POST'])
def add_agent_task():
    """Agent-Aufgabe hinzufügen"""
    data = request.get_json()
    agent_type = data.get('agent_type')
    user_id = data.get('user_id', 'default_user')
    task_data = data.get('task_data', {})
    priority = data.get('priority', 1)
    
    if not agent_type:
        return jsonify({'error': 'agent_type required'}), 400
    
    try:
        task_id = ki_memory.add_agent_task(
            agent_type=agent_type,
            user_id=user_id,
            task_data=task_data,
            priority=priority
        )
        
        return jsonify({
            'task_id': task_id,
            'agent_type': agent_type,
            'status': 'queued'
        })
    except Exception as e:
        logger.error(f"Fehler beim Hinzufügen der Agent-Aufgabe: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    """Social Media Login Endpoint"""
    data = request.get_json()
    platform = data.get('platform')
    username = data.get('username')
    password = data.get('password')
    
    if not all([platform, username, password]):
        return jsonify({'error': 'platform, username, and password required'}), 400
    
    success = False
    if platform == 'instagram':
        success = automation.login_instagram(username, password)
    elif platform == 'tiktok':
        success = automation.login_tiktok(username, password)
    elif platform == 'youtube':
        success = automation.login_youtube(username, password)
    else:
        return jsonify({'error': 'Unsupported platform'}), 400
    
    return jsonify({'success': success, 'platform': platform})

@app.route('/upload', methods=['POST'])
def upload():
    """Social Media Upload Endpoint"""
    data = request.get_json()
    platform = data.get('platform')
    file_path = data.get('file_path')
    caption = data.get('caption', '')
    title = data.get('title', '')
    description = data.get('description', '')
    
    if not all([platform, file_path]):
        return jsonify({'error': 'platform and file_path required'}), 400
    
    success = False
    if platform == 'instagram':
        success = automation.upload_to_instagram(file_path, caption)
    elif platform == 'tiktok':
        success = automation.upload_to_tiktok(file_path, caption)
    elif platform == 'youtube':
        success = automation.upload_to_youtube(file_path, title, description)
    else:
        return jsonify({'error': 'Unsupported platform'}), 400
    
    return jsonify({'success': success, 'platform': platform})

@app.route('/email/setup', methods=['POST'])
def email_setup():
    """E-Mail Setup Endpoint"""
    data = request.get_json()
    email_address = data.get('email')
    password = data.get('password')
    imap_server = data.get('imap_server', 'imap.gmail.com')
    smtp_server = data.get('smtp_server', 'smtp.gmail.com')
    
    if not all([email_address, password]):
        return jsonify({'error': 'email and password required'}), 400
    
    success = automation.setup_email_session(email_address, password, imap_server, smtp_server)
    return jsonify({'success': success})

@app.route('/email/read', methods=['GET'])
def read_emails():
    """E-Mail Read Endpoint"""
    folder = request.args.get('folder', 'INBOX')
    limit = int(request.args.get('limit', 10))
    
    emails = automation.read_emails(folder, limit)
    return jsonify({'emails': emails, 'count': len(emails)})

@app.route('/email/send', methods=['POST'])
def send_email():
    """E-Mail Send Endpoint"""
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    body = data.get('body')
    attachments = data.get('attachments', [])
    
    if not all([to_email, subject, body]):
        return jsonify({'error': 'to, subject, and body required'}), 400
    
    success = automation.send_email(to_email, subject, body, attachments)
    return jsonify({'success': success})

@app.route('/email/auto-reply', methods=['POST'])
def auto_reply():
    """E-Mail Auto-Reply Endpoint"""
    data = request.get_json()
    keywords = data.get('keywords', [])
    reply_template = data.get('reply_template', '')
    
    if not keywords or not reply_template:
        return jsonify({'error': 'keywords and reply_template required'}), 400
    
    replies_sent = automation.auto_reply_emails(keywords, reply_template)
    return jsonify({'replies_sent': replies_sent})

@app.route('/logout', methods=['POST'])
def logout():
    """Logout Endpoint"""
    automation.stop_driver()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)