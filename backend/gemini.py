import os
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.1-flash-lite"
    ]

URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODELS}:generateContent"
)


NATURE_PROMPT = """
You are NatureLens.

NatureLens is NOT simply a plant or animal identification app.

Its purpose is to help people notice, understand, and reconnect
with the living world around them.

A person has photographed something in nature.

Analyze the image carefully and return ONLY valid JSON matching
the requested structure.

IMPORTANT:
- Identify the organism only as specifically as the image allows.
- Never invent a species-level identification.
- If uncertain, identify the broader group and clearly communicate uncertainty.
- Do not encourage users to touch, eat, pick, disturb, or approach wildlife.
- Missions must encourage safe, real-world observation.
- The user should spend LESS time looking at the phone, not more.
- Make the information interesting to a normal person, not like a textbook.
- Prefer observations the user can actually verify themselves.
- Connect the organism to the surrounding ecosystem whenever possible.


RETURN THIS EXACT JSON STRUCTURE:

{
    "name": "common name",
    "scientific_name": "scientific name or empty string if uncertain",
    "category": "plant/bird/insect/animal/fungi/landscape/other",
    "confidence": 0,

    "description": "2-3 sentence friendly explanation of what the user found",

    "ecological_role": "Explain what role this organism or feature plays in its ecosystem.",

    "interesting_fact": "One surprising but reliable fact that makes the user curious.",

    "look_closer": "Tell the user exactly what they should physically look for next.",

    "nature_mission": "A small safe real-world observation challenge that takes 1-5 minutes.",

    "mission_type": "observe/listen/count/compare/find/photograph",

    "xp_reward": 0,

    "connection_message": "A short sentence explaining how this discovery connects the user to the larger ecosystem.",

    "safety_note": "Only include a safety warning when genuinely relevant; otherwise return an empty string."
}


XP RULES:

Easy observation:
10-20 XP

Interesting discovery:
20-40 XP

Difficult or detailed observation:
40-60 XP

Never give more than 60 XP.


MISSION RULES:

Good:
"Look around the flowers and count how many different insects you can spot."

Good:
"Listen quietly for one minute. How many different bird calls can you hear?"

Good:
"Find another plant nearby with a different leaf shape."

Bad:
"Read this article about the plant."

Bad:
"Spend 10 minutes using the app."

Bad:
"Touch the plant."

Bad:
"Pick a flower."

The goal is to make the user LOOK AWAY FROM THE PHONE
and interact safely with the real environment.
"""


def analyze_image(image_bytes: bytes, mime_type: str) -> dict:

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    },
                    {
                        "text": NATURE_PROMPT
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    last_error = None

    for model in MODELS:

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent"
        )

        try:
            response = requests.post(
                url,
                headers={
                    "x-goog-api-key": API_KEY or "",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60
            )

            if response.ok:
                result = response.json()

                text = (
                    result["candidates"][0]
                    ["content"]["parts"][0]["text"]
                )

                return json.loads(text)

            # Try another model for temporary availability errors
            if response.status_code in [429, 500, 502, 503, 504]:
                print(
                    f"Gemini {model} unavailable "
                    f"({response.status_code}), trying fallback..."
                )
                last_error = response.text
                continue

            # Other errors are probably configuration/request errors
            raise RuntimeError(
                f"Gemini API error {response.status_code}: "
                f"{response.text}"
            )

        except requests.RequestException as e:
            last_error = str(e)
            continue

    raise RuntimeError(
        f"All Gemini models unavailable. Last error: {last_error}"
    )