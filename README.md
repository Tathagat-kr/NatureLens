````markdown
# 🌿 NatureLens

> **Look closer. Reconnect with nature.**

NatureLens is an AI-powered nature discovery app that uses image recognition to help users identify plants, animals, birds, insects, fungi, and natural features — then encourages real-world observation through nature missions.

## ✨ Features

- 📷 AI-powered nature identification
- 🌱 Common and scientific names
- 🌎 Ecological role and interesting facts
- 👀 "Look closer" observation prompts
- 🎯 AI-generated real-world nature missions
- ⭐ XP and nature-level progression
- 📖 Personal discovery history
- 👤 Anonymous user profiles
- 📱 Installable Progressive Web App (PWA)
- 📱 Mobile camera support

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **AI:** Google Gemini Vision
- **Database:** SQLite
- **Deployment:** Render
- **Mobile:** PWA
- **Containerization:** Docker

## 📁 Project Structure

```text
naturelens/
├── backend/
│   ├── main.py
│   ├── gemini.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── static/
│       ├── index.html
│       ├── style.css
│       ├── app.js
│       ├── manifest.json
│       ├── service-worker.js
│       └── icon.svg
├── Dockerfile
├── README.md
└── .gitignore
```

## 🚀 Installation

### Prerequisites

* Python 3.11+
* Git
* A Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/naturelens.git
cd naturelens
```

### 2. Create a Python environment

Using Conda:

```bash
conda create -n naturelens python=3.11
conda activate naturelens
```

Or using Python venv:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Gemini API

Create a file:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
cd backend
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 📱 Mobile / PWA

NatureLens is a Progressive Web App.

After deployment, open the public HTTPS URL on an Android phone using Chrome.

Select:

**Menu → Add to Home screen / Install app**

NatureLens can then be launched directly from the phone's home screen and can use the device camera for nature discovery.

## ☁️ Deployment

NatureLens is deployed using **Render** with Docker.

The repository includes a `Dockerfile`, so Render can build and start the application automatically.

Add the following environment variable in the Render service:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit the API key to GitHub.

### Render Configuration

* **Service Type:** Web Service
* **Runtime:** Docker
* **Branch:** `main`
* **Root Directory:** Leave blank
* **Dockerfile:** `./Dockerfile`
* **Docker Command:** Leave blank
* **Instance:** Free

The application listens on Render's `$PORT` environment variable.

## 👤 Anonymous Users

NatureLens does not require account creation.

Each browser receives a unique anonymous user ID. Discoveries and XP are associated with that ID, keeping different users' histories separate.

Clearing browser storage creates a new anonymous profile.

## 🧠 AI

Gemini Vision analyzes uploaded images and returns structured information about the visible natural subject, including:

* Identification
* Scientific name
* Confidence
* Description
* Ecological role
* Interesting facts
* Observation prompts
* Nature missions
* XP rewards

The AI is instructed not to invent precise species information when the image is ambiguous.

## 🔮 Future Improvements

* 🗺️ Personal nature discovery map
* 📍 Location-aware discoveries
* 🐦 Bird sound recognition
* 🌦️ Weather and seasonal context
* 🏆 Biodiversity challenges
* 👥 Community exploration
* 📊 Personal biodiversity statistics
* 🌳 Ecosystem health insights
* 🔐 Optional user accounts
* ☁️ Persistent cloud database

## 🌿 Philosophy

> **Technology should help people experience nature, not replace it.**

NatureLens uses AI as the starting point for curiosity, then encourages users to put the phone down and explore the world around them.

---

**Built with ❤️ for reconnecting people with nature.**
