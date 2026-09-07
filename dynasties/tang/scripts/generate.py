#!/usr/bin/env python3
"""唐 · 盛唐华贵 · museav 出图 wrapper

骨架版：复用本仓库 dynasties/common-prompt-base.md 的通用骨架。
等你给"反复调了几十组"的调参经验 + 完整 prompt，我填充唐朝专属部分。
"""
import sys
from pathlib import Path

# 复用宋的骨架脚本结构（避免重复）
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "dynasties" / "song" / "scripts"))
from generate import generate  # noqa: E402

if __name__ == "__main__":
    # TODO: 当唐朝专属参数经验到了后，覆写这里的 generate 调用
    # 临时直接复用宋的骨架
    generate(dynasty="tang", subject=None, ratio="3:4", out_dir=None, raw_prompt=None)
