FROM python:3.10-slim

WORKDIR /app

# Copy dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

EXPOSE 8000

# Run FastAPI using uvicorn
# Format: <module>:<app_instance>
# Since main.py is in the root, we just use main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
