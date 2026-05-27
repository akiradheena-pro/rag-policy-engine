# Use official Python slim image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (if needed by packages like chromadb or sentence-transformers)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy entire application code into container
COPY . .

# Expose port 10000 (Render's default for Docker services)
EXPOSE 10000

# Run Streamlit app on port 10000, accessible from any IP
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "10000", "--server.address", "0.0.0.0"]
