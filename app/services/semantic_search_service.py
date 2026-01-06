import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import pickle
import os

class SemanticSearchService:
    def __init__(self):
        # Use a lightweight but effective model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store documents and metadata
        self.documents = []
        self.metadata = []
        
        # Create directory for persistence
        self.index_path = "faiss_index"
        os.makedirs(self.index_path, exist_ok=True)
        
        # Load existing index if available
        self._load_index()
    
    def add_document(self, text: str, metadata: dict = None) -> dict:
        """Add a document to the FAISS index"""
        
        # Generate embedding
        embedding = self.model.encode([text])[0]
        
        # Add to FAISS index
        self.index.add(np.array([embedding], dtype=np.float32))
        
        # Store document and metadata
        self.documents.append(text)
        self.metadata.append(metadata or {})
        
        # Save index
        self._save_index()
        
        return {
            "status": "success",
            "document_id": len(self.documents) - 1,
            "total_documents": len(self.documents)
        }
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        
        if len(self.documents) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Search in FAISS
        k = min(top_k, len(self.documents))
        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32), 
            k
        )
        
        # Prepare results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                # Convert L2 distance to similarity score (0-1 range)
                similarity = 1 / (1 + distance)
                
                results.append({
                    "rank": i + 1,
                    "text": self.documents[idx],
                    "similarity_score": float(similarity),
                    "metadata": self.metadata[idx]
                })
        
        return results
    
    def get_stats(self) -> dict:
        """Get index statistics"""
        return {
            "total_documents": len(self.documents),
            "index_size": self.index.ntotal,
            "dimension": self.dimension
        }
    
    def _save_index(self):
        """Save FAISS index and documents to disk"""
        try:
            faiss.write_index(self.index, os.path.join(self.index_path, "index.faiss"))
            with open(os.path.join(self.index_path, "documents.pkl"), "wb") as f:
                pickle.dump({"documents": self.documents, "metadata": self.metadata}, f)
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def _load_index(self):
        """Load FAISS index and documents from disk"""
        try:
            index_file = os.path.join(self.index_path, "index.faiss")
            docs_file = os.path.join(self.index_path, "documents.pkl")
            
            if os.path.exists(index_file) and os.path.exists(docs_file):
                self.index = faiss.read_index(index_file)
                with open(docs_file, "rb") as f:
                    data = pickle.load(f)
                    self.documents = data["documents"]
                    self.metadata = data["metadata"]
                print(f"Loaded {len(self.documents)} documents from index")
        except Exception as e:
            print(f"Error loading index: {e}")
    
    def clear_index(self):
        """Clear all documents from the index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.metadata = []
        self._save_index()
        return {"status": "success", "message": "Index cleared"}