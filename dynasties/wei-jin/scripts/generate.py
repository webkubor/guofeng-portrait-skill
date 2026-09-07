#!/usr/bin/env python3
"""魏晋 · 风骨飘逸 · museav 出图 wrapper

骨架版：复用本仓库 dynasties/common-prompt-base.md 的通用骨架。
等你给调参经验 + 完整 prompt，我填充魏晋专属部分。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "dynasties" / "song" / "scripts"))
from generate import generate  # noqa: E402

if __name__ == "__main__":
    # TODO: 魏晋专属参数到位后覆写
    generate(dynasty="wei-jin", subject=None, ratio="16:9", out_dir=None, raw_prompt=None)
