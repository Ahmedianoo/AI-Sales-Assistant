from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_gemini_llm(model: str = "gemini-2.5-flash"):
    """Return Gemini model wrapped for LangChain."""
    return ChatGoogleGenerativeAI(
        model=model,
        # google_api_key=os.environ.get("GOOGLE_API_KEY")
        google_api_key="AIzaSyAFwBWcUc0uX8_uSImzpYxjGemqI5zfmfQ"
    )
