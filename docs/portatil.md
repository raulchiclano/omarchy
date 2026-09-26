# Llevar Lavanda al portátil

Esta guía reproduce la personalización aprobada el 25 de septiembre de 2026.
El instalador lleva el aspecto y comportamiento de escritorio; las aplicaciones,
cuentas y ajustes de hardware siguen siendo propios de cada equipo.

## 1. Comprobar antes de instalar

En el portátil, como tu usuario habitual:

```bash
git clone https://github.com/raulchiclano/omarchy.git
cd omarchy
./install.sh doctor
```

Si ya tienes el repositorio, entra en él y ejecuta `git pull --ff-only`.
Si aparece «Base no validada», detente: comparte el resultado para adaptar el
paquete a esa versión. No copies los archivos de sistema de la VM ni actualices
la lista de huellas para eludir el diagnóstico. Esta edición necesita Omarchy
con Quickshell y Hyprland Lua; un escritorio con Waybar/Hyprlock requiere otra adaptación.

Para copiar el diagnóstico sin perder los errores:

```bash
./install.sh doctor 2>&1 | wl-copy
```

Si faltan herramientas o fuentes, el diagnóstico las identifica. Los paquetes
principales se detallan en el README. Para reproducir también las sugerencias de
Bash, instala la dependencia opcional con `./install.sh install-blesh`.

## 2. Revisar e instalar

La instalación normal incluye escritorio, terminal, Bash, iconos y dock:

```bash
./install.sh plan --diff
./install.sh apply
```

Para incluir también los atajos de escritorios usados en el equipo de origen
(Ctrl+Super+←/→), revisa y aplica esta selección en lugar de la anterior:

```bash
./install.sh plan --only desktop,terminal,shell,icons,dock,workspaces --diff
./install.sh apply --only desktop,terminal,shell,icons,dock,workspaces
```

Se crea una copia reversible. Hazlo con la sesión desbloqueada: el instalador
comprueba el bloqueo antes de tocar los paneles y recarga la shell al finalizar.
Las contraseñas y la autenticación no se trasladan: se usan las del portátil.
El bloqueo obtiene el nombre completo de la cuenta local o su nombre de usuario.

## 3. Completar el mismo aspecto

Selecciona el tema y la terminal de origen después de aplicar:

```bash
omarchy theme set tokyo-night
omarchy default terminal foot
```

El fondo no se distribuye en este repositorio público. Lleva tu copia de
`12-Dark.jpg` al portátil. Si usas el archivo personal `lavanda-fondo-personal.zip`,
descomprímelo y, desde su carpeta, ejecuta:

```bash
mkdir -p ~/.config/omarchy/backgrounds/tokyo-night
cp -i 12-Dark.jpg ~/.config/omarchy/backgrounds/tokyo-night/12-Dark.jpg
omarchy theme bg set ~/.config/omarchy/backgrounds/tokyo-night/12-Dark.jpg
```

La selección del tema o del fondo se realiza mediante comandos de Omarchy y no
forma parte de la copia del instalador. Conserva el fondo anterior si quieres
volver a él.

Abre una terminal nueva para ver el prompt, la fuente y el historial.
En una instalación nueva el dock fija, en este orden: Archivos, Foot, Zen,
VS Code, WhatsApp, ChatGPT y Spotify. Instala las aplicaciones que falten y crea
los lanzadores web con Omarchy. Sus cuentas y perfiles no se importan. Para repetir los ajustes del navegador, sigue [Zen: configuración manual](zen.md). Si ya
había un dock con favoritos, el instalador conserva su lista: puedes reordenarla
con el ratón.

## 4. Comprobación rápida

- Barra y paneles: tipografía Adwaita Sans, lavanda y calendario en español.
- Botón de nueve puntos del dock: abre el buscador de aplicaciones; el botón no
  se amplía y las aplicaciones pasan suavemente de 32 a unos 37 px.
- Ctrl+Super+V: portapapeles con historial separado de la vista previa.
- Ctrl+Super+E: busca «feliz», «corazon» o «fiesta»; también acepta inglés.
- `omarchy-shell lock preview`: vista previa del bloqueo. Un clic la cierra.
  Después prueba bloquear y desbloquear con la contraseña del portátil.
- Terminal: `ls` con colores, Ctrl+R y prompt con estado Git.
- Dock: visible en espacio libre; se oculta cuando una ventana lo cubre.
- `hyprctl configerrors`: sin errores de configuración.

La escala, resolución, monitores, teclado, audio, red, batería, suspensión y
sesiones siguen configurados para el portátil. Los tamaños físicos pueden
variar con la pantalla y su escala aunque los valores de Lavanda sean iguales.
La instalación estándar se probó en el portátil con Omarchy nativo 4.0.4-1 el
26 de septiembre de 2026. El shell y el dock quedaron funcionando; comprueba
visualmente cada panel y flujo de interacción después de aplicar actualizaciones.

## 5. Actualizar o volver atrás

```bash
git pull --ff-only
./install.sh doctor
./install.sh plan --diff
./install.sh apply
```

Para volver a la configuración anterior:

```bash
./install.sh backups
./install.sh restore ID_DE_LA_COPIA
```

No copies toda `~/.config` de la VM: no es necesario para reproducir Lavanda.
