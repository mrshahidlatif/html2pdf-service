FROM python:3.11-slim

# Install system dependencies required for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Debug: List contents of current directory and src directory
RUN echo "Current directory contents:" && ls -la && \
    echo "\nSrc directory contents:" && ls -la src/

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install the package (using PYTHONPATH to ensure src is in the path)
ENV PYTHONPATH=/app/src
RUN pip install --no-cache-dir -e . --verbose

EXPOSE 5007

# Use Gunicorn with 4 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:5007", "--workers", "4", "src:app"]
