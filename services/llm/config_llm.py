from services.llm.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os

class LLMFactory:

    _cache = {}

    @classmethod
    def gemini(cls):
        if "gemini" not in cls._cache:
            os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY or ""
            cls._cache["gemini"] = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                temperature=1.0, 
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
        return cls._cache["gemini"]

    @classmethod
    def gemini_embeddings(cls):
        if "gemini_embeddings" not in cls._cache:
            os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY or ""
            cls._cache["gemini_embeddings"] =  GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        return cls._cache["gemini_embeddings"]