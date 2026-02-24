from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import magic
from services import gemini

router = APIRouter(
    prefix="/lab",
    tags=["lab"]
)

ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "application/pdf"}

def read_prompt(filename: str) -> str:
    path = Path(__file__).parent.parent / "prompts" / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

async def validate_file(file: UploadFile = File(...)) -> UploadFile:
    content = await file.read(2048)
    await file.seek(0)
    
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {mime} not supported. Use PDF, JPEG or PNG."
        )
    return file

@router.post("/read-analysis")
async def read_analysis(file: UploadFile = Depends(validate_file)):
    content = await file.read()
    prompt = read_prompt("analysis.txt")
    
    result = await gemini.analyze_lab_file(
        file_content=content,
        mime_type=file.content_type,
        prompt=prompt
    )
    
    return {
        "filename": file.filename,
        "analysis": result
    }

@router.post("/read-medication")
async def read_medication(file: UploadFile = Depends(validate_file)):
    content = await file.read()
    prompt = read_prompt("medication.txt")
    
    result = await gemini.analyze_lab_file(
        file_content=content,
        mime_type=file.content_type,
        prompt=prompt
    )
    
    return {
        "filename": file.filename,
        "analysis": result
    }
