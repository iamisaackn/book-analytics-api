# syntax=docker/dockerfile:1
# Stage 1: dependency builder
FROM python:3.13-slim AS builder
RUN pip install --upgrade pip
WORKDIR /build
COPY requirements/prod.txt .
RUN pip install --no-cache-dir --prefix=/install -r prod.txt

# Stage 2: lean runtime image
FROM python:3.13-slim AS runtime

ARG GIT_COMMIT=unknown
ARG GIT_BRANCH=unknown

LABEL org.opencontainers.image.source="https://github.com/YOUR_USERNAME/book-analytics-api" \
      git.commit="${GIT_COMMIT}" \
      git.branch="${GIT_BRANCH}"

COPY --from=builder /install /usr/local
WORKDIR /app

COPY app ./app
COPY scripts ./scripts

# Seed the demo DB on first run
RUN python scripts/seed.py

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker \
     -w ${GUNICORN_WORKERS:-2} \
     -b 0.0.0.0:8000 \
     --timeout 60 \
     --access-logfile - \
     --error-logfile - \
     app.main:app"]