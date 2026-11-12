# Mercenaries 2: World in Flames 中文汉化补丁（雇佣兵 2：战火世界）

[![状态](https://img.shields.io/badge/status-v0.5%20beta-yellow.svg)](#汉化进度)
[![游戏](https://img.shields.io/badge/game-Mercenaries%202-orange.svg)](https://en.wikipedia.org/wiki/Mercenaries_2:_World_in_Flames)
[![平台](https://img.shields.io/badge/platform-Windows%20XP%2B-lightgrey.svg)](#兼容性)
[![许可](https://img.shields.io/badge/license-see%20LICENSE-green.svg)](LICENSE)

> **A Chinese (Simplified) localization patch for Mercenaries 2: World in Flames (2008, Pandemic Studios / EA), PC version.**
> 本项目是《雇佣兵 2：战火世界》（Mercenaries 2: World in Flames）的**简体中文汉化补丁**，覆盖界面、菜单、HUD、字幕、任务文本；不含游戏本体。

> **中文名称**：雇佣兵 2：战火世界 / 雇佣兵2 / 雇佣兵2：战火纪元
> **英文名称**：Mercenaries 2: World in Flames
> **搜索关键词**：Mercenaries 2: World in Flames 中文汉化补丁、雇佣兵2：战火纪元中文汉化补丁、雇佣兵 2 战火世界汉化
> **开发**：Pandemic Studios（2008）　**发行**：Electronic Arts

> 这是 2008 年 Pandemic Studios 的开放世界动作游戏，PC 版只有英文。
> 本项目为它做完整汉化：界面、菜单、HUD、字幕、任务文本。
> 补丁基于 **PC 英文版 v1.0（cracked）** 制作，不含游戏本体。

2008 年的委内瑞拉，玩家扮演雇佣兵，在政变、石油财团与各方武装的混战里接单、炸桥、抢油轮。游戏以"能炸的一切都能炸"的物理破坏和庞大的开放地图闻名。原版全程英文配音与英文界面，本补丁覆盖**文本**部分（界面/菜单/HUD/字幕/任务），配音保持原版。

** 补丁不包含游戏本体。

- 目标版本：**Mercenaries 2 PC v1.0（cracked）**，`Mercenaries2.exe` 53,482,288 字节
  sha256 `958eb22776067c2dbb7d684e472c5045d419ec0ecfb49bfea7d23fcf4a83f115`
- 补丁形态：`data/*-patch.wad`，按 **asset hash** 覆盖原 WAD 资源，不改原版 WAD
- 汉化文本：`translate/zh_full.tsv`，18,299 条中 17,651 条中文（96.5%）

---

## 目录

- [汉化进度](#汉化进度)
- [汉化范围](#汉化范围)
- [技术说明](#技术说明中文是怎么进到-pandemic-的-wad-里的)
- [逆向研究与致谢](#逆向研究与致谢)
- [安装](#安装)
- [兼容性](#兼容性)
- [已知问题](#已知问题)
- [仓库结构](#仓库结构)
- [English](#english)
- [授权](#授权)
- [免责声明](#免责声明)

---

## 汉化进度

> 当前为 **v0.5 beta**：核心文本已全量翻译，大部分界面已中文，PDA 等少数界面仍在攻克。

| 区域 | 字体/载体 | 状态 |
|---|---|---|
| 主菜单按钮（继续/新游戏/选项/退出…） | 预渲染 DXT5 纹理 | ✅ 中文 |
| 主菜单 / 设置菜单文字 | `fonts_enext`（GFx 字体） | ✅ 中文 |
| 主菜单 6 条描述 | 回收码位方案 | ✅ 中文 |
| HUD（字幕/弹药/任务提示） | `english_20` / `english_18` | ✅ 中文 |
| 游戏内长文本（对话/任务） | `english_20/18`、`fonts_enext` | ✅ 中文 |
| ESC 暂停菜单 | GFx（`pause_menu.swf`） | ⚠️ 5/6 行中文，第 2 行 + 底部说明仍方块 |
| PDA（MAP / STOCKPILE / INFO） | GFx 内置字体 | ❌ 方块（未解决） |
| PDA 顶栏 MAP/STOCKPILE/INFO | 纹理 `pda_titles` | ❌ 英文（待重画） |

---

## 效果截图

截图放在 `docs/screenshots/`，对应上表的几个区域：

| 界面 | 截图文件 | 说明 |
|---|---|---|
| 主菜单 | `docs/screenshots/mainmenu.png` | 按钮与 6 条描述均为中文 |
| 游戏内 HUD | `docs/screenshots/hud.png` | 字幕 / 弹药 / 任务提示 |
| ESC 暂停菜单 | `docs/screenshots/pausemenu.png` | 5/6 行中文 |
| PDA | `docs/screenshots/pda.png` | 仍是方块，作为待解决项留档 |

> 截图待补，欢迎 PR。

---

## 汉化范围

### 已汉化

| 载体 | 内容 | 数量 |
|---|---|---|
| `vz.wad` / `shell.wad` 的 `english_P` stringdb | 全部游戏文本（对话、任务、UI） | 17,651 / 18,299 条（96.5%） |
| `fonts_enext`（GFx 语言字体） | 4,070 字形 / 3,584 个汉字 / 2048×2048 图集 | 1 套 |
| `english_20` / `english_18`（UCFX 字体） | 4,134 字符 / 2048×2048 图集 | 2 套 |
| 主菜单按钮纹理 | 6 按钮 × 2 状态 | 1 张 |
| 主菜单描述 | 回收码位 + 图集重画 | 6 条 |

### 有意未汉化

| 项 | 原因 |
|---|---|
| 游戏内语音/配音 | 原版语音保留（汉化只覆盖文本） |
| 街道招牌、广告牌 | 属于 2008 年委内瑞拉街景氛围，汉化会破坏原作设计 |
| 部分专有名词（人名牌、武器型号） | 保持英文原名，避免与贴图/字幕对不上 |

### 补丁改了什么

| 文件 | 作用 |
|---|---|
| `data/loading-patch.wad` | `fonts_enext` 字体 + 图集 |
| `data/shell-patch.wad` | shell 界面 `english_P` + `_shell_*` 字体 + resident |
| `data/vz-patch.wad` | 游戏内 `english_P`（17,603 条译文）+ 语言字体 |
| `data/English-patch.wad` | 主菜单按钮中文纹理 |

---

## 技术说明：中文是怎么进到 Pandemic 的 WAD 里的

> 完整细节见 [TECHNICAL.md](TECHNICAL.md)。这里只讲结论。

### 1. FFCS v2 WAD

游戏资源都在 `data/*.wad`（FFCS v2 容器）。补丁机制是**按 asset hash 覆盖**，不是按文件路径——这也是最容易踩的坑：两个补丁里同名资源会互相覆盖（详见 TECHNICAL.md 的「hash 冲突」一节）。

### 2. 文本层：stringdb

每份 `english_P` 是一个 stringdb：`INFO/KEYS/STRS` 三段，KEYS = `(u32 hash, u32 byte_offset)`，STRS = UTF-16LE 堆。汉化时**保留原堆、追加新文本并重指向**，未改动的条目字节级不变。

### 3. 字体层：两套完全不同的字体

| 字体 | 形态 | 用途 |
|---|---|---|
| `english_20/18` | UCFX(INFO/CHAR/MTRL) | HUD/字幕 |
| `fonts_enext` | CFX（zlib 压缩的 GFx 字体记录 + 图集） | 菜单/描述 |
| `gfxfontlib` | GFx 纹理字体（`gfxfontlib.swf` 内置） | 暂停菜单/PDA |

**关键限制**：GFx 的 FontTextureInfo 只读第一个 tex 子资源、图集必须单页（512×256 或 2048×2048 都行，但 `pages` 必须是 1）。

### 4. 未解决的部分：GFx 内置字体

暂停菜单/PDA 是 GFx 电影（`pause_menu.swf` / PDA 界面），通过 `ImportAssets2` 导入 `_normal_Font`（来自 `gfxfontlib.swf`）。这个字体库**不在任何 WAD 的路径表里**，是引擎内置的；改 WAD 图集、改系统字体替换、hook GDI 都验证无效（详见 TECHNICAL.md 的「失败方案记录」）。

---

## 逆向研究与致谢

本项目大量依赖 **Mercenaries-Fan-Build** 社区的逆向成果，特别感谢：

| 项目 | 用途 |
|---|---|
| [notes-on-the-released-game](https://github.com/Mercenaries-Fan-Build/notes-on-the-released-game) | WAD/资源/引擎逆向笔记；本项目的 WAD 结构、GFx 字体链路、Lua UI 源码（`dlc01_pausescreen.lua`、`dlc01_mrxguipda.lua`）都参考自这里 |
| [mercs2-wad-simulator](https://github.com/Mercenaries-Fan-Build/mercs2-wad-simulator) | Rust 写的 WAD 校验器，可在进游戏前验证 patch 结构 |
| [pmc-blackbox](https://github.com/Mercenaries-Fan-Build/pmc-blackbox) | 游戏内日志/黑盒 DLL，用于运行时诊断 |
| [mercs2-languages](https://github.com/Mercenaries-Fan-Build/mercs2-languages) | 语言切换 ASI 插件（`mercs2_language.asi`） |
| [mercs2-securom-bypass](https://github.com/Mercenaries-Fan-Build/mercs2-securom-bypass) | SecuROM 绕过工具 |

如果你也在做这个引擎的汉化/Mod，建议先读他们的 `docs/` —— 格式、地址、工具链都很完整。

---

## 安装

1. 确认游戏是 **PC v1.0**（`Mercenaries2.exe` 53,482,288 字节）；
2. 备份 `data/` 目录；
3. 把本仓库 `data/` 下的 `*-patch.wad` 复制到游戏的 `data/`；
4. 启动游戏。补丁随游戏加载，无需安装器。

> 不要直接改原版 WAD（`vz.wad`、`shell.wad` 等）——FFCS 容器重建会破坏结构导致黑屏。

---

## 兼容性

- Windows XP / 7 / 10 / 11（32 位游戏，需对应的 DirectX 9 运行库）
- 仅支持 **v1.0 cracked**（见 [汉化进度](#汉化进度) 的版本说明）；v1.1 地址不同，不兼容
- 与其它 `data/*-patch.wad` Mod 可能因 asset hash 冲突而互相覆盖，安装前先备份

---

## 已知问题

| 问题 | 影响 | 说明 |
|---|---|---|
| PDA 界面方块 | 中 | PDA 文本用的是 GFx 内置字体，WAD 补丁层改不到，需要改 GFx 电影/引擎 |
| 暂停菜单第 2 行 + 底部说明方块 | 中 | 用字超出 82 槽回收码位方案的上限 |
| 字距不统一 | 轻微 | 汉字复用拉丁字形的 advance，宽度不一；**原版英文同样不统一**，属引擎固有行为 |
| PDA 顶栏 MAP/STOCKPILE/INFO 仍是英文 | 轻微 | 那是 `pda_titles` 纹理，需要重画（待做） |

---

## 仓库结构

```
mercs2-cn/
├── README.md                本文件
├── TECHNICAL.md             技术实现细节（WAD/字体/GFx 逆向、失败方案记录）
├── CHANGELOG.md             版本记录
├── LICENSE                  授权条款
├── data/                    补丁本体（*-patch.wad，放游戏 data/）
├── docs/
│   ├── screenshots/         效果截图
│   └── reverse-notes/       逆向笔记（本次汉化的发现与结论）
├── tools/                   WAD/字体处理脚本（Python）
│   └── ...
└── release-notes/           各版本发布说明
```

**补丁本体较大**（三个 WAD 合计约 10 MB），可以直接放仓库，也可以走 Releases。

### 为什么公开技术细节

这个引擎的汉化不是"把文本换成中文"：WAD 是 FFCS v2 + sges 压缩 + UCFX 容器，字体有三套完全不同的格式，GFx 还有自己的一套字体加载链路。`TECHNICAL.md` 记录了完整过程——包括哪些方案失败、为什么失败，以及 GFx 内置字体这个暂时无解的硬限制。如果以后有人做同引擎的游戏，这些内容可以直接复用。

---

## English

Mercenaries 2: World in Flames (PC, 2008, Pandemic Studios / Electronic Arts) — **Chinese translation patch**.

- Full text translation (dialogue, missions, UI): 17,651 / 18,299 strings (96.5%)
- Menu, HUD, subtitles, objectives in Chinese
- Install: copy `data/*-patch.wad` into the game's `data/` folder
- Only compatible with PC v1.0 (exe 53,482,288 bytes, sha256 `958eb227...`)
- Known issue: PDA text still shows boxes (uses an engine-internal GFx font that cannot be patched at the WAD layer)

This is a fan translation. No game files are included.

---

## 授权

- 本仓库的补丁文件与文档：见 [LICENSE](LICENSE)
- 游戏本体与原始资源版权归 Electronic Arts / Pandemic Studios 所有
- 引用的 Mercenaries-Fan-Build 项目按其各自许可证（多为 MIT）

---

## 免责声明

本项目为**非商业性粉丝汉化**，不包含游戏本体，不提供盗版下载。
使用本补丁前请确保你拥有游戏的合法副本。因使用本补丁造成的任何问题，作者不承担责任。
