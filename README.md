# Omarchy Lavanda

Mi personalización de Omarchy, inspirada en elementaryOS y macOS: lavanda, bordes suaves, menús en español y una terminal cómoda de leer.

Incluye la configuración que uso y un instalador que **enseña los cambios, guarda una copia y permite deshacerlos**. No requiere `sudo` ni modifica archivos de `/usr/share/omarchy`.

> Esta edición parte de **Try Omarchy, runtime 4.0.3-4**, con Hyprland **Lua** y la shell **Quickshell**. Los paneles usan APIs de esa edición: el instalador compara la base instalada antes de activarlos. No es un tema universal para todas las versiones de Omarchy. [Compatibilidad](docs/compatibilidad.md).

**Para el portátil:** [guía paso a paso](docs/portatil.md), con los últimos paneles, atajos y el fondo personal por separado.

## Instalar en otro Omarchy

Desde una terminal de tu usuario habitual:

```bash
git clone https://github.com/raulchiclano/omarchy.git
cd omarchy
./install.sh doctor
./install.sh plan
./install.sh apply
```

`apply` muestra los archivos que va a cambiar y pide confirmación. Para ver el contenido exacto antes de decidir:

```bash
./install.sh plan --diff
```

Instala con la sesión desbloqueada. El instalador recarga la shell al finalizar. Abre una **terminal nueva** para ver Foot y Bash. Para completar la combinación original de colores e iconos, elige Tokyo Night:

```bash
omarchy theme set tokyo-night
```

Esto último es opcional y aplica también los demás ajustes del tema Tokyo Night. El instalador no cambia tu tema activo ni tu fondo por su cuenta.

## Qué incluye

