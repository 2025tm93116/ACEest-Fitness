FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATABASE_PATH=/data/aceest.db
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt     && useradd --create-home --uid 10001 appuser     && mkdir -p /data && chown -R appuser:appuser /app /data
COPY app.py .
COPY templates ./templates
COPY tests ./tests
USER appuser
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
