# Dressmaker · Asistente de idiomas para mods

[简体中文](README.zh-CN.md) · [English](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Una herramienta independiente para macOS que traduce Yuuma ModLoader y los textos ingleses de los mods. **0.1.5 es una versión inicial; la integración dentro del juego aún no se ha probado.**

## Funciones

- Idiomas separados para el juego y la interfaz: chino, inglés, japonés, coreano, francés, alemán y español.
- Diccionarios, correcciones y caché sin conexión; modelos Argos opcionales para frases desconocidas.
- MyMemory sin clave, adaptador web experimental de Bing o instancia LibreTranslate disponible.
- Analiza campos JSON habituales de nuevos mods y recoge inglés desconocido mostrado en el juego.
- Guarda traducciones por idioma, prioriza las correcciones y protege variables y etiquetas.

## Para jugadores

1. Instala [Yuuma ModLoader para Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files).
2. Descarga **Dressmaker-Languages-Mac-0.1.5.zip** de Releases y extrae toda la carpeta. Se necesita Python 3.9 o posterior.
3. Abre `Start.command` o `针影裁梦多语言助手.app`.
4. Elige el idioma de la interfaz, comprueba la carpeta y el idioma del juego, guarda, instala el parche y reinicia el juego.
5. Analiza después de instalar mods nuevos y mantén abierto el asistente para traducir. Puedes corregir los resultados.

La [guía española](docs/es.md) explica modelos, desinstalación y datos. Download ZIP de GitHub contiene fuentes sin plugin compilado ni `.app`. Los jugadores deben usar el archivo Release.

## Cobertura y verificación

Se leen campos JSON como `name`, `displayName`, `display_name`, `description`, `tooltip` y `title`. Los hooks cubren Unity Text / TextMeshPro en el loader o nombres detectados. No se garantizan interfaces propias, textos en imágenes, formatos binarios especiales ni fuentes no inglesas. La herramienta no añade telas ni una localización completa del juego base.

El plugin se compiló para ModLoader 0.7.3 / BepInEx 5.4.23.5 / Unity 6000.3.4f1. Pasaron las 66 pruebas automatizadas. Se comprobó el cambio de idioma local y Bing y MyMemory devolvieron traducciones reales. La red, los límites o cambios de página pueden interrumpir los adaptadores web. Faltan pruebas de nombres de telas de terceros, disposición y fuentes en el juego.

El modo en línea envía textos ingleses desconocidos al servicio elegido. Las solicitudes se separan al menos 3 segundos y el presupuesto predeterminado es de 4.500 bytes UTF-8 diarios. Los fallos conservan el original. La alternativa MyMemory está desactivada por defecto; al activarla ambos intentos cuentan. El diccionario y la caché funcionan sin conexión.

## Desarrollo y contribuciones

Fuentes en `src/` y `assistant/`. El asistente básico utiliza solo la biblioteca estándar de Python.

```sh
python3 -m unittest discover -s tests -v
```

Para compilar necesitas tus ensamblados del juego y del loader y un SDK .NET. El asistente es 0.1.5; el plugin sin cambios conserva la versión interna 0.1.0. Las comprobaciones de GitHub Actions están activadas; consulta los resultados en la página Actions del repositorio.

Se aceptan Issues y Pull Requests sobre terminología, fuentes y compatibilidad. Incluye versiones de juego, sistema y loader y un ejemplo publicable. Actualiza los siete catálogos y guías al cambiar textos. No subas partidas, mods privados ni recursos del juego.

## Publicación en GitHub

1. Crea un repositorio **Public** vacío. Ya se incluyen README y licencia; no generes otros.
2. Extrae **Dressmaker-Languages-GitHub-0.1.5.zip** y sube su contenido con `README.md` en la raíz. Incluye `.github/`, `.gitignore` y `.gitattributes`. Finder muestra archivos ocultos con `Command + Shift + .`. Git conserva los permisos ejecutables de los scripts.
3. Crea la Release `v0.1.5` y adjunta el archivo Mac. Las fuentes son para el repositorio; el archivo Mac es para jugadores.
4. Verifica el parche en tu juego antes de publicarlo y actualiza los resultados. Se excluyen datos personales, rutas, tokens e historial Git. 

`UPLOAD-MANIFEST.json` enumera los archivos exactos. Las instrucciones oficiales de GitHub aparecen abajo.

Instrucciones oficiales de GitHub: [Create repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) · [Create Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

## Créditos y licencia

Implementación independiente basada en las [funciones públicas de SallyHCA](https://www.nexusmods.com/dressmaker/mods/339), sin su código, diccionarios ni recursos. El código propio y los diccionarios redactados usan [MIT](LICENSE), sin conceder derechos sobre recursos del juego o del proyecto citado. Sin afiliación con el juego, Nexus Mods, Microsoft o Argos.

## Agradecimientos

Gracias a los autores y equipos cuyo trabajo hizo posible este proyecto:

- [Cozy Lives (desarrollo) y Free Lives (edición)](https://store.steampowered.com/app/4019220/Dressmaker/) — Gracias por crear y publicar Dressmaker, donde podemos diseñar, cortar y coser nuestras prendas.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Gracias por el loader y el soporte de contenido personalizado que permiten crear telas y accesorios comunitarios.
- [SallyHCA — Herramienta automática de traducción al chino](https://www.nexusmods.com/dressmaker/mods/339) — Gracias por compartir el enfoque para traducir el gestor de mods y los nombres del contenido. Tu herramienta y su descripción pública inspiraron el proceso de traducción de este proyecto.

La implementación es independiente; los agradecimientos no implican respaldo de los autores. No se redistribuyen sus programas, diccionarios, recursos del juego ni modelos.


## Descargar paquete de instalación manual

Exporta el plugin, el diccionario y las traducciones del idioma del juego guardado sin escribir en su carpeta. Vuelve a exportar después de traducir o cambiar de idioma. El ZIP incluye instrucciones en siete idiomas. [Descargar paquete de instalación manual](docs/manual-es.md).


## Progreso de traducción

Se actualiza cada segundo. El progreso cuenta textos procesados; originales conservados y fallos no son traducciones correctas. La lista se actualiza conservando las ediciones sin guardar.

## Google web y traducciones guardadas

Las solicitudes web de Google no necesitan clave. La disponibilidad depende de la red; los cambios o límites pueden causar fallos. Las solicitudes se espacian al menos 3 segundos.

Ejemplo: Hoy (UTC): 4,498 / 4,500 bytes usados · 2 restantes. Es un presupuesto local; aumentarlo no aumenta la cuota del servicio.

Las traducciones se guardan localmente y se reutilizan sin conexión. Conserva la carpeta data al actualizar; se mantienen las cachés por idioma y las correcciones.

## Búsqueda y filtros del diccionario (0.1.4)

La búsqueda incluye el original y la traducción guardada. Los resultados se actualizan al escribir o al pulsar Enter. La lista combina los textos recopilados, el diccionario y la caché del idioma de destino actual, con una fila por original.

- **Estado**: sin traducir, traducido u original conservado. El recuento usa los valores guardados que se aplican realmente; los cambios sin guardar no cuentan como traducciones realizadas.
- **Canal**: diccionario, términos combinados, corrección manual, modelo sin conexión, Google, Bing, MyMemory o LibreTranslate. Se muestra el canal usado, por ejemplo diccionario cuando sustituye una traducción automática anterior.
- **Origen**: todos, recopilados, visibles en el juego, contenido de mods, candidatos del gestor o solo diccionario/caché. Combina « Sin traducir » y « Textos visibles en el juego » para localizar traducciones faltantes visibles.
- **Orden y páginas**: original ascendente/descendente, guardados recientes o textos del juego primero; 25, 50 o 100 filas por página y acceso por número. Si no hay resultados, aparece una indicación; puedes borrar los filtros.

Los filtros y las páginas conservan los cambios sin guardar y muestran su número. Guarda cada fila antes de cerrar o recargar la página: los borradores sin guardar se pierden al recargar. Una fila guardada puede salir del filtro actual. La búsqueda y los filtros no contactan con servicios de traducción ni consumen presupuesto.

Los filtros solo afectan a la lista; la traducción de textos pendientes procesa la cola recopilada.

El recuento separa textos visibles del juego, contenido de mods, candidatos del gestor y entradas solo del diccionario/caché. El análisis puede recoger formatos internos, errores y textos sin usar; los candidatos no son un recuento de omisiones visibles. El modo automático procesa textos visibles y mods. Filtra Sin traducir + Textos visibles en el juego para revisar lo recopilado; abre las pantallas no visitadas para recogerlas.

Un fallo del servicio pausa el lote y deja el resto sin procesar. Tras la espera se reintentan las tareas incompletas con el mismo idioma y alcance, incluidos candidatos iniciados manualmente. Volver a pulsar no evita la espera ni reinicia el progreso. Cambiar los ajustes cancela el reintento anterior. Solo las traducciones guardadas correctamente reducen el recuento.

Se corrigió el tratamiento de espacios iniciales y finales de Google: se envía el cuerpo, se verifica completo y se restauran los espacios. Ya no se rechazan respuestas correctas por recortar los bordes; etiquetas, variables e integridad siguen protegidas.
