FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/eden881/trmnl-teslamate-reporter
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY main.py pyproject.toml uv.lock .
RUN uv sync --no-dev --locked
CMD ["uv",  "run", "--no-dev", "main.py"]
