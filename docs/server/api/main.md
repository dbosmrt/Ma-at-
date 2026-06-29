# `server/api/main.py`

## Module Overview
`main.py` serves as the primary entry point and configuration hub for the FastAPI backend application. It is responsible for instantiating the web server, loading environment variables, mounting middleware (like CORS), and registering all HTTP API routes.

## Dependencies
- `fastapi`: Core framework for building the REST API.
- `fastapi.middleware.cors`: Provides Cross-Origin Resource Sharing capabilities to allow frontend clients to communicate with the API.
- `api.routes`: Imports the `router` which contains all endpoint definitions.
- `pathlib`, `dotenv`: Used to securely traverse the directory tree and load secrets from the root `.env` file before the application boots.
- `uvicorn`: The ASGI web server used to run the application natively if the file is executed directly.

## Core Setup & Logic

### 1. Environment Loading Block
```python
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass
```
- **Purpose**: Ensures that API keys (like `MAAT_API_KEY` and `NVIDIA_API_KEY`) are loaded into the system environment before FastAPI initializes any internal dependencies that might rely on them.

### 2. FastAPI Application Instance
```python
app = FastAPI(
    title="Ma-at Legal AI API",
    description="Backend RAG API for the Indian Legal Code AI Assistant.",
    version="1.0.0"
)
```
- **Purpose**: Creates the global `app` object. The metadata provided here is automatically rendered on the interactive Swagger UI (`/docs`).

### 3. CORS Middleware Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
- **Purpose**: By default, browsers block frontend web applications (like React) from making HTTP requests to a backend on a different port or domain. This middleware explicitly allows cross-origin requests.
- > [!WARNING]
  > **Security Note**: `allow_origins=["*"]` allows any website on the internet to attempt to ping this API. While protected by API Keys, this should be restricted in production to exactly match the frontend client's domain (e.g., `allow_origins=["https://maat-legal.com"]`).

### 4. Router Registration
```python
app.include_router(router)
```
- **Purpose**: Hooks the endpoint logic defined in `server/api/routes.py` into the main application.

### 5. Uvicorn Execution Hook
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
```
- **Purpose**: Allows the developer to start the server simply by running `python main.py`. It binds the server to all network interfaces (`0.0.0.0`) on port `8000` and enables auto-reloading for rapid development.
