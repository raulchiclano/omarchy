# Portátil de escritura: primera sesión y retorno

**Continuación actual:** leer primero el [traspaso del 21/10](retornos/2026-10-21-laboratorio.md).
La reparación inicial ya se realizó. Ahora toca comprobar la continuidad real
de ChatGPT y GitHub desde casa; esta guía conserva el procedimiento de la primera sesión.

Traspaso del laboratorio, 2026-10-19. Estado: preparado, pendiente de ejecutar
en el portátil. Esta guía no es una versión nueva del instalador de Lavanda.

## Encargo y alcance autorizado

Raúl quiere continuar su proyecto literario desde distintos equipos, conservando
Obsidian, Longform y el repositorio privado existente. Ha pedido dejar aquí lo
necesario para aplicarlo en el portátil, probarlo y publicar un retorno.

Explica brevemente el plan y continúa con las inspecciones, copias y reparaciones
inequívocas descritas aquí: no hace falta otra aprobación para ese mismo alcance.
Consulta a Raúl si hay que elegir entre textos distintos o cambiar el sistema de
sincronización sin poder demostrar cuál debe mantenerse. No deduzcas decisiones
literarias del orden de los archivos ni de su fecha.

No instalar aplicaciones nuevas, actualizar el sistema, migrar el libro a otra
herramienta, crear otro repositorio ni contratar servicios en esta sesión.
No editar el manuscrito para mejorar su estilo. El dictado y la configuración del
asistente literario quedan para después de validar la continuidad del libro.

## Qué se queda

- Omarchy Lavanda como escritorio; conservar los ajustes propios del portátil.
- Obsidian como lugar principal del libro y las notas; Longform para las escenas.
- El repositorio privado actual para el historial. No copiar el manuscrito aquí.
- Un futuro proyecto de ChatGPT para conversaciones literarias entre equipos.
  No está creado ni probado por este traspaso, y no sincroniza Obsidian por sí solo.

## Lo observado en el laboratorio, que debes comprobar de nuevo

- La copia de Obsidian consultada tenía su último commit el 2026-10-01.
  No significa que el portátil esté en ese estado ni que no haya avances remotos.
- Longform, GitHub Sync, Remotely Save y LanguageTool Integration figuraban
  habilitados. Habilitado no demuestra sincronización activa ni configuración válida.
- El índice del proyecto literario contenía marcas de conflicto ya guardadas en
  Git y omitía una escena existente. Un estado Git limpio no detecta ese defecto.
- La lectura encontró duplicaciones y variantes dentro de borradores. Son
  material privado: conservarlo y consultar antes de descartar cualquier versión.

## Procedimiento en el portátil

1. **Recuperar contexto.** Lee AGENTS.md, los últimos retornos y esta guía desde
   main actualizado. Las instrucciones de continuidad pueden ser posteriores a
   la última etiqueta estable. Para cambios de escritorio, sigue por separado el
   protocolo de releases: descargar esta guía no instala Lavanda.
2. **Localizar la copia real.** Identifica la bóveda que abre Obsidian y el
   repositorio privado correspondiente. Comprueba rama, remoto y cambios locales.
   No supongas rutas, usuario, nombres de carpetas ni identidad de archivos por
   lo que se vio en el laboratorio. No clonar una segunda bóveda innecesaria.
3. **Proteger el trabajo antes de integrar.** Pide guardar los documentos abiertos
   y cerrar Obsidian antes de copiar o modificar su configuración. Conserva una
   copia privada local del proyecto, índice y ajustes de los complementos fuera
   de la bóveda y de cualquier carpeta sincronizada. Verifica que puede leerse.
   No incluyas su contenido, credenciales o ruta personal en este repositorio.
4. **Averiguar la sincronización real.** Inspecciona las opciones de GitHub Sync
   y Remotely Save sin imprimir secretos. Determina destino, automatismos y si
   hay dos mecanismos actuando sobre los mismos archivos. Guarda los ajustes
   anteriores. No ejecutes ambos para probar qué ocurre. Si interfieren, pausa
   temporalmente los automatismos durante la reparación y registra cómo estaban.
   No desactives permanentemente un complemento solo porque esté instalado.
