# Dressmaker · Sprachassistent für Mods

[简体中文](README.zh-CN.md) · [English](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Ein unabhängiges macOS-Werkzeug zur Übersetzung der Yuuma-ModLoader-Oberfläche und englischer Mod-Texte. **0.1.4 ist eine frühe Version; die Integration im Spiel wurde noch nicht getestet.**

## Funktionen

- Getrennte Sprachwahl für Spiel und Assistent: Chinesisch, Englisch, Japanisch, Koreanisch, Französisch, Deutsch und Spanisch.
- Offline-Wörterbücher, manuelle Korrekturen und Cache; optionale Argos-Modelle für unbekannte Sätze.
- MyMemory ohne Schlüssel, experimentelle Bing-Web-Anbindung oder nutzbare LibreTranslate-Instanz.
- Häufige JSON-Anzeigefelder neuer Mods scannen und im Spiel angezeigtes unbekanntes Englisch sammeln.
- Übersetzungen pro Sprache speichern, manuelle Korrekturen priorisieren und Variablen sowie Tags schützen.

## Für Spieler

1. Installieren Sie [Yuuma ModLoader für Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files).
2. Laden Sie **Dressmaker-Languages-Mac-0.1.4.zip** aus den Releases und entpacken Sie den gesamten Ordner. Python 3.9 oder neuer ist nötig.
3. Öffnen Sie `Start.command` oder `针影裁梦多语言助手.app`.
4. Wählen Sie die Oberflächensprache, prüfen Sie Spielordner und Zielsprache, speichern Sie, installieren Sie das Plugin und starten Sie das Spiel neu.
5. Nach neuen Mods scannen und den Assistenten für Übersetzungen offen lassen. Ergebnisse lassen sich korrigieren.

Details zu Modellen, Deinstallation und Daten stehen in der [deutschen Anleitung](docs/de.md). GitHubs Download ZIP enthält Quellen ohne kompiliertes Plugin oder `.app`. Spieler sollten das Release-Archiv nutzen.

## Umfang und Prüfung

Der Scanner liest JSON-Felder wie `name`, `displayName`, `display_name`, `description`, `tooltip` und `title`. Laufzeit-Hooks betreffen Unity Text / TextMeshPro in der Loader-Oberfläche oder gescannte Namen. Eigene Oberflächen, Bildtext, besondere Binärformate und nicht englische Quellen sind nicht garantiert. Das Werkzeug fügt keine Stoffe hinzu und übersetzt das Basisspiel nicht vollständig in neue Sprachen.

Das Plugin wurde für ModLoader 0.7.3 / BepInEx 5.4.23.5 / Unity 6000.3.4f1 gebaut. Alle 56 automatisierten Tests bestanden. Die lokale Sprachumschaltung wurde geprüft; Bing und MyMemory lieferten reale Übersetzungen. Web-Anbindungen können durch Netzwerk, Limits oder Seitenänderungen ausfallen. Stoffnamen anderer Anbieter, Layout und Schrift im Spiel bleiben zu prüfen.

Online werden unbekannte englische Anzeigetexte an den gewählten Dienst gesendet. Anfragen haben mindestens 3 Sekunden Abstand; das Tagesbudget beträgt standardmäßig 4.500 UTF-8-Bytes. Bei Fehlern bleibt der Originaltext erhalten. Der MyMemory-Ersatz ist zunächst ausgeschaltet; aktiv zählen beide Versuche zum Budget. Wörterbuch und Cache bleiben offline nutzbar.

## Entwicklung und Beiträge

Quellen liegen in `src/` und `assistant/`. Der Basisassistent nutzt nur die Python-Standardbibliothek.

```sh
python3 -m unittest discover -s tests -v
```

Zum Bauen werden eigene Spiel- und Loader-Assemblies sowie ein .NET SDK benötigt. Der Assistent ist 0.1.4; das unveränderte Spielplugin bleibt intern bei 0.1.0. GitHub Actions-Prüfungen sind aktiviert. Ergebnisse stehen auf der Actions-Seite des Repositorys.

Issues und Pull Requests zu Begriffen, Schriften und Kompatibilität sind willkommen. Geben Sie Spiel-, OS- und Loader-Versionen sowie einen öffentlich teilbaren Text an. Aktualisieren Sie bei Textänderungen alle sieben Kataloge und Anleitungen. Keine Spielstände, privaten Mods oder Spielressourcen hochladen.

## Auf GitHub veröffentlichen

1. Erstellen Sie ein leeres **Public**-Repository. README und Lizenz sind vorhanden; keine zusätzlichen erzeugen.
2. Entpacken Sie **Dressmaker-Languages-GitHub-0.1.4.zip** und laden Sie den Inhalt mit `README.md` im Stammverzeichnis hoch. `.github/`, `.gitignore` und `.gitattributes` gehören dazu. Finder zeigt versteckte Dateien mit `Command + Shift + .`. Git erhält die Ausführungsrechte der Startskripte.
3. Erstellen Sie Release `v0.1.4` und hängen Sie das Mac-Archiv an. Quellen gehören ins Repository, das Mac-Paket ist für Spieler.
4. Prüfen Sie das Plugin vor Veröffentlichung im eigenen Spiel und aktualisieren Sie die Ergebnisse. Persönliche Daten, Pfade, Tokens und Git-Verlauf sind ausgeschlossen. 

Die genaue Liste steht in `UPLOAD-MANIFEST.json`. Offizielle GitHub-Anleitungen sind unten verlinkt.

Offizielle GitHub-Anleitungen: [Create repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) · [Create Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

## Quellen und Lizenz

Unabhängig nach den [öffentlich beschriebenen Funktionen von SallyHCAs Werkzeug](https://www.nexusmods.com/dressmaker/mods/339) erstellt, ohne dessen Code, Wörterbücher oder Ressourcen. Eigener Code und erstellte Wörterbücher stehen unter [MIT](LICENSE), ohne Rechte an Spiel- oder Referenzressourcen. Keine Verbindung zum Spiel, Nexus Mods, Microsoft oder Argos.

## Danksagung

Vielen Dank an die Autoren und Teams, deren Arbeit dieses Projekt ermöglicht hat:

- [Cozy Lives (Entwicklung) und Free Lives (Veröffentlichung)](https://store.steampowered.com/app/4019220/Dressmaker/) — Danke für Dressmaker, in dem Spieler Kleidung selbst entwerfen, zuschneiden und nähen können.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Danke für den Loader und die Unterstützung eigener Inhalte, mit denen die Community Stoffe und Accessoires erstellen kann.
- [SallyHCA — Automatisches chinesisches Übersetzungswerkzeug](https://www.nexusmods.com/dressmaker/mods/339) — Danke für den veröffentlichten Ansatz zur Übersetzung der Mod-Verwaltung und Inhaltsnamen. Das Werkzeug und die öffentliche Beschreibung haben den Übersetzungsablauf dieses Projekts inspiriert.

Dies ist eine unabhängige Implementierung. Die Danksagung bedeutet keine Unterstützung durch die Autoren. Ihre Programme, Wörterbücher, Spielressourcen und Modelle werden nicht mitgeliefert.


## Paket zur manuellen Installation herunterladen

Exportiert Plugin, Wörterbuch und gespeicherte Übersetzungen für die gespeicherte Spielsprache, ohne in den Spielordner zu schreiben. Nach neuen Übersetzungen oder einem Sprachwechsel erneut exportieren. Die ZIP enthält Anleitungen in sieben Sprachen. [Paket zur manuellen Installation herunterladen](docs/manual-de.md).


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
