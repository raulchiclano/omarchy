# Retorno del laboratorio — 22 de octubre de 2026

## Acceso de la VM de oficina

- Desactivado el inicio automático de SDDM solo en la VM. Confirmación del usuario tras arranque: PASS.
- Tema local Lavanda con textos españoles y configuración de teclado español. Confirmación final del usuario tras reiniciar y acceder: PASS.
- Incidencia: se probó inicialmente con greeter Qt 6 mientras SDDM arrancaba Qt 5. Pantalla negra por biblioteca Qt 5 ausente; recuperación asistida en otro chat instalando qt5-declarative. Después se instaló qt5-quickcontrols2 con la herramienta de paquetes de Omarchy y se seleccionó el estilo Default compatible con Qt 5. Vista previa con el ejecutable real y acceso tras arranque comprobados por separado.
- SDDM carga todos los archivos de su directorio de configuración, también los terminados en .bak. Las copias deben guardarse FUERA de ese directorio. Se corrigieron ambos casos encontrados.
- No trasladar esta personalización de acceso al portátil automáticamente. No se publicó una versión ni un instalador del tema.
- Disco de la VM casi lleno; pendiente revisión del espacio sin borrar datos personales.

## Salvapantallas durante vídeos en el portátil

- El usuario informa de que aparece el salvapantallas OMARCHY durante YouTube. No se reprodujo ni inspeccionó directamente en el portátil.
- El código instalado en oficina dispone de `omarchy toggle screensaver`, que alterna solo el salvapantallas, y `omarchy toggle idle stay-awake`, que desactiva temporalmente la gestión de inactividad hasta ejecutar `omarchy toggle idle allow-idle`. Este último también impide el bloqueo automático y no debe dejarse como solución permanente inadvertidamente.
- Pendiente en portátil: comprobar versión y estado, navegador y reproducción, y si se respeta la inhibición de inactividad. Proponer quitar solo el salvapantallas decorativo conservando bloqueo; no modificar bloqueo ni suspensión sin acordar el alcance.
- No se modificó el comportamiento de inactividad de ninguno de los equipos en esta revisión.
