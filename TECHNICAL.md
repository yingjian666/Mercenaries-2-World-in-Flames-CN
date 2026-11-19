# 技术实现：雇佣兵 2 汉化

> 本文记录汉化过程中确认的格式、地址、方案与失败记录。目标是可复现，而不是只给结论。

## 0. 目标与环境

| 项 | 值 |
|---|---|
| 游戏 | Mercenaries 2: World in Flames（PC） |
| 版本 | v1.1 派生（已去除 SecuROM），`Mercenaries2.exe` 约 53,482,288 B |
| 文件指纹 | `958E…`（短哈希；完整值见发布说明） |
| 补丁形态 | `data/*-patch.wad`（FFCS v2），按 asset hash 覆盖 |
| 基线 | 原始 WAD（`vz.wad` / `shell.wad` / `Loading.wad` / `English.wad`） |

## 1. FFCS v2 WAD

- 头 256 B；chunk 行 `INDX/DATA/CSUM/ASET/PTHS`
- 块数据是 **sges** 压缩；解压后常为 `UCFX` 容器：
  `"UCFX"` + hdr_size + 段表（每段 20 B：tag, rel_off, size, count, zero）+ 数据区，尾部 `CSUM` = JAMCRC。
- **覆盖判据是 asset hash，不是块路径**。两个 patch 里 asset hash 相同的资源会互相覆盖（曾导致 shell 界面乱码，见第 5 节）。

## 2. stringdb

- UCFX 内 `INFO/KEYS/STRS` 三段
- `KEYS` = `(u32 hash, u32 byte_offset)`；`STRS` = UTF-16LE 堆
- 键哈希 = Pandemic `pandemic_hash_m2`（键名去方括号、大小写不敏感）
- 汉化时保留原堆、追加新文本并重指向，未改条目字节级不变
- 两份 `english_P` 必须同步：`shell.wad` 块 29（shell 界面）与 `vz.wad` 块 3419（游戏内）

### 2.1 stringdb 的 key 按界面资源顺序连续排列（2026-11 新发现）

`KEYS` 段的顺序**不是按 hash 排序，而是按界面资源的原始顺序**。因此同一界面的条目在表里是**连续区间**，可以直接按下标整段处理，不必逐条猜 key：

| 区间（原始顺序下标） | 内容 |
|---|---|
| 1320–1351 | SCORE 页统计标签 |
| 2360–2764 | 商店/装备/载具/船只描述 + PDA 四页 DETAILS |
| 4845–4861 | 人物/派系介绍长文 |

锚点：`Looking for something with real presence?` → 2545、`Need some real firepower?` → 2669、
`A collection of statistics that track…` → 2734、`Fiona started in IT…` → 4850。

**注意**：`18130–18151` 与 LOG 显示内容相同，但属**对话字幕**（用带 CJK 的字体正常显示），不在回退范围。

### 2.2 文本与字体的对应关系决定「能不能显示中文」

| 界面 | 字体 | CJK 能力 | 结论 |
|---|---|---|---|
| 对话、字幕、HUD | `english_18/20` | 已扩 4,134 字形 + 2048 图集 | 中文正常 |
| 暂停菜单、PDA 文本 | `fonts_enext` | 486 字形，仅 82 个可牺牲拉丁槽 | 超出即方块 |
| 设置页、部分菜单 | `SHELL.gfx` 内嵌 Times New Roman | 114 码位，可用 5–6 个 | 基本无法中文 |
| 俄语专用（`index==8`） | `fonts_ru` | 691 字形、512×512 图集 | **不控制菜单**，见 2.3 |

**判据**：方块个数恒等于汉化后的中文字数（`ON/OFF` 各 1 个方块 = 「开/关」；`Loading` 3 个 = 「载入中」）。
这是「字体无 CJK 字形」而不是「字体损坏」，也是本项目把 PDA/设置界面 **646 条文本回退英文**的原因。

### 2.3 `fonts_enext` 的槽位能不能放中文，取决于**像素框尺寸**

实测两轮对比：

| 槽框 | 字号 | 结果 |
|---|---|---|
| 13~17 px | 13~18 | 锯齿、断笔（DXT5 的 4×4 量化把笔画打碎） |
| **18×27 px** | **25** | **清晰可读** |

所以判别标准不是「还剩多少槽」，而是「还剩多少 **≥18×24 的槽**」。本项目实测：82 个纯槽里大框约 20 个，26 节菜单用掉 53 个码位后，剩余大框基本耗尽。

