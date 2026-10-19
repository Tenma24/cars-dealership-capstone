FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd -m appuser
COPY app.py ./
USER appuser
EXPOSE 5050
CMD ["waitress-serve","--host=0.0.0.0","--port=5050","app:app"]
