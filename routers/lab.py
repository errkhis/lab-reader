from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import magic
from services import gemini

router = APIRouter(
    prefix="/lab",
    tags=["lab"]
)

ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "application/pdf"}

async def validate_file(file: UploadFile = File(...)) -> UploadFile:
    """
    This function reads the actual bytes to verify the file is what it says it is.
    Using 'magic' is much safer than just checking the extension.
    """
    # Read first 2048 bytes to detect type
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
    
    # Placeholder for analysis specific prompt
    # Example: "Extract all lab results and highlight anything out of range."
    prompt = "" 
    
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
    
    # Placeholder for medication specific prompt
    # Example: "Identify names of medications, dosages, and frequencies."
    prompt = "" 
    
    result = await gemini.analyze_lab_file(
        file_content=content,
        mime_type=file.content_type,
        prompt=prompt
    )
    
    return {
        "filename": file.filename,
        "analysis": result
    }
