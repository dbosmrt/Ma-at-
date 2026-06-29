# `security.py`

## Module Overview
Implements the HTTP authentication layer for the FastAPI backend, utilizing header-based API key validation to protect the AI endpoints from unauthorized access.

## Dependencies
- `fastapi.Security, HTTPException, status`: Used to cleanly throw standard HTTP 403 errors and integrate with FastAPI's dependency injection system.
- `fastapi.security.api_key.APIKeyHeader`: A built-in FastAPI security scheme that explicitly defines what HTTP header to look for and automatically hooks into the Swagger UI generation.

## Component Breakdown

### 1. Scheme Definition
```python
API_KEY_NAME = "X-API-Key"
api_key_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
```
- **Logic**: Instructs FastAPI to look for the header `X-API-Key` on incoming requests. `auto_error=False` is set so that if the header is completely missing, the framework passes `None` into our validation function rather than automatically crashing with a generic 403, allowing us to throw a highly specific, custom error message instead.

### 2. `get_api_key(api_key: str = Security(api_key_scheme)) -> str`
- **Role**: This function is injected into the route definitions via `Depends(get_api_key)`. FastAPI automatically executes this function *before* it allows the request to reach the core route logic.
- **Environment Fallback**: It attempts to load `MAAT_API_KEY` from the system environment. If it is not found, it falls back to a hardcoded string `"maat-local-dev-key-777"`. This ensures smooth local testing for new developers without forcing them to configure `.env` files immediately.
- **Validation**: If the incoming key matches the expected key, the request is allowed to proceed. If it fails, it raises an `HTTPException(status_code=403)` and prints out the exact key it received to aid in frontend integration debugging.
