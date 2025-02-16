import logging
import time
from datetime import datetime
import os
import aiohttp  # Importuj bibliotekę aiohttp

_LOGGER = logging.getLogger(__name__)

class PVObserver:
    def __init__(self):
        self.production = 0
        self._last_updated = None
        self._running = False
        self._thread = None

    def get_production(self):
        """Zwraca aktualną produkcję (pobiera dane asynchronicznie)."""
        return self.production #zwraca wartosc

    async def _update_data(self):
        """Aktualizuje dane (asynchronicznie z Home Assistant)."""
        hass_url = os.environ.get("SUPERVISOR_API") or os.environ.get("HOMEASSISTANT_API") #pobierz url
        hass_token = os.environ.get("SUPERVISOR_TOKEN")

        if hass_url is None or hass_token is None:
            _LOGGER.error("Brak wymaganych zmiennych środowiskowych (SUPERVISOR_API/HOMEASSISTANT_API, SUPERVISOR_TOKEN).")
            return

        production = await self.get_sensor_data(hass_url, hass_token, "sensor.pv_production") #pobierz dane z HA
        if production is not None:
            try:
                self.production = float(production)
            except ValueError:
                _LOGGER.error(f"Nieprawidłowa wartość produkcji: {production}")
                self.production = 0 #w przypadku bledu
        else:
              _LOGGER.warning("Brak danych o produkcji.")
              self.production = 0

        self._last_updated = datetime.now()
        _LOGGER.info(f"Dane zaktualizowane. Produkcja: {self.production}")



    async def get_sensor_data(self, hass_url, token, entity_id):
        """Pobiera dane sensora z Home Assistant (asynchronicznie)."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        try: #dodana obsługa błędów
          async with aiohttp.ClientSession() as session:
              async with session.get(f"{hass_url}/api/states/{entity_id}", headers=headers) as resp:
                  if resp.status == 200:
                      data = await resp.json()
                      return data["state"]
                  else:
                      _LOGGER.error(f"Błąd pobierania danych z HA (status {resp.status}): {await resp.text()}")
                      return None
        except aiohttp.ClientError as e: #dodana obsługa wyjątków
            _LOGGER.error(f"Błąd połączenia z Home Assistant: {e}")
            return None
        except Exception as e:
            _LOGGER.error(f"Nieoczekiwany błąd podczas pobierania danych: {e}")
            return None