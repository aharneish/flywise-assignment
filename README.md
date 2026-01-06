# AI-Powered Text Intelligence API

A production-ready NLP API built with FastAPI and Groq AI, featuring sentiment analysis, text summarization, and semantic search capabilities.

## 🚀 Features

* **Sentiment Analysis** : Analyze text sentiment (positive/negative/neutral) with confidence scores and extract top 5 keywords
* **Text Summarization** : Generate AI-powered summaries using Groq's LLM
* **Semantic Search** : Store and search documents using FAISS vector database with sentence embeddings
* **RESTful API** : Clean, well-documented FastAPI endpoints
* **Docker Support** : Fully containerized for easy deployment
* **Swagger UI** : Interactive API documentation at `/docs`

## 🛠️ Tech Stack

* **Framework** : FastAPI
* **LLM** : Groq API (Mixtral-8x7b)
* **NLP** : spaCy, NLTK, scikit-learn
* **Embeddings** : Sentence Transformers (all-MiniLM-L6-v2)
* **Vector Database** : FAISS
* **Containerization** : Docker

## 📋 Prerequisites

* Python 3.8+
* Docker (optional)
* Groq API Key ([Get one here](https://console.groq.com))

## 🔧 Installation

### Option 1: Local Setup

1. **Clone the repository**

bash

```bash
git clone <your-repo-url>
cd ai-text-intelligence-api
```

2. **Create virtual environment**

bash

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

bash

```bash
pip install -r requirements.txt
```

4. **Download required models**

bash

```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

5. **Set up environment variables**

bash

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

6. **Run the application**

bash

```bash
uvicorn app.main:app --reload
```

### Option 2: Docker Setup

1. **Build the Docker image**

bash

```bash
docker build -t ai-text-api .
```

2. **Run the container**

bash

```bash
docker run -d -p 8000:8000 -e GROQ_API_KEY=your_api_key_here ai-text-api
```

Or using docker-compose:

yaml

```yaml
# docker-compose.yml
version:'3.8'
services:
api:
build: .
ports:
-"8000:8000"
environment:
- GROQ_API_KEY=${GROQ_API_KEY}
volumes:
- ./faiss_index:/app/faiss_index
```

bash

```bash
docker-compose up -d
```

## 📚 API Documentation

Once running, visit:

* **Swagger UI** : [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc** : [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔍 API Endpoints

### 1. Sentiment Analysis

**POST** `/api/v1/analyze`

Analyze text sentiment and extract keywords.

**Request:**

json

```json
{
"text":"I love working with AI! It makes everything efficient."
}
```

**Response:**

json

```json
{
"sentiment":"positive",
"confidence":0.95,
"keywords":["AI","efficient","love","working","makes"]
}
```

**cURL Example:**

bash

```bash
curl -X POST "http://localhost:8000/api/v1/analyze"\
  -H "Content-Type: application/json"\
  -d '{"text": "I love working with AI! It makes everything efficient."}'
```

### 2. Text Summarization

**POST** `/api/v1/summarize`

Generate concise summaries of long text.

**Request:**

json

```json
{
"text":"Long text to summarize...",
"max_length":150
}
```

**Response:**

json

```json
{
"summary":"This is a concise summary...",
"original_length":500,
"summary_length":120
}
```

**cURL Example:**

bash

```bash
curl -X POST "http://localhost:8000/api/v1/summarize"\
  -H "Content-Type: application/json"\
  -d '{"text": "Artificial intelligence has revolutionized the way we interact with technology...", "max_length": 100}'
```

### 3. Add Document to Index

**POST** `/api/v1/add-document`

Add documents to the semantic search index.

**Request:**

json

```json
{
"text":"FastAPI is a modern web framework for Python",
"metadata":{"source":"documentation","category":"tech"}
}
```

**Response:**

json

```json
{
"status":"success",
"document_id":0,
"total_documents":1
}
```

**cURL Example:**

bash

```bash
curl -X POST "http://localhost:8000/api/v1/add-document"\
  -H "Content-Type: application/json"\
  -d '{"text": "FastAPI is a modern web framework for Python", "metadata": {"category": "tech"}}'
```

### 4. Semantic Search

**POST** `/api/v1/semantic-search`

Search for similar documents.

**Request:**

json

```json
{
"query":"Python web frameworks",
"top_k":5
}
```

**Response:**

json

```json
{
"query":"Python web frameworks",
"results":[
{
"rank":1,
"text":"FastAPI is a modern web framework for Python",
"similarity_score":0.87,
"metadata":{"category":"tech"}
}
]
}
```

**cURL Example:**

bash

```bash
curl -X POST "http://localhost:8000/api/v1/semantic-search"\
  -H "Content-Type: application/json"\
  -d '{"query": "Python web frameworks", "top_k": 3}'
```

### 5. Index Statistics

**GET** `/api/v1/index-stats`

Get semantic search index statistics.

**Response:**

json

```json
{
"total_documents":10,
"index_size":10,
"dimension":384
}
```

### 6. Health Check

**GET** `/api/v1/health`

Check API health status.

**Response:**

json

```json
{
"status":"healthy",
"version":"1.0.0",
"message":"AI Text Intelligence API is running"
}
```

## 🧪 Testing

### Manual Testing

1. Start the server
2. Visit [http://localhost:8000/docs](http://localhost:8000/docs)
3. Use the interactive Swagger UI to test endpoints

### Python Script Testing

python

```python
import requests

BASE_URL ="http://localhost:8000/api/v1"

# Test sentiment analysis
response = requests.post(
f"{BASE_URL}/analyze",
    json={"text":"This is amazing!"}
)
print(response.json())

# Test summarization
response = requests.post(
f"{BASE_URL}/summarize",
    json={
"text":"Long text here...",
"max_length":100
}
)
print(response.json())

# Add document
response = requests.post(
f"{BASE_URL}/add-document",
    json={
"text":"Machine learning is a subset of AI",
"metadata":{"topic":"AI"}
}
)
print(response.json())

# Search
response = requests.post(
f"{BASE_URL}/semantic-search",
    json={"query":"artificial intelligence","top_k":3}
)
print(response.json())
```

## 📁 Project Structure

```
ai-text-intelligence-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── sentiment_service.py      # Sentiment analysis
│   │   ├── summarization_service.py  # Text summarization
│   │   └── semantic_search_service.py # Vector search
│   └── routes/
│       ├── __init__.py
│       └── api.py           # API endpoints
├── faiss_index/             # FAISS index storage (created at runtime)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

## 🔒 Environment Variables

Create a `.env` file with:

env

```env
GROQ_API_KEY=your_groq_api_key_here
ENVIRONMENT=development
```

## 🚀 Deployment

### Docker Deployment

bash

```bash
docker build -t ai-text-api .
docker run -d -p 8000:8000 -e GROQ_API_KEY=your_key ai-text-api
```

### Cloud Deployment Options

* **AWS ECS/Fargate** : Deploy container to AWS
* **Google Cloud Run** : Serverless container deployment
* **Azure Container Instances** : Quick container deployment
* **Heroku** : Use heroku.yml for container deployment
* **DigitalOcean App Platform** : Easy container deployment

## 🎯 Key Features Implementation

### Sentiment Analysis

* Uses Groq API for accurate sentiment classification
* Extracts top 5 keywords using spaCy NLP
* Provides confidence scores
* Handles multiple languages (with appropriate models)

### Text Summarization

* Powered by Groq's Mixtral-8x7b model
* Configurable summary length
* Maintains context and key information
* Fast processing times

### Semantic Search

* FAISS-based vector search
* Sentence Transformers embeddings
* Persistent storage
* Metadata support
* Similarity scoring

## 🔧 Performance Optimization

* Caching of ML models
* Efficient vector operations with FAISS
* Async API endpoints
* Connection pooling
* Lightweight embedding model (all-MiniLM-L6-v2)

## 📝 Notes

* The FAISS index persists data in the `faiss_index/` directory
* First request may be slower due to model loading
* Groq API has rate limits - check your quota
* For production, consider adding authentication and rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙋 Support

For issues or questions:

* Open an issue on GitHub
* Check the API documentation at `/docs`
* Review Groq API documentation

## 🎓 Assignment Completion

This project fulfills all requirements:

✅ Sentiment Analysis with keyword extraction

✅ Text Summarization using Transformer (Groq/Mixtral)

✅ Semantic Search with FAISS vector database

✅ FastAPI with Pydantic models

✅ Docker containerization

✅ Swagger UI documentation at `/docs`

✅ Clean code structure and documentation

✅ Production-ready deployment setup

**Bonus Features:**

* Persistent FAISS index
* Metadata support for documents
* Health check endpoint
* Comprehensive error handling
* RESTful API design
* Interactive documentation
