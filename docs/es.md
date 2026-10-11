# Asistente multilingüe de Dressmaker 0.1.6

[简体中文](zh-CN.md) · [English](en.md) · [日本語](ja.md) · [한국어](ko.md) · [Français](fr.md) · [Deutsch](de.md) · **Español**

Un asistente independiente para Mac y un parche que traduce la interfaz de Yuuma ModLoader y los nombres mostrados de los objetos de los mods. Se basa en la descripción pública de [la herramienta de SallyHCA](https://www.nexusmods.com/dressmaker/mods/339) y de [su proyecto](https://github.com/Sally-4869/dressmaker-mods-cn). No incluye código, diccionarios ni recursos de ese proyecto.

Download ZIP de GitHub contiene fuentes sin plugin compilado ni `.app`. Los jugadores deben usar la Release Mac; los usuarios de fuentes deben compilar con los pasos siguientes. Descripción del proyecto: [README](../README.es.md).

## Instalación

1. Instala primero la [versión para Mac de Yuuma ModLoader](https://www.nexusmods.com/dressmaker/mods/1?tab=files). El parche se compiló con la versión 0.7.3 instalada en este ordenador.
2. Extrae el paquete completo en una carpeta con permiso de escritura. Necesitas Python 3.9 o posterior. Las funciones básicas no requieren paquetes adicionales de Python ni el entorno de ejecución .NET.
3. Abre `Start.command` o `针影裁梦多语言助手.app`. Se abrirá una página local en el navegador. Mantén abierta la ventana de comandos mientras uses el asistente.
4. Elige **Idioma del asistente** en la parte superior. Los textos y el enlace a la guía cambian inmediatamente, y la selección se guarda en este navegador. No modifica el idioma de traducción del juego. Al principio se usa el idioma del navegador; si no está disponible, se usa inglés.
5. Comprueba la carpeta del juego, elige **Idioma de traducción del juego** y pulsa **Guardar ajustes**. El idioma de destino inicial del juego es chino simplificado.
6. Pulsa **Instalar / actualizar el parche**. Solo se crean o actualizan las carpetas propias `BepInEx/plugins/DressmakerLanguages/` y `BepInEx/config/DressmakerLanguages/`.
7. Guarda la partida y reinicia el juego normalmente. Comprueba el resultado en Mod Manager o Mod Settings. Los cambios posteriores de diccionario e idioma suelen actualizar los textos recopilados en unos 2 segundos.
8. Tras instalar nuevos mods, pulsa **Analizar mods y el gestor**. El parche también recopila textos ingleses desconocidos mostrados en el juego.

Para una instalación manual, copia la carpeta incluida `BepInEx/plugins/DressmakerLanguages/` a la ubicación correspondiente del juego y usa después el botón de instalación del asistente para generar la configuración. No necesitas asistentes Windows `.exe` ni Vortex.

## Idiomas y cobertura

La interfaz y las guías Markdown están disponibles en chino, inglés, japonés, coreano, francés, alemán y español. El idioma de la interfaz y el de traducción del juego son ajustes independientes.

Los diccionarios del juego incluyen 148 términos comunes por idioma para chino, japonés, coreano y francés, y 14 para alemán y español. El chino y el japonés también importan las tablas oficiales de tu propia instalación del juego. Este ordenador generó 5.157 entradas chinas, pero la cantidad depende de la versión instalada. Las traducciones oficiales se generan localmente y no se distribuyen en el archivo ZIP. El inglés restaura el texto original.

Cada idioma de destino tiene su propia caché. El parche traduce textos mostrados de los mods; no ofrece una localización completa nueva del juego base.

## Traducción sin conexión y en línea

Las correcciones manuales tienen prioridad. Las demás entradas siguen este orden: **diccionario → traducción en caché → combinación de términos totalmente reconocidos → modelo Argos sin conexión instalado → servicio gratuito en línea**.

Los diccionarios y las traducciones guardadas funcionan sin conexión desde el principio. Un nombre compuesto solo se traduce si se reconocen todas sus palabras. Sin modelo ni servicio en línea, el texto desconocido permanece en inglés en la lista de traducciones pendientes.

Para traducir frases desconocidas sin conexión, elige el idioma de destino del juego y pulsa **Descargar el modelo sin conexión de este idioma**. La primera instalación descarga un entorno Python independiente y un modelo, por lo que necesita internet y puede tardar. Cuando termine, cierra y vuelve a abrir el asistente. Desactiva la traducción en línea y guarda los ajustes para trabajar totalmente sin conexión. Debes instalar un modelo por idioma; su disponibilidad depende del índice actual de Argos. Los modelos no están incluidos en el paquete y su instalación aún no se ha probado de principio a fin.

El servicio predeterminado es la API pública de MyMemory, sin clave. Se aplican sus cuotas. El asistente añade un presupuesto prudente de 4.500 bytes UTF-8 diarios, separación entre solicitudes y una pausa tras un fallo. Cada solicitud gratuita admite como máximo 500 bytes; usa un modelo sin conexión o traducción manual para entradas más largas. También puedes indicar una instancia HTTPS disponible de LibreTranslate, sin garantía de gratuidad o disponibilidad permanente.

El modo en línea solo envía al proveedor elegido textos ingleses mostrados que no tengan traducción local; no envía partidas guardadas ni paquetes de mods. Los resultados correctos se guardan. Los fallos de conexión, las cuotas o las respuestas no válidas conservan el texto original. No se implementan suplantación de identidad ni mecanismos para eludir pagos o CAPTCHA.

## Servicios gratuitos de traducción

Elige un servicio y pulsa **Guardar ajustes**.

- **MyMemory**: API pública predeterminada, sin clave. Se aplican los límites del proveedor.
- **Adaptador web de Bing (experimental)**: sin clave. Obtiene una sesión temporal de la página pública de traducción y la usa para traducir. No es una API oficial estable; los cambios en la página, la sesión o los límites pueden interrumpirla.
- **LibreTranslate**: indica una instancia HTTPS disponible para ti. Su coste y sus requisitos de cuenta dependen de la instancia. Actualmente solo se admiten instancias sin clave.

La opción de recurrir a MyMemory está desactivada por defecto. Hace un único intento alternativo tras un fallo de red o del servicio, nunca por presupuesto agotado, texto demasiado largo, formato dañado o dirección vacía. El mismo texto puede enviarse a dos servicios; ambos intentos cuentan para el presupuesto diario. Las solicitudes se separan al menos 3 segundos. Los fallos repetidos activan una pausa de 5 minutos y se conserva el original. El diccionario y la caché siguen disponibles sin conexión.

La sesión de Bing permanece en memoria. No se inicia sesión, no se guardan cuentas, no se rotan proxies ni se evitan CAPTCHA. Los resultados válidos se guardan por idioma de destino y las correcciones manuales tienen prioridad.

Pasaron las 72 pruebas automatizadas: sesión, código del chino, respuestas inválidas, caché sin conexión, alternativa y presupuesto. Bing devolvió traducciones reales en chino, japonés, coreano, francés, alemán y español. Se comprobaron la caché sin conexión y la conservación de `{0}`. También hubo errores de conexión y tiempos de espera agotados; el adaptador sigue siendo experimental.

## Corrección y desinstalación

Busca el original inglés, edita su traducción y pulsa **Guardar**. Las correcciones manuales sustituyen las traducciones automáticas y los diccionarios del mismo idioma. Conserva variables, saltos de línea y etiquetas de formato: se rechazan las traducciones que los dañen. Cambiar el idioma del asistente conserva los borradores de traducción sin guardar.

**Traducir los textos pendientes** también intenta procesar cadenas candidatas del gestor. El modo automático prioriza los textos realmente mostrados y el contenido de los mods para evitar consumir la cuota con cadenas sin usar del programa.

Pulsa **Desinstalar el parche** y reinicia el juego. Las carpetas propias del plugin y su configuración se trasladan a `data/backups/`. Las traducciones se conservan. Este parche no modifica el cargador original, mods, identificadores de objetos, texturas ni partidas guardadas.

## Archivos locales

- `data/translations.sqlite3`: caché y correcciones por idioma.
- `data/settings.json`: idioma de destino, opciones en línea y ruta del juego.
- `data/model-install.log`: registro de instalación de modelos.
- `.venv/` y `models/`: entorno y modelos opcionales.
- En el juego, `BepInEx/config/DressmakerLanguages/pending.jsonl`: textos desconocidos recopilados.
- En el juego, `BepInEx/LogOutput.log`: busca `Dressmaker Languages` para problemas de carga o fuentes.

La página solo escucha en el ordenador local y protege las operaciones de escritura con un token de sesión aleatorio. Tras cerrar el asistente, el parche sigue usando los diccionarios y traducciones publicados. La traducción automática necesita que el asistente permanezca abierto.

## Verificación y limitaciones

El plugin se compiló con ModLoader 0.7.3, BepInEx 5.4.23.5 y Unity 6000.3.4f1. Pasaron once pruebas del núcleo de traducción. Las solicitudes reales a MyMemory devolvieron traducciones en chino, japonés, coreano y francés. La localización de la interfaz y las guías se añadió en 0.1.6.

**La integración dentro del juego aún no se ha probado.** Quedan por comprobar la cobertura, la disposición, las fuentes japonesas y coreanas y los nombres de telas de terceros. No había paquetes de contenido instalados en este ordenador durante el desarrollo.

El parche usa las rutas habituales de visualización Unity Text / TextMeshPro. No se garantiza la cobertura de textos dibujados de forma personalizada, texto en imágenes, fuentes distintas del inglés o modificación directa de guiones narrativos. Los archivos narrativos no se modifican. Los términos textiles, modificadores de color o la gramática pueden traducirse mal; puedes corregirlos manualmente.

## Código fuente y compilación

El plugin está en `src/DressmakerLanguages.cs` y el asistente en `assistant/`. Compila con tu propio SDK .NET y los ensamblados del juego:

```sh
python3 src/build.py --game "/path/to/game" --dotnet "/path/to/dotnet"
```

El código independiente y los diccionarios redactados para esta herramienta usan la licencia MIT. Esta licencia no concede derechos sobre los recursos del juego ni el proyecto de referencia.

## Agradecimientos

Gracias a los autores y equipos cuyo trabajo hizo posible este proyecto:

- [Cozy Lives (desarrollo) y Free Lives (edición)](https://store.steampowered.com/app/4019220/Dressmaker/) — Gracias por crear y publicar Dressmaker, donde podemos diseñar, cortar y coser nuestras prendas.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Gracias por el loader y el soporte de contenido personalizado que permiten crear telas y accesorios comunitarios.
- [SallyHCA — Herramienta automática de traducción al chino](https://www.nexusmods.com/dressmaker/mods/339) — Gracias por compartir el enfoque para traducir el gestor de mods y los nombres del contenido. Tu herramienta y su descripción pública inspiraron el proceso de traducción de este proyecto.

La implementación es independiente; los agradecimientos no implican respaldo de los autores. No se redistribuyen sus programas, diccionarios, recursos del juego ni modelos.


## Descargar paquete de instalación manual

Exporta el plugin, el diccionario y las traducciones del idioma del juego guardado sin escribir en su carpeta. Vuelve a exportar después de traducir o cambiar de idioma. El ZIP incluye instrucciones en siete idiomas. [Descargar paquete de instalación manual](manual-es.md).


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

Un fallo del servicio pausa el lote y deja el resto sin procesar. Tras la espera se reintentan las tareas incompletas con el mismo idioma y alcance, incluidos candidatos iniciados manualmente. Volver a pulsar no evita la espera ni reinicia el progreso. Cambiar el idioma de destino o la carpeta del juego cancela la tarea anterior. Cambiar de servicio conserva el alcance y continúa las entradas pendientes. Solo las traducciones guardadas correctamente reducen el recuento.

Se corrigió el tratamiento de espacios iniciales y finales de Google: se envía el cuerpo, se verifica completo y se restauran los espacios. Ya no se rechazan respuestas correctas por recortar los bordes; etiquetas, variables e integridad siguen protegidas.


Cambiar y continuar (0.1.6)

Reintenta las entradas fallidas y pendientes sin perder traducciones guardadas. Cambiar el servicio en ajustes también retoma el alcance original. Una solicitud en curso puede tardar unos 15 segundos. Se mantienen la espera y el presupuesto diario del mismo servicio.
