# Compatibilidad

## Base de esta edición

Exportada de una personalización en uso el 24 de septiembre de 2026:

| Elemento | Versión observada |
| --- | --- |
| Paquete de la VM | `try-omarchy-runtime 4.0.3-4` |
| Fuente de Omarchy | commit `0534987009061cbe2dacdde4ad564092ab698d12` |
| Hyprland | `0.56.2-3`, configuración Lua |
| Quickshell | `0.3.1-1` |
| Foot | `1.28.0-2` |
| fzf | `0.74.4-1` |
| Starship | `1.26.0-1` |

Los números de versión por sí solos no garantizan que las APIs sean iguales. `compatibility.json` contiene SHA-256 de los archivos de la shell, los valores predeterminados de Hyprland y la integración Bash que usa esta edición. No contiene archivos privados ni copias de sesiones.

`desktop` y `workspaces` requieren que coincida la base de escritorio. `shell` requiere que coincidan `default/bash/rc` e `init`. `terminal` puede instalarse por separado sin esa base, si está Foot y la fuente. `icons` requiere el tema Tokyo Night.

La comprobación es deliberadamente conservadora: también puede bloquear una actualización inocua. No tiene una opción de «forzar». Un mantenedor debe comparar las diferencias y probar los plugins antes de actualizar las huellas. No basta con regenerar `compatibility.json`.

No se ha validado aún una instalación gráfica completa en una segunda máquina. Se han reutilizado los paneles que funcionaban en la máquina de origen y probado la instalación/restauración en directorios aislados. La comprobación de archivos no sustituye a una prueba visual en el equipo destino.

## Formatos y rutas

- Instalación estándar en `/usr/share/omarchy`; no compatible con `omarchy dev link`.
- Configuración de usuario en `~/.config` y estado en `~/.local/state`. Un XDG personalizado se rechaza para no escribir archivos que la sesión no usaría.
- Hyprland debe cargar `hypr.looknfeel` y, para los atajos opcionales, `hypr.bindings` desde `hyprland.lua`.
- Bash debe conservar la línea estándar `source "$OMARCHY_PATH/default/bash/rc"`. Se conserva el resto del archivo y se añaden bloques identificados.
- Los destinos enlazados simbólicamente se rechazan. Si usas otro gestor de dotfiles, integra el payload en él conscientemente en lugar de superponer ambos instaladores.
- Los plugins `lavanda.*` tienen nombres fijos y funcionan con cualquier nombre de usuario. No dependen del usuario de la máquina original.

## Después de actualizar Omarchy

Ejecuta `./install.sh doctor`. Si la base difiere, los paneles que ya estaban instalados no se desinstalan automáticamente: el diagnóstico impide volver a desplegarlos sin revisión. Conserva las copias locales.

La integración ble.sh comprueba también los dos archivos de arranque al abrir cada terminal. Si cambian, carga Bash estándar y avisa, evitando inicializar fzf dos veces. El prompt y el historial mantienen su configuración mientras sean compatibles con las herramientas instaladas.

Un cambio de tema conserva los plugins de usuario. Los paneles personalizados mantienen su paleta lavanda; las demás aplicaciones toman los colores del tema elegido. La capa de iconos Adwaita afecta solo a Tokyo Night.

## Si una comprobación se detiene

1. Lee el nombre del componente y los archivos que difieren.
2. No sustituyas los archivos de Omarchy por los de otra máquina.
3. Puedes instalar componentes independientes, por ejemplo `./install.sh apply --only terminal`.
4. Para adaptar el escritorio, compara la nueva API con los imports y servicios de `payload/plugins`, prueba en una sesión de laboratorio y registra la nueva base validada.
