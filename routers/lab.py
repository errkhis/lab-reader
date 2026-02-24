from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import filetype
from services import gemini

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
    content = await file.read()
    base_prompt = read_prompt("analysis.txt")
    
    # Append language instruction to the prompt
    full_prompt = f"{base_prompt}\n\nPlease provide the final results in {language}."
    
    result = await gemini.analyze_lab_file(
        file_content=content,
        mime_type=file.content_type,
        prompt=full_prompt
    )
    
    return {
        "filename": file.filename,
        "language": language,
        "analysis": result
    }

@router.post("/read-medication")
async def read_medication(
    file: UploadFile = Depends(validate_file),
    language: str = "English"
):
    content = await file.read()
    base_prompt = read_prompt("medication.txt")
    
    # Append language instruction to the prompt
    full_prompt = f"{base_prompt}\n\nPlease provide the final results in {language}."
    
    result = await gemini.analyze_lab_file(
        file_content=content,
        mime_type=file.content_type,
        prompt=full_prompt
    )
    
    return {
        "filename": file.filename,
        "language": language,
        "analysis": result
    }
