from groq import Groq
from app.config import get_settings
import httpx

class SummarizationService:
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
    
    def summarize_text(self, text: str, max_length: int = 150) -> dict:
        """Summarize text using Groq API"""
        
        # Determine summary style based on max_length
        if max_length < 100:
            style = "very concise"
        elif max_length < 200:
            style = "concise"
        else:
            style = "detailed"
        
        summarization_prompt = f"""Summarize the following text in a {style} manner. 
Keep the summary under {max_length} words while capturing the main points.

Text: {text}

Summary:"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating clear, concise summaries that capture key information."
                    },
                    {
                        "role": "user",
                        "content": summarization_prompt
                    }
                ],
                model=self.settings.groq_model,
                temperature=0.5,
                max_tokens=max_length * 2  # Allow some buffer
            )
            
            summary = chat_completion.choices[0].message.content.strip()
            
            return {
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary)
            }
            
        except Exception as e:
            raise Exception(f"Error in summarization: {str(e)}")