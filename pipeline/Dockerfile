FROM python:3.13.11-slim

# Copy UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (for Docker layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# Install dependencies
RUN uv sync --locked

# Copy application code
COPY ingest_data.py ingest_data.py

# Set entry point
ENTRYPOINT ["python", "ingest_data.py"]