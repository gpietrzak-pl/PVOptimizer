FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików aplikacji i listy zależności
COPY app/ /app
COPY requirements.txt /app

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Eksponowanie portu (np. 8000)
EXPOSE 8000

# Uruchomienie aplikacji przez uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]