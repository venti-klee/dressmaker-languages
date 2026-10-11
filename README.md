# Dressmaker · Mod Language Assistant

[简体中文](README.zh-CN.md) · [English](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

An independent macOS companion that translates the Yuuma ModLoader interface and English mod display text. **Version 0.1.5 is an early release; integration inside the game has not been tested.**

## Features

- Separate language choices for the game target and assistant UI: Chinese, English, Japanese, Korean, French, German, and Spanish.
- Offline dictionaries, manual corrections, and cached translations; optional Argos models for unfamiliar sentences.
- Keyless MyMemory, an experimental Bing web adapter, or an available LibreTranslate instance.
- Scan common JSON display fields from newly installed mods; collect unknown English displayed in the game.
- Cache successful translations per language, prioritize manual corrections, and protect variables and rich-text tags.

## For players

1. Install [Yuuma ModLoader for Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files).
2. Download **Dressmaker-Languages-Mac-0.1.5.zip** from the repository’s Releases and extract the complete folder. Python 3.9 or later is required.
3. Double-click `Start.command` or `针影裁梦多语言助手.app`.
4. Choose the assistant language, check the game folder and target language, save settings, install the patch, then restart the game.
5. Scan after installing new mods, keep the assistant running for translation, and review or edit the results.

See the [English user guide](docs/en.md) for model setup, uninstalling, and local data. GitHub’s Download ZIP is a source snapshot without the compiled plugin or `.app`; players should use the Release archive.

## Coverage and verification

The scanner recognizes common JSON fields such as `name`, `displayName`, `display_name`, `description`, `tooltip`, and `title`. Runtime hooks cover Unity Text / TextMeshPro in the loader UI or names discovered by scanning. Custom interfaces, image text, special binary content, and non-English sources are not guaranteed. This tool does not add fabric content or a complete new localization of the base game.

The plugin compiled against ModLoader 0.7.3 / BepInEx 5.4.23.5 / Unity 6000.3.4f1, and 66 automated tests passed. Local UI language switching was checked. Bing and MyMemory returned live translations, but free web adapters can fail because of network conditions, service limits, or page changes. Third-party fabric names, in-game layout, and font rendering still need verification.

Online mode sends untranslated English display text to the selected provider. Translation requests are spaced at least 3 seconds apart; the default daily budget is 4,500 UTF-8 bytes. Failures retain the original text. MyMemory fallback is off by default; both attempts count toward the budget when enabled. Dictionaries and existing cache stay available offline.

## Development and contributions

Source is in `src/` and `assistant/`. The basic assistant uses only Python’s standard library. Run tests with:

```sh
python3 -m unittest discover -s tests -v
```

Building the plugin requires your own game and loader assemblies plus a .NET SDK; see the full guide. The assistant is 0.1.5; the unchanged game plugin retains internal version 0.1.0. GitHub Actions checks are enabled; see the repository Actions page for results.

Issues and pull requests for terminology, fonts, and compatibility are welcome. Include game, OS, and loader versions plus a shareable source-text example. Update all seven catalogs and guides when changing UI text. Do not commit saves, private mod files, or game assets.

## Publishing your GitHub repository

1. Create an empty **Public** repository. Do not generate another README or license; both are included here.
2. Extract **Dressmaker-Languages-GitHub-0.1.5.zip** and upload its contents with `README.md` at the repository root. Include hidden `.github/`, `.gitignore`, and `.gitattributes` entries. Finder shows hidden files with `Command + Shift + .`. Uploading through Git preserves executable script permissions.
3. Create a `v0.1.5` Release and attach the Mac archive. The source archive is for repository contents; the Mac archive is for players.
4. Verify the patch in your own game before publishing and update the verification notes. Personal data, paths, tokens, and Git history are excluded from this archive. 

`UPLOAD-MANIFEST.json` lists the exact upload files. GitHub’s official publishing documentation is linked below.

Official GitHub instructions: [Create repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) · [Create Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

## Credits and license

Independently implemented from the public feature description of [SallyHCA’s tool](https://www.nexusmods.com/dressmaker/mods/339); its code, dictionaries, and assets are not included. Original code and authored dictionaries use the [MIT license](LICENSE), which grants no rights to game or reference-project assets. This project is not affiliated with the game, Nexus Mods, Microsoft, or Argos.

## Acknowledgements

Thank you to the authors and teams whose work made this project possible:

- [Cozy Lives (developer) and Free Lives (publisher)](https://store.steampowered.com/app/4019220/Dressmaker/) — Thank you for creating and bringing us Dressmaker, where players can design, cut, and sew their own garments.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Thank you for the loader and custom-content support that enable community fabrics and accessories.
- [SallyHCA — Fully Automatic Chinese Localization Tool](https://www.nexusmods.com/dressmaker/mods/339) — Thank you for sharing the approach to translating the mod manager and content names. Your tool and public description inspired this project’s translation workflow.

This is an independent implementation; acknowledgement does not imply endorsement. Their programs, dictionaries, game assets, and models are not redistributed in this package.


## Download manual installation package

Export the plugin, dictionary and saved translations for the saved game language without writing to the game folder. Export again after translating or changing language. The ZIP includes instructions in seven languages. [Download manual installation package](docs/manual-en.md).


## Translation progress

Updates every second. Progress counts processed entries; unchanged originals and failures are not successful translations. The list updates automatically and preserves unsaved edits.

## Google web and saved translations

Google web requests need no key. Availability depends on your network; page changes or rate limits can cause failures. Requests are spaced at least 3 seconds apart.

Example: Today (UTC): 4,498 / 4,500 bytes used · 2 remaining. This is a local budget; increasing it does not increase the service’s quota.

Translations are saved locally and reusable offline. Keep the data folder when updating; language caches and manual corrections are preserved.

## Dictionary search and filters (0.1.4)

Search matches both the source and saved translation. Results update as you type, or press Enter. The list combines collected text with the current target language’s dictionary and cache, with one row per source.

- **Status**: untranslated, translated, or original retained. Missing counts use effective saved values; unsaved edits do not count as successful translations.
- **Channel**: dictionary, composed terms, manual corrections, offline model, Google, Bing, MyMemory, or LibreTranslate. This shows the channel actually used, so a dictionary overriding an old machine translation is shown as dictionary.
- **Source**: all entries, collected text, game display text, mod content, manager candidates, or dictionary/cache only. Choose “Untranslated” + “Game display text” to focus on visible missing translations.
- **Sorting and pages**: source ascending/descending, recently saved, or game display text first; 25, 50 or 100 rows per page and direct page jumps. Empty results have a hint; “Clear filters” resets the query.

Filters and page changes preserve unsaved edits and show their count. Save each row before closing or reloading the page; unsaved drafts are lost on reload. A saved row may disappear from the current filter. Searching and filtering do not contact translation services or spend the translation budget.

Filters affect the list only; “Translate missing text” still processes the collected queue.

Missing counts now separate game display text, mod content, manager candidates and dictionary/cache-only entries. Program scans can collect internal formats, errors and unused text; candidate counts do not represent visible missing translations. Automatic translation handles displayed text and mod content. Filter Untranslated + Game display text to check collected visible text; unvisited screens still need to be opened in game.

A service failure pauses the batch and leaves the rest unprocessed, not translated or processed. After cooldown, unfinished tasks retry with the same language and scope, including manually started candidates. Clicking again does not bypass cooldown or reset progress. Changed settings cancel the old retry. Missing counts decrease only when translations are successfully saved; “No translation produced” is not completion.

Google boundary-whitespace handling is fixed: send the body, strictly verify its complete source echo, then restore boundary whitespace. Valid replies are no longer rejected merely for trimmed boundaries; tags, variables and body completeness remain protected.
