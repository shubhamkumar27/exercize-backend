# Use official Python image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy only requirement files first for better caching
COPY requirements.txt .
COPY requirements-dev.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the application code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]