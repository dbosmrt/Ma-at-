import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Serve static frontend files if they exist (for single-container Docker deployment)
static_dir = Path(__file__).parent.parent.parent / "app" / "dist"
if static_dir.exists():
    # Mount the assets directory explicitly
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
    
    # Catch-all route to serve the SPA
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        path = static_dir / full_path
        if path.exists() and path.is_file():
            return FileResponse(path)
        return FileResponse(static_dir / "index.html")

if __name__ == "__main__":
    import uvicorn
    # When run directly
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
