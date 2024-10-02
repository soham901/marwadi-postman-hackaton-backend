FROM python:3.11-slim

# Install system dependencies
RUN apt update && apt install -y gcc build-essential libpq-dev

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 to allow access to FastAPI
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
