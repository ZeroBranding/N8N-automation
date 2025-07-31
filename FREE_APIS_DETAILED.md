# 🆓 Kostenlose APIs - Komplette Übersicht

## 📊 **Alle APIs sind kostenlos verfügbar!**

| Service | Kostenlos | n8n Integration | Setup |
|---------|-----------|-----------------|-------|
| **ElevenLabs** | 10.000 Zeichen/Monat | ✅ Native Node | Einfach |
| **D-ID** | 20 Credits/Monat | ✅ HTTP Request | Einfach |
| **Unsplash** | 50 Requests/Stunde | ✅ Native Node | Einfach |
| **Remove.bg** | 50 Bilder/Monat | ✅ HTTP Request | Einfach |
| **Cloudinary** | 25 Credits/Monat | ✅ Native Node | Einfach |
| **OpenAI** | $5 Guthaben | ✅ Native Node | Einfach |
| **Hugging Face** | Unbegrenzt | ✅ HTTP Request | Einfach |
| **Stability AI** | 25 Credits/Monat | ✅ HTTP Request | Einfach |
| **Replicate** | 500 Requests/Monat | ✅ HTTP Request | Einfach |

---

## 🎤 **1. ElevenLabs - Text zu Sprache**

### 📊 Kostenlose Limits
- **10.000 Zeichen pro Monat** (kostenlos)
- **28 verschiedene Stimmen** verfügbar
- **Hohe Qualität** (Eleven Multilingual v2)

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://elevenlabs.io/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 📝 n8n Integration
```json
{
  "url": "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
  "method": "POST",
  "headers": {
    "xi-api-key": "{{ $env.ELEVENLABS_API_KEY }}",
    "Content-Type": "application/json"
  },
  "body": {
    "text": "{{ $json.text }}",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
    }
  }
}
```

### 💡 Verwendung
- Video-Narration
- Podcast-Erstellung
- Audiobooks
- Social Media Content

---

## 🎬 **2. D-ID - Avatar Video Generation**

### 📊 Kostenlose Limits
- **20 Credits pro Monat** (kostenlos)
- **1 Credit = 1 Video**
- **HD-Qualität** verfügbar
- **Verschiedene Avatare** verfügbar

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://www.d-id.com/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 📝 n8n Integration
```json
{
  "url": "https://api.d-id.com/talks",
  "method": "POST",
  "headers": {
    "Authorization": "Basic {{ $env.DID_API_KEY }}",
    "Content-Type": "application/json"
  },
  "body": {
    "script": {
      "type": "text",
      "input": "{{ $json.text }}"
    },
    "config": {
      "fluent": true,
      "pad_audio": 0.0
    },
    "source_url": "https://create-images-results.d-id.com/DefaultPresenters/Noelle_f/image.jpeg"
  }
}
```

### 💡 Verwendung
- Social Media Videos
- Präsentationen
- Schulungsvideos
- Marketing Content

---

## 📸 **3. Unsplash - Kostenlose Fotos**

### 📊 Kostenlose Limits
- **50 Requests pro Stunde** (kostenlos)
- **Unbegrenzte Downloads**
- **Hohe Auflösung** (bis zu 4K)
- **Kommerzielle Nutzung** erlaubt

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://unsplash.com/developers
# 2. Registrieren Sie sich als Developer
# 3. Erstellen Sie eine neue App
# 4. Kopieren Sie den Access Key
```

### 📝 n8n Integration
```json
{
  "url": "https://api.unsplash.com/photos/random",
  "method": "GET",
  "query": {
    "query": "{{ $json.search_term }}",
    "client_id": "{{ $env.UNSPLASH_API_KEY }}"
  }
}
```

### 💡 Verwendung
- Social Media Posts
- Blog-Bilder
- Marketing Material
- Website Design

---

## 🖼️ **4. Remove.bg - Hintergrund entfernen**

### 📊 Kostenlose Limits
- **50 Bilder pro Monat** (kostenlos)
- **HD-Qualität** verfügbar
- **Sofortige Verarbeitung**
- **Verschiedene Formate** (PNG, JPG)

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://www.remove.bg/api
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 📝 n8n Integration
```json
{
  "url": "https://api.remove.bg/v1.0/removebg",
  "method": "POST",
  "headers": {
    "X-Api-Key": "{{ $env.REMOVEBG_API_KEY }}"
  },
  "body": {
    "image_url": "{{ $json.image_url }}",
    "size": "auto"
  }
}
```

### 💡 Verwendung
- Produktfotos
- Portrait-Bearbeitung
- Social Media Content
- E-Commerce

---

## ☁️ **5. Cloudinary - Bild/Video Hosting**

### 📊 Kostenlose Limits
- **25 Credits pro Monat** (kostenlos)
- **25 GB Speicher**
- **25 GB Bandbreite**
- **Unbegrenzte Transformationen**

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://cloudinary.com/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu Dashboard
# 4. Kopieren Sie Cloud Name, API Key und Secret
```