### 2.4 否证：复用 `index 8` / `fonts_ru` 不能救菜单

`FUN_0060E9C0` 对 `index==8` 选 `fonts_ru`，其余选 `fonts_enext`。`fonts_ru` 有 691 字形与 512×512 图集（4 倍面积），看似可白捡 200+ 槽。

**探针**：`fonts_ru` 有西里尔字形、`fonts_enext` 没有。把 stringdb 的菜单 key 写成俄语词（`Опции` / `Продолжить` / `Выход`），设 `index = 8`。

**结果**：菜单显示**方块**（不是西里尔）→ stringdb 命中但菜单字体没变 → **`FUN_0060E9C0` 只控制 HUD/基础字体，不控制菜单**。

### 2.5 需求与供给的最终账目

| 项 | 数字 |
|---|---|
| 中文 stringdb 条目 | 16,862 |
| 全部不同汉字 | 2,235 |
| 短文本（菜单/PDA 类）用字 | **1,537** |
| `fonts_enext` 可牺牲槽 | **82** |

**差 19 倍**——「改 WAD 做全量菜单中文」在数量上不可能。菜单字体的三条路径因此全封：

| 路径 | 状态 |
|---|---|
| `fonts_enext` | ✅ 唯一可用，82 槽 |
| `fonts_ru`（index 8） | ❌ 不控制菜单 |
| block 18 `Times New Roman` | ❌ 改就崩 `0x6D057C` |

## 3. 字体（四套，格式各不相同）

### 3.1 `english_20` / `english_18` — UCFX(INFO/CHAR/MTRL)

| 段 | 大小 | 说明 |
|---|---|---|
| INFO | 16 B | 末尾 4 B = 字符数 |
| CHAR | n × 14 B | 字符记录 |
| MTRL | 840 B | 材质 |

- 图集：`0xF011157A` 类型，DXT5，**alpha 才是字形掩码**，RGB 全 255
- 扩字形后图集扩到 2048×2048，实测引擎可正常采样（FontTextureInfo 只读第一个 tex 子资源，**单页**是硬限制，尺寸不是）

### 3.2 `fonts_enext` — CFX（zlib 压缩的 GFx 字体记录）

payload 16,384 B（原版），字段地图：

| 偏移 | 内容 |
|---|---|
| 0–57 | header |
| 57 / 58–66 | name_len / `"Gunplay\0"` |
| 66–70 | glyph_count = 486 |
| 70–72 | flag |
| 72–1044 | 码位表（升序） |
| 1044–1050 | ascent/descent/line_gap |
| 1050–2022 | advance |
| 2022–2994 | res |
| 2994–2996 | kern_n |
| 2996–7082 | kerning |
| 7082–7122 | 纹理头 + TGA 名 + W/H/fmt/pad/uvCount |
| 7122–11898 | 199 × 24 B UV（4×f32 L/T/R/B + 2×f32 origin） |
| 11898–12700 | pairs（nFonts/fontId/count + count×4 B） |
| 12700–16384 | tail |

- 扩到 4,070 字形 / 3,584 个汉字 / 2048 图集
- **铁律**：原图区（左上 512×256）必须保留，新字从第 8 行（y=256）起画；不要动 advance

### 3.3 `gfxfontlib` — GFx 纹理字体（未解决）

- GFx 电影（`scaleform_shell`）通过 `ImportAssets2` 导入 `_normal_Font`（font_id 90），URL 为 `gfxfontlib.swf`
- `gfxfontlib.swf` **不在任何 WAD 的 PTHS 路径表**；exe 里也没有 `UCFX`/`CFX` 字体容器
- resident 里有 `gfxfontlib` 字体记录（entry 53）和 `gfxfontlib_f0` 图集（entry 54），但**实测引擎并不用它渲染暂停菜单/PDA**
- 结论：这是引擎内置的 GFx 字体库，WAD 层改不到（见第 5 节失败记录）

## 4. GFx 字体链路（逆向确认）

```
scaleform_shell 电影
  └─ ImportAssets2(url="gfxfontlib.swf", id=90, name="_normal_Font")
       └─ 引擎内置 FontLib
            └─ FontTextureInfo 读取器 0x7D62C0（虚表调用）
                 ├─ 读 tagType/id/name(W/H/fmt/pad/uvCount)
                 ├─ 读 count×24B UV → TEXGLYPH 对象
                 ├─ 读 nFonts / fontId → 0x7D45D0 构造 GFxFont
                 └─ 读 pairs → glyphTable[glyphIndex] = uvIndex
```

