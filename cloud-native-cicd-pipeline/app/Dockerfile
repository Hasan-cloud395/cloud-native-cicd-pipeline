# ---- Build stage ----
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime stage ----
FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