| Componente | Personalización |
| --- | --- |
| `desktop` | Barra superior transparente, botón de aplicaciones de nueve puntos, escritorios con indicador lavanda y reloj/calendario en español. |
| `desktop` | Menú, sonido, red, monitor, uso de agentes, indicador de volumen y notificaciones con tipografía Adwaita Sans, esquinas suaves y contraste claro. |
| `desktop` | Buscador de aplicaciones espacioso; portapapeles con lista y vista previa separadas y texto desplazable. |
| `desktop` | Emojis con nombres y búsqueda en español e inglés, con o sin tildes; reloj, fecha y usuario dinámico en el bloqueo. |
| `desktop` | Ventanas con radio 8, borde de foco lavanda, sombras y animaciones cortas. |
| `desktop` | Notificaciones separadas del borde, con duración de 5 segundos, pausada al pasar el ratón. También las críticas usan este plazo. |
| `terminal` | Foot: JetBrainsMono Nerd Font 10, margen 14, cursor fino y fondo al 94 % de opacidad. Conserva la paleta del tema. |
| `shell` | Prompt Starship con iconos, carpeta y estado Git; ble.sh si está instalado; historial Ctrl+R con separación, resaltado y números atenuados. |
| `dock` | Dock inferior lavanda, iconos de 32 px, ampliación sutil hasta unos 37 px, ocultación inteligente e inicio automático; usa una revisión probada de [mi fork](https://github.com/raulchiclano/hyprland-dock). |
| `icons` | Adwaita al elegir Tokyo Night, mediante una capa de configuración del tema. |
| `workspaces` | **Opcional:** Ctrl+Super+←/→ para cambiar al escritorio contiguo. Reemplaza los atajos de grupo de esas teclas. |

El selector de archivos `ff` y los alias originales de Omarchy se conservan. El panel de agentes usa los datos que ya existan en cada equipo; no transporta cuentas ni inicia sesión.

### Instalar solo una parte

```bash
./install.sh plan --only terminal,shell
./install.sh apply --only terminal,shell
```

La instalación normal incluye `desktop,terminal,shell,icons,dock`. El dock ya queda configurado como en mi escritorio; no necesita `--only dock` para instalarse. Los atajos de escritorios se activan aparte:

```bash
./install.sh apply --only workspaces
```

### Instalar o actualizar solo el dock

```bash
./install.sh doctor --only dock
./install.sh plan --only dock --diff
./install.sh apply --only dock
```

En una instalación nueva fija Archivos (Nautilus), Foot, Zen, VS Code, WhatsApp, ChatGPT y Spotify. El botón de aplicaciones aparece antes de los favoritos y mantiene su tamaño al pasar el ratón. Estas aplicaciones deben estar instaladas en cada equipo; sus perfiles y cuentas no se copian. Si ya tienes una lista de aplicaciones en el dock, la conserva. Aplica el aspecto y comportamiento de Lavanda y mantiene las opciones desconocidas.

El código procede de una revisión exacta del fork, registrada en `dock.lock.json`, y se comprueba con SHA-256 por archivo. `doctor`, `plan` y `apply` necesitan Internet cuando incluyen el dock; la descarga se mantiene en memoria y no se ejecuta el instalador remoto. `restore` funciona sin Internet. [Funcionamiento y mantenimiento del dock](docs/dock.md).

## Dependencias

El diagnóstico comprueba las herramientas y fuentes principales. En esta instalación se usan `foot`, `starship`, `fzf` 0.74.4 o posterior, `jq`, `adwaita-fonts`, `noto-fonts-emoji` y `ttf-jetbrains-mono-nerd`. El dock necesita Hyprland y Quickshell 0.3.0 o posterior (`qs`). El instalador está escrito con la biblioteca estándar de Python 3: no instala paquetes del sistema; sí descarga los archivos del dock fijado cuando se selecciona ese componente.

Si faltan estos paquetes en un Omarchy compatible:

```bash
omarchy pkg add foot starship fzf jq adwaita-fonts noto-fonts-emoji ttf-jetbrains-mono-nerd
```

Las sugerencias y edición de línea de ble.sh son opcionales:

```bash
omarchy pkg aur add blesh-git
```

Sin ble.sh se conserva Bash estándar con el prompt y el historial personalizados. Se probó con `blesh-git 0.4.0_devel4.r2350.d81fd54f-1`. No se empaqueta ble.sh ni se cambia de shell.

## Actualizar o deshacer

Para recoger cambios futuros del repositorio:

```bash
git pull --ff-only
./install.sh plan --diff
./install.sh apply
```

Repetir la instalación sin cambios no duplica bloques ni genera otra copia.

Para deshacer una instalación, usa el identificador que mostró el instalador:

```bash
./install.sh backups
./install.sh restore ID_DE_LA_COPIA
```

La restauración muestra su plan y también guarda una copia de lo que va a deshacer. Si has editado alguno de esos archivos después, **se detiene antes de escribir** para que puedas conservar tus cambios. Deshaz varias instalaciones en orden inverso, empezando por la última. [Detalles y recuperación](docs/instalacion.md).

## Qué se conserva en cada equipo

- Monitores, resolución, escala, teclado, red, Bluetooth, cuentas, claves SSH, historial y documentos.
- Autenticación, suspensión y tiempos de inactividad existentes; cambia la presentación del bloqueo.
- Configuraciones de aplicaciones ajenas al paquete y extensiones personales del menú.
- Widgets de terceros y servicios ajenos a Lavanda; la distribución de los widgets nativos sí se reorganiza como en mi escritorio.
- El fondo actual. El fondo de macOS **no se redistribuye**; puedes añadir un fondo propio localmente a `~/.config/omarchy/backgrounds/tokyo-night/` y seleccionarlo desde Omarchy.

Los ajustes de Zen se reproducen con la [guía manual](docs/zen.md). El instalador no incluye perfiles del navegador, configuración de OpenCode ni paquetes completos de iconos Yaru. Son ajustes o dependencias independientes. Tampoco intenta arreglar la captura de teclado de Try Omarchy en Windows.

## Archivos y pruebas

- `payload/`: configuración portable y trece plugins con identificadores `lavanda.*`.
- `installer.py`: revisión, instalación, copias y restauración.
- `dock.lock.json`: revisión del fork y huellas de sus archivos; `payload/dock/`: preferencias y lanzador gestionado.
- `compatibility.json`: huellas de la base con la que se han validado los paneles.
- `docs/`: compatibilidad, diseño y mantenimiento.
- `tests/`: pruebas de preservación, restauración, repetición y tratamiento de errores.

```bash
python3 -m unittest discover -s tests -v
node tests/emoji-search.cjs
```

Las pruebas de archivos usan directorios temporales; no cambian el escritorio de quien las ejecuta. La prueba de selección del historial se omite si no hay fzf instalado.

## Licencia

MIT. Los paneles derivados de Omarchy conservan su licencia y atribución en [LICENSES/Omarchy-MIT.txt](LICENSES/Omarchy-MIT.txt). Los datos españoles de emojis conservan la licencia Unicode en [LICENSES/Unicode-3.0.txt](LICENSES/Unicode-3.0.txt). Consulta [THIRD_PARTY.md](THIRD_PARTY.md). Proyecto personal, sin afiliación con Omarchy, elementaryOS o Apple.
