from pydantic import BaseModel, Field
from typing import List, Optional

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="Input text to analyze")

class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Sentiment classification: positive, negative, or neutral")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    keywords: List[str] = Field(..., description="Top 5 keywords extracted from text")

class SummarizeInput(BaseModel):
    text: str = Field(..., min_length=10, description="Text to summarize")
    max_length: Optional[int] = Field(150, ge=50, le=500, description="Maximum length of summary")

class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(..., description="Original text length in characters")
    summary_length: int = Field(..., description="Summary length in characters")

class SemanticSearchInput(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    top_k: Optional[int] = Field(5, ge=1, le=10, description="Number of results to return")

class SemanticSearchResponse(BaseModel):
    query: str
    results: List[dict] = Field(..., description="List of similar texts with scores")

class AddDocumentInput(BaseModel):
    text: str = Field(..., min_length=1, description="Document text to add to the index")
    metadata: Optional[dict] = Field(default_factory=dict, description="Optional metadata")

class HealthResponse(BaseModel):
    status: str
    version: str
    message: str