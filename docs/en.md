# Dressmaker Language Assistant 0.1.5

[简体中文](zh-CN.md) · **English** · [日本語](ja.md) · [한국어](ko.md) · [Français](fr.md) · [Deutsch](de.md) · [Español](es.md)

An independent Mac companion and game patch for translating the Yuuma ModLoader interface and mod item display names. It follows the public feature description of [SallyHCA’s tool](https://www.nexusmods.com/dressmaker/mods/339) and [its project](https://github.com/Sally-4869/dressmaker-mods-cn). No code, dictionaries, or assets from that project are included.

GitHub Download ZIP contains source without the compiled plugin or `.app`. Players should use the Mac Release archive; source users must build the plugin as described below. Project and publishing instructions: [README](../README.md).

## Installation

1. Install the [Mac version of Yuuma ModLoader](https://www.nexusmods.com/dressmaker/mods/1?tab=files) first. This patch was compiled against the locally installed version 0.7.3.
2. Extract the complete package into a writable folder. Python 3.9 or later is required. The basic assistant needs no third-party Python packages or .NET runtime.
3. Double-click `Start.command` or `针影裁梦多语言助手.app`. A local browser page opens. Keep its command window open while using the assistant.
4. Set **Assistant language** at the top of the page. It changes all interface messages and the guide link immediately, remembers the choice in this browser, and does not change the game translation language. The initial choice follows your browser language, falling back to English.
5. Check the game folder, choose **Game translation language**, and click **Save settings**. The default game target is Simplified Chinese.
6. Click **Install / update the game patch**. Only `BepInEx/plugins/DressmakerLanguages/` and `BepInEx/config/DressmakerLanguages/` are created or updated.
7. Save your progress and restart the game normally. Open Mod Manager or Mod Settings to check the result. Later dictionary and language changes usually refresh collected text within about 2 seconds.
8. After installing new mods, click **Scan mods and the manager**. The patch also collects unknown English text shown in the game.

For manual installation, copy the included `BepInEx/plugins/DressmakerLanguages/` folder to the corresponding game location, then use the assistant’s install button to generate the configuration. Windows `.exe` assistants and Vortex are not needed.

## Language coverage

The assistant interface and these Markdown guides support Chinese, English, Japanese, Korean, French, German, and Spanish. Interface language and game translation target are separate.

The game dictionaries contain 148 common terms each for Chinese, Japanese, Korean, and French, and 14 each for German and Spanish. Chinese and Japanese also import the official translation tables from your own game installation. This computer produced 5,157 Chinese dictionary entries; that number depends on the installed game. Official game translations are generated locally and are not distributed in the archive. English restores the original text.

Caches are separate for every target language. This patch translates mod display text; it does not provide a complete Korean, French, or other new localization of the base game.

## Offline and online translation

Manual corrections have the highest priority. Other entries use: **dictionary → cached translation → fully recognized term combinations → installed Argos offline model → free online service**.

Dictionaries and saved translations work offline immediately. A combined name is translated only if every word is recognized. Without a model or online service, unfamiliar text remains in English and stays in the pending list.

For unfamiliar sentences offline, select a game target and click **Download this language’s offline model**. The first setup downloads an isolated Python environment and a model, so it needs internet access and may take time. When it finishes, quit and reopen the assistant. Disable online translation and save settings to work entirely offline. Models must be installed separately for each target, depend on the current Argos model index, and are not included in the archive. The model installation flow has not yet been tested end to end.

The default online resource is MyMemory’s public query API, without an API key. Service quotas apply. The assistant adds a conservative daily budget of 4,500 UTF-8 bytes, request spacing, and a failure cooldown. Each free request supports at most 500 bytes; use an offline model or a manual translation for longer entries. You may supply a usable LibreTranslate HTTPS instance, but its availability and pricing are not guaranteed.

Online mode sends only English display text without a local translation to the selected provider, not save files or mod packages. Successful translations are cached. Connection failures, quotas, or invalid responses leave the original text intact. No impersonation, payment bypass, or CAPTCHA bypass is implemented.

## Free translation providers

Choose a translation service and click **Save settings**.

- **MyMemory**: the default public API, without a key. Provider quotas apply.
- **Bing web adapter (experimental)**: no key is needed. It obtains a temporary session from the public translation page and requests translation within that session. This is not a stable official developer API; page, session, or service changes may break it.
- **LibreTranslate**: provide an HTTPS instance you can use. Its cost and account requirements depend on the instance; this adapter currently supports instances that do not require a key.

**Use MyMemory if the selected service is unavailable** is off by default. It makes one fallback attempt for network or service failures, never for an exceeded budget, oversized text, damaged formatting, or an empty instance address. The same text may be sent to both providers; each attempt counts toward the daily text budget. All translation requests are spaced at least 3 seconds apart. Repeated failures trigger a 5-minute cooldown; dictionaries and cached translations stay available offline.

The Bing session stays in memory. No login, account storage, proxy rotation, or CAPTCHA bypass is used. Successful results are cached separately for each game target; manual corrections retain priority.

Tests cover session parsing, Chinese language mapping, invalid responses, offline cache, fallback, and budgets. All 66 automated tests passed. Bing returned live Chinese, Japanese, Korean, French, German, and Spanish translations. Offline cache reuse and preservation of `{0}` were also checked. Connection errors and timeouts occurred during testing, so the adapter remains experimental.

## Editing and uninstalling

Search the English source text, edit its translation, and click **Save**. Manual corrections override both machine translations and dictionaries for that target. Preserve variables, line breaks, and rich-text tags; malformed translations are rejected. Changing the assistant language preserves unsaved translation drafts.

**Translate missing text** also tries candidate strings from the manager. Automatic mode prioritizes text actually displayed in the game and mod content, rather than spending the quota on unused assembly strings.

Click **Uninstall the patch**, then restart the game. Owned plugin and configuration folders move into `data/backups/`. Translation data stays available. The original loader, mods, item IDs, textures, and save files are not modified by this patch.

## Local files

- `data/translations.sqlite3`: per-language cache and manual corrections.
- `data/settings.json`: game target, online options, and game path.
- `data/model-install.log`: offline model setup log.
- `.venv/` and `models/`: optional model environment and models.
- Game `BepInEx/config/DressmakerLanguages/pending.jsonl`: collected unknown display text.
- Game `BepInEx/LogOutput.log`: search for `Dressmaker Languages` for loading or font issues.

The page listens only on the local computer and protects write operations with a random session token. Quitting the assistant leaves published dictionaries and translations usable by the patch; automatic translation needs the assistant running.

## Verification and limitations

The game plugin compiled against ModLoader 0.7.3, BepInEx 5.4.23.5, and Unity 6000.3.4f1. Eleven translation-core tests passed. MyMemory returned Chinese, Japanese, Korean, and French translations in live requests. Interface and guide localization are additional features of 0.1.5.

**Integration inside the game has not been tested.** Text coverage, layout, Japanese/Korean font rendering, and third-party fabric names still require in-game verification; no content packs were installed on this computer during development.

The patch hooks common Unity Text / TextMeshPro display paths. Custom-drawn text, text inside images, non-English sources, and direct story-script rewriting are not guaranteed. Story files are not modified. Machine translations may get fabric terminology, color modifiers, or grammar wrong; review and correct them when needed.

## Source and build

Plugin source is in `src/DressmakerLanguages.cs`; assistant source is in `assistant/`. Build using your own .NET SDK and game assemblies:

```sh
python3 src/build.py --game "/path/to/game" --dotnet "/path/to/dotnet"
```

Independent code and authored dictionaries use the MIT license. This license grants no rights to game assets or the reference project.

## Acknowledgements

Thank you to the authors and teams whose work made this project possible:

- [Cozy Lives (developer) and Free Lives (publisher)](https://store.steampowered.com/app/4019220/Dressmaker/) — Thank you for creating and bringing us Dressmaker, where players can design, cut, and sew their own garments.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Thank you for the loader and custom-content support that enable community fabrics and accessories.
- [SallyHCA — Fully Automatic Chinese Localization Tool](https://www.nexusmods.com/dressmaker/mods/339) — Thank you for sharing the approach to translating the mod manager and content names. Your tool and public description inspired this project’s translation workflow.

This is an independent implementation; acknowledgement does not imply endorsement. Their programs, dictionaries, game assets, and models are not redistributed in this package.


## Download manual installation package

Export the plugin, dictionary and saved translations for the saved game language without writing to the game folder. Export again after translating or changing language. The ZIP includes instructions in seven languages. [Download manual installation package](manual-en.md).


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
