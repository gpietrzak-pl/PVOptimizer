FROM python:3.9-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu
COPY . /app

# Instalacja zależności (np. FastAPI i inne wymagane biblioteki)
RUN pip install --no-cache-dir fastapi uvicorn

# Opcjonalnie: instalacja innych zależności lub narzędzi diagnostycznych
# RUN pip install --no-cache-dir <inne-pakiety>

# Ustawienie portu (jeśli aplikacja nasłuchuje, np. na 8000)
EXPOSE 8000

# Punkt wejścia – uruchomienie aplikacji FastAPI przez uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
