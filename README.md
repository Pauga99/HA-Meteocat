# Meteocat per a Home Assistant

**Avís important:** aquest projecte **encara no és funcional** i es troba **en proves**. Les instruccions següents serveixen per preparar la instal·lació quan estigui disponible.

Add-on per integrar la predicció del temps de Meteocat (Servei Meteorològic de Catalunya) a Home Assistant mitjançant sensors MQTT.

[![Obre Home Assistant i afegeix el repositori d'add-ons](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/Pauga99/HA-Meteocat)

## Add-ons disponibles

- **Meteocat - Predicció per municipi**: consulta la predicció del temps per al municipi que triïs i publica entitats a Home Assistant.

## Instal·lació (pas a pas)

1. Obre Home Assistant i prem el botó **“Afegeix el repositori d'add-ons”** de dalt.
2. A **Supervisor → Add-ons**, comprova que el repositori **Meteocat** apareix a la llista.
3. Entra a l'add-on **“Meteocat - Predicció per municipi”** i prem **Instal·la**.
4. Espera que finalitzi la instal·lació.

## Configuració (pas a pas)

1. Obre la pestanya **Configuració** de l'add-on.
2. Introdueix la **Clau API de Meteocat**.
3. Introdueix el **Codi del municipi** (ID Meteocat).
4. Si vols, afegeix el **Nom del municipi** per veure'l a les entitats.
5. Configura el **Servidor MQTT** i el **Port MQTT**.
6. Si el teu broker requereix credencials, omple **Usuari** i **Contrasenya**.
7. Defineix l'**Interval d'actualització** (mínim 5 minuts).
8. Desa els canvis i inicia l'add-on.

## Notes

- Les entitats es creen automàticament via MQTT Discovery.
- Pots veure-les a **Ajustos → Dispositius i serveis → MQTT**.

## Resolució d'errors habituals

Si en afegir el repositori veus aquest error:

`fatal: could not read Username for 'https://github.com'`

vol dir que la URL configurada apunta a un repositori privat o incorrecte.

Per solucionar-ho:

1. Fes **fork** d'aquest projecte al teu compte de GitHub.
2. Verifica que el repositori del fork és **públic**.
3. Substitueix `Pauga99` del botó per el teu usuari real de GitHub.
4. Torna a afegir el repositori des de Home Assistant amb la URL pública final, per exemple:
   `https://github.com/nom_usuari/HA-Meteocat`


Si en instal·lar l'add-on veus errors com:

`pull access denied for local/meteocat-amd64` o `Failed to fetch manifest for docker.io/local/...`

vol dir que tenies una versió antiga de l'add-on que intentava usar la imatge `local/meteocat-*`. Amb aquesta versió ja s'utilitza `ghcr.io/pauga99/meteocat-{arch}`.

Passos recomanats després d'actualitzar el repositori:

1. A Home Assistant, elimina l'add-on instal·lat (si existeix).
2. A **Ajustos → Add-ons → Repositoris**, elimina i torna a afegir aquest repositori.
3. Recarrega la botiga d'add-ons.
4. Torna a instal·lar **Meteocat - Predicció per municipi**.
