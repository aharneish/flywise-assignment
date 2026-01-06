from fastapi import APIRouter, HTTPException
from app.models import (
    TextInput, SentimentResponse, SummarizeInput, SummarizeResponse,
    SemanticSearchInput, SemanticSearchResponse, AddDocumentInput, HealthResponse
)
from app.services.sentiment_service import SentimentService
from app.services.summarization_service import SummarizationService
from app.services.semantic_search_service import SemanticSearchService

router = APIRouter()

# Lazy initialization of services
_sentiment_service = None
_summarization_service = None
_semantic_search_service = None

def get_sentiment_service():
    global _sentiment_service
    if _sentiment_service is None:
        _sentiment_service = SentimentService()
    return _sentiment_service

def get_summarization_service():
    global _summarization_service
    if _summarization_service is None:
        _summarization_service = SummarizationService()
    return _summarization_service

def get_semantic_search_service():
    global _semantic_search_service
    if _semantic_search_service is None:
        _semantic_search_service = SemanticSearchService()
    return _semantic_search_service

@router.post("/analyze", response_model=SentimentResponse, tags=["Text Analysis"])
async def analyze_text(input_data: TextInput):
    """
    Analyze text sentiment and extract top keywords.
    
    - **text**: Input text to analyze
    
    Returns sentiment (positive/negative/neutral), confidence score, and top 5 keywords.
    """
    try:
        sentiment_service = get_sentiment_service()
        result = sentiment_service.analyze_sentiment(input_data.text)
        return SentimentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/summarize", response_model=SummarizeResponse, tags=["Text Analysis"])
async def summarize_text(input_data: SummarizeInput):
    """
    Summarize the provided text using Groq AI.
    
    - **text**: Text to summarize (minimum 10 characters)
    - **max_length**: Maximum length of summary in words (50-500)
    
    Returns a concise summary of the input text.
    """
    try:
        summarization_service = get_summarization_service()
        result = summarization_service.summarize_text(
            input_data.text, 
            input_data.max_length
        )
        return SummarizeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@router.post("/semantic-search", response_model=SemanticSearchResponse, tags=["Semantic Search"])
async def semantic_search(input_data: SemanticSearchInput):
    """
    Search for semantically similar documents.
    
    - **query**: Search query text
    - **top_k**: Number of results to return (1-10)
    
    Returns the most similar documents from the index.
    """
    try:
        semantic_search_service = get_semantic_search_service()
        results = semantic_search_service.search(input_data.query, input_data.top_k)
        return SemanticSearchResponse(query=input_data.query, results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/add-document", tags=["Semantic Search"])
async def add_document(input_data: AddDocumentInput):
    """
    Add a document to the semantic search index.
    
    - **text**: Document text to index
    - **metadata**: Optional metadata (key-value pairs)
    
    Returns confirmation and document ID.
    """
    try:
        semantic_search_service = get_semantic_search_service()
        result = semantic_search_service.add_document(
            input_data.text, 
            input_data.metadata
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add document: {str(e)}")

@router.get("/index-stats", tags=["Semantic Search"])
async def get_index_stats():
    """
    Get statistics about the semantic search index.
    
    Returns total documents and index information.
    """
    try:
        semantic_search_service = get_semantic_search_service()
        return semantic_search_service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.delete("/clear-index", tags=["Semantic Search"])
async def clear_index():
    """
    Clear all documents from the semantic search index.
    
    Returns confirmation message.
    """
    try:
        semantic_search_service = get_semantic_search_service()
        return semantic_search_service.clear_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear index: {str(e)}")

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns API status and version information.
    """
    from app.config import get_settings
    settings = get_settings()
    
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        message="AI Text Intelligence API is running"
    )