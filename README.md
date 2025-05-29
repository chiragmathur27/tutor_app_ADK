# Tutor Agent

A FastAPI-based backend service that implements a conversational AI tutor using Google's AI Development Kit (ADK).

Frontend Repo : https://github.com/chiragmathur27/tutor_app_adk_fe
Deployed URL : https://tutor-app-adk-fe.vercel.app/

## Overview

This project is a backend service that provides an AI-powered tutoring system. It uses Google's AI Development Kit (ADK) to create an interactive tutoring experience, allowing users to have natural conversations with an AI tutor.

## Features

- FastAPI-based RESTful API server
- Real-time conversational AI tutoring
- Session management for maintaining conversation context
- CORS support for frontend integration
- Integration with Google's AI Generative Language API
- Customizable agent responses

## Technical Stack

- Backend Framework: FastAPI
- AI Development: Google ADK
- Session Management: InMemorySessionService
- API Client: Google AI Generative Language
- Environment Management: python-dotenv

## Setup Instructions

### Prerequisites

1. Python 3.8+
2. pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/chiragmathur27/tutor_app_ADK
cd tutor_agent
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
GOOGLE_API_KEY="AIz.."
GOOGLE_GENAI_USE_VERTEXAI=FALSE
WOLFRAM_ALPHA_APPID=""
PORT=8000
```

### Running the Service

1. Start the FastAPI server:
```bash
uvicorn backend:app --reload
```

The server will start on `http://localhost:8000` by default.

### API Endpoints

- `POST /chat`: Main chat endpoint for sending messages to the AI tutor
- `GET /health`: Health check endpoint

### Example Usage

```python
import requests

# Send a message to the tutor
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "content": "I need help with Python programming",
    }
)

# Get the tutor's response
tutor_response = response.json()
```

## Project Structure

```
tutor_agent/
├── backend.py           # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── .gitignore          # Git ignore file
└── tutor_agent/        # Agent implementation directory
```
