FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app . .

ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/app

USER app

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
