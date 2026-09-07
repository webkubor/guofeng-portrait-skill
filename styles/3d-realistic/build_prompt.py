#!/usr/bin/env python3
"""
Build prompts for the Donghua 3D Realistic style skill.

Supports two subject categories (this is a portrait-only skill):
  - character-male : swordsman, sect master, demon lord, young hero
  - character-female: immortal fairy, enchantress, demoness, female warrior

Supports two media types:
  - image : static image (default)
  - video : video clip (adds motion keywords)

Supports four aspect ratios:
  - 3:4  (portrait, character default)
  - 16:9 (landscape, scene default)
  - 9:16 (mobile portrait)
  - 1:1  (square, weapon default)

Example:
  python scripts/build_prompt.py \
      --subject "冷峻的青年剑修，月下山巅" \
      --category character-male \
      --ratio 3:4

Output is JSON written to stdout:
  {
    "category": "character-male",
    "media": "image",
    "ratio": "3:4",
    "subject": "...",
    "positive_zh": "...",
    "positive_en": "...",
    "negative_zh": "...",
    "negative_en": "...",
    "recommended_size": "1024x1536"
  }
"""

import argparse
import json
import sys


# ============================================================
# Category-specific positive prompt fragments
# ============================================================

CHARACTER_MALE = {
    "fixed_zh": (
        "国产3D动漫风格，电影级3D光影，写实人像，UE5 Nanite + Lumen 渲染，"
        "PBR材质，皮肤毛孔清晰，发丝根根分明，东方美学，仙侠玄幻，"
        "气势磅礴，史诗感"
    ),
    "fixed_en": (
        "Chinese 3D donghua anime style, cinematic 3D lighting, realistic portrait, "
        "UE5 Nanite + Lumen render, PBR materials, visible skin pores, "
        "individual hair strands, oriental aesthetics, xianxia fantasy, "
        "epic atmosphere, masterpiece"
    ),
}

CHARACTER_FEMALE = {
    "fixed_zh": (
        "国产3D动漫风格，电影级3D光影，写实人像，UE5 Nanite + Lumen 渲染，"
        "PBR材质，皮肤有呼吸感，发丝半透明通透，丝绸材质若隐若现，"
        "东方美学，仙侠玄幻，唯美空灵"
    ),
    "fixed_en": (
        "Chinese 3D donghua anime style, cinematic 3D lighting, realistic portrait, "
        "UE5 Nanite + Lumen render, PBR materials, luminous skin, "
        "translucent hair strands, sheer silk textures, "
        "oriental aesthetics, xianxia fantasy, ethereal beauty, masterpiece"
    ),
}




CATEGORIES = {
    "character-male": CHARACTER_MALE,
    "character-female": CHARACTER_FEMALE,
}


# ============================================================
# Negative prompts (universal + category-specific)
# ============================================================

NEGATIVE_BASE_ZH = (
    "2D动漫，赛璐璐，二次元眼睛，水墨画，工笔，平面卡通，"
    "日漫风格，皮克斯，迪士尼，现代元素，手机，汽车，"
    "西方元素，西式盔甲，塑料皮肤，磨皮过度，"
    "头发糊成一片，手部畸形，六根手指，武器比例失调，"
    "服饰混搭，中西混杂，过度饱和，糖果色，廉价光效"
)

NEGATIVE_BASE_EN = (
    "2D anime, cel-shading, big anime eyes, watercolor, ink wash, flat cartoon, "
    "Japanese anime style, Pixar, Disney, modern elements, smartphones, cars, "
    "Western elements, European armor, plastic skin, over-smoothed, "
    "hair blending into one mass, deformed hands, six fingers, incorrect weapon proportions, "
    "mixed costumes, East-meets-West chaos, oversaturated, candy colors, cheap light effects"
)

NEGATIVE_VIDEO_ZH = (
    "，动作僵直，构图松散，人物重叠混乱，特效堆积，"
    "动作不到位，缺少动感模糊"
)

NEGATIVE_VIDEO_EN = (
    ", stiff motion, loose composition, character overlap chaos, effect pile-up, "
    "unconvincing action, lacking motion blur"
)


# ============================================================
# Aspect ratio → recommended pixel size
# ============================================================

RATIO_TO_SIZE = {
    "3:4": "1024x1536",
    "16:9": "1536x1024",
    "9:16": "1024x1536",  # mobile portrait uses same vertical resolution
    "1:1": "1024x1024",
}


def build_prompt(category: str, media: str, subject: str, ratio: str) -> dict:
    """Assemble positive and negative prompts for the chosen category and media."""
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")

    cat_data = CATEGORIES[category]

    # Build positive prompts
    if media == "video":
        positive_zh = f"{cat_data['fixed_zh']}，{subject}，电影级动态"
        positive_en = f"{cat_data['fixed_en']}, {subject}, cinematic motion"
    else:
        positive_zh = f"{cat_data['fixed_zh']}，{subject}"
        positive_en = f"{cat_data['fixed_en']}, {subject}"

    # Build negative prompts
    if media == "video":
        negative_zh = NEGATIVE_BASE_ZH + NEGATIVE_VIDEO_ZH
        negative_en = NEGATIVE_BASE_EN + NEGATIVE_VIDEO_EN
    else:
        negative_zh = NEGATIVE_BASE_ZH
        negative_en = NEGATIVE_BASE_EN

    return {
        "category": category,
        "media": media,
        "ratio": ratio,
        "subject": subject,
        "positive_zh": positive_zh,
        "positive_en": positive_en,
        "negative_zh": negative_zh,
        "negative_en": negative_en,
        "recommended_size": RATIO_TO_SIZE.get(ratio, "1024x1024"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Build donghua 3D realistic style generation prompts.",
    )
    parser.add_argument(
        "--category",
        choices=list(CATEGORIES.keys()),
        required=True,
        help=(
            "主体分类：character-male男性角色，character-female女性角色，"
            "scene场景，weapon武器法宝，action战斗动作"
        ),
    )
    parser.add_argument(
        "--media",
        choices=["image", "video"],
        default="image",
        help="生成媒介：image=静态图片（默认），video=视频片段",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="主体描述，例如：冷峻的青年剑修，月下山巅",
    )
    parser.add_argument(
        "--ratio",
        choices=list(RATIO_TO_SIZE.keys()),
        default="3:4",
        help="画面比例：3:4竖版（默认）/ 16:9横版 / 9:16手机竖版 / 1:1方形",
    )
    args = parser.parse_args()

    result = build_prompt(args.category, args.media, args.subject, args.ratio)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()