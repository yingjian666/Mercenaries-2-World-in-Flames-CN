# 《雇佣兵 2：战火世界》简体中文汉化

[English](README.en.md) | **中文**

> **项目状态：开发中，补丁尚未发布。**
> PC 英文版的汉化补丁（不含游戏本体）。对话 / 字幕 / 任务 / HUD 已中文；**菜单与 PDA 界面受字体硬限制未通过**，所以暂不发布 —— **做完才发，不做半成品**。
> 本仓库公开全部逆向记录，也是与社区同步进度的窗口。

[![状态](https://img.shields.io/badge/status-v0.6.3-yellow.svg)](#一眼看现状)
[![游戏](https://img.shields.io/badge/game-Mercenaries%202-orange.svg)](https://en.wikipedia.org/wiki/Mercenaries_2:_World_in_Flames)
[![平台](https://img.shields.io/badge/platform-Windows%20XP%2B-lightgrey.svg)](#兼容性)

---

## 一眼看现状

| 内容 | 状态 |
|---|---|
| 游戏内对话、字幕 | ✅ **中文** |
| 任务提示、HUD（弹药/血量/提示） | ✅ **中文** |
| 主菜单 6 个按钮 | ✅ 中文（纹理重画） |
| PDA 顶栏（地图/信息/物资/图例） | ✅ 中文（纹理重画） |
| 暂停菜单 | ✅ 52 条菜单项中文（拉丁码位 + 图集复用） |
| **PDA 正文 / 设置 / 弹窗 / 底部状态行** | ⚙️ **已按字体能力回退为英文**（646 条），见下 |

> 一句话：**能撑住中文的地方（对话、字幕、任务、HUD）都是中文**；剩下那批界面**中文会变成方块，所以主动回退成英文**——这是刻意的取舍，不是没做完。

## 为什么菜单/PDA 不能全中文（根因已定位）

游戏里并存**三套字体**，它们的能力完全不同：

| 界面 | 用的字体 | 中文字形 | 结果 |
|---|---|---|---|
| 对话、字幕、HUD | 语言块字体（4,134 字形 + 2048×2048 图集） | 已扩 | ✅ 中文正常 |
| 暂停菜单、PDA 文本 | `fonts_enext`（486 字形，仅 82 个可牺牲拉丁扩展槽） | 只有 82 个 | ⚠️ 超出即方块 |
| 设置页、部分菜单 | `SHELL.gfx` 内嵌 `Times New Roman`（114 码位） | 只有 5–6 个 | ❌ 基本无法中文 |

**方块不是字体损坏，而是「汉字塞进了没有 CJK 字形的字体」**。判定依据：方块个数恒等于汉化后的中文字数（`ON/OFF` 各 1 个方块 = 被译成单字「开/关」；`Status: Offline` → 「状态：离线」；玩家名 4+3 方块 = 「马蒂亚斯·尼尔森」）。

因此要消除方块，只有两条路：**扩字体**（已证明在 `SHELL.gfx` 上会崩）或**把文本退回英文**。本版选择了后者，覆盖 PDA 与设置界面的 646 条文本。

## 已知问题

- **PDA 正文 / 设置页文字是英文**：中文会方块，故回退（本版刻意如此）；
- 字距：个别汉字偏挤（引擎按拉丁宽度排版，固有）；
- 暂停菜单的 52 条中文靠借用拉丁扩展码位实现，若文本里出现 `À Á Â Ý` 这类字符，可能显示成汉字（已知、可接受）；
- 极少数「文字写成纹理」的按钮（主菜单、PDA 页签）只能靠重画纹理，字体改了不生效。

## 阶段性总结（2026-11）

### 已完成

- **全量文本翻译**：17,651 / 18,299 条（96.5%），含人物、派系、地名术语表
- **游戏内 HUD / 字幕 / 任务**：语言块字体扩页，实测无缺字
- **主菜单 6 个按钮、PDA 顶栏**：纹理重画为中文
- **暂停菜单 52 条**：拉丁码位 + `fonts_enext` 图集复用
- **PDA/设置界面 646 条回退英文**：按「英文字面 → hash」和「stringdb 顺序区间」批量定位，方块清零（本版新增）

### 踩过的死路（全部实战验证，供后来者省时间）

| # | 方案 | 结果 |
|---|---|---|
| 1 | 把图集扩到 2048×2048 | 游戏启动即崩（纹理上传 `0xC0000005`） |
| 2 | 改 `SHELL.gfx` 内嵌字体（`DefineFont3`） | 崩（对象 vtable 无效） |
| 3 | 只改图集不改字体（b1c） | 静态校验全通过，运行仍崩 |
| 4 | 运行时替换字体对象（DLL hook） | 不崩，但渲染不认（时序 `g_font=NULL`） |
| 5 | 扩 `fonts_enext` 码位表 | 三次尝试均失败（图集尺寸硬限制） |
| 6 | cjk2（2048 图集 CJK 注入） | 无效，界面仍方块，已回滚 |
| 7 | 系统字体替换（注册表 `FontSubstitutes`） | 无效——不是 GDI 字体 |
| 8 | 新语言 WAD + ASI（Route C） | ✅ **已跑通** —— `qm` 构建 + ASI 挂载 + stringdb 生效（指南 55/56 节） |
| 9 | 用「码位借用」硬塞全部菜单文本 | 上限 82 槽，只能覆盖 52 条 |
| 10 | 复用 index 8 走 `fonts_ru`（691 字形 / 512×512） | ❌ **不控制菜单**，实测菜单仍走 `fonts_enext`（指南 56 节） |

### 需求与供给的最终账目

| 项 | 数字 |
|---|---|
| 全部中文条目 | 16,862 |
| 全部不同汉字 | 2,235 |
| 其中 ≤8 字的短文本（菜单/PDA 类）用字 | **1,537** |
| `fonts_enext` 可牺牲槽（菜单唯一可用） | **82** |

**菜单/PDA 全中文需要 1,537 个槽，可用 82 个——差 19 倍。** 这不是技巧问题，是数量级问题，所以「改 WAD 做全量菜单中文」在物理上不可能。

### 下一步（可选，非承诺）

- 外挂式实时文本替换（不改游戏文件）；
- 或维持现状：对话/字幕/HUD 中文 + 界面英文。

## 安装

> **补丁目前还没发布**（原因见顶部状态）。以下步骤说明本项目的补丁形态，供复现研究使用。

1. **备份**游戏的 `data` 目录（重要）；
2. 把本仓库的 `shell-patch.wad`、`vz-patch.wad`、`loading-patch.wad`、`English-patch.wad` 复制进游戏 `data` 目录；
3. 启动游戏。

**卸载**：把这几个 `*-patch.wad` 删掉即可（原版 WAD 从未被修改）。

> 补丁本体约 17 MB，不放进 Git；完成后走 **Releases** 发布。

## 兼容性

- 目标版本：**Mercenaries 2 PC v1.1**（已去除 SecuROM 的可运行版本），`Mercenaries2.exe` 约 53,482,288 字节
  （文件指纹：`958E…`，完整哈希见发布说明）
- 补丁形态：`data/*-patch.wad`，按 **asset hash** 覆盖，**不改原版 WAD**
- 本补丁不含破解，请自备可运行的游戏版本

## 仓库结构

```
README.md                  本文件
CHANGELOG.md               版本记录
TECHNICAL.md               格式与工具（开发者向）
LICENSE                    许可
docs/reverse-notes/        完整逆向记录（汉化完全指南）
docs/screenshots/          截图（待补）
release-notes/             发布说明
tools/                     构建/推送脚本
data/                      补丁放置处（*.wad 不进 Git，走 Releases）
```

## 致谢

- [notes-on-the-released-game](https://github.com/Mercenaries-Fan-Build/notes-on-the-released-game)（格式文档、逆向语料）
- [mercs2-wad-simulator](https://github.com/Mercenaries-Fan-Build/mercs2-wad-simulator)（WAD 写入器）
- [mercs2-languages](https://github.com/Mercenaries-Fan-Build/mercs2-languages)（语言 ASI）
- [mercs2-securom-bypass](https://github.com/Mercenaries-Fan-Build/mercs2-securom-bypass)（去 SecuROM）

## 许可

见 [LICENSE](LICENSE)。游戏版权归 Pandemic Studios / EA 所有；本补丁仅包含文本与资源改写，**不含游戏本体**。
