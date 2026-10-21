# Continuidad del portátil de escritura — 21 de octubre

## Encargo para el agente del portátil

Raúl trabajará desde casa sin acceso a la tarea local del laboratorio. Lee
AGENTS.md, este retorno y los del 19/10 antes de actuar. El encargo es completar
el entorno técnico de escritura, no editar la novela. GitHub es la memoria del
trabajo técnico; la conversación editorial debe continuar en ChatGPT web.

## Estado confirmado y límites

- En el portátil se reparó Longform, se protegieron los originales y se comprobó
  la subida y recuperación técnica de una nota. No repetir esas reparaciones.
- En oficina se recibió el índice; Raúl comprobó visualmente las siete entradas
  y probó editar una nota y subirla mediante el icono de GitHub Sync. La API de
  GitHub confirmó contenido idéntico entre local y remoto.
- Raúl conectó ChatGPT web desde Zen al repositorio privado de Obsidian solamente.
  Comunicó dos lecturas correctas de la nota, incluida una actualización posterior.
- Las instrucciones editoriales aprobadas están en las notas del proyecto privado,
  junto con el taller y el contexto. El commit de preparación fue 0efd0f5; es una
  referencia histórica, no una orden de volver a él. Consultar la versión actual.
- Al comenzar el 21/10 el proyecto de ChatGPT seguía pendiente. Después Raúl
  confirmó «proyecto listo» y aportó la respuesta de validación dentro del proyecto.
  Véase la comprobación posterior al final de este retorno; no crear otro proyecto.
- No se han instalado ni probado dictado o corrector local en este flujo.
- El navegador integrado del laboratorio se atascó en la verificación de acceso;
  Zen permitió continuar. No invertir la sesión en repetir aquel inicio de sesión.

## Reglas del flujo aprobadas por Raúl

- Raúl escribe siempre: teclado o dictado fiel, sin reformulación creativa.
- La IA es editor: observaciones justificadas, preguntas y referencias. No escribe
  escenas, reescribe párrafos ni modifica el manuscrito.
- La revisión consulta la versión publicada en GitHub. Los cambios solo locales
  requieren sincronización antes de pedir su revisión desde ChatGPT.
- Misma conversación desde oficina y casa, con la oficina apagada. No sustituir
  este requisito por resúmenes, exportaciones o chats locales independientes.
- Distinguir manuscrito vigente, compilaciones, variantes y apuntes. Acceso al
  repositorio no equivale a haber leído todo ni a recordar todos sus detalles.
- La conexión de GitHub es para consulta; no afirmar que una decisión tomada en
  el chat se guardó automáticamente en Obsidian. Para decisiones importantes,
  ofrecer un resumen breve que Raúl guarde y sincronice cuando corresponda.

## Secuencia en casa

1. Inspeccionar el clon de Lavanda y consultar origin/main sin perder trabajo
   local. Esta sesión no necesita actualizar Omarchy ni reaplicar Lavanda.
2. Localizar la bóveda que realmente usa Obsidian. Revisar cambios locales y
   remotos antes de integrar; no usar reset, clean, stash automático ni forzar
   conflictos. Conservar cualquier texto nuevo del autor.
3. Recibir las notas privadas del taller, contexto e instrucciones del editor.
   Comprobar la nota desechable de sincronización y su última revisión. No copiar
   textos ni datos del repositorio privado a este retorno público.
4. Abrir ChatGPT en Zen con la misma cuenta usada en oficina. Encontrar la
   conversación que ya leyó la nota de prueba; no crear otra para simular continuidad.
5. Si el proyecto editorial aún no está preparado, guiar a Raúl para crear uno
   llamado Simetría, pegar el contenido íntegro de la nota privada de instrucciones
   en las instrucciones del proyecto y mover allí la conversación de pruebas.
   No confundir adjuntar un archivo con configurar las instrucciones del proyecto.
   No crear un enlace público de conversación ni de proyecto.
6. Con la oficina apagada, comprobar que el historial anterior aparece. Pedir en
   esa misma conversación una lectura nueva de la nota desde GitHub, con referencia
   verificable. Contrastar con la versión remota actual.
7. Para completar la vuelta: Raúl añade una frase nueva a la nota desechable en
   Obsidian y pulsa el gato. Verificar la subida real. Pedir al mismo chat que
   consulte otra vez el archivo sin proporcionarle la frase esperada. Comprobar
   que encuentra la nueva línea. Esto prueba actualización, no memoria literaria.
