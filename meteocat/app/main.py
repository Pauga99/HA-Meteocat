import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests
from paho.mqtt import client as mqtt

LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger("meteocat")

API_KEY = os.environ["METEOCAT_API_KEY"]
CODI_MUNICIPI = os.environ["METEOCAT_CODI_MUNICIPI"]
NOM_MUNICIPI = os.environ.get("METEOCAT_NOM_MUNICIPI") or CODI_MUNICIPI
MQTT_HOST = os.environ["METEOCAT_MQTT_HOST"]
MQTT_PORT = int(os.environ["METEOCAT_MQTT_PORT"])
MQTT_USUARI = os.environ.get("METEOCAT_MQTT_USUARI")
MQTT_CONTRASENYA = os.environ.get("METEOCAT_MQTT_CONTRASENYA")
INTERVAL_MINUTS = int(os.environ.get("METEOCAT_INTERVAL_MINUTS", "30"))
USE_HTTPS = os.environ.get("METEOCAT_HTTPS", "true").lower() == "true"

BASE_URL = f"{'https' if USE_HTTPS else 'http'}://api.meteo.cat/xema/v1"

SENSORS = {
    "temp_max": {
        "name": "Temperatura màxima",
        "device_class": "temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
    },
    "temp_min": {
        "name": "Temperatura mínima",
        "device_class": "temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
    },
    "humitat": {
        "name": "Humitat",
        "device_class": "humidity",
        "unit": "%",
        "icon": "mdi:water-percent",
    },
    "precipitacio": {
        "name": "Precipitació",
        "device_class": "precipitation",
        "unit": "mm",
        "icon": "mdi:weather-rainy",
    },
    "prob_precipitacio": {
        "name": "Probabilitat de precipitació",
        "device_class": "precipitation_probability",
        "unit": "%",
        "icon": "mdi:weather-pouring",
    },
    "vent_velocitat": {
        "name": "Velocitat del vent",
        "device_class": "wind_speed",
        "unit": "m/s",
        "icon": "mdi:weather-windy",
    },
    "estat_cel": {
        "name": "Estat del cel",
        "device_class": None,
        "unit": None,
        "icon": "mdi:weather-partly-cloudy",
    },
    "ultima_actualitzacio": {
        "name": "Última actualització",
        "device_class": "timestamp",
        "unit": None,
        "icon": "mdi:clock-outline",
    },
}


def _mqtt_client() -> mqtt.Client:
    client = mqtt.Client(client_id=f"meteocat_{CODI_MUNICIPI}")
    if MQTT_USUARI:
        client.username_pw_set(MQTT_USUARI, MQTT_CONTRASENYA)
    return client


def _discovery_topic(sensor_id: str) -> str:
    return f"homeassistant/sensor/meteocat_{CODI_MUNICIPI}/{sensor_id}/config"


def _state_topic(sensor_id: str) -> str:
    return f"homeassistant/sensor/meteocat_{CODI_MUNICIPI}/{sensor_id}/state"


def publish_discovery(client: mqtt.Client) -> None:
    device = {
        "identifiers": [f"meteocat_{CODI_MUNICIPI}"],
        "manufacturer": "Meteocat",
        "name": f"Meteocat {NOM_MUNICIPI}",
        "model": "Predicció municipal",
    }
    for sensor_id, meta in SENSORS.items():
        payload = {
            "name": f"{meta['name']} ({NOM_MUNICIPI})",
            "state_topic": _state_topic(sensor_id),
            "unique_id": f"meteocat_{CODI_MUNICIPI}_{sensor_id}",
            "device": device,
            "icon": meta.get("icon"),
        }
        if meta.get("device_class"):
            payload["device_class"] = meta["device_class"]
        if meta.get("unit"):
            payload["unit_of_measurement"] = meta["unit"]
            payload["state_class"] = "measurement"
        client.publish(_discovery_topic(sensor_id), json.dumps(payload), retain=True)


def _extract_from_variables(variables: list[Dict[str, Any]], keys: set[str]) -> Optional[Any]:
    for variable in variables:
        code = str(variable.get("codi", "")).lower()
        if code in keys:
            values = variable.get("valors") or variable.get("valorsPrediccio") or []
            if isinstance(values, list) and values:
                return values[0].get("valor") if isinstance(values[0], dict) else values[0]
            return variable.get("valor")
    return None


def parse_forecast(data: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    dies = data.get("dies") or data.get("days") or []
    if not dies:
        return result
    dia = dies[0]
    variables = dia.get("variables") or dia.get("variablesPrediccio") or []

    result["temp_max"] = (
        dia.get("tempmax")
        or dia.get("tmax")
        or _extract_from_variables(variables, {"tmax", "tempmax", "temp_max"})
    )
    result["temp_min"] = (
        dia.get("tempmin")
        or dia.get("tmin")
        or _extract_from_variables(variables, {"tmin", "tempmin", "temp_min"})
    )
    result["humitat"] = (
        dia.get("humitat")
        or dia.get("humidity")
        or _extract_from_variables(variables, {"hr", "humitat", "humidity"})
    )
    result["precipitacio"] = (
        dia.get("precipitacio")
        or dia.get("precipitation")
        or _extract_from_variables(variables, {"prec", "precipitacio", "precipitation"})
    )
    result["prob_precipitacio"] = (
        dia.get("probprecip")
        or dia.get("prob_precipitacio")
        or _extract_from_variables(variables, {"probprecip", "prob_precipitacio", "pp"})
    )
    result["vent_velocitat"] = (
        dia.get("vent")
        or dia.get("vent_velocitat")
        or _extract_from_variables(variables, {"vent", "vent_velocitat", "ff"})
    )
    result["estat_cel"] = (
        dia.get("estat_cel")
        or dia.get("cel")
        or _extract_from_variables(variables, {"estat_cel", "cel", "sky"})
    )

    return {k: v for k, v in result.items() if v is not None}


def fetch_forecast() -> Dict[str, Any]:
    url = f"{BASE_URL}/prediccio/municipi/{CODI_MUNICIPI}/diaria"
    headers = {"X-Api-Key": API_KEY}
    LOGGER.info("Consultant Meteocat: %s", url)
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def publish_states(client: mqtt.Client, states: Dict[str, Any]) -> None:
    for sensor_id in SENSORS:
        if sensor_id not in states:
            continue
        value = states[sensor_id]
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        client.publish(_state_topic(sensor_id), payload=str(value), retain=True)


def main() -> None:
    client = _mqtt_client()
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    publish_discovery(client)

    while True:
        try:
            forecast = fetch_forecast()
            states = parse_forecast(forecast)
            states["ultima_actualitzacio"] = datetime.now(timezone.utc).isoformat()
            publish_states(client, states)
            LOGGER.info("Predicció publicada correctament.")
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Error en obtenir o publicar la predicció: %s", exc)
        time.sleep(INTERVAL_MINUTS * 60)


if __name__ == "__main__":
    main()
