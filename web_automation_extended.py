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

    def understand_natural_language(self, text):
        """Natürliche Sprache verstehen - Kostenlos, keine API-Keys nötig"""
        try:
            text = text.lower().strip()
            
            # Intention erkennen
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
                'help': ['hilfe', 'help', 'was', 'kannst', 'du', 'machen']
            }
            
            detected_intention = None
            confidence = 0.0
            
            for intention, keywords in intentions.items():
                for keyword in keywords:
                    if keyword in text:
                        detected_intention = intention
                        confidence = 0.8
                        break
                if detected_intention:
                    break
            
            # Parameter extrahieren
            params = {}
            
            if detected_intention == 'search':
                # Suchmaschine erkennen
                search_engines = ['google', 'bing', 'duckduckgo', 'youtube']
                for engine in search_engines:
                    if engine in text:
                        params['engine'] = engine
                        break
                
                # Query extrahieren (alles nach "suche", "finde", etc.)
                search_words = ['suche', 'finde', 'search', 'google', 'bing', 'youtube']
                for word in search_words:
                    if word in text:
                        query_start = text.find(word) + len(word)
                        params['query'] = text[query_start:].strip()
                        break
            
            elif detected_intention == 'weather':
                # Stadt extrahieren
                weather_words = ['wetter', 'weather', 'in', 'für']
                for word in weather_words:
                    if word in text:
                        city_start = text.find(word) + len(word)
                        params['city'] = text[city_start:].strip()
                        break
            
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
                'parameters': params
            }
            
            logger.info(f"Natürliche Sprache verstanden: {detected_intention} mit {confidence} Konfidenz")
            return result
            
        except Exception as e:
            logger.error(f"Fehler beim Verstehen natürlicher Sprache: {e}")
            return {
                'intention': 'unknown',
                'confidence': 0.0,
                'original_text': text,
                'parameters': {},
                'error': str(e)
            }

    def generate_smart_response(self, intention, params, original_text):
        """Intelligente Antwort generieren - Kostenlos, keine API-Keys nötig"""
        try:
            responses = {
                'video': {
                    'template': "🎬 Ich erstelle ein Avatar-Video für dich!\n\n📝 Text: {content}\n✅ Verarbeite mit ElevenLabs + D-ID...",
                    'action': 'create_video'
                },
                'photo': {
                    'template': "📸 Ich suche ein passendes Foto für dich!\n\n🔍 Beschreibung: {content}\n✅ Verarbeite mit Unsplash...",
                    'action': 'get_photo'
                },
                'search': {
                    'template': "🔍 Ich suche das für dich!\n\n🔎 Suchmaschine: {engine}\n📋 Query: {query}\n✅ Führe Suche durch...",
                    'action': 'perform_search'
                },
                'weather': {
                    'template': "🌤️ Ich schaue nach dem Wetter für dich!\n\n🏙️ Stadt: {city}\n✅ Hole Wetterdaten...",
                    'action': 'get_weather'
                },
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
                },
                'help': {
                    'template': """🤖 Ich bin dein intelligenter Assistent!

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

💬 **Sprich einfach mit mir:**
"Erstelle ein Video über KI"
"Suche nach Python Tutorials"
"Wie ist das Wetter in Berlin?"
"Zeig mir die neuesten Nachrichten"

🎤 **Oder sende Sprachmemos!**

🆓 **Alles kostenlos - keine API-Keys nötig!**""",
                    'action': 'show_help'
                },
                'unknown': {
                    'template': "🤔 Entschuldigung, ich habe dich nicht verstanden.\n\n💡 Tippe 'Hilfe' oder 'Help' für eine Übersicht meiner Fähigkeiten!",
                    'action': 'unknown'
                }
            }
            
            response_info = responses.get(intention, responses['unknown'])
            template = response_info['template']
            action = response_info['action']
            
            # Template mit Parametern füllen
            try:
                formatted_response = template.format(**params)
            except:
                formatted_response = template
            
            result = {
                'response': formatted_response,
                'action': action,
                'intention': intention,
                'parameters': params,
                'confidence': 0.9 if intention != 'unknown' else 0.0
            }
            
            logger.info(f"Intelligente Antwort generiert für {intention}")
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
            'ai_conversation': 'available'
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
    """Complete Conversation Handler Endpoint"""
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'text required'}), 400
    
    # 1. Natürliche Sprache verstehen
    understanding = automation.understand_natural_language(text)
    
    # 2. Intelligente Antwort generieren
    response = automation.generate_smart_response(
        understanding['intention'],
        understanding['parameters'],
        understanding['original_text']
    )
    
    # 3. Kombiniertes Ergebnis zurückgeben
    result = {
        'understanding': understanding,
        'response': response,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(result)

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