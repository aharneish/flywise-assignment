## Features

* **Sentiment Analysis** : Analyze text sentiment (positive/negative/neutral) with confidence scores and extract top 5 keywords
* **Text Summarization** : Generate AI-powered summaries using Groq
* **Semantic Search** : Store and search documents using FAISS vector database with sentence embeddings
* **Docker Support** : Fully containerized for easy deployment
* **Swagger UI** : Interactive API documentation at `/docs`

## Tech Stack

* **Framework** : FastAPI
* **LLM** : Groq API (openai/gpt-oss-120b)
* **NLP** : spaCy, NLTK, scikit-learn
* **Embeddings** : Sentence Transformers (all-MiniLM-L6-v2)
* **Vector Database** : FAISS
* **Containerization** : Docker

## Prerequisites

* Python 3.8+
* Docker (optional)
* Groq API Key ([Get one here](https://console.groq.com))

## Installation

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

## API Documentation

Once running, visit:

* **Swagger UI** : [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc** : [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Sample data for API Endpoints

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

## Environment Variables

Create a `.env` file with:

env

```env
GROQ_API_KEY=your_groq_api_key_here
ENVIRONMENT=development
```

## Deployment

### Docker Deployment

bash

```bash
docker build -t ai-text-api .
docker run -d -p 8000:8000 -e GROQ_API_KEY=your_key ai-text-api
```

## Key Features Implementation

### Sentiment Analysis

* Uses Groq API for accurate sentiment classification
* Extracts top 5 keywords using spaCy NLP
* Provides confidence scores
* Handles multiple languages (with appropriate models)

### Text Summarization

* Powered by Groq's openai/gpt-oss-120b model
* Configurable summary length
* Maintains context and key information
* Fast processing times

### Semantic Search

* FAISS-based vector search
* Sentence Transformers embeddings
* Persistent storage
* Metadata support
* Similarity scoring

