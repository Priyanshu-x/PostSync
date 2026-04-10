import os
import openai
from typing import List

async def generate_platform_captions(base_text: str, platforms: List[str]) -> dict:
    """
    Uses OpenAI to format the base_text appropriately for each social media platform.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    
    # We use the legacy OpenAI client format or new one depending on the module version, 
    # Here using the newer OpenAI 1.x pattern via an instantiated client.
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=api_key)

    platform_captions = {}

    for platform in platforms:
        prompt = f"""
        You are an expert social media manager for an AI automation agency.
        Convert the following base text into an engaging, optimized post specifically for {platform}.
        
        Guidelines for {platform}:
        - If Twitter/X: keep it under 280 characters, use a hook, maybe a thread style but summarized. Max 2 hashtags.
        - If Instagram: use an engaging hook, emojis, spacing, and 5-10 relevant hashtags at the bottom.
        - If LinkedIn: make it professional, insightful, use line breaks, and 3-5 professional hashtags.
        - If Facebook: keep it conversational, engage the community, ask a question at the end.
        
        Base Text:
        "{base_text}"
        
        Output JUST the post content, ready to be copied and pasted.
        """

        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional social media manager."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            generated_text = response.choices[0].message.content.strip()
            platform_captions[platform] = generated_text

        except Exception as e:
            print(f"Error generating content for {platform}: {e}")
            # Fallback to base text if AI generation fails
            platform_captions[platform] = base_text

    return platform_captions