5. **Contrastar versiones.** Consulta el remoto privado y compara con la copia
   local antes de integrar. Si ambas tienen cambios, conserva las dos y revisa
   las diferencias. No usar reset, clean, stash automático, force-push ni elegir
   siempre «la nuestra» o «la remota». Si hace falta una decisión sobre el texto,
   explica a Raúl la diferencia y conserva el resto del trabajo preparado.
6. **Reparar lo inequívoco.** En el índice de Longform, resolver marcas de
   conflicto y recuperar referencias a escenas existentes sin alterar su texto.
   Mantener el orden establecido; confirmar con Raúl si hay varias alternativas.
   No modificar los capítulos para eliminar duplicaciones sin su elección.
   Revisar la estructura y abrir Longform: índice y escenas deben ser accesibles.
7. **Probar con material desechable.** Usando un único mecanismo de sincronización
   comprobado, crea una nota de prueba identificada como tal, fuera del manuscrito
   pero dentro del alcance sincronizado. Escribe una frase con tilde y un enlace,
   guarda y sube solo los archivos revisados al repositorio privado. No uses
   «añadir todo» si aparecen ajustes, secretos o cambios ajenos.
8. **Validar recuperación.** Recupera esa nota desde el remoto en una ubicación
   temporal privada y compara su contenido. Esto demuestra subida y recuperación,
   NO demuestra todavía la ida y vuelta real con el equipo de oficina. Deja la
   nota para esa segunda comprobación; registra su ubicación solo en el contexto
   privado. No sobrescribas una nota anterior de pruebas.
9. **Prueba de Raúl.** Que abra el libro, navegue por las escenas y confirme que
   ve su material esperado. Que modifique la nota de prueba y confirme que queda
   guardada y subida. El informe debe distinguir su confirmación de las pruebas
   técnicas del agente. No declarar validación visual si todavía no la hizo.
10. **Cerrar sin sorpresas.** Deja documentado qué mecanismo queda funcionando,
    cuáles están pausados y cómo guardar/subir el trabajo al terminar. Si no se
    ha podido resolver un conflicto, no reactivar automatismos que puedan agravarlo.
    Explica el siguiente paso y publica el retorno depurado.

## Resultado esperado, explicado a Raúl

«Este es tu libro, este es el mecanismo que lo lleva a GitHub y este es el modo
de comprobar que tu sesión quedó subida». La primera sesión no necesita dictado,
modelos locales, nuevos plugins de IA ni servicios en el VPS.

Si quiere iniciar el proyecto de ChatGPT por su cuenta, puede hacerlo después:
comprobar acceso desde ambos equipos con la misma cuenta y compartir únicamente
el contexto literario elegido. No cargar toda la bóveda ni su documentación privada
como efecto colateral de esta tarea.

## Retorno para el laboratorio

Crear o completar `docs/retornos/AAAA-MM-DD-portatil.md` sin borrar hitos anteriores.
Publicar en este repositorio únicamente el resumen depurado. Las correcciones del
libro pertenecen a su repositorio privado. Los detalles necesarios para recuperar
copias o resolver conflictos deben permanecer en un registro privado local.

Plantilla para añadir al retorno:

```markdown
## Portátil de escritura — primera sesión

- Estado: completado / parcial / bloqueado.
- Contexto consultado: commit de Lavanda y fecha de esta guía.
- Copia previa: creada y comprobada / pendiente. Detalles conservados en privado.
- Bóveda e historial: inspeccionados; divergencias resueltas / pendientes.
- Longform: índice reparado / ya correcto / pendiente; escenas abiertas: sí/no.
- Borradores: originales conservados; decisiones literarias pendientes: sí/no.
- Sincronización elegida: mecanismo y modo manual/automático, sin cuentas o rutas.
- Otros sincronizadores: inactivos / pausados / sin interferencia comprobada.
- Subida de nota de prueba y recuperación desde remoto: PASS / FAIL / pendiente.
- Confirmación de Raúl: qué probó y resultado, sin reproducir texto del libro.
- Cambios privados: publicados / solo locales / no hubo; sin diffs ni contenido.
- Pendiente del laboratorio: recuperar y comprobar la nota desde el otro equipo.
- Incidencias y siguiente paso concreto:
```

Haz commit y push del retorno conforme a AGENTS.md. Si no hay acceso a GitHub,
conserva el informe e indica expresamente que todavía no es visible desde el otro
equipo. No prometas un aviso automático: el laboratorio lo leerá al reanudar.
