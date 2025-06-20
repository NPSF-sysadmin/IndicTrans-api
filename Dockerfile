FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Create venv inside container (optional)
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Copy source code
COPY app ./app

# Use venv's Python
ENV PATH="/venv/bin:$PATH"

# Expose the port FastAPI runs on
EXPOSE 8088

# Command to run the API
CMD ["uvicorn", "app.translate_openai_api:app", "--host", "0.0.0.0", "--port", "8088"]
