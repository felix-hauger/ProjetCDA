# Stage 1 : build deps
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2 : runtime
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
COPY --from=builder /root/.local /root/.local
COPY ./app ./app
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
