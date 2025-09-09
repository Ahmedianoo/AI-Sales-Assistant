# Start with a slim Python image
FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies needed for Python packages (build + runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc wget curl \
    && rm -rf /var/lib/apt/lists/*

# -----------------------
# Install dependencies
# -----------------------

# Copy only requirements first (better Docker caching)
COPY requirements.txt .

# First install CPU-only PyTorch, then the rest
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# -----------------------
# Copy app code
# -----------------------
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
