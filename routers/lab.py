from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import filetype
import logging
import base64
import io
import edge_tts
import emoji
from services import gemini

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/lab",
    tags=["lab"]
)

# Localized Disclaimers for token optimization (added in code)
DISCLAIMERS = {
    "Arabic": "\n\n_تنبيه: هذا التحليل آلي وبغرض التثقيف فقط. يرجى استشارة طبيبك._",
    "Spanish": "\n\n_Aviso: Este es un análisis automático con fines educativos. Consulte a su médico._",
    "French": "\n\n_Avis : Il s'agit d'une analyse automatique à des fins éducatives. Consultez votre médecin._",
    "English": "\n\n_Disclaimer: AI interpretation for education. Consult a doctor._"
}

VOICE_MAP = {
    "Arabic": "ar-SA-HamedNeural",
    "Spanish": "es-ES-AlvaroNeural",
    "French": "fr-FR-HenriNeural",
    "English": "en-US-GuyNeural"
}

async def generate_voice_base64(text: str, language: str) -> str:
    """Generates a clean male voice audio from text using edge-tts (strips emojis)."""
    try:
        # Remove emojis
        clean_text = emoji.replace_emoji(text, replace='')
        # Remove markdown before TTS
        clean_text = clean_text.replace("*", "").replace("_", "").replace("#", "").replace("`", "").strip()
        
        voice = VOICE_MAP.get(language, "en-US-GuyNeural")
        
        communicate = edge_tts.Communicate(clean_text, voice)
        fp = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fp.write(chunk["data"])
                
        return base64.b64encode(fp.getvalue()).decode("utf-8")
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        return ""

ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"]

def read_prompt(filename: str) -> str:
    path = Path(__file__).parent.parent / "prompts" / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

async def validate_file(file: UploadFile = File(...)) -> UploadFile:
    """
    Validates file using magic numbers (header bytes) via the 'filetype' library.
    This replaces python-magic which requires external system dependencies.
    """
    content = await file.read(2048)
    await file.seek(0)
    
    kind = filetype.guess(content)
    
    # If filetype can't guess (it's sometimes strict with PDFs), 
    # we fallback to the content_type provided by the request but still log the mismatch
    mime = kind.mime if kind else file.content_type
    
    if mime not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {mime} not supported. Use PDF, JPEG or PNG."
        )
    
    return file

@router.post("/read-analysis")
async def read_analysis(
    file: UploadFile = Depends(validate_file),
    language: str = "English"
):
    try:
        content = await file.read()
        base_prompt = read_prompt("analysis.txt")
        
        # Detect MIME type from content to ensure accuracy for Gemini
        kind = filetype.guess(content)
        mime_type = kind.mime if kind else file.content_type
        
        # Language instruction: ensure EVERYTHING is translated
        full_prompt = f"{base_prompt}\nTranslate everything (including headers) to: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        # Add localized disclaimer
        disclaimer = DISCLAIMERS.get(language, DISCLAIMERS["English"])
        if not result.startswith("⚠️"):
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result,
            "voice": await generate_voice_base64(result, language)
        }
    except Exception as e:
        logger.error(f"Error in read_analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/read-medication")
async def read_medication(
    file: UploadFile = Depends(validate_file),
    language: str = "English"
):
    try:
        content = await file.read()
        base_prompt = read_prompt("medication.txt")
        
        # Detect MIME type from content to ensure accuracy for Gemini
        kind = filetype.guess(content)
        mime_type = kind.mime if kind else file.content_type
        
        # Language instruction: ensure EVERYTHING is translated
        full_prompt = f"{base_prompt}\nTranslate everything (including headers) to: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        disclaimer = DISCLAIMERS.get(language, DISCLAIMERS["English"])
        if not result.startswith("⚠️"):
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result,
            "voice": await generate_voice_base64(result, language)
        }
    except Exception as e:
        logger.error(f"Error in read_medication: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/read-prescription")
async def read_prescription(
    file: UploadFile = Depends(validate_file),
    language: str = "English"
):
    try:
        content = await file.read()
        base_prompt = read_prompt("prescription.txt")
        
        # Detect MIME type from content to ensure accuracy for Gemini
        kind = filetype.guess(content)
        mime_type = kind.mime if kind else file.content_type
        
        # Language instruction: ensure EVERYTHING is translated
        full_prompt = f"{base_prompt}\nTranslate everything (including headers) to: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        disclaimer = DISCLAIMERS.get(language, DISCLAIMERS["English"])
        if not result.startswith("⚠️"):
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result,
            "voice": await generate_voice_base64(result, language)
        }
    except Exception as e:
        logger.error(f"Error in read_prescription: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/read-radiography")
async def read_radiography(
    file: UploadFile = Depends(validate_file),
    language: str = "English"
):
    try:
        content = await file.read()
        base_prompt = read_prompt("radiography.txt")
        
        # Detect MIME type from content to ensure accuracy for Gemini
        kind = filetype.guess(content)
        mime_type = kind.mime if kind else file.content_type
        
        # Language instruction: ensure EVERYTHING is translated
        full_prompt = f"{base_prompt}\nTranslate everything (including headers) to: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        disclaimer = DISCLAIMERS.get(language, DISCLAIMERS["English"])
        if not result.startswith("⚠️"):
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result,
            "voice": await generate_voice_base64(result, language)
        }
    except Exception as e:
        logger.error(f"Error in read_radiography: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
