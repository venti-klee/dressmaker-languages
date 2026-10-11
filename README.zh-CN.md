# 针影裁梦 · 多语言 Mod 助手

[简体中文](README.zh-CN.md) · [English](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

适用于 macOS 的独立翻译补丁，翻译 Yuuma ModLoader 界面和 Mod 的英文显示文字。**0.1.3 为早期版本，游戏内集成尚未实测。**

## 能做什么

- 游戏翻译与助手界面分别选择中、英、日、韩、法、德、西七种语言。
- 内置词典、人工译文和缓存可离线使用；可选下载 Argos 模型，补译词典外的句子。
- 可选择免密钥 MyMemory、必应网页接口（实验性）或可用的 LibreTranslate 实例。
- 新安装的 Mod 可通过扫描常见 JSON 显示字段加入词典；游戏中实际显示的英文也会加入补译队列。
- 成功译文按语言缓存，人工修正优先；保护变量与富文本标签。

## 普通玩家开始使用

1. 先安装 [Yuuma ModLoader 的 Mac 版](https://www.nexusmods.com/dressmaker/mods/1?tab=files)。
2. 下载仓库 Releases 中的 **Dressmaker-Languages-Mac-0.1.3.zip**，解压整个目录。需要 Python 3.9 或更新版本。
3. 双击 `Start.command` 或 `针影裁梦多语言助手.app`。
4. 选择助手界面语言，确认游戏目录及游戏目标语言，保存设置，然后安装补丁并重启游戏。
5. 新装 Mod 后点扫描，保持助手运行，补译后可手动修正。

完整步骤、离线模型、卸载及数据位置见 [中文使用说明](docs/zh-CN.md)。GitHub 的“Download ZIP”是源码快照，不包含编译好的游戏插件和 `.app`；普通玩家请使用 Release 安装包。

## 覆盖与验证

扫描支持 `name`、`displayName`、`display_name`、`description`、`tooltip`、`title` 等常见 JSON 字段。运行时接入 Unity Text / TextMeshPro，范围限于 ModLoader 界面或已扫描名称。自绘界面、图片文字、特殊二进制内容及非英语源文本不保证覆盖。本工具不会安装新的布料内容，也不提供完整游戏本体本地化。

插件针对 ModLoader 0.7.3 / BepInEx 5.4.23.5 / Unity 6000.3.4f1 编译，45 项自动测试已通过。本机网页语言切换已检查；必应及 MyMemory 已取得实际译文，但免费网页接口可能受网络、服务限制或页面变化影响。第三方布料包名称、游戏内布局和字体仍需验证。

联网补译会把未命中的英文显示文字发送到所选服务。所有翻译请求至少间隔 3 秒，每日默认预算为 4,500 UTF-8 字节；失败保留原文。备用 MyMemory 默认关闭，开启后两次尝试分别计入预算。离线词典与已有缓存不受联网失败影响。

## 开发与贡献

源码在 `src/` 和 `assistant/`，基础助手仅使用 Python 标准库。运行测试：

```sh
python3 -m unittest discover -s tests -v
```

编译游戏插件需要自己安装的游戏、ModLoader 程序集及 .NET SDK；参见完整说明。助手版本为 0.1.3，游戏插件未改动，内部版本仍为 0.1.0。GitHub Actions 自动检查已启用，结果可在仓库 Actions 页面查看。

欢迎通过 Issue / Pull Request 反馈术语、字体和兼容问题。请附游戏、系统和 ModLoader 版本，以及可公开的示例原文。修改界面文案时同步更新七份语言表和说明；不要提交存档、私人 Mod 文件或游戏资产。

## 发布到你的 GitHub

1. 在 GitHub 新建空仓库，选择 **Public**。不要另行生成 README 或许可证；此包已提供。
2. 解压 **Dressmaker-Languages-GitHub-0.1.3.zip**，上传解压目录内的内容，让 `README.md` 位于仓库根目录。包含 `.github/`、`.gitignore` 和 `.gitattributes` 等隐藏项；Finder 可用 `Command + Shift + .` 显示它们。用 Git 上传会保留启动脚本的可执行权限。
3. 在 Releases 创建 `v0.1.3`，附上 Mac 安装包。源码包用于仓库，Mac 包用于玩家下载，两者分别上传。
4. 发布前在你自己的游戏里检查补丁，并将验证结果更新到说明。此包已排除本机数据、路径和令牌，未包含任何 Git 历史。

上传的准确文件清单见 `UPLOAD-MANIFEST.json`。发布方法参见下方 GitHub 官方文档。

GitHub 官方说明: [Create repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) · [Create Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

## 来源与许可

根据 [SallyHCA 工具的公开功能](https://www.nexusmods.com/dressmaker/mods/339)独立实现，未复制其代码、词典和资产。独立代码及手工词典使用 [MIT 许可证](LICENSE)；不授权游戏或参考项目的资产。项目与游戏、Nexus Mods、微软及 Argos 无官方关联。

## 致谢

感谢以下作者和团队，让这个补丁有了创作与使用的基础：

- [Cozy Lives（开发）与 Free Lives（发行）](https://store.steampowered.com/app/4019220/Dressmaker/) — 感谢你们制作和带来《针影裁梦》，让玩家能够亲手设计、裁剪与缝制服装。
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — 感谢你提供 ModLoader 和自定义内容支持，让社区可以制作更多布料与配饰。
- [SallyHCA — 全自动中文汉化工具](https://www.nexusmods.com/dressmaker/mods/339) — 感谢你分享 Mod 管理器与内容名称汉化的思路。你发布的工具及公开说明启发了本项目的翻译流程。

本项目为独立实现；致谢不代表原作者为本项目背书。没有随包分发上述作者的程序、词典、游戏资产或模型。


## 下载手动安装包

按已保存的游戏语言，导出插件、词典和已有译文，无需写入游戏目录。新译文或语言变化后请重新导出；压缩包内有七种语言的安装说明。 [下载手动安装包](docs/manual-zh-CN.md).


## 补译进度

每秒更新。进度表示本轮已处理数量；保留原文和失败不算翻译成功。列表会自动更新，并保留尚未保存的修改。

## Google 网页与译文保存

Google 网页请求无需密钥；能否使用取决于当前网络，网页变化或限流可能导致失败。每次请求至少间隔 3 秒。

示例：今日（UTC）已用 4,498 / 4,500 字节 · 剩余 2 字节。这是本地预算，调高不会增加远端服务的额度。

译文自动保存在本机，可以离线复用。更新助手请保留 data 文件夹；各语言缓存与人工修正会保留。
