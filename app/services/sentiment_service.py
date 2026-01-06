import spacy
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
from app.config import get_settings
import re
from collections import Counter
import httpx

class SentimentService:
    def __init__(self):
        self.settings = get_settings()
        
        http_client = httpx.Client(
            timeout=30.0,
            trust_env=False  # 🚀 THIS is the key line
        )

        self.client = Groq(
            api_key=self.settings.groq_api_key,
            http_client=http_client
        )
        
        # Load spacy model for NLP processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Download NLTK data if needed
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
    
    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment using Groq API and extract keywords"""
        
        # Get sentiment from Groq
        sentiment_prompt = f"""Analyze the sentiment of the following text and respond with ONLY a JSON object in this exact format:
{{"sentiment": "positive" or "negative" or "neutral", "confidence": 0.0-1.0}}

Text: {text}

Respond with ONLY the JSON object, no other text."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analysis expert. Respond only with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": sentiment_prompt
                    }
                ],
                model=self.settings.groq_model,
                temperature=0.75,
                max_tokens=1024
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            # Parse JSON response
            import json
            sentiment_data = json.loads(response_text)
            
            # Extract keywords
            keywords = self.extract_keywords(text)
            
            return {
                "sentiment": sentiment_data.get("sentiment", "neutral"),
                "confidence": sentiment_data.get("confidence", 0.5),
                "keywords": keywords
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            # Fallback to basic keyword extraction
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "keywords": self.extract_keywords(text)
            }
    
    def extract_keywords(self, text: str, top_n: int = 5) -> list:
        """Extract top keywords using spaCy and TF-IDF"""
        
        # Process with spaCy
        doc = self.nlp(text.lower())
        
        # Extract nouns, proper nouns, and adjectives
        candidates = []
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                candidates.append(token.lemma_)
        
        # Also extract named entities
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT', 'EVENT']:
                candidates.append(ent.text.lower())
        
        # Count frequency
        if candidates:
            word_freq = Counter(candidates)
            keywords = [word for word, _ in word_freq.most_common(top_n)]
            return keywords[:top_n]
        
        # Fallback: simple word frequency
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        filtered_words = [w for w in words if w not in self.stop_words]
        word_freq = Counter(filtered_words)
        return [word for word, _ in word_freq.most_common(top_n)]