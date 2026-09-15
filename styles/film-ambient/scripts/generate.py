#!/usr/bin/env python3
"""film-ambient · museav 出图 wrapper（端到端：整理提示词 → 出图 → 落盘）

把 build_prompt.py 的槽位化提示词直接接到中台出图，并默认带上垫图锁脸。

用法:
  # 最小用法：直接点一个命名风格（21 个，--list 可查）
  ./generate.py --preset blossom-veil --subject "凑近花枝，微微侧脸"
  ./generate.py --preset lantern-walk --subject "提着灯笼走过石阶"

  # 风格 + 覆盖单个槽位（其余沿用风格预设）
  ./generate.py --preset snow-court --subject "抬头看雪" --shot candid-close

  # 不用预设，手搭槽位
  ./generate.py --subject "..." --scene snow-court --light snow-diffuse --mood fragile

  # 换胶片型号（默认 pro400h 日系青绿；夜景配 cinestill800t，暖调配 portra400）
  ./generate.py --subject "..." --light lantern-night --film cinestill800t

  # 锁脸：稳定出同一个人（强烈建议每次都带）
  ./generate.py --preset green-glance --subject "..." --ref ~/refs/face-anchor.jpg

  # 只看提示词不出图
  ./generate.py --preset bamboo-tea --subject "..." --dry-run

  # 批量（每行一个 subject，其余槽位/风格作为公共参数）
  ./generate.py --batch subjects.txt --ref ~/refs/face-anchor.jpg

依赖:
  - museav CLI 已登录（~/.museav.json）
  - Python 3.10+
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from build_prompt import build_prompt, resolve_slots, PRESETS, RATIO_TO_SIZE  # noqa: E402

DEFAULT_OUT = Path.home() / "Movies" / "guofeng-portrait" / "film-ambient"


def make_prompt(args, subject):
    """按命名风格 / 槽位生成完整提示词（英文，给 GPT Image 2.5）。"""
    slots = resolve_slots(
        getattr(args, "preset", None),
        scene=args.scene, light=args.light, mood=args.mood,
        film=args.film, shot=args.shot, era=args.era,
    )
    result = build_prompt(
        slots["scene"], slots["light"], slots["mood"], slots["shot"],
        slots["era"], slots["film"],
        subject, "image", args.ratio, preset=getattr(args, "preset", None),
    )
    prompt = result["positive_en"]
    if not args.no_negative:
        prompt = f"{prompt} Avoid: {result['negative_en']}"
    if args.ref:
        prompt = f"{prompt}; keep the same face as image 1"
    return prompt, result


def run_museav(prompt, args):
    """调 museav gen，返回 stdout（成功时是中台图片 URL）。"""
    cmd = [
        "museav", "gen",
        "--prompt", prompt,
        "--ratio", args.ratio,
        "--quality", args.quality,
    ]
    for ref in args.ref:
        cmd += ["--ref", str(Path(ref).expanduser())]
    if args.project:
        cmd += ["--project", args.project]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or "museav gen 调用失败\n")
        return None
    return proc.stdout.strip()


def main():
    parser = argparse.ArgumentParser(
        description="film-ambient 端到端出图（古风氛围胶片人像）",
    )
    parser.add_argument("--subject", help="主体与姿态描述")
    parser.add_argument("--batch", help="批量模式：每行一个 subject 的文本文件")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default=None,
                        help=f"命名风格（{len(PRESETS)} 个：花影柔光 / 雪落庭院 / 竹影清茶 ...）；"
                             "单槽位参数可覆盖预设")
    parser.add_argument("--scene", default=None)
    parser.add_argument("--light", default=None)
    parser.add_argument("--mood", default=None)
    parser.add_argument("--shot", default=None)
    parser.add_argument("--era", default=None, help="song / tang / wei-jin / none")
    parser.add_argument("--film", default=None,
                        help="胶片型号：pro400h 日系青绿（默认）/ portra400 暖奶油 / "
                             "superia 纪实 / cinestill800t 夜景钨丝灯 / none 通用")
    parser.add_argument("--ratio", default="3:4", choices=list(RATIO_TO_SIZE.keys()))
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high"],
                        help="定稿用 high；摸槽位组合时用 low 省钱")
    parser.add_argument("--ref", action="append", default=[],
                        help="垫图路径，可重复（最多 5 张，建议第 1 张锁脸）")
    parser.add_argument("--project", help="归档进中台工作区")
    parser.add_argument("--no-negative", action="store_true", help="不带负面词")
    parser.add_argument("--dry-run", action="store_true", help="只打印提示词，不出图")
    args = parser.parse_args()

    if args.batch:
        subjects = [
            line.strip() for line in Path(args.batch).expanduser().read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    elif args.subject:
        subjects = [args.subject]
    else:
        parser.error("要给 --subject，或用 --batch 传文件")
        return 2

    for i, subject in enumerate(subjects, 1):
        prompt, _ = make_prompt(args, subject)
        print(f"\n=== [{i}/{len(subjects)}] {subject}")
        if args.dry_run:
            print(prompt)
            continue
        url = run_museav(prompt, args)
        if url:
            print(url)
        else:
            print("出图失败", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
