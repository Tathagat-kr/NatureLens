---
title: NatureLens
emoji: 🌿
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
---

# NatureLens 🌿

NatureLens is an AI-powered nature exploration experience.

Instead of simply identifying plants and animals, NatureLens helps users:
- discover nature around them
- understand ecological connections
- complete real-world observation missions
- earn Nature XP
- build a personal history of discoveries

## Stack

- Frontend: HTML / CSS / JavaScript
- Backend: FastAPI / Python
- AI: Gemini Vision
- Database: SQLite
- Deployment: Hugging Face Docker Space
- Mobile: PWA

## Local development

```bash
uvicorn main:app --reload
```

The app runs at `http://127.0.0.1:8000`.

## Deployment

Set `GEMINI_API_KEY` as a secret in the Hugging Face Space.
Never commit the API key or `.env` file.
