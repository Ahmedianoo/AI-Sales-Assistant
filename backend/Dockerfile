FROM python:3.10-slim as base

WORKDIR /app

# System dependencies for Python + Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc wget curl git \
    libnss3 libatk-bridge2.0-0 libcups2 libxss1 libasound2 libgtk-3-0 \
    libx11-xcb1 libxcomposite1 libxrandr2 libgbm1 libpangocairo-1.0-0 libpango-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install PyTorch CPU + Python dependencies
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Install Playwright browsers
RUN playwright install --with-deps

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
