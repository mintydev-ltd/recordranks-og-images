# Python version should match .python-version
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install Python dependencies from the lockfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Install Chromium and its system dependencies
RUN uv run playwright install --with-deps chromium

COPY main.py ./

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "--proxy-headers", "--port", "80"]
