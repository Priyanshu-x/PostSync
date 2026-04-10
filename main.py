from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from services.ayrshare_service import post_to_platforms
from services.ai_service import generate_platform_captions

load_dotenv()

app = FastAPI(title="PostSync API", description="Automated social media posting with AI")

class PostRequest(BaseModel):
    base_text: str
    image_url: Optional[str] = None
    platforms: List[str] = ["facebook", "instagram", "twitter", "linkedin"]

class PostResponse(BaseModel):
    status: str
    platforms: List[str]
    ayrshare_response: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to PostSync API. Setup your agency workflows!"}

@app.post("/auto-post", response_model=PostResponse)
async def create_auto_post(request: PostRequest):
    """
    Takes a base thought, uses AI to adapt it to each platform, 
    and posts them via Ayrshare.
    """
    try:
        # Step 1: Generate tailored text for different platforms using AI
        # If no platforms are specified, just return
        if not request.platforms:
            raise HTTPException(status_code=400, detail="No platforms specified")

        # Let the AI format the caption based on the base_text
        captions = await generate_platform_captions(request.base_text, request.platforms)

        # Step 2: Post to Ayrshare
        posting_responses = {}
        for platform in request.platforms:
            platform_text = captions.get(platform, request.base_text)
            
            # Post to individual platforms via Ayrshare
            result = post_to_platforms(
                post_text=platform_text, 
                platforms=[platform], 
                image_url=request.image_url
            )
            posting_responses[platform] = result

        return PostResponse(
            status="success",
            platforms=request.platforms,
            ayrshare_response=posting_responses
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
