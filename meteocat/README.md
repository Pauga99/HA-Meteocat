# Meteocat - Predicció per municipi

Aquest add-on consulta la predicció del temps de Meteocat per al municipi que triïs i publica sensors a Home Assistant mitjançant MQTT Discovery.

## Funcionalitats

- Configuració guiada amb camps clars en català.
- Sensors amb tipus i icones adequades per a cada magnitud.
- Publicació automàtica via MQTT Discovery (no cal crear entitats manualment).

## Requisits

- Home Assistant Supervisor.
- Broker MQTT (per exemple, l'add-on Mosquitto oficial).
- Clau API de Meteocat.

## Configuració

1. **Clau API**: introdueix la teva clau API de Meteocat.
2. **Codi del municipi**: ID oficial de Meteocat del municipi.
3. **Nom del municipi (opcional)**: es mostrarà a les entitats.
4. **MQTT**: configura host, port i credencials si cal.
5. **Interval**: temps entre actualitzacions (mínim 5 minuts).

Un cop desat, l'add-on crearà automàticament les entitats.

## Sensors creats

- Temperatura màxima
- Temperatura mínima
- Humitat
- Precipitació
- Probabilitat de precipitació
- Velocitat del vent
- Estat del cel
- Última actualització

## Notes

- Si canvies el codi del municipi, es crearan entitats noves amb el nou identificador.
- Pots veure els sensors a **Ajustos → Dispositius i serveis → MQTT**.

