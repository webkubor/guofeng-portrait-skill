#!/usr/bin/env python3
"""
Build prompts for the GuoMan Ink Wash (Chinese ink wash painting) style skill.

Supports five subject categories:
  - character : scholar, ancient lady, monk, hermit, child
  - scene     : mountain landscape, river, temple, pavilion, garden
  - nature    : bamboo, plum, orchid, lotus, crane, fish
  - creature  : dragon, phoenix, tiger, crane in flight
  - poetry    : moonlit night, snow scene, autumn mood, spring

Supports three ink treatment levels:
  - light  : minimal ink, vast negative space
  - medium : balanced ink coverage (default)
  - bold   : heavy ink, strong brush

Supports three color palettes:
  - monochrome    : pure black ink (default)
  - accent-red    : monochrome with red accents
  - accent-gold   : monochrome with gold accents

Supports two media types:
  - image : static image (default)
  - video : video clip

Supports four aspect ratios:
  - 3:4  (portrait)
  - 16:9 (landscape, default for ink wash)
  - 9:16 (mobile portrait)
  - 1:1  (square)

Example:
  python scripts/build_prompt.py \
      --category scene --subject "远山云雾，江上孤舟" \
      --ink light --color monochrome --ratio 16:9

Output is JSON written to stdout:
  {
    "category": "scene",
    "ink": "light",
    "color": "monochrome",
    "media": "image",
    "ratio": "16:9",
    "subject": "...",
    "positive_zh": "...",
    "positive_en": "...",
    "negative_zh": "...",
    "negative_en": "...",
    "recommended_size": "1536x1024"
  }
"""

import argparse
import json
import sys


# ============================================================
# Subject-category fixed prompt fragments
# ============================================================

CHARACTER = {
    "fixed_zh": (
        "中国传统水墨画，手绘毛笔笔触，宣纸纹理，"
        "墨色浓淡变化，大面积留白，写意风格，"
        "传统国画美学，诗意空灵，禅意；"
        "画中人是古典仕女：成年东方女性，清雅端庄的古典美人气质，"
        "鹅蛋脸，五官以简练笔触写意、不刻画过度，眉目疏朗，"
        "姿态含蓄（侧身、回眸、执扇、垂眸），衣纹线条流畅飘逸，"
        "不幼态、不网红、不浓妆"
    ),
    "fixed_en": (
        "traditional Chinese ink wash painting, hand-painted brushwork, "
        "rice paper texture, ink density variation, "
        "vast negative space, freehand aesthetic, "
        "traditional Chinese painting, poetic ethereal mood, Zen; "
        "the figure is a classical Chinese beauty (shinu): an adult East Asian woman with "
        "refined serene classical elegance, oval face, features suggested with economical "
        "brushwork rather than over-rendered, sparse graceful brows and eyes, "
        "a reserved pose (three-quarter turn, glancing back, holding a fan, lowered gaze), "
        "flowing concise drapery lines; not childlike, not an influencer face, no heavy makeup"
    ),
}





CATEGORIES = {
    "character-female": CHARACTER,
}


# ============================================================
# Ink treatment modifiers
# ============================================================

INK_MODIFIERS = {
    "light": {
        "zh": "淡墨为主，大量留白，仅极轻笔触，意境深远",
        "en": "light ink dominant, vast empty paper, minimal brushwork, deep atmosphere",
    },
    "medium": {
        "zh": "中墨平衡，主体清晰，意境与细节兼具",
        "en": "medium ink density, clear subject, balanced atmosphere and detail",
    },
    "bold": {
        "zh": "浓墨重彩，笔触强烈，对比鲜明，气势磅礴",
        "en": "bold heavy ink, strong brushwork, high contrast, epic grandeur",
    },
}


# ============================================================
# Color palette modifiers
# ============================================================

COLOR_MODIFIERS = {
    "monochrome": {
        "zh": "纯水墨，黑白为主，传统",
        "en": "pure monochrome, black ink on white paper, traditional",
    },
    "accent-red": {
        "zh": "水墨为主，朱砂点缀（梅花、唇色、丝带、印章）",
        "en": "monochrome base with vermillion red accents (plum blossoms, lips, ribbons, stamp)",
    },
    "accent-gold": {
        "zh": "水墨为主，金色点缀（龙鳞、印章、金线）",
        "en": "monochrome base with gold accents (dragon scales, seals, gold thread)",
    },
}


# ============================================================
# Negative prompts (universal + ink-wash specific)
# ============================================================

