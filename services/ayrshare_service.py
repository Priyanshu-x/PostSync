import os
import requests
from typing import List, Optional

AYRSHARE_API_URL = "https://app.ayrshare.com/api/post"

def post_to_platforms(post_text: str, platforms: List[str], image_url: Optional[str] = None) -> dict:
    """
    Sends a post to scheduled platforms using the Ayrshare API.
    """
    api_key = os.getenv("AYRSHARE_API_KEY")
    if not api_key:
        raise ValueError("AYRSHARE_API_KEY is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "post": post_text,
        "platforms": platforms,
    }

    if image_url:
        payload["mediaUrls"] = [image_url]

    try:
        response = requests.post(AYRSHARE_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Ayrshare: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Ayrshare Error Details: {e.response.text}")
        return {"error": str(e), "details": getattr(e, 'response', None) and e.response.text}
