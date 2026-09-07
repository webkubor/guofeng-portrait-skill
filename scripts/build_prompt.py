#!/usr/bin/env python3
"""
古风人像提示词构建器 —— 按风格分发到 styles/<style>/build_prompt.py。

两种风格的提示词体系完全不同（3D 写实讲渲染与材质，水墨讲笔触与留白），
硬合成一份会让两边都变钝，所以各自保留完整的一份，这里只做路由。

  python scripts/build_prompt.py --style 3d-realistic \
      --subject "冷峻的青年剑修，月下山巅" --category character-male --ratio 3:4

  python scripts/build_prompt.py --style ink-wash \
      --subject "白衣书生，竹林独坐" --category character --ratio 3:4

不带 --style 时默认 3d-realistic（人像最常用的起点）。
其余参数原样透传，由各风格脚本自己校验——它们的 category 取值不同：
  3d-realistic : character-male / character-female / scene / weapon / action
  ink-wash     : character / creature / nature / poetry / scene
"""

import os
import subprocess
import sys

STYLES = ("3d-realistic", "ink-wash")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    argv = sys.argv[1:]
    style = "3d-realistic"
    if "--style" in argv:
        i = argv.index("--style")
        if i + 1 >= len(argv):
            sys.stderr.write("--style 后面要跟风格名\n")
            return 2
        style = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if style not in STYLES:
        sys.stderr.write(f"未知风格 {style!r}，可选：{' / '.join(STYLES)}\n")
        return 2
    target = os.path.join(ROOT, "styles", style, "build_prompt.py")
    return subprocess.call([sys.executable, target, *argv])


if __name__ == "__main__":
    raise SystemExit(main())
