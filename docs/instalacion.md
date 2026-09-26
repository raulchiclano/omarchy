# Instalación, copias y recuperación

## Qué escribe

| Destino | Método |
| --- | --- |
| `~/.config/omarchy/plugins/lavanda.*` | Copia los plugins propios. |
| `~/.config/omarchy/shell.json` | Fusiona barra y selección de plugins; mantiene otras preferencias y servicios. |
| `~/.config/omarchy-lavanda/` | Archivos auxiliares de Hyprland, Bash y Starship. |
| `~/.config/hypr/looknfeel.lua` | Añade un bloque que carga el aspecto, sin borrar otros ajustes. |
| `~/.config/hypr/bindings.lua` | Solo con `--only workspaces`: añade la carga de los dos atajos. |
| `~/.local/share/hyprland-dock/` | Archivos verificados de la revisión fijada del fork y registro de versión. |
| `~/.config/hyprland-dock/dock.json` | Aplica el preset actual y conserva aplicaciones fijadas existentes y opciones desconocidas. |
| `~/.local/bin/hyprland-dock` | Lanzador ejecutable gestionado, con actualizaciones a través de este instalador. |
| `~/.config/autostart/hyprland-dock.desktop` | Arranque automático del dock en Hyprland. |
| `~/.local/share/applications/hyprland-dock.desktop` | Entrada del dock en el menú de aplicaciones. |
| `~/.config/foot/foot.ini` | Edita únicamente fuente, márgenes, cursor, desplazamiento y opacidad. |
| `~/.bashrc` | Sustituye la carga estándar por la integración y añade el historial al final. Conserva alias y funciones personales. |
| `~/.config/omarchy/themes/tokyo-night/icons.theme` | Define Adwaita para ese tema. |

Starship usa su archivo separado mediante `STARSHIP_CONFIG`. El anterior `~/.config/starship.toml` permanece disponible. Las preferencias modificadas aparecen con detalle en `plan --diff`.

Los bloques de Hyprland se añaden al final para que prevalezcan los valores visuales del paquete. No se eliminan ajustes antiguos de aspecto; al restaurar reaparece exactamente el archivo anterior. Si posteriormente añades otros valores después del bloque, esos últimos pueden prevalecer.

El instalador reconoce la integración Bash y los identificadores `raulchiclano.*` de la configuración original para migrarlos sin duplicar los servicios. Los archivos de esos plugins antiguos no se borran. Se desactivan los servicios antiguos al activar sus equivalentes `lavanda.*`.

## Copias

Se guardan bajo `~/.local/state/omarchy-lavanda/backups/ID/`. Cada copia tiene permisos privados y un manifiesto con rutas, permisos y huellas; los archivos originales se guardan con nombres numéricos. Estas copias pueden contener preferencias personales: **no las añadas a Git**.

Antes de escribir se revisan todos los destinos. Si cambian plugins de una sesión activa, se comprueba que esté desbloqueada y se detiene temporalmente la shell de Omarchy para evitar recargas mientras se copian archivos; se arranca de nuevo incluso si falla la operación. Las escrituras usan reemplazo atómico de cada archivo y se activa `shell.json` al final. Si falla una escritura, se revierten las ya completadas. Esto no convierte el conjunto de archivos en una transacción del sistema de archivos: un corte eléctrico puede interrumpirlo. Una copia con estado `prepared` permite revisar/restaurar los archivos que llegaron a aplicarse.

La restauración comprueba que no haya cambios posteriores ni copias dañadas. También crea su propia copia, por lo que puedes deshacer una restauración. Los directorios vacíos que creó la instalación pueden permanecer; no se eliminan recursivamente directorios de usuario.

## Validar tras instalar

1. Comprueba la barra, el calendario, los menús y los paneles de sonido/red/monitor.
2. Abre una terminal nueva y prueba `ls`, Ctrl+R y un repositorio Git.
3. Comprueba `hyprctl configerrors`. El instalador recarga y consulta errores cuando detecta una sesión activa y ha cambiado archivos de Hyprland.
4. Comprueba el dock: aparece en un espacio libre, se oculta al superponer una ventana y reaparece al acercar el puntero al borde inferior.
5. Prueba Ctrl+Super+V (portapapeles), Ctrl+Super+E (emojis) y `omarchy-shell lock preview` (un clic cierra la vista previa).
6. Opcionalmente envía una notificación: `notify-send 'Lavanda' 'Prueba de aspecto y duración'`.

Foot toma los cambios en ventanas nuevas. No hace falta cerrar terminales con trabajo en curso. El instalador recarga la shell al terminar cuando hay una sesión activa. Se niega a cambiar sus paneles si la sesión está bloqueada o no puede comprobar su estado. La misma comprobación protege la restauración. El servicio de autenticación del bloqueo es idéntico al de la base validada; solo cambia su vista.

## Si algo no aparece

- **Sin colores en `ls`:** comprueba que el proceso que abre la terminal no le esté pasando `NO_COLOR=1` o `TERM=dumb`. El paquete no anula globalmente esas variables.
- **Iconos como cuadrados:** revisa las fuentes con `./install.sh doctor`.
- **Notificaciones ocultas:** la comprobación de pantalla las oculta si no puede confirmar que esté desbloqueada y sin salvapantallas. Revisa que los comandos públicos de Omarchy sigan siendo compatibles.
- **La barra no se ve:** puede estar oculta por un atajo; revisa los atajos de tu versión antes de reinstalar.
- **Errores después de aplicar:** usa `./install.sh restore ID`. Si hay modificaciones posteriores, compara el archivo actual con su copia en vez de forzar su eliminación.

## Probar sin tocar tu escritorio

`--home DIRECTORIO` permite preparar una copia de configuración en otro directorio existente. No ejecuta recargas de la sesión cuando ese directorio no es tu HOME real. Debe contener los archivos base de Omarchy correspondientes a los componentes elegidos.

Las pruebas automatizadas crean sus propios directorios temporales. Nunca uses `sudo` para instalar o probar.

El dock se detiene antes de cambiar sus archivos y se vuelve a abrir después si hay una sesión Hyprland activa en el HOME real. Con `--home` no se toca la sesión. Si restauras la copia de una primera instalación, se retiran sus archivos y su arranque automático; si había un dock anterior, vuelve su configuración. La barra superior es un proceso independiente.
