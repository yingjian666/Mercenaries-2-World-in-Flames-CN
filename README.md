# 《雇佣兵 2：战火世界》简体中文汉化

> PC 英文版的汉化补丁（**不含游戏本体**）。游戏内对话、字幕、任务提示已中文；**菜单、暂停、设置、弹窗仍在攻关**。

[![状态](https://img.shields.io/badge/status-v0.5%20beta-yellow.svg)](#一眼看现状)
[![游戏](https://img.shields.io/badge/game-Mercenaries%202-orange.svg)](https://en.wikipedia.org/wiki/Mercenaries_2:_World_in_Flames)
[![平台](https://img.shields.io/badge/platform-Windows%20XP%2B-lightgrey.svg)](#兼容性)

---

## 一眼看现状

| 内容 | 状态 |
|---|---|
| 游戏内对话、字幕 | ✅ **中文** |
| 任务提示、HUD（弹药/血量/提示） | ✅ **中文** |
| 主菜单 6 个按钮 | ✅ 中文（图片） |
| PDA 顶栏（地图/信息/物资/图例） | ✅ 中文（图片） |
| **暂停菜单（ESC）** | ⚠️ **中英混合**（“继续游戏/选项/退出”等已中文，其余仍英文） |
| **设置菜单（OPTIONS）文字** | ⚠️ 部分中文，其余英文 |
| **弹窗按钮（是/否/确定）** | ⚠️ 部分中文 |
| **PDA 正文** | ❌ 英文 / 方块 |

> 一句话：**能玩的部分（对话、字幕、任务、HUD）已经是中文**；**菜单类界面还没完成**。

## 为什么菜单只做了“一部分”（简单说）

菜单文字用的是**游戏内部一个 Flash 电影文件里的字体**（`SHELL.gfx`，在 `shell.wad` 里）：

- 这套字体只有 **114 个字母位**，能腾出来放汉字的只有 **5～6 个**——只够“继续/选项/退出”这类短词；
- 把图片放大到能放更多字，**游戏一启动就崩**；
- 直接改这个电影文件，**游戏也崩**（文件结构、校验值、压缩方式全部核对正确，仍崩）。

所以菜单的完整汉化需要更深层的改造，**目前到此为止**。暂停菜单能显示的中文，是用“借用拉丁字母位 + 重画图片”的方式实现的，覆盖 52 条菜单文本。

## 安装

1. **备份**游戏的 `data` 目录（重要）；
2. 把本仓库的 `shell-patch.wad`、`vz-patch.wad`、`loading-patch.wad`、`English-patch.wad` 复制进游戏 `data` 目录；
3. 启动游戏。

**卸载**：把这几个 `*-patch.wad` 删掉即可（原版 WAD 从未被修改）。

> 补丁本体约 17 MB，不放进 Git，走 **Releases** 下载。

## 兼容性

- 目标版本：**Mercenaries 2 PC v1.1**（已去除 SecuROM 的可运行版本），`Mercenaries2.exe` 约 53,482,288 字节
  （文件指纹：`958E…`，完整哈希见发布说明）
- 补丁形态：`data/*-patch.wad`，按 **asset hash** 覆盖，**不改原版 WAD**
- 本补丁不含破解，请自备可运行的游戏版本

## 已知问题

- 菜单 / 暂停 / 设置 / 弹窗 / PDA 正文：英文或方块（见上）；
- 字距：个别汉字偏挤（引擎按拉丁宽度排版，固有）；
- 少数符号（`<` `>` `#` `$` 等）被临时借用来显示汉字，极少数文本里这些符号会显示成汉字（已知、可接受）。

## 阶段性总结（2026-11）

### 已完成

- **全量文本翻译**：17,651 / 18,299 条（96.5%），含人物、派系、地名术语表
- **游戏内 HUD / 字幕 / 任务**：语言块字体扩页（4,134 字形 + 2048×2048 图集），实测无缺字
- **主菜单 6 个按钮、PDA 顶栏**：纹理重画为中文
- **暂停菜单部分文本**：1,000+ 条菜单 key 中已改 52 条（拉丁码位 + `fonts_enext` 图集复用）

### 未完成（技术限制已确认）

- **菜单 / 暂停 / 设置 / 弹窗 / PDA 正文**仍是英文或方块。原因：
  - 这些文字用 `SHELL.gfx`（Flash 电影）内嵌字体（Time New Roman，114 字形）；
  - 扩图集 → 崩（`0xC0000005`，纹理上传）；
  - 改电影内嵌字体 → 崩（对象 vtable 无效）；
  - 运行时替换字体对象 → 渲染不认。
- 结论：**WAD / 电影层已到极限**，剩余问题需要改引擎或外挂，不属于补丁层范围。

### 尝试过的方案（均未采用）

| 方案 | 结果 |
|---|---|
| 扩图集到 2048 | 崩 |
| 改电影内嵌字体 | 崩 |
| 运行时改字体对象 | 不崩，渲染不认 |
| 新语言 WAD + ASI | 编译成功，未验证 |
| 像素复用（拉丁槽位） | 部分可用，字量有限 |

### 下一步（可选，非承诺）

- 外挂式实时文本替换（不修改游戏文件）；
- 或接受当前状态，仅维护文本与纹理补丁。

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
