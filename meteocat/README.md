# Meteocat - Predicció per municipi

**Avís important:** aquest add-on **encara no és funcional** i es troba **en proves**. La informació següent serveix per preparar la configuració quan estigui disponible.

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

## Instal·lació (pas a pas)

1. Afegeix el repositori a Home Assistant amb el botó del README del repositori.
2. Entra a **Supervisor → Add-ons** i selecciona **Meteocat - Predicció per municipi**.
3. Prem **Instal·la** i espera que finalitzi.

## Configuració detallada (pas a pas)

1. Obre la pestanya **Configuració** de l'add-on.
2. Introdueix la **Clau API de Meteocat**.
3. Introdueix el **Codi del municipi** (ID Meteocat).
4. Si vols, afegeix el **Nom del municipi** per veure'l a les entitats.
5. Configura el **Servidor MQTT** i el **Port MQTT**.
6. Si el teu broker requereix credencials, omple **Usuari** i **Contrasenya**.
7. Defineix l'**Interval d'actualització** (mínim 5 minuts).
8. Desa els canvis i inicia l'add-on.

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


## Resolució d'errors habituals

Si Home Assistant mostra `fatal: could not read Username for 'https://github.com'`, la URL del repositori és privada o incorrecta.

- Publica el repositori al teu compte de GitHub.
- Fes-lo públic.
- Utilitza l'URL pública final del teu fork en afegir el repositori (exemple: `https://github.com/nom_usuari/HA-Meteocat`).
