# tools — WAD / 字体处理脚本

汉化过程中写的逆向工具，按原样公开，供同引擎（Pandemic **FFCS v2** + `sges` 压缩 + UCFX 容器）的项目复用。

这些脚本在本作 retail 版 WAD 上实际跑过，但**没有做过通用化改造**：区块索引、PTHS 路径串、哈希常量都是对着具体 WAD 实测出来的。

## 目录

| 文件 | 用途 |
|---|---|
| `rea_tools/ffcs_wad.py` | 解析 FFCS v2 `.wad` 的区块表（INDX/ASET/PTHS/DATA），可输出 JSON 或抽出原始 chunk / `paths.txt` |
| `rea_tools/sges_decompress.py` | 解压 DATA 里的 `sges` 段（一个逻辑 block 一段），支持按索引/名字/正则单块解或整档批量解 |
| `rea_tools/sges_compress.py` | 把解压后的 block 重新压成 `sges`（v4 头 + 16 字节对齐分段），是解压的逆过程，`--verify` 会解回来逐字节比对 |
| `rea_tools/ffcs_patch_wad.py` | 组装 `<name>-patch.wad` 的公共模块：PTHS trailer、证书 blob、页对齐、单/多 block 打包、合并已有补丁 WAD |
| `rea_tools/build_patch_wad.py` | 命令行入口：从原版 WAD 取指定 block 的元数据，塞进改动后的 block，生成最小的 `vz-patch.wad` |
| `rea_tools/wad_patcher.py` | 一站式原地改 WAD：定位脚本的 UCFX chunk、替换 Lua 字节码/payload、重算 CSUM、重压写回 |
| `fontblock.py` | GFx 字体块（UCFX type `0xFE0E8320`）编解码：解出 zlib 字体数据，改完字形后按模板重建块并重算 CSUM |

`build_patch_wad.py` 依赖 `ffcs_wad.py`、`sges_compress.py`、`sges_decompress.py`、`ffcs_patch_wad.py`、`wad_patcher.py`，调用时脚本会自动把自身目录加进 `sys.path`，所以这几个文件**必须放在同一目录**。

## 依赖

- **Python 3.9+**（代码用了 `from __future__ import annotations` 与 `int | None` 注解，推荐 3.10+）
- 上面这些 WAD / sges / 字体块脚本：**只用标准库**（`struct`、`zlib`、`mmap`、`argparse`、`hashlib`）
- 字体位图与纹理流水线（生成字形图集、写 TGA/DDS 的那部分，未收录）：另需 **numpy**、**Pillow**
- `build_patch_wad.py` 的 Lua 自动补齐 / DLC 端口分支：还需要一个和本作字节码兼容的 **`luac`**（脚本会在 PATH 与常见安装位置查找）

## 典型用法

```bash
# 1. 看 WAD 结构，顺便导出 paths.txt（后续 --ffcs-out 要用）
python tools/rea_tools/ffcs_wad.py data/vz.wad --json > vz-chunks.json
python tools/rea_tools/ffcs_wad.py data/vz.wad --out-dir out/ffcs

# 2. 列出所有 block 及对应路径
python tools/rea_tools/sges_decompress.py --wad data/vz.wad --ffcs-out out/ffcs --list

# 3. 定位单个 block 并解压（--name 是对 PTHS 路径做子串匹配）
python tools/rea_tools/sges_decompress.py --wad data/vz.wad --ffcs-out out/ffcs \
    --name scripts_vz --out scripts_vz.block.bin

# 4. 批量解压（要走 --data-bin，速度明显更快）
python tools/rea_tools/sges_decompress.py --data-bin data/DATA.BIN --paths out/ffcs/paths.txt \
    --bulk-out-dir out/blocks --skip-existing --bulk-manifest out/blocks.json

# 5. 改完重新压缩（--verify 解回来比对，防止写坏）
python tools/rea_tools/sges_compress.py scripts_vz.block.bin scripts_vz.sges.bin --verify

# 6. 生成 patch WAD（给未压缩的 block 加 --raw，脚本自动压缩）
python tools/rea_tools/build_patch_wad.py --source-wad data/vz.wad \
    --block-index 1257 --modified-block scripts_vz.sges.bin --output data/vz-patch.wad

# 7. 或者让 wad_patcher 直接改：先列脚本，再换字节码
python tools/rea_tools/wad_patcher.py --wad data/vz.wad --list-scripts
python tools/rea_tools/wad_patcher.py --wad data/vz.wad \
    --script wiftutorialtank --lua-bytecode compiled.luac
```

## 说明

- 脚本按原样复制，未清洗。`fontblock.py` 末尾的 `__main__` 自检块里还留着开发机路径（`H:/.../Loading.wad`）和指向 `../work/rea_tools` 的 `sys.path`，只当用法示例读；直接执行会报找不到文件。
- 区块索引（如 `1257`）、脚本名（如 `wiftutorialtank`）、PTHS 路径串都来自本作 retail 版，换 WAD 版本要重新定位。
- 生成的 `*-patch.wad` 体积较大，`.gitignore` 已排除 `data/*.wad`，发补丁请走 Releases。
- 仅用于学习研究与单机汉化，见仓库 [LICENSE](../LICENSE) 与 README 里的免责声明。
