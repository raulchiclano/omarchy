# Dock de Lavanda

`./install.sh apply` incluye el dock por defecto. `--only dock` limita la operación al dock. Si no lo quieres en un equipo, selecciona `--only desktop,terminal,shell,icons`.

## Configuración inicial

- Abajo y centrado, fondo lavanda con opacidad 88 %, margen de 10 px y esquinas con radio de 14 px, a juego con los paneles.
- Iconos de 32 px, ampliación 1.375 (hasta 44 px) y radio de ampliación de 95 px.
- Visible cuando ninguna ventana se superpone; se oculta al taparlo. Acercar el puntero al borde inferior lo revela.
- No reserva espacio permanentemente para el dock.
- Menús y selector en español, Adwaita Sans, selección lavanda y paneles de radio 14 px.
- Clic: enfoca la aplicación si está abierta o la inicia.
- Nautilus, Zen, Foot, VS Code y WhatsApp como favoritos iniciales. No instala esas aplicaciones ni transporta cuentas. Conserva la lista existente, incluso si está vacía.
- Inicio automático mediante una entrada XDG de Hyprland. Mantiene el dock como proceso separado de la shell principal.

El aspecto y comportamiento están probados en el entorno descrito en `compatibility.json`. Una versión de Quickshell compatible no garantiza por sí sola todas las combinaciones de controlador, escala y monitores: verifica el resultado visual en cada equipo.

## Relación entre repositorios

El código del dock se desarrolla en `raulchiclano/hyprland-dock`. `dock.lock.json` fija una revisión completa y las huellas SHA-256 de los archivos necesarios para ejecutarlo. El preset y el lanzador de la instalación conjunta están en `payload/dock/`.

El instalador descarga el archivo de esa revisión desde GitHub, valida cada archivo elegido y prepara el plan completo en memoria. No ejecuta código de instalación remoto, no extrae rutas del archivo comprimido al disco y no descarga la rama `master` flotante. Si la descarga o validación falla, no aplica cambios. La revisión previa requiere conexión, pero no escribe preferencias ni una caché local. Las pruebas unitarias simulan la descarga; se ha probado además la descarga real y el ciclo instalar/restaurar en un HOME temporal.

El lanzador gestionado permite iniciar, detener y reiniciar. `hyprland-dock update` y `uninstall` muestran cómo usar el instalador de Lavanda para conservar el control de versiones y las copias; no actualizan o borran por su cuenta. No se debe ejecutar manualmente un instalador antiguo que pueda quedar en una instalación previa. Esos archivos anteriores no se borran indiscriminadamente.

No actives a la vez el dock como plugin de la shell: esta instalación utiliza exclusivamente su modo independiente. Si tu sesión no procesa entradas XDG de inicio automático, revisa la configuración de inicio de tu sesión antes de añadir otro arranque que pudiera duplicarlo.

## Actualizar

Desde el repositorio `omarchy`:

```bash
git pull --ff-only
./install.sh plan --only dock --diff
./install.sh apply --only dock
```

Las actualizaciones vuelven a aplicar el estilo Lavanda; la lista de favoritos se conserva. La lista completa de archivos, el inicio automático y cualquier cambio del lanzador aparecen en el plan. Los originales y sus permisos quedan en la copia de seguridad.

Para publicar una nueva versión del dock en este instalador:

1. Desarrolla y prueba los cambios en el fork del dock; publícalos.
2. Actualiza `revision` en `dock.lock.json` con el identificador completo del commit probado y actualiza las huellas SHA-256 de todos sus archivos seleccionados. Si cambian los archivos necesarios, revisa también esa lista.
3. Ajusta `payload/dock/dock.json` si cambia el preset.
4. Ejecuta las pruebas de `omarchy`, prueba la descarga real, revisa el plan y valida el dock en una sesión real.
5. Publica ambos cambios juntos en `omarchy`. Los demás equipos adoptarán la revisión al aplicar esta actualización.

## Recuperar

```bash
./install.sh backups
./install.sh restore ID_DE_LA_COPIA
```

La restauración funciona sin descargar nada. Se detiene si has modificado después un archivo afectado, incluida una nueva lista de favoritos: así no borra cambios más recientes. También guarda una copia de lo que va a restaurar.
