import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# Ensure .env is loaded
from pathlib import Path
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

app = FastAPI(
    title="Ma-at Legal AI API",
    description="Backend RAG API for the Indian Legal Code AI Assistant.",
    version="1.0.0"
)

# CORS Middleware for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this in production to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # When run directly
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
