from flask import Flask, jsonify, request
import logging
import os
from .observer import PVObserver  # Importuj klasę obserwatora
import asyncio #import biblioteki

app = Flask(__name__)

# Konfiguracja logowania (pobiera poziom z opcji dodatku)
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=log_level)
_LOGGER = logging.getLogger(__name__)

# Inicjalizacja obserwatora
observer = PVObserver()

async def update_data_periodically():  # Asynchroniczna funkcja do aktualizacji danych
    """Aktualizuje dane z określoną częstotliwością."""
    while True:
        await observer._update_data()  # Użyj await, bo _update_data jest asynchroniczne
        await asyncio.sleep(60)  # Czekaj 60 sekund (możesz dostosować)

@app.route('/api/health')
def health_check():
    """Endpoint sprawdzający, czy aplikacja działa."""
    return jsonify({"status": "ok"})

@app.route('/pvoptimizer')
def index():
	return "Witaj w panelu Optymalizatora PV!"

@app.route('/pvoptimizer/api/data')
async def get_data():
     """Przykładowy endpoint zwracający dane."""
     data = {
         "production": observer.get_production(),
         "consumption": 1500,  # Przykładowe dane (docelowo z HA)
         "battery_level": 80    # Przykładowe dane (docelowo z HA)
     }
     return jsonify(data)

@app.before_first_request #uruchomienie funkcji przy starcie
def activate_job():
  asyncio.create_task(update_data_periodically()) #dodanie taska



if __name__ == '__main__':
    # Uruchom pętlę asynchroniczną
     # Uruchom serwer Flask
    app.run(host='0.0.0.0', port=8123, debug=(log_level == 'DEBUG'))
    # loop = asyncio.get_event_loop()  # Pobierz pętlę zdarzeń # Stara wersja
    # loop.run_until_complete(app.run_task(host='0.0.0.0', port=8123, debug=(log_level == 'DEBUG'))) # Stara wersja - nie działa z before_first_request