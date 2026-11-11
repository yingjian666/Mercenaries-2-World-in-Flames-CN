# 版本记录

## v0.5.0 — 2026-11-11

首个公开测试版（beta）。

### 已实现

- 全量文本翻译：17,651 / 18,299 条（96.5%）
- 主菜单按钮（纹理）中文
- 主菜单 / 设置菜单文字中文（`fonts_enext`）
- 主菜单 6 条描述中文（回收码位方案）
- HUD / 字幕 / 目标提示中文（`english_20/18`）
- ESC 暂停菜单 5/6 行中文

### 已知问题

- PDA 界面方块（GFx 内置字体，WAD 层不可改）
- 暂停菜单第 2 行 + 底部说明方块（码位槽位不足）
- 字距不统一（引擎固有）
- PDA 顶栏纹理仍英文

### 技术

- 建立 FFCS v2 WAD / stringdb / 三套字体的完整文档（TECHNICAL.md）
- 确认 GFx 字体链路（ImportAssets2 → gfxfontlib → FontTextureInfo）
- 记录 `.rdata` 反篡改与运行时 hook 的失败结论
