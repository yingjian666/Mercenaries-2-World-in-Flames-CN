# -*- coding: utf-8 -*-
"""Mercenaries 2 GFx 字体块 (UCFX type 0xFE0E8320) 编解码。

块结构：
    u32 count + count×16 {name_hash, type_hash, field_c, chunk_size}
    UCFX: "UCFX" + u32 hdr_size + u32 0 + u32 0 + u32 nchunks
          + nchunks×20 {tag, rel_off, size, count, 0}
          body...
    每个 UCFX 末尾: "CSUM" + u32

字体块的唯一 chunk 是 "data"，body = b"CFX\\x08" + u32 + zlib(level9)
zlib 解压后是字体记录 + 贴图 UV 子资源。
"""
from __future__ import annotations
import struct, zlib

CSUM_TAG = b"CSUM"
FONT_TYPE = 0xFE0E8320


def crc32_mercs2(data: bytes) -> int:
    """CRC-32 poly 0xEDB88320 reflected, init 0, no final xor（实测）。"""
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xEDB88320 if crc & 1 else crc >> 1
    return crc & 0xFFFFFFFF


def _fast_crc_table():
    t = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
        t.append(c)
    return t


_CRC_TAB = _fast_crc_table()


def crc32_mercs2_fast(data: bytes) -> int:
    crc = 0
    for b in data:
        crc = _CRC_TAB[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return crc


def parse_block_entries(block: bytes):
    n = struct.unpack_from("<I", block, 0)[0]
    out = []
    pos = 4 + n * 16
    for i in range(n):
        h, t, fc, sz = struct.unpack_from("<IIII", block, 4 + i * 16)
        out.append({"index": i, "name_hash": h, "type_hash": t, "field_c": fc,
                    "size": sz, "offset": pos})
        pos += sz
    return out


def parse_ucfx(u: bytes):
    hs = struct.unpack_from("<I", u, 4)[0]
    n = struct.unpack_from("<I", u, 16)[0]
    chunks = []
    for i in range(n):
        o = 20 + i * 20
        tag = u[o:o + 4].decode("ascii", "replace")
        rel, size, cnt, z = struct.unpack_from("<IIII", u, o + 4)
        chunks.append({"tag": tag, "hdr_off": o, "rel": rel, "size": size,
                       "count": cnt, "zero": z, "off": hs + rel})
    return hs, chunks


def decode_font_block(block: bytes):
    """返回 (payload_raw, info) —— payload_raw 是 zlib 解压后的字体数据。"""
    es = parse_block_entries(block)
    e = next(x for x in es if x["type_hash"] == FONT_TYPE)
    u = block[e["offset"]:e["offset"] + e["size"]]
    hs, chunks = parse_ucfx(u)
    c = chunks[0]
    body = u[c["off"]:c["off"] + c["size"]]
    assert body[:4] == b"CFX\x08", body[:4]
    magic2 = struct.unpack_from("<I", body, 4)[0]
    z = body.find(b"\x78", 8)
    raw = zlib.decompress(body[z:])
    return raw, {"magic2": magic2, "z": z, "comp_len": len(body) - z,
                 "chunks": chunks, "hs": hs, "entry": e, "ucfx": u}


def build_font_block(raw: bytes, tmpl_block: bytes, magic2: int | None = None) -> bytes:
    """用 raw 重建字体块（沿用模板的 UCFX 头/名字哈希）。"""
    payload, info = decode_font_block(tmpl_block)
    if magic2 is None:
        magic2 = info["magic2"]
    comp = zlib.compress(raw, 9)
    body = b"CFX\x08" + struct.pack("<I", magic2) + comp

    u = info["ucfx"]
    hs, chunks = parse_ucfx(u)
    # 只重建第一个 chunk（data），其余原样
    hdr = bytearray(u[:hs])
    new_body_off = hs
    struct.pack_into("<IIII", hdr, 20 + 4, 0, len(body), chunks[0]["count"], chunks[0]["zero"])
    ucfx = bytes(hdr) + body
    ucfx = ucfx + CSUM_TAG + struct.pack("<I", crc32_mercs2_fast(ucfx))

    # 重建块
    es = parse_block_entries(tmpl_block)
    out = bytearray()
    head = bytearray(4 + len(es) * 16)
    struct.pack_into("<I", head, 0, len(es))
    for x in es:
        c = ucfx if x["index"] == info["entry"]["index"] else tmpl_block[x["offset"]:x["offset"] + x["size"]]
        struct.pack_into("<IIII", head, 4 + x["index"] * 16,
                         x["name_hash"], x["type_hash"], x["field_c"], len(c))
        out += c
    return bytes(head) + bytes(out)


if __name__ == "__main__":
    import sys, os
    base = os.path.dirname(os.path.abspath(__file__))
    work = os.path.join(base, "..", "work")
    sys.path.insert(0, os.path.join(work, "rea_tools"))
    from ffcs_wad import parse_ffcs, dump_paths_from_pths
    from sges_decompress import decompress_sges_block, find_sges_offsets
    from pathlib import Path

    p = Path("H:/3DMGAME_Mercenaries_2_World_in_Flames.EN.Green/Mercenaries2/data/Loading.wad")
    a = parse_ffcs(p)
    by = {c.tag: c for c in a.chunks}
    raw_wad = p.read_bytes()
    paths = dump_paths_from_pths(raw_wad[by["PTHS"].offset:by["PTHS"].offset + by["PTHS"].size])
    offs = find_sges_offsets(raw_wad)
    i = next(k for k, s in enumerate(paths) if "fonts_enext_P" in s)
    blk = decompress_sges_block(raw_wad, offs[i], offs[i + 1] if i + 1 < len(offs) else len(raw_wad))
    print("block", len(blk), "path", paths[i])

    payload, info = decode_font_block(blk)
    print("payload", len(payload), "magic2=0x%X z=%d comp=%d" % (info["magic2"], info["z"], info["comp_len"]))
    # 验证：重新压缩后能否得到原始压缩字节
    z_orig = blk[info["entry"]["offset"]:][:0]
    u = info["ucfx"]
    c = info["chunks"][0]
    body = u[c["off"]:c["off"] + c["size"]]
    orig_comp = body[info["z"]:]
    for lvl in (9, 6):
        mine = zlib.compress(payload, lvl)
        print("  zlib level %d -> %d 字节，与原始 %d 字节一致: %s" % (lvl, len(mine), len(orig_comp), mine == orig_comp))
    nb = build_font_block(payload, blk)
    print("重建块 %d -> %d 字节，逐字节一致: %s" % (len(blk), len(nb), nb == blk))
