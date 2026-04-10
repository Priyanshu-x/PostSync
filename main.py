from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from services.ayrshare_service import post_to_platforms
from services.ai_service import generate_platform_captions

load_dotenv()

app = FastAPI(title="PostSync API", description="Automated social media posting with AI")

# Configure CORS
origins = [
    "http://localhost:5173", # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    base_text: str
    image_url: Optional[str] = None
    platforms: List[str] = ["facebook", "instagram", "twitter", "linkedin"]

class PublishRequest(BaseModel):
    captions: dict # map of platform -> tailored string
    image_url: Optional[str] = None
    platforms: List[str]

class PublishResponse(BaseModel):
    status: str
    platforms: List[str]
    ayrshare_responses: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to PostSync API. Setup your agency workflows!"}

@app.post("/generate-preview")
async def generate_preview(request: PostRequest):
    """
    Takes a base thought and generates AI tailored text for each platform.
    Returns the previews WITHOUT publishing.
    """
    try:
        if not request.platforms:
            raise HTTPException(status_code=400, detail="No platforms specified")

        captions = await generate_platform_captions(request.base_text, request.platforms)
        
        return {
            "status": "success",
            "platforms": request.platforms,
            "captions": captions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/publish", response_model=PublishResponse)
async def publish_posts(request: PublishRequest):
    """
    Takes the approved/edited captions and publishes them via Ayrshare.
    """
    try:
        if not request.platforms:
            raise HTTPException(status_code=400, detail="No platforms specified")

        posting_responses = {}
        for platform in request.platforms:
            platform_text = request.captions.get(platform)
            if not platform_text:
                continue
            
            result = post_to_platforms(
                post_text=platform_text, 
                platforms=[platform], 
                image_url=request.image_url
            )
            posting_responses[platform] = result

        return PublishResponse(
            status="success",
            platforms=request.platforms,
            ayrshare_responses=posting_responses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
