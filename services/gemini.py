import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import io

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

async def analyze_lab_file(file_content: bytes, mime_type: str, prompt: str = ""):
    """
    Analyzes a lab file (image or PDF) using Gemini 2.0 Flash.
    """
    if not prompt:
        # User requested an empty placeholder prompt for now
        prompt = "Explain what this document is about." 

    response = await client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(
                data=file_content,
                mime_type=mime_type
            ),
            prompt
        ]
    )
    
    return response.text
