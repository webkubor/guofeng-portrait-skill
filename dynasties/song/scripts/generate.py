#!/usr/bin/env python3
"""宋韵美人 · museav 出图 wrapper

用法:
  # 一键按主题出图
  ./generate.py --subject "春日庭院，少女倚栏观花，海棠初开" --ratio 3:4
  ./generate.py --subject "夏日荷塘，少女摘莲蓬" --ratio 16:9

  # 用 prompt 模板指定朝代
  ./generate.py --dynasty song --subject "少女倚栏" --ratio 3:4 --out ~/Movies/guofeng-portrait/song/

  # 直接给完整 prompt（绕过 skill 整理）
  ./generate.py --prompt "..." --ratio 16:9

依赖:
  - museav CLI 已登录 ~/.museav.json（账号：山鬼映画）
  - Python 3.10+
"""
import argparse, sys, json, os, subprocess
from pathlib import Path
from datetime import datetime

# 通用骨架片段（来自 dynasties/common-prompt-base.md）
COMMON_BASE = """
Southern Song Dynasty noblewoman, low chignon with loose strands and simple jade hairpin, sheer silk beizi in oat color over soft cream inner robe, soft smile gazing into the distance, half-lidded eyes, relaxed serene expression, {scene}, foreground lotus leaf / willow branch partially framing, half the frame left as breathing empty space, distant pavilions and lotus pond in soft misty silhouette, soft golden backlight at dusk creating rim light on hair and hem, thin atmospheric haze softening shadows, realistic skin texture, 85mm portrait lens, low saturation palette of warm apricot and lotus-leaf green, subtle film grain, museum-quality composition
"""

# 反面清单
NEGATIVE = (
    "anime, illustration, painting, sketch, 3d render, cgi, plastic skin, glossy skin, "
    "airbrushed, oversaturated, vibrant neon colors, heavy makeup, modern hairstyle, "
    "western dress, fantasy armor, blurry eyes, extra fingers, mutated hands, deformed face, "
    "text, watermark, low quality, worst quality, blurry, jpeg artifacts"
)

DEFAULT_OUT_BASE = "/Volumes/AI素材资源/图片素材/山鬼映画/古风美人"

def build_song_prompt(subject: str) -> str:
    """宋韵：根据主题套通用骨架。subject = 画面描述（人物+场景+季节物候）"""
    scene = subject  # 主体描述直接当场景段
    return COMMON_BASE.format(scene=scene).strip()

def generate(dynasty: str, subject: str, ratio: str, out_dir: str, raw_prompt: str | None = None):
    # 1. 构造 prompt
    if raw_prompt:
        prompt = raw_prompt
    elif dynasty == "song":
        prompt = build_song_prompt(subject)
    else:
        # 唐/魏晋 先用 subject 当 raw，其他朝代后续补
        prompt = subject
    
    # 2. 输出目录（按朝代+日期+主题）
    if not out_dir:
        out_dir = DEFAULT_OUT_BASE
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_subject = "".join(c if c.isalnum() else "-" for c in subject[:30]) if subject else "default"
    full_out = Path(out_dir) / dynasty / date_str
    full_out.mkdir(parents=True, exist_ok=True)
    out_path = full_out / f"{date_str}-{safe_subject}.jpg"
    
    # 3. 调用 museav gen（stdout 打 URL，没有 -o 选项）
    cmd = [
        "museav", "gen",
        "-p", prompt,
        "--ratio", ratio,
    ]
    print("=" * 60)
    print(f"朝代: {dynasty}")
    print(f"主题: {subject}")
    print(f"比例: {ratio}")
    print(f"输出: {out_path}")
    print("-" * 60)
    print("Prompt:")
    print(prompt)
    print("-" * 60)
    print("Negative:")
    print(NEGATIVE)
    print("-" * 60)
    print("执行:", " ".join(cmd))
    print("=" * 60)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ 出图失败:")
        print(result.stderr or result.stdout)
        sys.exit(1)
    print(result.stdout)
    
    # 4. 从 stdout / stderr 解析 URL（museav 最后一行是 https://img.webkubor.online/...png）
    url = None
    for line in (result.stdout or "").splitlines() + (result.stderr or "").splitlines():
        line = line.strip()
        if line.startswith("https://") and line.endswith((".png", ".jpg", ".jpeg")):
            url = line
            break
    if not url:
        print("❌ 没找到图片 URL，请检查 museav 输出")
        sys.exit(1)
    print(f"✅ museav 输出 URL: {url}")
    
    # 5. 下载到 AI 素材盘（扩展名跟随 museav 实际返回）
    out_path = out_path.with_suffix(Path(url).suffix or ".jpg")
    print(f"下载到 {out_path} ...")
    import urllib.request
    with urllib.request.urlopen(url) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    print(f"✅ 出图完成 → {out_path}")

def main():
    p = argparse.ArgumentParser(description="古风美人 · museav 出图")
    p.add_argument("--dynasty", choices=["tang", "song", "wei-jin"], default="song", help="朝代（默认 song）")
    p.add_argument("--subject", "-s", default=None, help="画面主题（如：春日庭院，少女倚栏观花，海棠初开）")
    p.add_argument("--ratio", "-r", default="3:4", choices=["16:9","9:16","1:1","3:4","4:3"], help="画面比例（默认 3:4 竖版）")
    p.add_argument("--out", "-o", default=None, help="输出目录（默认 /Volumes/AI素材资源/图片素材/山鬼映画/古风美人）")
    p.add_argument("--prompt", default=None, help="直接给完整 prompt（绕过 skill 整理）")
    args = p.parse_args()
    
    if not args.subject and not args.prompt:
        print("❌ 必须给 --subject 或 --prompt")
        sys.exit(1)
    
    generate(args.dynasty, args.subject, args.ratio, args.out, args.prompt)

if __name__ == "__main__":
    main()
