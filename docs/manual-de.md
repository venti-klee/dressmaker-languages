# Manuelle Installation von Dressmaker Languages

Installieren Sie zuerst [Yuuma ModLoader für Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files). Diese ZIP enthält nur den unabhängigen Patch, keinen Loader, kein Spiel und keine Stoff-Mods.

1. Beenden Sie das Spiel vollständig.
2. Entpacken Sie die ZIP. Der Export des Assistenten enthält die **gespeicherte Spielsprache**, Wörterbuch, Cache und Korrekturen. Sprachänderungen vor dem Export speichern. Das öffentliche Basispaket auf GitHub ist auf vereinfachtes Chinesisch eingestellt und enthält nur unser selbst erstelltes Wörterbuch.
3. In Steam das Spiel rechts anklicken und Verwalten → Lokale Dateien durchsuchen wählen. Verwenden Sie den Spielordner mit dem vorhandenen `BepInEx`, nicht `Dressmaker.app/Contents`.
4. Kopieren Sie `BepInEx/plugins/DressmakerLanguages` aus der ZIP nach `BepInEx/plugins` im Spiel.
5. Kopieren Sie `BepInEx/config/DressmakerLanguages` nach `BepInEx/config`. Falls nötig, `config` anlegen. **Die beiden Unterordner einzeln kopieren; niemals den gesamten BepInEx-Ordner ersetzen.**
6. Vorhandene `DressmakerLanguages`-Ordner zuerst andernorts sichern, dann nur diese beiden ersetzen. Alle anderen Plugins und Mods behalten.
7. Starten Sie das Spiel neu.

Benötigte Dateien (`LANG` ist die exportierte Sprache, etwa `zh-CN`, `ja` oder `fr`):

```text
BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll
BepInEx/config/DressmakerLanguages/runtime.json
BepInEx/config/DressmakerLanguages/known-sources.json
BepInEx/config/DressmakerLanguages/translations.LANG.json
```

Berechtigungsabfragen von Finder gemäß macOS bestätigen. Falls das Kopieren scheitert, im Spielordner unter Informationen → Teilen & Zugriffsrechte die Rechte Lesen & Schreiben für das eigene Konto prüfen. Nicht allen Benutzern Zugriff gewähren. Verwaltete Geräte können ein berechtigtes Konto erfordern.

Manuelles Kopieren gibt dem Assistenten keine Schreibrechte. Scannen, Übersetzen und lokales Speichern bleiben möglich. Bis die Rechte stimmen, nach neuen Übersetzungen oder einem Sprachwechsel erneut exportieren, das Spiel beenden und die Aktualisierung kopieren. Kann auch das Spiel nicht in die Konfiguration schreiben, kann die Laufzeit-Erfassung neuer Texte scheitern; übliche JSON-Anzeigefelder lassen sich weiterhin scannen. Beim Neustart prüft der Assistent Plugin und Konfiguration.

Zur Deinstallation das Spiel beenden und nur die zwei `DressmakerLanguages`-Ordner entfernen. Der Ordner `data` des Assistenten bewahrt Übersetzungen auf.

Ein lokaler Export kann eigene Mod-Namen, Korrekturen und vorhandene Spielübersetzungen enthalten. Für öffentliche Verteilung das Basispaket des Projekt-Paketierungsskripts verwenden.

Version 0.1.3 ist eine frühe Ausgabe; Darstellung und Schriften im Spiel sind noch ungeprüft. [Anleitungen und Danksagung](https://github.com/venti-klee/dressmaker-languages).
