FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && apt-get clean

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .
RUN rm -rf .venv

# Install dependencies
RUN uv sync

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Run your Python app that initializes and launches FastAPI
CMD ["uv", "run", "python", "main.py"]