### 📝 n8n Integration
```json
{
  "url": "https://api.cloudinary.com/v1_1/{{ $env.CLOUDINARY_CLOUD_NAME }}/image/upload",
  "method": "POST",
  "body": {
    "file": "{{ $json.image_data }}",
    "api_key": "{{ $env.CLOUDINARY_API_KEY }}",
    "timestamp": "{{ Math.floor(Date.now() / 1000) }}"
  }
}
```

### 💡 Verwendung
- Bild-Hosting
- Video-Hosting
- Bild-Transformationen
- CDN für Medien

---

## 🤖 **6. OpenAI - KI-Modelle**

### 📊 Kostenlose Limits
- **$5 Guthaben** (kostenlos)
- **GPT-3.5-turbo** verfügbar
- **DALL-E 2** verfügbar
- **Whisper** verfügbar

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://platform.openai.com/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 📝 n8n Integration
```json
{
  "url": "https://api.openai.com/v1/chat/completions",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer {{ $env.OPENAI_API_KEY }}",
    "Content-Type": "application/json"
  },
  "body": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "{{ $json.prompt }}"
      }
    ]
  }
}
```

### 💡 Verwendung
- Text-Generierung
- Bild-Generierung
- Übersetzungen
- Content-Creation

---

## 🧠 **7. Hugging Face - Open Source KI**

### 📊 Kostenlose Limits
- **Unbegrenzte Requests** (kostenlos)
- **Tausende von Modellen** verfügbar
- **Text, Bild, Audio** Modelle
- **Open Source** Modelle

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://huggingface.co/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "Access Tokens"
# 4. Erstellen Sie einen Token
```

### 📝 n8n Integration
```json
{
  "url": "https://api-inference.huggingface.co/models/{{ $json.model_name }}",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer {{ $env.HUGGINGFACE_API_KEY }}"
  },
  "body": {
    "inputs": "{{ $json.input }}"
  }
}
```

### 💡 Verwendung
- Text-Generierung
- Bild-Klassifikation
- Übersetzungen
- Sentiment-Analyse

---

## 🎨 **8. Stability AI - Bild-Generierung**

### 📊 Kostenlose Limits
- **25 Credits pro Monat** (kostenlos)
- **1 Credit = 1 Bild**
- **HD-Qualität** verfügbar
- **Verschiedene Stile** verfügbar

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://platform.stability.ai/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Keys"
# 4. Kopieren Sie den API Key
```

### 📝 n8n Integration
```json
{
  "url": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer {{ $env.STABILITY_API_KEY }}",
    "Content-Type": "application/json"
  },
  "body": {
    "text_prompts": [
      {
        "text": "{{ $json.prompt }}"
      }
    ],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1
  }
}
```

### 💡 Verwendung
- Social Media Bilder
- Marketing Material
- Website Design
- Content Creation

---

## 🔄 **9. Replicate - KI-Modelle Hosting**

### 📊 Kostenlose Limits
- **500 Requests pro Monat** (kostenlos)
- **Tausende von Modellen** verfügbar
- **GPU-beschleunigt** verfügbar
- **Open Source** Modelle

### 🔗 Setup
```bash
# 1. Gehen Sie zu: https://replicate.com/
# 2. Registrieren Sie sich (kostenlos)
# 3. Gehen Sie zu "API Tokens"
# 4. Erstellen Sie einen Token
```

