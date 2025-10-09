import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI

def load_env():
    
    load_dotenv()

    for k in ("PDF_PATH", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Variável de ambiente ausente: {k}")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
    PDF_PATH = os.getenv("PDF_PATH")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # Provider (default: openai)  
    if OPENAI_API_KEY:
        EMBEDDINGS_PROVIDER = "openai"
        API_KEY = OPENAI_API_KEY
        EMBEDDING_MODEL = OPENAI_EMBEDDING_MODEL
        EMBEDDINGS = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY
        )    
    elif GOOGLE_API_KEY:
        EMBEDDINGS_PROVIDER = "google"
        API_KEY = GOOGLE_API_KEY
        EMBEDDING_MODEL = GOOGLE_EMBEDDING_MODEL
        EMBEDDINGS = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
    else:
        raise RuntimeError(f"Variável de ambiente ausente: OPENAI_API_KEY ou GOOGLE_API_KEY")  
    
    return {
        "EMBEDDINGS_PROVIDER": EMBEDDINGS_PROVIDER,
        "DATABASE_URL": DATABASE_URL,
        "PG_VECTOR_COLLECTION_NAME": PG_VECTOR_COLLECTION_NAME,
        "PDF_PATH": PDF_PATH,
        "EMBEDDING_MODEL": EMBEDDING_MODEL,
        "API_KEY": API_KEY,
        "EMBEDDINGS": EMBEDDINGS
    }


def get_llm(envLoaded):
    TEMPERATURE = 0
    if envLoaded["EMBEDDINGS_PROVIDER"] == "openai":
        return ChatOpenAI(
            model=envLoaded.get("OPENAI_LLM_MODEL", "gpt-5-nano"),
            temperature=TEMPERATURE,
            api_key=envLoaded["API_KEY"]
        )
    elif envLoaded["EMBEDDINGS_PROVIDER"] == "google":
        from langchain.chat_models import ChatGooglePaLM
        return ChatGooglePaLM(
            model=envLoaded.get("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite"),
            api_key=envLoaded["API_KEY"],
            temperature=TEMPERATURE
        )
    else:
        raise RuntimeError("Nenhum LLM configurado")