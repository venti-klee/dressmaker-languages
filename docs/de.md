# Dressmaker Sprachassistent 0.1.6

[简体中文](zh-CN.md) · [English](en.md) · [日本語](ja.md) · [한국어](ko.md) · [Français](fr.md) · **Deutsch** · [Español](es.md)

Ein unabhängig entwickelter Mac-Assistent und Spiel-Patch zur Übersetzung der Oberfläche von Yuuma ModLoader und der Anzeigenamen von Mod-Gegenständen. Grundlage ist die öffentliche Funktionsbeschreibung von [SallyHCAs Werkzeug](https://www.nexusmods.com/dressmaker/mods/339) und [dessen Projekt](https://github.com/Sally-4869/dressmaker-mods-cn). Code, Wörterbücher und andere Inhalte dieses Projekts sind nicht enthalten.

GitHubs Download ZIP enthält Quellen ohne kompiliertes Plugin oder `.app`. Spieler sollten das Mac-Release verwenden; mit Quellen muss das Plugin nach der Anleitung unten gebaut werden. Veröffentlichung: [README](../README.de.md).

## Installation

1. Zuerst die [Mac-Version von Yuuma ModLoader](https://www.nexusmods.com/dressmaker/mods/1?tab=files) installieren. Der Patch wurde mit der auf diesem Computer vorhandenen Version 0.7.3 kompiliert.
2. Das gesamte Paket in einen beschreibbaren Ordner entpacken. Python 3.9 oder neuer ist erforderlich. Die Grundfunktionen benötigen keine zusätzlichen Python-Pakete und keine .NET-Laufzeit.
3. `Start.command` oder `针影裁梦多语言助手.app` öffnen. Im Browser erscheint eine lokale Seite. Das Befehlsfenster während der Nutzung geöffnet lassen.
4. Oben auf der Seite **Sprache des Assistenten** wählen. Oberflächentexte und Anleitungslink wechseln sofort; die Auswahl wird in diesem Browser gespeichert. Die Übersetzungssprache des Spiels bleibt unverändert. Beim ersten Start gilt die Browsersprache, bei nicht unterstützten Sprachen Englisch.
5. Den Spielordner prüfen, **Übersetzungssprache des Spiels** wählen und **Einstellungen speichern** drücken. Die anfängliche Zielsprache des Spiels ist vereinfachtes Chinesisch.
6. **Spiel-Patch installieren / aktualisieren** wählen. Nur die eigenen Ordner `BepInEx/plugins/DressmakerLanguages/` und `BepInEx/config/DressmakerLanguages/` werden angelegt oder aktualisiert.
7. Den Spielstand speichern und das Spiel wie gewohnt neu starten. Das Ergebnis in Mod Manager oder Mod Settings prüfen. Spätere Änderungen an Wörterbuch und Sprache erscheinen für erfasste Texte meist nach etwa 2 Sekunden.
8. Nach der Installation neuer Mods **Mods und Verwaltung durchsuchen** wählen. Der Patch erfasst außerdem unbekannte englische Texte, die im Spiel angezeigt werden.

Für die manuelle Installation den enthaltenen Ordner `BepInEx/plugins/DressmakerLanguages/` an die entsprechende Stelle im Spiel kopieren. Anschließend mit der Installationsschaltfläche des Assistenten die Konfiguration erzeugen. Windows-Assistenten als `.exe` und Vortex werden nicht benötigt.

## Sprachen und Umfang

Die Oberfläche und Markdown-Anleitungen unterstützen Chinesisch, Englisch, Japanisch, Koreanisch, Französisch, Deutsch und Spanisch. Oberflächensprache und Übersetzungssprache des Spiels sind getrennte Einstellungen.

Die Spielwörterbücher enthalten je 148 häufige Begriffe für Chinesisch, Japanisch, Koreanisch und Französisch sowie je 14 für Deutsch und Spanisch. Chinesisch und Japanisch importieren zusätzlich die offiziellen Übersetzungstabellen aus deiner eigenen Spielinstallation. Auf diesem Computer entstanden 5.157 chinesische Einträge; die Zahl hängt von der Spielversion ab. Offizielle Übersetzungen werden lokal erzeugt und nicht im ZIP verteilt. Englisch stellt den Originaltext wieder her.

Jede Zielsprache hat einen eigenen Cache. Der Patch übersetzt Anzeigetexte von Mods und liefert keine vollständige neue Lokalisierung des Basisspiels.

## Offline- und Online-Übersetzung

Manuelle Korrekturen haben Vorrang. Für andere Einträge gilt: **Wörterbuch → gespeicherte Übersetzung → Kombination vollständig bekannter Begriffe → installiertes Argos-Offline-Modell → kostenloser Online-Dienst**.

Wörterbücher und gespeicherte Übersetzungen sind sofort offline nutzbar. Zusammengesetzte Namen werden nur übersetzt, wenn jedes Wort erkannt wird. Ohne Modell oder Online-Dienst bleiben unbekannte Texte auf Englisch in der Liste offener Übersetzungen.

Für unbekannte Sätze offline die Spielzielsprache wählen und **Offline-Modell für diese Sprache herunterladen** drücken. Die erste Einrichtung lädt eine separate Python-Umgebung und das Modell herunter, benötigt Internet und kann länger dauern. Danach den Assistenten beenden und erneut öffnen. Online-Übersetzung deaktivieren und die Einstellungen speichern, um vollständig offline zu arbeiten. Modelle müssen je Sprache installiert werden; ihre Verfügbarkeit hängt vom aktuellen Argos-Modellverzeichnis ab. Sie sind nicht im Paket enthalten. Die vollständige Modelleinrichtung wurde noch nicht praktisch getestet.

Der Standarddienst ist die öffentliche MyMemory-API ohne API-Schlüssel. Es gelten die Kontingente des Dienstes. Zusätzlich setzt der Assistent ein vorsichtiges Tagesbudget von 4.500 UTF-8-Bytes, Abstände zwischen Anfragen und eine Wartezeit nach Fehlern. Pro kostenloser Anfrage sind höchstens 500 Bytes möglich. Längere Texte mit einem Offline-Modell oder manuell übersetzen. Eine verfügbare LibreTranslate-HTTPS-Instanz kann angegeben werden; kostenlose und dauerhafte Verfügbarkeit ist nicht garantiert.

Im Online-Modus werden nur englische Anzeigetexte ohne lokale Übersetzung an den gewählten Dienst gesendet, keine Spielstände oder Mod-Pakete. Erfolgreiche Ergebnisse werden gespeichert. Bei Verbindungsproblemen, ausgeschöpften Kontingenten oder ungültigen Antworten bleibt der Originaltext erhalten. Identitätstäuschung sowie Umgehung von Zahlungen oder CAPTCHAs sind nicht eingebaut.

## Kostenlose Übersetzungsdienste

Wählen Sie einen Dienst und klicken Sie auf **Einstellungen speichern**.

- **MyMemory**: voreingestellte öffentliche API ohne Schlüssel. Die Kontingente des Anbieters gelten.
- **Bing-Web-Anbindung (experimentell)**: ohne Schlüssel. Eine temporäre Sitzung wird von der öffentlichen Übersetzungsseite bezogen und für Anfragen genutzt. Dies ist keine stabile offizielle Entwickler-API; Änderungen an Seite, Sitzung oder Limits können sie unterbrechen.
- **LibreTranslate**: geben Sie eine nutzbare HTTPS-Instanz an. Kosten und Kontopflicht hängen von der Instanz ab. Aktuell werden nur Instanzen ohne Schlüssel unterstützt.

Die Ersatzoption mit MyMemory ist standardmäßig deaktiviert. Bei Netzwerk- oder Dienstfehlern erfolgt ein einziger weiterer Versuch. Ein überschrittenes Budget, zu langer Text, beschädigte Formatierung oder eine leere Adresse lösen keinen Ersatzversuch aus. Derselbe Text kann an zwei Dienste gehen; beide Versuche zählen zum Tagesbudget. Alle Anfragen erfolgen mit mindestens 3 Sekunden Abstand. Wiederholte Fehler führen zu einer Pause von 5 Minuten; der Originaltext bleibt erhalten. Wörterbuch und Cache sind weiter offline nutzbar.

Die Bing-Sitzung bleibt im Arbeitsspeicher. Es gibt keine Anmeldung, Kontospeicherung, Proxyrotation oder CAPTCHA-Umgehung. Gültige Ergebnisse werden je Zielsprache gespeichert; manuelle Korrekturen behalten Vorrang.

Alle 72 automatisierten Tests bestanden: Sitzung, chinesischer Sprachcode, ungültige Antworten, Offline-Cache, Ersatzdienst und Budget. Bing lieferte reale chinesische, japanische, koreanische, französische, deutsche und spanische Übersetzungen. Offline-Cache und Erhalt von `{0}` wurden geprüft. Es gab auch Verbindungsfehler und Zeitüberschreitungen; die Anbindung bleibt experimentell.

## Korrekturen und Deinstallation

Den englischen Originaltext suchen, die Übersetzung bearbeiten und **Speichern** wählen. Manuelle Korrekturen überschreiben maschinelle Übersetzungen und Wörterbücher derselben Zielsprache. Variablen, Zeilenumbrüche und Formatierungstags erhalten; fehlerhafte Übersetzungen werden abgelehnt. Beim Wechsel der Assistentensprache bleiben nicht gespeicherte Übersetzungsentwürfe erhalten.

**Fehlende Texte übersetzen** verarbeitet auch Textkandidaten der Verwaltung. Der automatische Modus bevorzugt tatsächlich angezeigte Texte und Mod-Inhalte, damit ungenutzte Programmtexte das kostenlose Kontingent nicht verbrauchen.

**Patch deinstallieren** wählen und das Spiel neu starten. Eigene Plugin- und Konfigurationsordner werden nach `data/backups/` verschoben; Übersetzungsdaten bleiben erhalten. Der ursprüngliche Loader, Mods, Gegenstands-IDs, Texturen und Spielstände werden vom Patch nicht verändert.

## Lokale Dateien

- `data/translations.sqlite3`: sprachabhängige Übersetzungen und manuelle Korrekturen.
- `data/settings.json`: Spielzielsprache, Online-Optionen und Spielpfad.
- `data/model-install.log`: Protokoll der Modelleinrichtung.
- `.venv/` und `models/`: optionale Modellumgebung und Modelle.
- Im Spiel: `BepInEx/config/DressmakerLanguages/pending.jsonl` enthält erfasste unbekannte Texte.
- Im Spiel: `BepInEx/LogOutput.log`; nach `Dressmaker Languages` suchen, um Lade- und Schriftprobleme zu prüfen.

Die Seite ist nur auf dem lokalen Computer erreichbar. Ein zufälliges Sitzungstoken schützt Schreibvorgänge. Nach dem Beenden des Assistenten verwendet der Patch weiterhin veröffentlichte Wörterbücher und gespeicherte Übersetzungen. Automatische Übersetzung erfordert einen laufenden Assistenten.

## Prüfung und Grenzen

Das Plugin wurde mit ModLoader 0.7.3, BepInEx 5.4.23.5 und Unity 6000.3.4f1 kompiliert. Elf Tests des Übersetzungskerns bestanden. Reale MyMemory-Anfragen lieferten chinesische, japanische, koreanische und französische Übersetzungen. Die Übersetzung der Oberfläche und Anleitungen wurde in 0.1.6 ergänzt.

**Die Integration im Spiel wurde noch nicht getestet.** Textabdeckung, Layout, japanische und koreanische Schriften und Namen externer Stoff-Mods müssen noch im Spiel geprüft werden. Bei der Entwicklung waren auf diesem Computer keine Inhaltspakete installiert.

Der Patch nutzt übliche Unity-Text-/TextMeshPro-Anzeigewege. Individuell gezeichnete Texte, Text in Bildern, nicht englische Quellen und direkte Änderungen an Handlungsskripten sind nicht garantiert. Handlungsskripte werden nicht geändert. Stoffbegriffe, Farbbezeichnungen oder Grammatik können falsch übersetzt sein und lassen sich manuell korrigieren.

## Quellcode und Build

Plugin-Code: `src/DressmakerLanguages.cs`; Assistent: `assistant/`. Mit eigenem .NET SDK und den Assemblies des Spiels bauen:

```sh
python3 src/build.py --game "/path/to/game" --dotnet "/path/to/dotnet"
```

Unabhängiger Code und selbst verfasste Wörterbücher stehen unter der MIT-Lizenz. Sie gewährt keine Rechte an Spielinhalten oder dem Referenzprojekt.

## Danksagung

Vielen Dank an die Autoren und Teams, deren Arbeit dieses Projekt ermöglicht hat:

- [Cozy Lives (Entwicklung) und Free Lives (Veröffentlichung)](https://store.steampowered.com/app/4019220/Dressmaker/) — Danke für Dressmaker, in dem Spieler Kleidung selbst entwerfen, zuschneiden und nähen können.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Danke für den Loader und die Unterstützung eigener Inhalte, mit denen die Community Stoffe und Accessoires erstellen kann.
- [SallyHCA — Automatisches chinesisches Übersetzungswerkzeug](https://www.nexusmods.com/dressmaker/mods/339) — Danke für den veröffentlichten Ansatz zur Übersetzung der Mod-Verwaltung und Inhaltsnamen. Das Werkzeug und die öffentliche Beschreibung haben den Übersetzungsablauf dieses Projekts inspiriert.

Dies ist eine unabhängige Implementierung. Die Danksagung bedeutet keine Unterstützung durch die Autoren. Ihre Programme, Wörterbücher, Spielressourcen und Modelle werden nicht mitgeliefert.


## Paket zur manuellen Installation herunterladen

Exportiert Plugin, Wörterbuch und gespeicherte Übersetzungen für die gespeicherte Spielsprache, ohne in den Spielordner zu schreiben. Nach neuen Übersetzungen oder einem Sprachwechsel erneut exportieren. Die ZIP enthält Anleitungen in sieben Sprachen. [Paket zur manuellen Installation herunterladen](manual-de.md).


## Übersetzungsfortschritt

Aktualisierung jede Sekunde. Der Fortschritt zählt bearbeitete Einträge; beibehaltene Originale und Fehler gelten nicht als erfolgreiche Übersetzungen. Die Liste aktualisiert sich und behält ungespeicherte Änderungen.

## Google-Web und gespeicherte Übersetzungen

Google-Webanfragen benötigen keinen Schlüssel. Die Verfügbarkeit hängt vom Netzwerk ab; Änderungen oder Beschränkungen können Fehler verursachen. Anfragen erfolgen im Abstand von mindestens 3 Sekunden.

Beispiel: Heute (UTC): 4,498 / 4,500 Bytes genutzt · 2 übrig. Dies ist das lokale Budget; ein höherer Wert erhöht nicht das Kontingent des Dienstes.

Übersetzungen werden lokal gespeichert und sind offline wiederverwendbar. Bei Updates den Ordner data behalten; Sprachcaches und manuelle Korrekturen bleiben erhalten.

## Wörterbuchsuche und Filter (0.1.4)

Die Suche erfasst Original und gespeicherte Übersetzung. Ergebnisse erscheinen beim Tippen oder mit Enter. Die Liste vereint erfasste Texte, Wörterbuch und Cache der aktuellen Zielsprache, mit einer Zeile je Original.

- **Status**: unübersetzt, übersetzt oder Original beibehalten. Die Anzahl basiert auf den tatsächlich verwendeten gespeicherten Werten; ungespeicherte Änderungen zählen nicht als erfolgreiche Übersetzungen.
- **Kanal**: Wörterbuch, kombinierte Begriffe, manuelle Korrektur, Offline-Modell, Google, Bing, MyMemory oder LibreTranslate. Angezeigt wird der tatsächlich verwendete Kanal, etwa Wörterbuch, wenn es eine ältere Maschinenübersetzung ersetzt.
- **Quelle**: alle Einträge, erfasste Texte, Spielanzeigetexte, Mod-Inhalte, Manager-Kandidaten oder nur Wörterbuch/Cache. „Unübersetzt“ + „Spielanzeigetexte“ zeigt sichtbare fehlende Übersetzungen.
- **Sortierung und Seiten**: Original auf-/absteigend, zuletzt gespeichert oder Spielanzeigetexte zuerst; 25, 50 oder 100 Zeilen pro Seite und direkte Seitenwahl. Leere Ergebnisse zeigen einen Hinweis; Filter lassen sich zurücksetzen.

Filter und Seitenwechsel behalten ungespeicherte Änderungen bei und zeigen ihre Anzahl. Jede Zeile vor dem Schließen oder Neuladen speichern: Ungespeicherte Entwürfe gehen beim Neuladen verloren. Gespeicherte Zeilen können aus dem aktuellen Filter verschwinden. Suche und Filter kontaktieren keine Übersetzungsdienste und verbrauchen kein Übersetzungsbudget.

Filter gelten nur für die Liste; die Übersetzung fehlender Texte verarbeitet die erfasste Warteschlange.

Die Anzahl unterscheidet Spielanzeigetexte, Mod-Inhalte, Manager-Kandidaten und reine Wörterbuch/Cache-Einträge. Programm-Scans erfassen auch interne Formate, Fehler und ungenutzte Texte; Kandidaten sind keine Anzahl sichtbarer Übersetzungslücken. Automatisch werden angezeigte Texte und Mod-Inhalte verarbeitet. Unübersetzt + Spielanzeigetexte prüft erfasste sichtbare Texte; noch nicht besuchte Ansichten im Spiel öffnen, um sie zu erfassen.

Bei Dienstausfall pausiert der Stapel; der Rest bleibt unbearbeitet. Nach der Wartezeit werden unerledigte Aufgaben mit derselben Sprache und Auswahl erneut versucht, einschließlich manuell gestarteter Kandidaten. Erneutes Klicken umgeht die Pause nicht und setzt den Fortschritt nicht zurück. Eine andere Zielsprache oder ein anderer Spielordner beendet die alte Aufgabe. Ein Dienstwechsel behält den Umfang bei und setzt offene Einträge fort. Nur erfolgreich gespeicherte Übersetzungen senken die Anzahl.

Google entfernt Rand-Leerzeichen: Jetzt wird der Textkörper gesendet, vollständig geprüft und die Leerzeichen werden wiederhergestellt. Gültige Antworten werden dadurch nicht mehr abgewiesen; Tags, Variablen und Vollständigkeit bleiben geschützt.


Wechseln und fortsetzen (0.1.6)

Fehlgeschlagene und offene Einträge erneut versuchen, ohne gespeicherte Übersetzungen zu verlieren. Ein Dienstwechsel in den Einstellungen setzt ebenfalls den ursprünglichen Umfang fort. Eine laufende Anfrage kann etwa 15 Sekunden benötigen. Wartezeit und Tagesbudget desselben Dienstes gelten weiterhin.
