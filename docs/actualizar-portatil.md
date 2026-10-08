# Actualizar Lavanda en el portátil

## Para Raúl

Abre el chat/agente que tenga acceso local al portátil y pega:

> Actualiza Lavanda siguiendo el protocolo del repositorio https://github.com/raulchiclano/omarchy. Detecta mi versión instalada y revisa los cambios pendientes. Explícame el plan antes de aplicarlo y deja un informe al terminar. Revisa también las novedades de Lavanda 0.3.0: atajos, Nano/VS Code y Transmission Qt; ofréceme las utilidades auxiliares por separado. No copies ajustes de hardware ni credenciales del equipo de oficina.

No necesitas este chat. La memoria del procedimiento está en AGENTS.md y
los documentos del repositorio. No se sincronizan conversaciones automáticamente.
El agente debe descargar la última publicación estable, leer las notas acumuladas
y comparar con el estado instalado. Tú apruebas el plan concreto. Después pruebas
las funciones y el agente completa el informe local.

## Para el agente del portátil

1. Localizar el clon existente (anteriormente se usó ~/Downloads/omarchy).
   Leer AGENTS.md, docs/actualizaciones.md y los informes locales de instalación.
2. Consultar git status y remoto. Fetch de origin y etiquetas. No reset/stash/clean.
   Elegir la última release estable. Si hay cambios locales, preparar otra copia.
   Descargar Git NO instala Lavanda.
3. Ejecutar status --json. No asumir que HEAD es la versión instalada.
4. Revisar release 0.3.0 y proponer componentes según los ya instalados.
   Referencia para escritorio completo con las mejoras:

```bash
./install.sh packages --only desktop,terminal,shell,icons,dock,shortcuts,editors,transmission
```

   Ofrecer utilities (Clocks, age, gvfs-dnssd) aparte. Mantener workspaces si procede.
   Comprobar `code`; conservar la variante de VS Code ya instalada.
5. Presentar dependencias y cambios; pedir la aprobación del plan si no existe.
   Si faltan paquetes de los componentes nuevos, Raúl puede ejecutar en terminal:

```bash
./install.sh install-packages --only editors,transmission
# Solo si también se aprobaron las utilidades:
./install.sh install-packages --only utilities
```

   Nano se instala explícitamente; no viene necesariamente en Omarchy.
   Dependencias originales de escritorio/shell: ver README. No hacer una
   actualización completa del sistema para sortear errores de paquetes o hashes.
6. Doctor y plan --diff con el MISMO alcance que apply. Ejemplo:

```bash
./install.sh doctor --only desktop,terminal,shell,icons,dock,shortcuts,editors,transmission
./install.sh plan --diff --only desktop,terminal,shell,icons,dock,shortcuts,editors,transmission
./install.sh apply --only desktop,terminal,shell,icons,dock,shortcuts,editors,transmission
```

   Cerrar Transmission antes. No usar --yes sin aprobación del plan. Si doctor
   se bloquea, investigar la versión nativa y sus diferencias, nunca forzar hashes.
7. Conservar ID de copia, comprobar Hyprland, abrir terminal nueva y probar los
   tres atajos, Nano/Git, asociaciones de archivos y Transmission/bandeja.
   Repetir plan; distinguir cambios legítimos de apps de fallos de instalación.
8. Ejecutar report y COMPLETAR el Markdown con resultados y pendientes. Preparar
   un resumen sin secretos para el siguiente chat; publicarlo solo con permiso.

La instalación de paquetes es separada de la restauración de configuración.
No desinstalar Transmission GTK ni otros editores como efecto colateral.
