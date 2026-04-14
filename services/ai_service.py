import os
from typing import List

def generate_platform_captions(base_text: str, platforms: List[str]) -> dict:
    """
    Uses OpenAI to format the base_text appropriately for each social media platform.
    """
    from google import genai
    import os
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
        
    client = genai.Client(api_key=api_key)

    platform_captions = {}

    for platform in platforms:
        prompt = f"""
        You are an expert social media manager for an AI automation agency.
        Convert the following base text into an engaging, optimized post specifically for {platform}.
        
        Guidelines for {platform}:
        - If Twitter/X: keep it under 240 characters TOTAL, use a hook, maybe a thread style but highly summarized. Max 2 hashtags.
        - If Instagram: use an engaging hook, emojis, spacing, and 5-10 relevant hashtags at the bottom.
        - If LinkedIn: make it professional, insightful, use line breaks, and 3-5 professional hashtags.
        - If Facebook: keep it conversational, engage the community, ask a question at the end.
        
        Base Text:
        "{base_text}"
        
        Output JUST the post content, ready to be copied and pasted.
        """

        try:
            prompt_instruction = f"SYSTEM: You are a professional social media manager. IMPORTANT: Never use more than 4 hashtags in any post.\nUSER: {prompt}"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_instruction,
                config=genai.types.GenerateContentConfig(
                    max_output_tokens=600,
                    temperature=0.7,
                )
            )
            
            generated_text = response.text.strip()
            platform_captions[platform] = generated_text

        except Exception as e:
            print(f"Error generating content for {platform}: {e}")
            # Fallback to base text if AI generation fails
            platform_captions[platform] = base_text

    return platform_captions
