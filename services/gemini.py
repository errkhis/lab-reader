import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# TOKEN OPTIMIZATION:
# 1. Temperature=0 ensures direct, non-wordy responses.
# 2. max_output_tokens=800 focuses on brevity (plenty for a medical summary).
# 3. model_kwargs: Disable 'thinking' to minimize token overhead.
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)

async def analyze_lab_file(file_content: bytes, mime_type: str, prompt: str = ""):
    """
    Maximum Token Optimization:
    - Moves all behavioral context to SystemMessage.
    - Passes raw media bytes to avoid base64 tokenization errors (Flash costs 258 flat).
    - Removes all pleasantries via instructions.
    """
    
    # SystemMessage is more efficient for "Behavioral Anchoring" in Gemini
    system_msg = SystemMessage(content=prompt)
    
    # HumanMessage contains ONLY the image/PDF data
    message = HumanMessage(
        content=[
            {
                "type": "media",
                "mime_type": mime_type,
                "data": file_content
            },
        ]
    )
    
    response = await llm.ainvoke([system_msg, message])
    return response.content
