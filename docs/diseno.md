# Diseño y mantenimiento

La intención es una interfaz tranquila inspirada en elementaryOS: letras claras, espacio entre elementos y un color de énfasis reconocible.

| Uso | Valor |
| --- | --- |
| Énfasis lavanda | `#B4A1F5` |
| Texto claro | `#F2EFFA` |
| Fondo de paneles | `#211E2C`, normalmente con aproximadamente 94 % de opacidad |
| Selección | `#393249` |
| Elementos secundarios | `#A69BB8` |
| Borde de ventana inactiva | `#393449` |
| Radio de ventanas | 8 |
| Radio habitual de paneles | 14 |
| Tipografía de interfaz | Adwaita Sans, con peso reforzado |
| Tipografía de terminal | JetBrainsMono Nerd Font |

Los paneles no son solo imágenes: conservan los controles nativos de Omarchy. Las traducciones de etiquetas no sustituyen los identificadores de acciones o proveedores de DNS.

La barra reorganiza los widgets nativos: reloj centrado, menú y escritorios a la izquierda, estado y controles a la derecha. El widget del tiempo se omite para dejar espacio. Los widgets de terceros permanecen en su sección.

## Mantener el repositorio

1. Trabaja sobre los archivos correspondientes de `payload/`.
2. Revisa `./install.sh plan --diff` antes de aplicar en una máquina de prueba.
3. Ejecuta las pruebas y comprueba visualmente los paneles afectados.
4. Registra cambios pequeños con Git, incluyendo el motivo y la versión donde se probaron.
5. En otros equipos, actualiza con `git pull --ff-only`, revisa el plan y aplica.

No sincronices automáticamente todo `~/.config`. El repositorio contiene solo archivos seleccionados. Una mejora hecha directamente en un equipo **no se exporta sola**: revísala y trasládala al payload antes de publicarla.

Los auxiliares `ElegantPopup.qml` son copias adaptadas de componentes de Omarchy. Se conservan junto a cada plugin para mantenerlos independientes y fáciles de revisar. Cuando cambie la API de Omarchy, revisa también el menú (`AppLibrary`), las comprobaciones de bloqueo de las notificaciones y la carga de los servicios.
