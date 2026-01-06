from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    AI-Powered Text Intelligence API built with FastAPI and Groq AI.
    
    ## Features
    
    * **Sentiment Analysis**: Analyze text sentiment and extract keywords
    * **Text Summarization**: Generate concise summaries using AI
    * **Semantic Search**: Store and search documents using vector embeddings
    
    ## Tech Stack
    
    - FastAPI for API framework
    - Groq API for LLM capabilities
    - spaCy for NLP processing
    - FAISS for vector search
    - Sentence Transformers for embeddings
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to AI Text Intelligence API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)