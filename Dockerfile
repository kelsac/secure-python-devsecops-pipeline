
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Apply the available Debian zlib security update
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Update affected Python packages and install app dependencies
RUN python -m pip install --no-cache-dir --upgrade \
        "msgpack>=1.2.3" \
        "setuptools>=78.1.1" \
        "urllib3>=2.8.0" \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && groupadd --system appuser \
    && useradd --system --gid appuser --home-dir /app appuser

COPY app ./app

# Remove the package installer from the production image.
# Flask and Waitress are already installed.
RUN python -m pip uninstall --yes pip

USER appuser

EXPOSE 8080

CMD ["waitress-serve", "--call", "--host=0.0.0.0", "--port=8080", "app.main:create_app"]
