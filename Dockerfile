FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    transformers \
    torch \
    accelerate \
    bitsandbytes

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Start the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 