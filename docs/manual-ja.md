# Dressmaker Languages の手動インストール

先に [Mac版 Yuuma ModLoader](https://www.nexusmods.com/dressmaker/mods/1?tab=files) を導入してください。このZIPには独立した翻訳パッチのみが含まれ、ローダー、ゲーム、布地Modは含まれません。

1. ゲームを完全に終了します。
2. ZIPを展開します。助手からの出力には**保存済みのゲーム言語**、現在の辞書、キャッシュ、手動修正が含まれます。言語変更は保存してから出力してください。GitHubの基本手動パッケージは簡体字中国語の自作辞書のみです。
3. Steamでゲームを右クリックし「管理 → ローカルファイルを閲覧」を選びます。既に `BepInEx` があるゲームのルートを使用してください。`Dressmaker.app/Contents` には入れません。
4. ZIP内の `BepInEx/plugins/DressmakerLanguages` をゲームの `BepInEx/plugins` にコピーします。
5. ZIP内の `BepInEx/config/DressmakerLanguages` をゲームの `BepInEx/config` にコピーします。`config` がなければ作成します。**この2つの子フォルダーを個別にコピーし、BepInEx全体を置き換えないでください。**
6. 既存の同名フォルダーは別の場所にバックアップしてから、2つの `DressmakerLanguages` のみを置き換えます。他のプラグインやModは残します。
7. ゲームを再起動します。

必要なファイル（`LANG` は `zh-CN`、`ja`、`fr` などの出力言語）：

```text
BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll
BepInEx/config/DressmakerLanguages/runtime.json
BepInEx/config/DressmakerLanguages/known-sources.json
BepInEx/config/DressmakerLanguages/translations.LANG.json
```

Finderで権限の確認が表示されたらmacOSの案内に従います。コピーできない場合はゲームフォルダーの「情報を見る → 共有とアクセス権」で自分のアカウントに「読み／書き」があるか確認してください。全員に権限を付与しないでください。管理された端末では権限のあるアカウントが必要な場合があります。

手動コピーだけでは助手の書き込み権限は変わりません。スキャン、翻訳、ローカル保存は続けられます。権限が直るまでは訳文やゲーム言語を変えるたびに再出力し、ゲームを終了してコピーしてください。ゲームも設定フォルダーに書けない場合、実行時の新語収集が失敗することがありますが、助手でModの一般的なJSON表示項目をスキャンできます。助手を再起動するとプラグインと設定の存在を確認します。

アンインストールはゲーム終了後、この2つの `DressmakerLanguages` のみを移動します。訳文を残すには助手の `data` を保存してください。

ローカル出力には自分のMod名、修正、ゲーム内の既存訳文が含まれる場合があります。公開配布にはプロジェクトのパッケージ処理で作る基本手動パッケージを使用してください。

0.1.3は初期版で、ゲーム内表示とフォントは未検証です。[説明と謝辞](https://github.com/venti-klee/dressmaker-languages)。
