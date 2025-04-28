FROM python:3.11-slim

WORKDIR /demo

# Install system dependencies including Git
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv venv && uv pip install -r requirements.txt

# Copy application code
COPY server.py .
COPY client-sse.py .

# Expose the port the server runs on
EXPOSE 8004

# Set environment variables for API keys
ENV EXCHANGE_RATE_API_KEY=${EXCHANGE_RATE_API_KEY}
ENV GROQ_API_KEY=${GROQ_API_KEY}

# Command to run the server
CMD ["uv", "run", "server.py"] 