### 📝 n8n Integration
```json
{
  "url": "https://api.replicate.com/v1/predictions",
  "method": "POST",
  "headers": {
    "Authorization": "Token {{ $env.REPLICATE_API_KEY }}",
    "Content-Type": "application/json"
  },
  "body": {
    "version": "{{ $json.model_version }}",
    "input": {
      "prompt": "{{ $json.prompt }}"
    }
  }
}
```

### 💡 Verwendung
- Bild-Generierung
- Video-Generierung
- Text-Generierung
- Audio-Verarbeitung

---

## 📊 **Kostenlose Limits Zusammenfassung**

| Service | Kostenlos | Pro Tag | Pro Monat | n8n Node |
|---------|-----------|---------|-----------|----------|
| **ElevenLabs** | ✅ | ~333 Zeichen | 10.000 Zeichen | ✅ |
| **D-ID** | ✅ | ~0.7 Videos | 20 Videos | ✅ |
| **Unsplash** | ✅ | 1.200 Requests | 36.000 Requests | ✅ |
| **Remove.bg** | ✅ | ~1.7 Bilder | 50 Bilder | ✅ |
| **Cloudinary** | ✅ | ~0.8 Credits | 25 Credits | ✅ |
| **OpenAI** | ✅ | $0.17 | $5 Guthaben | ✅ |
| **Hugging Face** | ✅ | Unbegrenzt | Unbegrenzt | ✅ |
| **Stability AI** | ✅ | ~0.8 Bilder | 25 Bilder | ✅ |
| **Replicate** | ✅ | ~17 Requests | 500 Requests | ✅ |

---

## 🚀 **n8n Integration Status**

### ✅ **Native n8n Nodes verfügbar:**
- ElevenLabs
- Unsplash
- Cloudinary
- OpenAI

### 🔧 **HTTP Request Nodes (einfach):**
- D-ID
- Remove.bg
- Hugging Face
- Stability AI
- Replicate

---

## 💡 **Empfehlungen für verschiedene Use Cases**

### 🎬 **Video Content Creation:**
1. **ElevenLabs** (Text zu Sprache)
2. **D-ID** (Avatar Videos)
3. **Unsplash** (Hintergrund-Bilder)

### 📸 **Social Media Content:**
1. **Unsplash** (Fotos)
2. **Remove.bg** (Hintergrund entfernen)
3. **Stability AI** (KI-Bilder)

### 🤖 **KI-Content Generation:**
1. **OpenAI** (Text & Bilder)
2. **Hugging Face** (Open Source)
3. **Replicate** (Spezialisierte Modelle)

### ☁️ **Media Hosting:**
1. **Cloudinary** (Bilder & Videos)
2. **Unsplash** (Fotos)

---

## 🔧 **Setup in n8n**

### **1. Environment Variables setzen:**
```bash
# In n8n Settings → Environment Variables
ELEVENLABS_API_KEY=your_key
DID_API_KEY=your_key
UNSPLASH_API_KEY=your_key
REMOVEBG_API_KEY=your_key
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
OPENAI_API_KEY=your_key
HUGGINGFACE_API_KEY=your_key
STABILITY_API_KEY=your_key
REPLICATE_API_KEY=your_key
```

### **2. Nodes in n8n verwenden:**
```bash
# Native Nodes (drag & drop):
- ElevenLabs
- Unsplash
- Cloudinary
- OpenAI

# HTTP Request Nodes (konfigurieren):
- D-ID
- Remove.bg
- Hugging Face
- Stability AI
- Replicate
```

---

## 🎯 **Fazit**

**Alle APIs sind kostenlos verfügbar** und bieten ausreichende Limits für:
- ✅ **Hobby-Projekte**
- ✅ **Kleine Unternehmen**
- ✅ **Content Creation**
- ✅ **Social Media Marketing**
- ✅ **Prototyping**

**Für größere Projekte** können Sie jederzeit upgraden, aber die kostenlosen Limits sind sehr großzügig!

**Starten Sie jetzt und nutzen Sie alle kostenlosen APIs!** 🚀