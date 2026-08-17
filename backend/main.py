from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from gemini import analyze_image
from database import init_db, save_observation, get_observations
from models import ObservationCreate

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="NatureLens API",
    description="AI-powered nature discovery and reconnection platform",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "NatureLens API"
    }


@app.post("/api/analyze")
async def analyze(image: UploadFile = File(...)):
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are supported"
        )

    image_bytes = await image.read()

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image must be smaller than 10MB"
        )

    try:
        result = analyze_image(
            image_bytes,
            image.content_type
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        import traceback
        print("\n========== GEMINI ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        traceback.print_exc()
        print("==================================\n")
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )


@app.post("/api/observations")
def create_observation(observation: ObservationCreate):
    observation_id = save_observation(
        observation.model_dump()
    )

    return {
        "success": True,
        "id": observation_id
    }


@app.get("/api/observations")
def observations():
    return {
        "success": True,
        "data": get_observations()
    }
