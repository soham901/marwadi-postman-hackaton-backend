FROM python:3.11-slim

# Install gcc and other necessary development tools
RUN apt update && apt install -y gcc build-essential

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Install Gunicorn
RUN pip install gunicorn

# Default command to run FastAPI using Gunicorn
CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]