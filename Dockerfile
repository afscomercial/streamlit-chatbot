FROM python:3.10-slim

# Disable telemetry
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/app/cache \
    HF_HOME=/app/cache

WORKDIR /app

# Install Python dependencies first (leverages Docker layer caching)
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Hugging Face sets the PORT env variable (default 7860)
EXPOSE 7860

RUN mkdir -p /app/cache && chmod 777 /app/cache

CMD bash -c "streamlit run app.py --server.port ${PORT:-7860} --server.address 0.0.0.0 --server.headless true" 