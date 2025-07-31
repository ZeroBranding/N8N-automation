#!/usr/bin/env python3
"""
Erweiterte Web Automation für Social Media und E-Mail
Verwendet normale Login-Daten anstatt API-Keys
"""

import time
import json
import logging
import smtplib
import imaplib
import email
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
import requests
from flask import Flask, request, jsonify
import os
from PIL import Image
import io
import base64

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            
            # Zu YouTube Studio navigieren
            self.driver.get("https://studio.youtube.com")
            time.sleep(3)
            
            if "youtube.com" in self.driver.current_url:
                logger.info("YouTube Login erfolgreich")
                return True
            else:
                logger.error("YouTube Login fehlgeschlagen")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim YouTube Login: {e}")
            return False
    
    # ==================== UPLOAD FUNCTIONS ====================
    
    def upload_to_instagram(self, image_path, caption=""):
        """Upload zu Instagram"""
        try:
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Plus Button klicken
            plus_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/create/select/')]"))
            )
            plus_button.click()
            
            time.sleep(2)
            
            # Datei hochladen
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(image_path)
            
            time.sleep(3)
            
            # Weiter Button
            next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
            next_button.click()
            
            time.sleep(2)
            
            # Filter anwenden (optional)
            filter_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
            filter_button.click()
            
            time.sleep(2)
            
            # Caption eingeben
            if caption:
                caption_field = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Write a caption...']")
                caption_field.send_keys(caption)
            
            # Teilen Button
            share_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Share')]")
            share_button.click()
            
            time.sleep(5)
            
            logger.info("Instagram Upload erfolgreich")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Instagram Upload: {e}")
            return False
    
    def upload_to_tiktok(self, video_path, caption=""):
        """Upload zu TikTok"""
        try:
            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(3)
            
            # Datei hochladen
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(video_path)
            
            time.sleep(5)
            
            # Caption eingeben
            if caption:
                caption_field = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']")
                caption_field.send_keys(caption)
            
            # Post Button
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
            self.driver.get("https://studio.youtube.com")
            time.sleep(3)
            
            # Upload Button
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'CREATE')]"))
            )
            upload_button.click()
            
            time.sleep(2)
            
            # Upload Video Option
            upload_video = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Upload video')]")
            upload_video.click()
            
            time.sleep(2)
            
            # Datei hochladen
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(video_path)
            
            time.sleep(10)
            
            # Titel eingeben
            title_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Add a title that describes your video']"))
            )
            title_field.clear()
            title_field.send_keys(title)
            
            # Beschreibung eingeben
            if description:
                description_field = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Tell viewers about your video']")
                description_field.send_keys(description)
            
            # Publish Button
            publish_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Publish')]")
            publish_button.click()
            
            time.sleep(5)
            
            logger.info("YouTube Upload erfolgreich")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim YouTube Upload: {e}")
            return False
    
    # ==================== EMAIL AUTOMATION ====================
    
    def setup_email_session(self, email_address, password, imap_server="imap.gmail.com", smtp_server="smtp.gmail.com"):
        """E-Mail Session einrichten"""
        try:
            # IMAP für Lesen
            self.imap = imaplib.IMAP4_SSL(imap_server)
            self.imap.login(email_address, password)
            
            # SMTP für Senden
            self.smtp = smtplib.SMTP_SSL(smtp_server, 465)
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
            _, message_numbers = self.imap.search(None, 'ALL')
            
            emails = []
            for num in message_numbers[0].split()[-limit:]:
                _, msg_data = self.imap.fetch(num, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                subject = email_message['subject']
                sender = email_message['from']
                date = email_message['date']
                
                # Body extrahieren
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_message.get_payload(decode=True).decode()
                
                emails.append({
                    "subject": subject,
                    "sender": sender,
                    "date": date,
                    "body": body,
                    "message_id": num.decode()
                })
            
            return emails
            
        except Exception as e:
            logger.error(f"Fehler beim E-Mail Lesen: {e}")
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
                    if attachment['type'] == 'image':
                        with open(attachment['path'], 'rb') as f:
                            img = MIMEImage(f.read())
                            img.add_header('Content-Disposition', 'attachment', filename=attachment['filename'])
                            msg.attach(img)
                    elif attachment['type'] == 'video':
                        with open(attachment['path'], 'rb') as f:
                            vid = MIMEVideo(f.read())
                            vid.add_header('Content-Disposition', 'attachment', filename=attachment['filename'])
                            msg.attach(vid)
            
            self.smtp.send_message(msg)
            logger.info(f"E-Mail erfolgreich an {to_email} gesendet")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim E-Mail Senden: {e}")
            return False
    
    def auto_reply_emails(self, keywords, reply_template):
        """Automatische E-Mail-Antworten"""
        try:
            emails = self.read_emails()
            
            for email_data in emails:
                subject = email_data['subject'].lower()
                body = email_data['body'].lower()
                
                # Prüfen ob Keywords enthalten sind
                if any(keyword.lower() in subject or keyword.lower() in body for keyword in keywords):
                    # Automatische Antwort senden
                    reply_body = reply_template.format(
                        sender_name=email_data['sender'].split('@')[0],
                        original_subject=email_data['subject']
                    )
                    
                    self.send_email(
                        email_data['sender'],
                        f"Re: {email_data['subject']}",
                        reply_body
                    )
                    
                    logger.info(f"Automatische Antwort an {email_data['sender']} gesendet")
            
            return True
            
        except Exception as e:
            logger.error(f"Fehler bei automatischen E-Mail-Antworten: {e}")
            return False

# Flask API für n8n Integration
app = Flask(__name__)
automation = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health Check Endpoint"""
    return jsonify({"status": "healthy", "message": "Extended Web Automation API läuft"})

@app.route('/login', methods=['POST'])
def login():
    """Login Endpoint für verschiedene Plattformen"""
    global automation
    
    data = request.json
    platform = data.get('platform')
    username = data.get('username')
    password = data.get('password')
    
    if not automation:
        automation = ExtendedSocialMediaAutomation(headless=True)
        if not automation.start_driver():
            return jsonify({"error": "Driver konnte nicht gestartet werden"}), 500
    
    try:
        if platform.lower() == 'instagram':
            success = automation.login_instagram(username, password)
        elif platform.lower() == 'tiktok':
            success = automation.login_tiktok(username, password)
        elif platform.lower() == 'youtube':
            success = automation.login_youtube(username, password)
        else:
            return jsonify({"error": "Plattform nicht unterstützt"}), 400
        
        if success:
            return jsonify({"status": "success", "message": f"Login zu {platform} erfolgreich"})
        else:
            return jsonify({"status": "error", "message": f"Login zu {platform} fehlgeschlagen"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    """Upload Endpoint für verschiedene Plattformen"""
    global automation
    
    if not automation:
        return jsonify({"error": "Nicht eingeloggt"}), 401
    
    data = request.json
    platform = data.get('platform')
    file_path = data.get('file_path')
    caption = data.get('caption', '')
    title = data.get('title', '')
    description = data.get('description', '')
    
    try:
        if platform.lower() == 'instagram':
            success = automation.upload_to_instagram(file_path, caption)
        elif platform.lower() == 'tiktok':
            success = automation.upload_to_tiktok(file_path, caption)
        elif platform.lower() == 'youtube':
            success = automation.upload_to_youtube(file_path, title, description)
        else:
            return jsonify({"error": "Plattform nicht unterstützt"}), 400
        
        if success:
            return jsonify({"status": "success", "message": f"Upload zu {platform} erfolgreich"})
        else:
            return jsonify({"status": "error", "message": f"Upload zu {platform} fehlgeschlagen"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/email/setup', methods=['POST'])
def email_setup():
    """E-Mail Setup Endpoint"""
    global automation
    
    data = request.json
    email_address = data.get('email')
    password = data.get('password')
    imap_server = data.get('imap_server', 'imap.gmail.com')
    smtp_server = data.get('smtp_server', 'smtp.gmail.com')
    
    if not automation:
        automation = ExtendedSocialMediaAutomation(headless=True)
    
    try:
        success = automation.setup_email_session(email_address, password, imap_server, smtp_server)
        
        if success:
            return jsonify({"status": "success", "message": "E-Mail Session eingerichtet"})
        else:
            return jsonify({"status": "error", "message": "E-Mail Setup fehlgeschlagen"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/email/read', methods=['GET'])
def read_emails():
    """E-Mails lesen Endpoint"""
    global automation
    
    if not automation:
        return jsonify({"error": "E-Mail Session nicht eingerichtet"}), 401
    
    folder = request.args.get('folder', 'INBOX')
    limit = int(request.args.get('limit', 10))
    
    try:
        emails = automation.read_emails(folder, limit)
        return jsonify({"status": "success", "emails": emails})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/email/send', methods=['POST'])
def send_email():
    """E-Mail senden Endpoint"""
    global automation
    
    if not automation:
        return jsonify({"error": "E-Mail Session nicht eingerichtet"}), 401
    
    data = request.json
    to_email = data.get('to_email')
    subject = data.get('subject')
    body = data.get('body')
    attachments = data.get('attachments', [])
    
    try:
        success = automation.send_email(to_email, subject, body, attachments)
        
        if success:
            return jsonify({"status": "success", "message": "E-Mail gesendet"})
        else:
            return jsonify({"status": "error", "message": "E-Mail konnte nicht gesendet werden"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/email/auto-reply', methods=['POST'])
def auto_reply():
    """Automatische E-Mail-Antworten Endpoint"""
    global automation
    
    if not automation:
        return jsonify({"error": "E-Mail Session nicht eingerichtet"}), 401
    
    data = request.json
    keywords = data.get('keywords', [])
    reply_template = data.get('reply_template', '')
    
    try:
        success = automation.auto_reply_emails(keywords, reply_template)
        
        if success:
            return jsonify({"status": "success", "message": "Automatische Antworten gesendet"})
        else:
            return jsonify({"status": "error", "message": "Automatische Antworten fehlgeschlagen"}), 500
            
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