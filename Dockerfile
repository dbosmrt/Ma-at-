# Stage 1: Build the React frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY app/package*.json ./
RUN npm install
COPY app/ ./
RUN npm run build

# Stage 2: Build the Python backend and serve everything
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies required for unstructured[pdf] and building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY server/ ./server/

# Copy the built frontend from Stage 1 into the location FastAPI expects
COPY --from=frontend-builder /app/dist ./app/dist

# Data and vector_store directories are excluded via .dockerignore
# They should be mounted as volumes at runtime using -v flag.

# Set working directory to server for correct relative imports and execution paths
WORKDIR /app/server

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI (which now serves both API and static frontend)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