NEGATIVE_BASE_ZH = (
    "3D渲染，CGI，立体感，电影级光影，UE5，PBR材质，写实照片，"
    "日漫风格，赛璐璐，二次元眼睛，线稿风格，皮克斯，迪士尼，"
    "现代元素，手机，汽车，霓虹灯，高饱和度，糖果色，鲜艳色彩，"
    "均匀笔触，平滑边缘，完美对称，过多细节，画面拥挤，塑料质感，"
    "幼态，娃娃脸，童颜，网红脸，网红妆，浓妆，过度刻画五官，写实五官，萌系"
)

NEGATIVE_BASE_EN = (
    "3D rendering, CGI, photorealistic, digital painting, "
    "UE5, PBR materials, cinematic lighting, volumetric light, "
    "Japanese anime style, cel-shading, line art, anime eyes, "
    "Pixar, Disney, modern elements, smartphones, cars, neon lights, "
    "oversaturated colors, candy colors, bright primary colors, "
    "uniform brushstrokes, smooth edges, perfect symmetry, cluttered composition, plastic texture, "
    "childlike, baby face, influencer face, heavy makeup, over-rendered facial features, "
    "hyper-realistic facial rendering, moe style"
)

NEGATIVE_VIDEO_ZH = (
    "，动作僵硬，构图松散，缺少笔触感，画面过满"
)

NEGATIVE_VIDEO_EN = (
    ", stiff motion, loose composition, lacking brushwork feel, cluttered frame"
)


# ============================================================
# Aspect ratio → recommended pixel size
# ============================================================

RATIO_TO_SIZE = {
    "3:4": "1024x1536",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "1:1": "1024x1024",
}


def build_prompt(category: str, subject: str, ink: str, color: str, media: str, ratio: str) -> dict:
    """Assemble positive and negative prompts for the chosen category, ink, color."""
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    if ink not in INK_MODIFIERS:
        raise ValueError(f"Unknown ink level: {ink}")
    if color not in COLOR_MODIFIERS:
        raise ValueError(f"Unknown color palette: {color}")

    cat_data = CATEGORIES[category]
    ink_data = INK_MODIFIERS[ink]
    color_data = COLOR_MODIFIERS[color]

    # Build positive prompts
    if media == "video":
        positive_zh = (
            f"{cat_data['fixed_zh']}，{ink_data['zh']}，{color_data['zh']}，"
            f"{subject}，手绘水墨动态，传统诗意动画"
        )
        positive_en = (
            f"{cat_data['fixed_en']}, {ink_data['en']}, {color_data['en']}, "
            f"{subject}, hand-painted ink wash motion, traditional poetic animation"
        )
    else:
        positive_zh = (
            f"{cat_data['fixed_zh']}，{ink_data['zh']}，{color_data['zh']}，{subject}"
        )
        positive_en = (
            f"{cat_data['fixed_en']}, {ink_data['en']}, {color_data['en']}, {subject}"
        )

    # Build negative prompts
    if media == "video":
        negative_zh = NEGATIVE_BASE_ZH + NEGATIVE_VIDEO_ZH
        negative_en = NEGATIVE_BASE_EN + NEGATIVE_VIDEO_EN
    else:
        negative_zh = NEGATIVE_BASE_ZH
        negative_en = NEGATIVE_BASE_EN

    return {
        "category": category,
        "ink": ink,
        "color": color,
        "media": media,
        "ratio": ratio,
        "subject": subject,
        "positive_zh": positive_zh,
        "positive_en": positive_en,
        "negative_zh": negative_zh,
        "negative_en": negative_en,
        "recommended_size": RATIO_TO_SIZE.get(ratio, "1536x1024"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Build Chinese ink wash (shuimo) style generation prompts.",
    )
    parser.add_argument(
        "--category",
        choices=list(CATEGORIES.keys()),
        required=True,
        help="主题分类：character人物，scene山水场景，nature花鸟，creature瑞兽，poetry诗意",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="具体主体描述，例如：远山云雾，江上孤舟",
    )
    parser.add_argument(
        "--ink",
        choices=list(INK_MODIFIERS.keys()),
        default="medium",
        help="墨色浓淡：light淡墨（默认）/ medium中墨 / bold浓墨",
    )
    parser.add_argument(
        "--color",
        choices=list(COLOR_MODIFIERS.keys()),
        default="monochrome",
        help="色彩：monochrome纯水墨（默认）/ accent-red朱砂点缀 / accent-gold金色点缀",
    )
    parser.add_argument(
        "--media",
        choices=["image", "video"],
        default="image",
        help="生成媒介：image静态图片（默认），video视频片段",
    )
    parser.add_argument(
        "--ratio",
        choices=list(RATIO_TO_SIZE.keys()),
        default="16:9",
        help="画面比例：16:9横版（默认）/ 3:4竖版 / 9:16手机竖版 / 1:1方形",
    )
    args = parser.parse_args()

    result = build_prompt(args.category, args.subject, args.ink, args.color, args.media, args.ratio)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()