8. Comprobar las instrucciones del proyecto: pedir que explique brevemente su
   papel y sus límites, y que consulte el índice para enumerar las escenas con
   referencias. Una respuesta obediente no demuestra por sí sola que se guardaron
   las instrucciones: Raúl debe comprobar también el campo de configuración.
9. Registrar qué comprobó directamente el agente y qué confirmó Raúl. Si un paso
   falla, conservar el estado, explicar el bloqueo y no declarar cerrado el flujo.

## Después de superar la continuidad

Siguiente fase propuesta: dictado local en el portátil y corrección mecánica.
No hay autorización genérica para instalar cualquier herramienta o modelo.

- Revisar versiones y compatibilidad actuales de Voxtype/Whisper para Hyprland.
  El portátil es un ASUS con i5 de décima generación, 20 GB de RAM y SSD de 512 GB
  según el usuario; verificar el hardware antes de elegir modelo.
- Preferir una prueba de Whisper multilingüe en español, sin modelo .en ni
  posprocesado generativo. Medir demora, errores y memoria con audio real del usuario.
  No prometer el rendimiento de otro procesador ni necesitar un servidor para dictar.
- Proponer paquete, tamaño de descarga, atajo sin conflictos y reversión. Explicar
  el plan y obtener la aprobación del alcance concreto antes de instalar. Leer la
  skill Omarchy antes de modificar configuración del escritorio.
- Probar primero en una nota desechable de Obsidian y luego en el compositor de
  ChatGPT. Revisar el texto reconocido antes de enviarlo; no enviar automáticamente.
- LanguageTool Integration ya figuraba habilitado en oficina. Inspeccionar el
  portátil y distinguir complemento, servicio local y servicio remoto; no afirmar
  que las correcciones son locales sin comprobar dónde se procesa el texto.
- No contratar servicios, instalar un modelo generativo grande, desplegar nada en
  el VPS ni cambiar el manuscrito como efecto colateral.

## Retorno obligatorio al terminar

Crear o completar el retorno de fecha real y alias portátil. Publicarlo conforme
a AGENTS.md, sin esperar una petición adicional. Si no se puede subir, decirlo.

```markdown
## Continuidad del editor y preparación de voz

- Bóveda actualizada sin pérdida de trabajo: PASS / pendiente / bloqueo.
- Proyecto ChatGPT creado y reglas pegadas: confirmado por usuario / observado / pendiente.
- Conversación de oficina accesible desde casa: PASS / FAIL / pendiente.
- Oficina apagada durante la prueba: confirmado / no comprobado.
- Consulta actual de GitHub en esa conversación: PASS / FAIL / pendiente.
- Nueva frase desde portátil, subida y leída por ChatGPT: PASS / FAIL / pendiente.
- Instrucciones y acceso al índice comprobados: resultado y límite.
- Dictado: no iniciado / plan presentado / aprobado e instalado / probado.
- Si hubo prueba de voz: modelo, idioma, demora y errores observados, sin grabaciones privadas.
- Corrección mecánica: estado y ubicación local/remota del servicio, sin credenciales.
- Incidencias, reversión y siguiente paso concreto:
```

Los fallos y pendientes forman parte del retorno. No rellenar PASS por inferencia
ni publicar el enlace de la conversación privada, el contenido del libro o secretos.

## Comprobación posterior del proyecto de ChatGPT

- Raúl confirma que el proyecto está listo y aporta la respuesta a la prueba de
  reglas editoriales, índice y contexto. La configuración en Zen se conoce por
  confirmación del usuario; no se inspeccionó directamente esa ventana.
- La respuesta enumera correctamente las siete entradas del índice y cita dos
  SHA de archivo. Ambos coinciden con los archivos locales de referencia,
  comprobados mediante git hash-object. No se publican aquí los contenidos.
- El editor respeta la autoría de Raúl, no genera prosa sustitutiva y distingue
  apuntes, variantes e hipótesis. Aclara expresamente que consultar el índice y
  el contexto no significa haber leído los capítulos. Prueba básica: PASS.
- Matiz observado: no confundir conservar variantes sin cambios con preferirlas
  o comprometerse a escoger una. El autor había rechazado ambas; siguen archivadas.
- Pendiente real en casa: abrir ESE proyecto y ESA conversación, consultar GitHub
  con la oficina apagada y completar la vuelta de una nueva nota de prueba. No
  recrear proyecto ni repetir instalación de instrucciones salvo fallo comprobado.
- Las referencias antiguas a «instrucciones pendientes» dentro de las notas del
  libro describen el estado anterior a esta confirmación; este retorno lo actualiza.
- La calidad editorial exhaustiva, el dictado y el corrector local no quedan
  validados por esta prueba de acceso y obediencia de instrucciones.
