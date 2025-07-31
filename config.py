#!/usr/bin/env python3
"""
Konfigurationsdatei für Social Media Automation
Sichere Verwaltung von Login-Daten
"""

import os
import json
from cryptography.fernet import Fernet
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file="credentials.json", key_file="secret.key"):
        self.config_file = config_file
        self.key_file = key_file
        self.cipher_suite = None
        self._load_or_create_key()
    
    def _load_or_create_key(self):
        """Lädt oder erstellt einen Verschlüsselungsschlüssel"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        self.cipher_suite = Fernet(key)
    
    def save_credentials(self, platform, username, password):
        """Speichert verschlüsselte Login-Daten"""
        credentials = {
            platform: {
                "username": username,
                "password": password
            }
        }
        
        # Verschlüsseln
        encrypted_data = self.cipher_suite.encrypt(json.dumps(credentials).encode())
        
        # Speichern
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_data)
        
        print(f"Credentials für {platform} gespeichert")
    
    def load_credentials(self, platform):
        """Lädt entschlüsselte Login-Daten"""
        if not os.path.exists(self.config_file):
            return None, None
        
        with open(self.config_file, 'rb') as f:
            encrypted_data = f.read()
        
        # Entschlüsseln
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        credentials = json.loads(decrypted_data.decode())
        
        if platform in credentials:
            return credentials[platform]["username"], credentials[platform]["password"]
        
        return None, None
    
    def list_platforms(self):
        """Listet alle gespeicherten Plattformen"""
        if not os.path.exists(self.config_file):
            return []
        
        with open(self.config_file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        credentials = json.loads(decrypted_data.decode())
        
        return list(credentials.keys())
    
    def remove_credentials(self, platform):
        """Entfernt Login-Daten für eine Plattform"""
        if not os.path.exists(self.config_file):
            return
        
        with open(self.config_file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        credentials = json.loads(decrypted_data.decode())
        
        if platform in credentials:
            del credentials[platform]
            
            if credentials:
                # Neue verschlüsselte Daten speichern
                encrypted_data = self.cipher_suite.encrypt(json.dumps(credentials).encode())
                with open(self.config_file, 'wb') as f:
                    f.write(encrypted_data)
            else:
                # Datei löschen wenn keine Credentials mehr vorhanden
                os.remove(self.config_file)
            
            print(f"Credentials für {platform} entfernt")

# Beispiel für die Verwendung
if __name__ == "__main__":
    config = ConfigManager()
    
    # Beispiel: Credentials speichern
    # config.save_credentials("instagram", "ihr_username", "ihr_password")
    # config.save_credentials("tiktok", "ihr_username", "ihr_password")
    
    # Beispiel: Credentials laden
    # username, password = config.load_credentials("instagram")
    # print(f"Instagram: {username}")
    
    # Beispiel: Plattformen auflisten
    platforms = config.list_platforms()
    print(f"Gespeicherte Plattformen: {platforms}")