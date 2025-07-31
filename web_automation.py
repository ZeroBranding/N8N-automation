#!/usr/bin/env python3
"""
Web Automation Tool für Social Media Plattformen
Verwendet normale Login-Daten anstatt API-Keys
"""

import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from flask import Flask, request, jsonify

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialMediaAutomation:
    def __init__(self, headless=True):
        """Initialisiert den Web Driver"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = None
        
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
            
            # Warten auf Login
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
            
            if "tiktok.com" in self.driver.current_url and "login" not in self.driver.current_url:
                logger.info("TikTok Login erfolgreich")
                return True
            else:
                logger.error("TikTok Login fehlgeschlagen")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim TikTok Login: {e}")
            return False
    
    def get_instagram_posts(self, username, count=10):
        """Holt Instagram Posts eines Users"""
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(3)
            
            posts = []
            post_elements = self.driver.find_elements(By.XPATH, "//article//img")
            
            for i, post in enumerate(post_elements[:count]):
                try:
                    post_data = {
                        "image_url": post.get_attribute("src"),
                        "alt_text": post.get_attribute("alt"),
                        "post_number": i + 1
                    }
                    posts.append(post_data)
                except:
                    continue
            
            return posts
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Instagram Posts: {e}")
            return []
    
    def get_tiktok_videos(self, username, count=10):
        """Holt TikTok Videos eines Users"""
        try:
            self.driver.get(f"https://www.tiktok.com/@{username}")
            time.sleep(3)
            
            videos = []
            video_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'video-feed')]//video")
            
            for i, video in enumerate(video_elements[:count]):
                try:
                    video_data = {
                        "video_url": video.get_attribute("src"),
                        "poster": video.get_attribute("poster"),
                        "video_number": i + 1
                    }
                    videos.append(video_data)
                except:
                    continue
            
            return videos
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der TikTok Videos: {e}")
            return []

# Flask API für n8n Integration
app = Flask(__name__)
automation = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health Check Endpoint"""
    return jsonify({"status": "healthy", "message": "Web Automation API läuft"})

@app.route('/login', methods=['POST'])
def login():
    """Login Endpoint für verschiedene Plattformen"""
    global automation
    
    data = request.json
    platform = data.get('platform')
    username = data.get('username')
    password = data.get('password')
    
    if not automation:
        automation = SocialMediaAutomation(headless=True)
        if not automation.start_driver():
            return jsonify({"error": "Driver konnte nicht gestartet werden"}), 500
    
    try:
        if platform.lower() == 'instagram':
            success = automation.login_instagram(username, password)
        elif platform.lower() == 'tiktok':
            success = automation.login_tiktok(username, password)
        else:
            return jsonify({"error": "Plattform nicht unterstützt"}), 400
        
        if success:
            return jsonify({"status": "success", "message": f"Login zu {platform} erfolgreich"})
        else:
            return jsonify({"status": "error", "message": f"Login zu {platform} fehlgeschlagen"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts', methods=['GET'])
def get_posts():
    """Holt Posts/Videos von einer Plattform"""
    global automation
    
    if not automation:
        return jsonify({"error": "Nicht eingeloggt"}), 401
    
    platform = request.args.get('platform')
    username = request.args.get('username')
    count = int(request.args.get('count', 10))
    
    try:
        if platform.lower() == 'instagram':
            posts = automation.get_instagram_posts(username, count)
        elif platform.lower() == 'tiktok':
            posts = automation.get_tiktok_videos(username, count)
        else:
            return jsonify({"error": "Plattform nicht unterstützt"}), 400
        
        return jsonify({"status": "success", "data": posts})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['POST'])
def logout():
    """Logout und Driver stoppen"""
    global automation
    
    if automation:
        automation.stop_driver()
        automation = None
    
    return jsonify({"status": "success", "message": "Logout erfolgreich"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)