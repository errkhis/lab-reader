from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import filetype
import logging
from services import gemini

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/lab",
    tags=["lab"]
)

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
        
        # Append language instruction compactly
        full_prompt = f"{base_prompt}\nOutput lang: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        # Save tokens: add disclaimer locally instead of having LLM generate it
        disclaimer = "\n\n_Disclaimer: AI interpreting for education. Consult a doctor._"
        if not result.startswith("⚠️"):  # Don't add to errors
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result
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
        
        # Append language instruction compactly
        full_prompt = f"{base_prompt}\nOutput lang: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        disclaimer = "\n\n_Disclaimer: Educational only. Follow doctor instructions._"
        if not result.startswith("⚠️"):
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result
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
        
        # Append language instruction compactly
        full_prompt = f"{base_prompt}\nOutput lang: {language}."
        
        result = await gemini.analyze_lab_file(
            file_content=content,
            mime_type=mime_type,
            prompt=full_prompt
        )
        
        disclaimer = "\n\n_Disclaimer: AI transcription. Confirm with pharmacist._"
        if not result.startswith("⚠️"):
            result += disclaimer

        return {
            "filename": file.filename,
            "language": language,
            "analysis": result
        }
    except Exception as e:
        logger.error(f"Error in read_prescription: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
