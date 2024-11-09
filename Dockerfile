FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all Python files
COPY *.py .
COPY .env .

# Add the current directory to PYTHONPATH
ENV PYTHONPATH=/app

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]