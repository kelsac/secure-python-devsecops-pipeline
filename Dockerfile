FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd --system appuser \
    && useradd --system --gid appuser --home-dir /app appuser
COPY app ./app
USER appuser
EXPOSE 8080
CMD ["waitress-serve", "--call", "--host=0.0.0.0", "--port=8080", "app.main:create_app"]
