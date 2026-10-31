FROM python:3.11-slim

# Avoid prompting tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal dependencies for Office file support
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser/sheetSort

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY sheetsort/ ./sheetsort/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    SHEETSORT_LOG_LEVEL=INFO

# Run the application
CMD ["streamlit", "run", "sheetsort/app/main.py"]