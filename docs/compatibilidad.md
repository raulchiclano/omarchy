# Compatibilidad

## Base de esta edición

Exportada de una personalización en uso el 25 de septiembre de 2026:

| Elemento | Versión observada |
| --- | --- |
| Paquete de la VM | `try-omarchy-runtime 4.0.3-4` |
| Fuente de Omarchy | commit `0534987009061cbe2dacdde4ad564092ab698d12` |
| Hyprland | `0.56.2-3`, configuración Lua |
| Quickshell | `0.3.1-1` |
| Foot | `1.28.0-2` |
| fzf | `0.74.4-1` |
| Starship | `1.26.0-1` |

La integración de historial admite `fzf` 0.74.3 o posterior. La VM tenía
0.74.4, mientras que el canal estable de la instalación nativa ofrece 0.74.3;
ambas variantes usan las opciones comprobadas por las pruebas.

La base de escritorio admite dos juegos de huellas revisados: el runtime de
Try Omarchy de la VM y Omarchy nativo 4.0.4-1. Try Omarchy conserva backports
propios en notificaciones e inactividad aunque el resto de la fuente proceda
del mismo commit. Para esos tres archivos, `compatibility.json` registra las
dos huellas aceptadas. El resto de los archivos debe seguir coincidiendo de
forma exacta.

Los números de versión por sí solos no garantizan que las APIs sean iguales. `compatibility.json` contiene SHA-256 de los archivos de la shell, los valores predeterminados de Hyprland y la integración Bash que usa esta edición. No contiene archivos privados ni copias de sesiones.

`desktop` y `workspaces` requieren que coincida una base de escritorio validada. Una entrada de `compatibility.json` puede contener una huella o una lista de huellas revisadas. `shell` requiere que coincidan `default/bash/rc` e `init`. `terminal` puede instalarse por separado sin esa base, si está Foot y la fuente. `icons` requiere el tema Tokyo Night.

La comprobación es deliberadamente conservadora: también puede bloquear una actualización inocua. No tiene una opción de «forzar». Un mantenedor debe comparar las diferencias y probar los plugins antes de actualizar las huellas. No basta con regenerar `compatibility.json`.

El 26 de septiembre de 2026 se instaló el paquete estándar en un portátil con Omarchy nativo 4.0.4-1. La copia terminó completa con 86 archivos; el shell respondió por IPC, Hyprland no mostró errores de configuración y el dock quedó en ejecución. Quickshell sufrió un único fallo durante la recarga simultánea de plugins y Omarchy lo reinició. Queda pendiente comprobar visualmente cada panel y flujo de interacción. También se probó la instalación/restauración en directorios aislados.

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
