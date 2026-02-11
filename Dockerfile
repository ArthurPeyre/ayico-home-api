FROM python:3.12-slim

# Dossier de travail
WORKDIR /app

# Installer les dépendances système pour compiler psycopg
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier de l'application
COPY ./app ./app

# Exposer le port
EXPOSE 8000

# Lancer Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
