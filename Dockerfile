FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Install system dependencies for moviepy/ffmpeg if not already in the image
# Playwright image usually has ffmpeg, but let's ensure we have what we need.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers (the base image has them, but sometimes we need to be sure)
RUN playwright install chromium

# Copy source code
COPY . .

# Default command (can be overridden)
CMD ["python", "src/main.py"]
