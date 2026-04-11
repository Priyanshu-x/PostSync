import os
import requests
from typing import List, Optional

AYRSHARE_API_URL = "https://app.ayrshare.com/api/post"

def post_to_platforms(post_text: str, platforms: List[str], image_base64: Optional[str] = None) -> dict:
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

    if image_base64:
        # We must host the image publicly since Ayrshare Free Tier denies direct media uploads.
        try:
            # image_base64 looks like "data:image/png;base64,iVBORw0KGgo..."
            encoded = image_base64.split(",", 1)[1] if "," in image_base64 else image_base64
            
            # Upload locally sourced base64 image to an anonymous public host (FreeImage.host)
            media_res = requests.post(
                "https://freeimage.host/api/1/upload", 
                data={
                    "key": "6d207e02198a847aa98d0a2a901485a5",
                    "action": "upload",
                    "source": encoded,
                    "format": "json"
                }
            )
            media_res.raise_for_status()
            
            media_url = media_res.json().get("image", {}).get("url")
            if media_url and media_url.startswith("http"):
                payload["mediaUrls"] = [media_url]
        except Exception as upload_err:
            print(f"Error proxying media to public host: {upload_err}")
            return {"error": "Failed to upload and proxy image. " + str(upload_err)}

    try:
        response = requests.post(AYRSHARE_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Ayrshare: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Ayrshare Error Details: {e.response.text}")
        details = e.response.text if hasattr(e, 'response') and e.response is not None else None
        return {"error": str(e), "details": details}
