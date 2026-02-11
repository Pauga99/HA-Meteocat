#!/usr/bin/env bashio
set -euo pipefail

API_KEY=$(bashio::config 'api_key')
CODI_MUNICIPI=$(bashio::config 'codi_municipi')
NOM_MUNICIPI=$(bashio::config 'nom_municipi')
MQTT_HOST=$(bashio::config 'mqtt_host')
MQTT_PORT=$(bashio::config 'mqtt_port')
MQTT_USUARI=$(bashio::config 'mqtt_usuari')
MQTT_CONTRASENYA=$(bashio::config 'mqtt_contrasenya')
INTERVAL_MINUTS=$(bashio::config 'interval_minuts')
HTTPS=$(bashio::config 'https')

if [[ -z "${API_KEY}" || -z "${CODI_MUNICIPI}" ]]; then
  bashio::log.error "Cal configurar 'api_key' i 'codi_municipi' per continuar."
  exit 1
fi

export METEOCAT_API_KEY="${API_KEY}"
export METEOCAT_CODI_MUNICIPI="${CODI_MUNICIPI}"
export METEOCAT_NOM_MUNICIPI="${NOM_MUNICIPI}"
export METEOCAT_MQTT_HOST="${MQTT_HOST}"
export METEOCAT_MQTT_PORT="${MQTT_PORT}"
export METEOCAT_MQTT_USUARI="${MQTT_USUARI}"
export METEOCAT_MQTT_CONTRASENYA="${MQTT_CONTRASENYA}"
export METEOCAT_INTERVAL_MINUTS="${INTERVAL_MINUTS}"
export METEOCAT_HTTPS="${HTTPS}"

python3 /app/main.py
