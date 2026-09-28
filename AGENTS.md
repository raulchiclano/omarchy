# Lavanda: continuidad entre equipos y agentes

Este repositorio es la memoria compartida. No presupongas acceso a otro chat.
Habla con Raúl en español y explica resultados con lenguaje sencillo.

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
ni copiar ~/.config completa. No publicar informes personales automáticamente.

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
