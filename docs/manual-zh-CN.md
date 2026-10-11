# 手动安装针影裁梦多语言补丁

需要先安装 [Yuuma ModLoader 的 Mac 版](https://www.nexusmods.com/dressmaker/mods/1?tab=files)。本包只包含独立补丁，不包含 ModLoader、游戏或布料 Mod。

1. 完全退出游戏。
2. 解压手动安装 ZIP。网页的“下载手动安装包”会包含**已保存的游戏目标语言**、当前词典、缓存和人工译文。修改语言后先保存设置再导出。GitHub 的独立手动包默认是简体中文，只包含本项目手写的基础词典。
3. 在 Steam 中右键游戏，选择“管理 → 浏览本地文件”，找到游戏根目录，也就是已经有 `BepInEx` 文件夹的那一层。不要放进 `Dressmaker.app/Contents`。
4. 进入解压包的 `BepInEx/plugins`，把其中的 `DressmakerLanguages` 文件夹复制到游戏的 `BepInEx/plugins`。
5. 进入解压包的 `BepInEx/config`，把其中的 `DressmakerLanguages` 文件夹复制到游戏的 `BepInEx/config`。没有 `config` 时先创建这个文件夹。**逐个复制这两个子文件夹，不要替换整个 BepInEx 文件夹。**
6. 已有同名补丁文件夹时，先将它们复制到别处备份，再用新包替换这两个 `DressmakerLanguages` 文件夹。不要删除其他插件或 Mod。
7. 重新启动游戏。

正确结构如下，`LANG` 表示导出的游戏语言，例如 `zh-CN`、`ja` 或 `fr`：

```text
游戏根目录/
  BepInEx/
    plugins/DressmakerLanguages/DressmakerLanguages.dll
    config/DressmakerLanguages/runtime.json
    config/DressmakerLanguages/known-sources.json
    config/DressmakerLanguages/translations.LANG.json
```

如果 Finder 提示权限不足，可以按 macOS 提示授权。若仍无法复制，在游戏根目录选择“显示简介 → 共享与权限”，检查自己的账户是否有“读与写”权限；只调整自己的游戏目录，不要给所有人开放权限。如果系统限制来自设备管理，请由有权限的账户安装。

手动复制并不会解决助手的写入权限。保持助手运行仍可扫描、补译和保存本地缓存；权限尚未恢复时，新译文或游戏语言变更后，要重新下载手动包、退出游戏并复制更新。游戏也无法写配置目录时，运行时新词收集可能失败；仍可用助手扫描 Mod 的常见 JSON 显示字段。首次重启助手后会检查插件和配置是否齐全。

卸载：退出游戏后只移走上述两个 `DressmakerLanguages` 文件夹。保留助手自己的 `data` 文件夹可保留译文。

本地导出的包可能包含你自己的 Mod 名称、人工译文和本机游戏已有译文，请自行保存；公开发布使用项目打包脚本生成的基础手动包。

0.1.3 为早期版本，实际游戏内显示与字体尚未验证。完整说明及作者致谢见 [GitHub 项目](https://github.com/venti-klee/dressmaker-languages)。
