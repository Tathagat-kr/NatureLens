from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from gemini import analyze_image
from database import init_db, save_observation, get_observations
from models import ObservationCreate

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
COOKIE_NAME = "naturelens_user_id"

app = FastAPI(title="NatureLens API", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup():
    init_db()


def get_or_create_user_id(request: Request, response: Response):
    user_id = request.cookies.get(COOKIE_NAME)
    if not user_id:
        user_id = str(uuid4())
        response.set_cookie(
            key=COOKIE_NAME,
            value=user_id,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="lax",
            secure=request.url.scheme == "https",
            path="/",
        )
    return user_id


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NatureLens API"}


@app.post("/api/analyze")
async def analyze(image: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, detail="Only JPG, PNG and WEBP images are supported"
        )
    image_bytes = await image.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be smaller than 10MB")
    try:
        return {"success": True, "data": analyze_image(image_bytes, image.content_type)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


@app.post("/api/observations")
def create_observation(
    observation: ObservationCreate, request: Request, response: Response
):
    user_id = get_or_create_user_id(request, response)
    return {"success": True, "id": save_observation(observation.model_dump(), user_id)}


@app.get("/api/observations")
def observations(request: Request, response: Response):
    user_id = get_or_create_user_id(request, response)
    return {"success": True, "data": get_observations(user_id)}
