import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Initialize the LangChain Gemini model
# Note: langchain-google-genai 4.x uses the consolidated google-genai SDK
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)

async def analyze_lab_file(file_content: bytes, mime_type: str, prompt: str = ""):
    """
    Analyzes a lab file (image or PDF) using Gemini via LangChain.
    Passes raw bytes directly using the 'media' block to match the native SDK behavior
    and avoid base64 overhead.
    """
    if not prompt:
        # Default fallback prompt
        prompt = "Explain what this document is about."

    # Construct the message with both text and the raw binary data.
    # We use the 'media' type block which is supported by langchain-google-genai 2.x/4.x
    # and maps directly to the underlying Google GenAI SDK's media parts.
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "media",
                "mime_type": mime_type,
                "data": file_content
            },
        ]
    )
    
    # Use ainvoke for asynchronous call
    response = await llm.ainvoke([message])
    
    # Return the content of the response
    return response.content
