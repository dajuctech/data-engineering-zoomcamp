# Start with slim Python 3.13 image
FROM python:3.13.11-slim

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# Install dependencies (only production, not dev)
RUN uv sync --locked --no-dev

# Copy application code
COPY ingest_data.py ingest_data.py

# Set entry point
ENTRYPOINT ["python", "ingest_data.py"]
