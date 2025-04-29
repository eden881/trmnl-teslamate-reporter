FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/eden881/trmnl-teslamate-reporter
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY main.py pyproject.toml uv.lock /app
WORKDIR /app
RUN uv sync --locked
CMD ["uv",  "run",  "main.py"]