- `0x7D62C0` 直接调用者 = 0（虚表调用）
- `0x7D45D0`（GFxFont ctor）调用者：`0x7D68D8`（解析 DefineFont 时）、`0x7FC172`
- `0x7F9070`（绑定纹理）调用者：`0x7D6930`
- `0x7DBDA0`（按名查找）调用者：`0x799565`、`0x79B2F4`、`0x7E588B`（`_normal_font` fallback）

## 5. 失败方案记录

| 方案 | 结果 | 原因 |
|---|---|---|
| 改 `gfxfontlib_f0` 图集（entry 54） | PDA/暂停菜单无变化 | 引擎不用它 |
| 改 `font_glyphs_f0` / `_shell_font_glyphs_f0` 图集 | 无变化 | 同上 |
| 扩 `_shell_bold_font` / `_shell_normal_font`（4,093 字形） | 无效 | 字体不是它们 |
| 扩 `gfxfontlib` 字体记录（entry 53）+ 图集 2048 | 无变化 | 引擎用内置字体 |
| 系统字体替换（`FontSubstitutes`：Times New Roman → Noto Sans SC） | 无效 | 不是 GDI 设备字体 |
| 改 `.rdata` 的 `"Times New Roman"` 字符串（同长度替换） | **游戏闪退** | exe 有 `.rdata` 反篡改 |
| hook `CreateFontIndirectA`（改 LOGFONT） | 注入后闪退 | 注入/loader lock 与反篡改组合问题 |
| hook `0x7D62C0`（FontTextureInfo 读取器） | 注入后闪退 | 同上 |
| 改 `SHELL.gfx` 图集（b1c：结构、CSUM、压缩全对，只改像素） | 崩 `0x6D057C` | 游戏对 `SHELL.gfx` 有运行时校验 |
| `SHELL.gfx` 图集扩 2048（j-only） | 崩 `0x874640` | 同上 |
| cjk2（2048 图集注入 3,584 汉字） | 界面仍方块 + 加载画面拉丁乱码 | 该路径不经过此图集 |
| 扩 `fonts_enext` 码位表（追加 CJK 码位） | 三次均失败 | 图集尺寸硬限制 |
| 用长度阈值批量把短中文改英文 | 会把 `Hello`/`Heya` 等对话也改掉 | 改用「英文字面白名单 + 顺序区间」 |

**教训**：这个 cracked exe 只容忍 `.text` 的 MinHook detour（m2 插件的注释也这么说），任何 `.rdata` 写入都会闪退；运行时字体 hook 需要更谨慎的注入时机。

## 6. 关键地址表（v1.0）

| 地址 | 作用 |
|---|---|
| `0x0060E9C0` | 语言字体选择（english → Gunplay/fonts_enext；russian → fonts_ru） |
| `0x004BFE20` | 语言 WAD 挂载（`%s%s.wad`） |
| `0x01176018` | 语言索引指针 |
| `0x00CF281C` | 语言名字表 `char*[9]` |
| `0x0060D930` | GFx 资源按名加载 |
| `0x007DBDA0` | 按名查找（GFx 内部） |
| `0x007D62C0` | FontTextureInfo 读取器 |
| `0x007D45D0` | GFxFont 构造 |
| `0x007F9070` | 字体绑定纹理 |
| `0x004AC8E0` | 语言字体块加载（UCFX） |
| `0x7E02EC` | `.rdata` 里的 `"Times New Roman"` 字符串（**不要写**） |

## 7. 工具与脚本

- `tools/`：WAD 解析/打包、sges 压缩/解压、字体块编解码、图集 DXT5 alpha 编解码
- 逆向：Ghidra 12.1（headless）、capstone（反汇编）、Python 自写解析
- 校验：`mercs2-wad-simulator`（社区 Rust 工具）可在进游戏前验证 patch

## 8. 后续方向

1. 全量真汉字到 PDA/暂停菜单：需要改 GFx 电影或引擎字体提供者（风险高，暂缓）
2. 外挂式实时文本替换（不改游戏文件，可绕过字体限制）
3. 补齐暂停菜单第 2 行 + 底部说明的码位槽位

**已放弃并记录在案**：扩 `SHELL.gfx` 图集、改电影内嵌字体、运行时替换字体对象、系统字体替换、cjk2 注入。
现在的策略是**按字体能力分配语言**：有 CJK 的界面给中文，没有的给英文，用
「英文字面 → hash」+「stringdb 顺序区间」批量回退。
