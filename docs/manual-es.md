# Instalación manual de Dressmaker Languages

Instala primero [Yuuma ModLoader para Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files). El ZIP solo contiene este parche independiente, sin loader, juego ni mods de telas.

1. Cierra el juego por completo.
2. Extrae el ZIP. La exportación del asistente contiene el **idioma del juego guardado**, diccionario, caché y correcciones. Guarda los cambios de idioma antes de exportar. El paquete manual básico de GitHub usa chino simplificado y solo incluye nuestro diccionario original.
3. En Steam, haz clic derecho en el juego y elige Administrar → Ver archivos locales. Usa la raíz que ya contiene `BepInEx`, no `Dressmaker.app/Contents`.
4. Copia `BepInEx/plugins/DressmakerLanguages` del ZIP a `BepInEx/plugins` del juego.
5. Copia `BepInEx/config/DressmakerLanguages` a `BepInEx/config`. Crea `config` si falta. **Copia estas dos subcarpetas por separado; nunca reemplaces toda la carpeta BepInEx.**
6. Guarda una copia de las dos carpetas `DressmakerLanguages` existentes antes de reemplazarlas. Conserva los demás plugins y mods.
7. Reinicia el juego.

Archivos necesarios (`LANG` es el idioma exportado, como `zh-CN`, `ja` o `fr`):

```text
BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll
BepInEx/config/DressmakerLanguages/runtime.json
BepInEx/config/DressmakerLanguages/known-sources.json
BepInEx/config/DressmakerLanguages/translations.LANG.json
```

Si Finder solicita permiso, sigue las indicaciones de macOS. Si falla la copia, comprueba Lectura y escritura para tu cuenta en Obtener información → Compartir y permisos de la carpeta del juego. No concedas acceso a todos. Un dispositivo administrado puede requerir una cuenta autorizada.

La copia manual no concede acceso de escritura al asistente. Puedes seguir escaneando, traduciendo y guardando la caché local. Mientras falten permisos, vuelve a exportar tras nuevas traducciones o cambios de idioma, cierra el juego y copia la actualización. Si tampoco el juego puede escribir en la configuración, puede fallar la recogida de textos nuevos en ejecución; el asistente puede seguir escaneando campos JSON comunes. Reiniciarlo comprueba la presencia del plugin y la configuración.

Para desinstalar, cierra el juego y retira solo las dos carpetas `DressmakerLanguages`. Conserva `data` del asistente para mantener las traducciones.

Un ZIP local puede contener tus nombres de mods, correcciones y traducciones existentes del juego. Para distribuir públicamente, usa el paquete básico generado por el script del proyecto.

0.1.1 es una versión inicial; faltan verificar textos y fuentes en el juego. [Guías y agradecimientos](https://github.com/venti-klee/dressmaker-languages).
