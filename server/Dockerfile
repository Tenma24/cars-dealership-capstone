FROM node:24-alpine AS frontend
WORKDIR /ui
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend /ui/build ./frontend/build
RUN DJANGO_DEBUG=1 python manage.py collectstatic --noinput && rm -f .local-secret && useradd -m appuser && mkdir -p /data && chown -R appuser:appuser /app /data
USER appuser
ENV DJANGO_DEBUG=0 SQLITE_PATH=/data/db.sqlite3 PORT=8000
EXPOSE 8000
CMD ["python","start.py"]
