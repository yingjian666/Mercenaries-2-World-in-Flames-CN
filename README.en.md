# Mercenaries 2: World in Flames — Simplified Chinese Localization

**English** | [中文](README.md)

> **Status: in development; no patch released yet.**
> A localization patch for the **PC English release** (game files not included). Dialogue / subtitles / missions / HUD are Chinese; **the menu and PDA layers are still blocked by a hard font limitation**, so the patch is not published — **it ships when it's finished, not before**.
> This repo publishes the full reverse-engineering record and doubles as the progress window for the community.

[![status](https://img.shields.io/badge/status-v0.6.3-yellow.svg)](#) [![game](https://img.shields.io/badge/game-Mercenaries%202-orange.svg)](https://en.wikipedia.org/wiki/Mercenaries_2:_World_in_Flames) [![platform](https://img.shields.io/badge/platform-Windows%20XP%2B-lightgrey.svg)](#compatibility)

---

## State of things

| Area | State |
|---|---|
| In-game dialogue, subtitles | ✅ **Chinese** |
| Mission text, HUD (ammo / health / prompts) | ✅ **Chinese** |
| Main menu buttons (6) | ✅ Chinese (textures redrawn) |
| PDA top bar (map / info / supplies / legend) | ✅ Chinese (textures redrawn) |
| Pause menu | ✅ 52 menu strings (Latin codepoint borrowing + atlas reuse) |
| **PDA body / Options / dialogs / status line** | ⚙️ **reverted to English on purpose** (646 strings) |

> Short version: **everywhere Chinese can actually render, it is Chinese.** The remaining UI would render as tofu, so it was deliberately reverted to English. That is a trade-off, not unfinished work.

## Why the menus can't be fully Chinese (root cause)

Three font paths coexist, with very different capacities:

| UI surface | Font | CJK glyphs | Result |
|---|---|---|---|
| Dialogue, subtitles, HUD | language-block font (4,134 glyphs, 2048×2048 atlas) | expanded | ✅ Chinese renders |
| Pause menu, PDA text | `fonts_enext` (486 glyphs, only **82** spare latin-ext slots) | 82 | ⚠️ tofu beyond that |
| Options, part of the menus | `SHELL.gfx` embedded `Times New Roman` (114 codepoints) | 5–6 | ❌ effectively impossible |

**Tofu is not a broken font — it is Chinese characters fed to a font with no CJK glyphs.** The proof: the tofu count always equals the character count of the Chinese string (`ON`/`OFF` → 1 box each because they were translated to single characters 开/关; `Status: Offline` → 状态：离线; the player name 4+3 boxes → 马蒂亚斯·尼尔森).

So there are only two ways out: **grow the font** (crashes on boot in `SHELL.gfx`, see below) or **revert the text to English**. This release takes the second path for 646 PDA/Options strings.

## Known issues

- **PDA body / Options text is English** — Chinese renders as tofu, so it was reverted on purpose;
- Kerning: some Chinese characters are slightly tight (the engine lays out by Latin widths; inherent);
- The 52 Chinese pause-menu strings use borrowed Latin-extended codepoints, so a literal `À Á Â Ý` in a string may display as a Chinese character (known, acceptable);
- Text that was baked into textures (main menu buttons, PDA tabs) can only be redrawn, not retargeted.

## What's done

- **Full text translation**: 17,651 / 18,299 stringdb entries (96.5%), with a consistent terminology table for people, factions and place names
- **HUD / subtitles / missions**: language-block font expanded, no missing glyphs observed
- **Main menu buttons, PDA top bar**: textures redrawn to Chinese
- **Pause menu**: 52 strings via Latin codepoint + `fonts_enext` atlas reuse
- **646 PDA/Options strings reverted to English**: located by "English literal → hash" and by contiguous `stringdb` index ranges; tofu eliminated on those surfaces

## Dead ends (all tested, documented so nobody pays twice)

| # | Approach | Result |
|---|---|---|
| 1 | Grow the atlas to 2048×2048 | crashes on boot (texture upload, `0xC0000005`) |
| 2 | Edit the `SHELL.gfx` embedded font (`DefineFont3`) | crashes (invalid object vtable) |
| 3 | Edit only the atlas, keep the font (b1c) | static checks all pass, still crashes at runtime |
| 4 | Replace the font object at runtime (DLL hook) | no crash, but never drawn (`g_font=NULL` timing) |
| 5 | Extend `fonts_enext`'s codepoint table | failed three times (atlas size hard limit) |
| 6 | cjk2 (2048 atlas, 3,584 CJK glyphs injected) | no effect, UI still tofu; rolled back |
| 7 | System font substitution (`FontSubstitutes`) | no effect — not a GDI device font |
| 8 | New language WAD + ASI (Route C) | ✅ **works** — `qm` build + ASI mount + stringdb resolves (guide §55–56) |
| 9 | Push all menu text through borrowed codepoints | 82-slot ceiling, covers 52 strings only |
| 10 | Reuse index 8 so menus use `fonts_ru` (691 glyphs / 512×512) | ❌ **doesn't control menus** — they still use `fonts_enext` (guide §56) |

Crash addresses: atlas growth `0x874640`, movie font edit `0x6D057C`.

## Demand vs supply (the final accounting)

| Item | Count |
|---|---|
| Chinese stringdb entries | 16,862 |
| Distinct Chinese characters | 2,235 |
| Distinct characters used by short strings (menu/PDA class) | **1,537** |
| Sacrificeable `fonts_enext` slots (the only font the menus use) | **82** |

**Full menu/PDA Chinese needs 1,537 slots; 82 are available — a 19× gap.** That is not a technique problem but an order-of-magnitude one, so "full menu Chinese via WAD edits" is physically impossible.

## Structure of the record

| File | Contents |
|---|---|
| [`docs/reverse-notes/汉化完全指南.en.md`](docs/reverse-notes/汉化完全指南.en.md) | **English guide** — all 44 section titles mapped, plus the engineering conclusions that matter |
| [`docs/reverse-notes/汉化完全指南.md`](docs/reverse-notes/汉化完全指南.md) | Full reverse-engineering record, 54 sections, ~126 KB (Chinese) |
| [`TECHNICAL.md`](TECHNICAL.md) | Condensed technical writeup: WAD/FFCS v2, stringdb, three font formats, GFx chain, failure table |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |

The long document is Chinese-only by design (it is the author's working notebook); the parts that matter to other researchers are summarized in `TECHNICAL.md` and in this README. Ask and I'll translate any specific section.

## Install (once released)

> The patch is not released yet. The steps describe the intended shape of the patch.

1. **Back up** your game's `data` folder;
2. Copy `shell-patch.wad`, `vz-patch.wad`, `loading-patch.wad`, `English-patch.wad` into `data`;
3. Launch the game.

**Uninstall**: delete those `*-patch.wad` files. The retail WADs are never modified.

> The patch is ~17 MB and is not committed to Git; it will ship via **Releases**.

## Compatibility

- Target: **Mercenaries 2 PC v1.1** (DRM-free build), `Mercenaries2.exe` ≈ 53,482,288 bytes (sha256 `958eb227…`)
- Patch format: `data/*-patch.wad`, overriding by **asset hash** — retail WADs untouched
- No DRM circumvention is included; bring your own working copy

## Repo layout

```
README.md / README.en.md   Chinese / English readme
CHANGELOG.md               version history
TECHNICAL.md               formats and tooling (developer-facing, English)
docs/reverse-notes/        full reverse-engineering record (Chinese)
release-notes/             release notes
tools/                     build / push helpers
data/                      patch drop-off (*.wad not in Git)
```

## Credits

- [notes-on-the-released-game](https://github.com/Mercenaries-Fan-Build/notes-on-the-released-game) — format docs, reverse-engineering corpus
- [mercs2-wad-simulator](https://github.com/Mercenaries-Fan-Build/mercs2-wad-simulator) — WAD writer
- [mercs2-languages](https://github.com/Mercenaries-Fan-Build/mercs2-languages) — language ASI / Route C
- [mercs2-securom-bypass](https://github.com/Mercenaries-Fan-Build/mercs2-securom-bypass) — DRM removal

The `mercs2-wad-simulator` / `mercs2-languages` toolchain is what made this work possible: `qm`, `wad_builder`, `stringdb_dump` and the `add_language` contract are the basis for the PDA/Options analysis above.

## License

See [LICENSE](LICENSE). Game copyright remains with Pandemic Studios / EA; this project only contains text and resource rewrites and **no game content**.
