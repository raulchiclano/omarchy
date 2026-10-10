# Lavanda: continuidad entre equipos y agentes

Este repositorio es la memoria compartida. No presupongas acceso a otro chat.
Habla con Raúl en español y explica resultados con lenguaje sencillo.

## Portal GitHub entre el portátil y el equipo de trabajo

Raúl autorizó el 2026-10-10 el intercambio continuo de resúmenes de trabajo
depurados mediante GitHub. Al comenzar una tarea de Lavanda en cualquiera de los
dos equipos:

1. Comprueba el estado y el remoto del clon; consulta `origin/main` y las
   etiquetas recientes con `git fetch` si hay red. Conserva los cambios locales:
   no uses reset, stash ni limpieza automática para ponerte al día.
2. Lee los commits recientes y los últimos documentos de `docs/retornos/`, en
   especial el último del otro equipo. Toma esos retornos como contexto, no como
   prueba de que algo esté instalado en este equipo; comprueba el estado local.
3. Si GitHub no está disponible, trabaja con el último estado descargado e indica
   que el contexto remoto podría estar desactualizado.

Al terminar una jornada o una tarea de Lavanda con avances, incidencias o decisiones
útiles para el otro equipo, actualiza o crea el retorno de fecha y alias local según
`docs/retornos/README.md`. Revisa la privacidad, haz commit y súbelo a GitHub sin
esperar a que Raúl pida un traspaso final: esta autorización ya está concedida para
resúmenes depurados. Si el remoto avanzó, intégralo sin perder trabajo; si no
puedes publicar, conserva el archivo local y comunica que el otro chat aún no lo
verá. Esta autorización no cubre publicar datos privados, código, etiquetas ni
versiones sin la autorización correspondiente. Los chats no se sincronizan solos:
el siguiente agente debe leer GitHub al empezar.

## Al recibir «Actualiza Lavanda siguiendo el protocolo del repositorio…»

Lee primero [el protocolo completo](docs/actualizaciones.md). La orden autoriza
la inspección y preparación; presenta el plan concreto antes de aplicar y espera
su aprobación si no la ha dado ya para ese plan. No cambies el escritorio solo
para descubrir qué tiene instalado.

1. Comprueba origen y estado del repositorio; conserva cambios locales.
2. Lee `./install.sh status --json` y los informes locales anteriores. El commit
   descargado NO es la versión instalada. Los eventos parciales no representan
   todo el escritorio; un restore tampoco instala el código que lo ejecuta.
3. Consulta versiones estables y notas acumuladas desde la última aplicación.
   Revisa el código nuevo antes de ejecutarlo. Usa una etiqueta estable en una
   copia/worktree separada si hace falta; no hagas reset, stash ni limpieza automática.
4. Ejecuta doctor y plan con el MISMO conjunto explícito de componentes. Revisa
   divergencias locales antes de proponer sobrescribirlas. Respeta ajustes de hardware.
5. Presenta cambios, dependencias, riesgos, pausa de shell, copia y recuperación.
6. Con el plan aprobado, aplica; valida y ejecuta otro plan. No declares éxito
   visual sin observación o confirmación de Raúl. No bloquees la sesión por tu cuenta.
7. Genera y COMPLETA el informe local, incluso si falla o se decide no actualizar.
   Indica qué está instalado, qué solo se descargó y qué queda pendiente.

No instalar paquetes ni actualizar Omarchy completo como efecto colateral.
No saltarse doctor, editar /usr/share/omarchy, relajar huellas sin estudiar cambios,
ni copiar ~/.config completa. No publicar informes personales completos.

## Al desarrollar aquí

Antes de cambiar, lee notas de publicación e informes de retorno autorizados.
Cada mejora portable debe incluir instalador, pruebas pertinentes, documentación
acumulativa y limitaciones conocidas. Conserva los ajustes por equipo.

Para publicar una versión: sigue docs/actualizaciones.md, sección Publicación.
Los commits de trabajo no son una recomendación de instalación. No reutilices
etiquetas publicadas. Deja registro de pruebas reales frente a pruebas simuladas.

Pruebas básicas:

```bash
python3 -m unittest discover -s tests -v
node tests/emoji-search.cjs
```

El fork del dock se fija en dock.lock.json: cualquier actualización exige revisar
su revisión y huellas; no seguir automáticamente la punta del fork.
