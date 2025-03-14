# Use official Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependencies first (to optimize Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY .env.local .
COPY src ./src

# Expose FastAPI default port
EXPOSE 8000

# Set environment variables (modify as needed)
# ENV ENVIRONMENT=local

# Run the FastAPI application via main.py
CMD ["python", "src/main.py"]
