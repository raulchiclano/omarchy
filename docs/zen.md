# Zen: ajustes manuales para el portátil

Comprobado en la configuración del equipo de origen el 25 de septiembre de 2026.
Estos ajustes se hacen en Zen; el instalador de Lavanda no modifica su perfil.

## Cerrar pestañas con doble clic

Este fue el ajuste solicitado y confirmado en el chat.

1. Escribe `about:config` en la barra de direcciones y acepta el aviso.
2. Busca `browser.tabs.closeTabByDblclick`.
3. Pon su valor en **true**.
4. Abre una pestaña de prueba, selecciónala y haz doble clic sobre ella para comprobar el cierre.

Para deshacerlo, vuelve a **false**. Si cierras una pestaña por error, puedes
recuperarla con **Ctrl+Mayús+T** ([atajos oficiales de Zen](https://docs.zen-browser.app/user-manual/shortcuts)).

## Otros ajustes observados en este equipo

Estos valores están guardados actualmente; no consta que todos se cambiaran
expresamente durante el chat.

| Preferencia en `about:config` | Valor actual | Para qué sirve |
| --- | --- | --- |
| `zen.view.compact.enable-at-startup` | `true` | Activar el modo compacto al iniciar. |
| `intl.locale.requested` | `es-ES,en-US` | Preferir español de España, con inglés como alternativa. |

Para reproducirlos, busca cada preferencia y establece el valor indicado.
Si tu versión no ofrece alguna, no la crees a ciegas: revisa sus ajustes de
apariencia o idioma. Para el idioma, también puedes usar la sección de idiomas
de los ajustes de Zen; puede requerir descargar el paquete y reiniciar.

## Alcance

No hay constancia suficiente para documentar una lista de extensiones, Zen Mods
o cambios de privacidad como parte de este trabajo. No es necesario copiar
`prefs.js`, el perfil completo, sesiones ni credenciales para repetir estos ajustes.
