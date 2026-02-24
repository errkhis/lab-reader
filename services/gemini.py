import os
import base64
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
    """
    if not prompt:
        # Default fallback prompt
        prompt = "Explain what this document is about."

    # Encode the binary content to base64 for LangChain's multimodal support
    base64_data = base64.b64encode(file_content).decode("utf-8")
    
    # Construct the message with both text and the file
    # For Gemini, LangChain supports passing images and PDFs via the image_url block structure
    # or as direct media parts depending on the specific LangChain version's implementation.
    # The standard way in LangChain for multimodal is using content blocks.
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_data}"}
            },
        ]
    )
    
    # Use ainvoke for asynchronous call
    response = await llm.ainvoke([message])
    
    # Return the content of the response
    return response.content
