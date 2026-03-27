
FROM python:3.13-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:c4f5de312ee66d46810635ffc5df34a1973ba753e7241ce3a08ef979ddd7bea5 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN useradd -u 10001 -m appuser

WORKDIR /home/appuser/app

ENV PATH="/home/appuser/app/.venv/bin:${PATH}"

COPY --chown=10001:10001 pyproject.toml .
COPY --chown=10001:10001 uv.lock .


FROM base AS dev
RUN uv sync --frozen --no-install-project
COPY --chown=10001:10001 src/ ./src/
COPY --chown=10001:10001 tests/ ./tests/
RUN uv sync --frozen
USER 10001
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]

FROM base AS runtime
RUN uv sync --frozen --no-dev --no-install-project
COPY --chown=10001:10001 src/ ./src/
RUN uv sync --frozen --no-dev
USER 10001
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]

