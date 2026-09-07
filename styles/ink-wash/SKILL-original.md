---
name: guoman-ink-wash
slug: guoman-ink-wash
version: 1.0.0
description: 生成中国传统水墨画（国风水墨）风格的图像与视频。适用于人物、山水、花鸟、诗意场景、传统题材。强调手绘笔触、留白、意境。
author: 山鬼映画
category: 内容创作
tags:
  - 国漫
  - 水墨
  - 写意
  - 国画
  - 古风
  - Chinese ink wash
  - shuimo
triggers:
  - 国风水墨
  - 水墨风格
  - 中国画
  - 写意山水
  - ink wash style
  - Chinese painting
  - 国画风格
  - generate ink wash
homepage: https://github.com/webkubor/guoman-ink-wash-skill
license: MIT
permissions:
  - image_generation
  - video_generation
---

# 国风水墨风格 / Chinese Ink Wash (Shuimo)

## Overview

Generate still images or short videos in the visual style of **Chinese traditional ink wash painting (水墨画 / 国画 / 写意)**. The style is characterized by:

- **手绘笔触** —— visible brush strokes, dry-brush breaks, wet blooms, ink wash splashing
- **宣纸质感** —— rice paper texture, paper fibers, aged paper hue
- **极致留白** —— vast negative space is part of the composition, not unused area
- **写意意境** —— ethereal atmosphere, poetic mood, restrained composition
- **2D 手绘** —— strictly 2D hand-painted, never 3D rendered
- **东方哲学** —— Zen-like simplicity, yin-yang balance, ink density variation

Style references include:
- 《大鱼海棠》(Big Fish & Begonia) - animated film, watercolor + ink
- 《中国奇谭》(Yao-Chinese Folk Tales) - 8 short films, traditional Chinese aesthetics
- 《天书奇谭》(Secrets of the Heavenly Book) - 1983 classic, ink wash animation
- 《小蝌蚪找妈妈》(Tadpoles Looking for Mama) - 1960, first Chinese ink animation
- 《山水情》(Feelings of Mountains and Waters) - 1988, pure ink animation masterpiece
- 《大闹天宫》(Havoc in Heaven) - 1961, traditional Chinese painting animation

## When to Use This Skill

Use this skill when the user asks for:
- "用水墨风格生成一张图"
- "中国画风格的山水"
- "国风水墨海报"
- "Chinese ink wash painting"
- "水墨动画风格"
- "传统国画"
- "中国奇谭风格"
- "大鱼海棠风格"
- "天书奇谭风格"
- Any request involving traditional Chinese painting, calligraphy aesthetic, or shuimo style image generation.

## Required Decisions Before Generating

1. **Subject category** (5 categories)
   - `character` — scholar, ancient lady, monk, child, hermit
   - `scene` — mountain landscape, river, temple, pavilion, garden
   - `nature` — bamboo, plum, orchid, lotus, crane, fish
   - `creature` — dragon, phoenix, tiger, crane in flight
   - `poetry` — moonlit night, snow scene, autumn mood, spring

2. **Ink treatment** (3 levels)
   - `light` — minimal ink, mostly empty paper, hint of brush
   - `medium` — balanced ink coverage, clear subject with atmosphere
   - `bold` — heavy ink, strong brush, dramatic composition

3. **Color palette** (3 options)
   - `monochrome` — pure black ink on white/cream paper
   - `accent-red` — monochrome with red plum blossoms, lips, ribbons
   - `accent-gold` — monochrome with gold dragon, seal stamps, calligraphy

4. **Media**
   - `image` — static picture (default)
   - `video` — short AI-generated video clip

5. **Aspect ratio**
   - `3:4` (portrait) — character, poetry cards
   - `16:9` (landscape) — scenes, mountain panoramas
   - `9:16` (mobile portrait) — wallpapers
   - `1:1` (square) — creature showcases, social posts

## Workflow

### Step 1 — Gather Inputs

Confirm the user's choices:
- Subject category
- Ink treatment level
- Color palette
- Media: image or video
- Aspect ratio
- Subject description (Chinese or English)

### Step 2 — Build the Prompt

Run the bundled prompt builder script from the skill root directory:

```bash
python scripts/build_prompt.py \
  --category <character|scene|nature|creature|poetry> \
  --subject "<subject description>" \
  --ink <light|medium|bold> \
  --color <monochrome|accent-red|accent-gold> \
  --ratio <3:4|16:9|9:16|1:1> \
  [--media image]
```

Example:

```bash
python scripts/build_prompt.py \
  --category scene \
  --subject "远山云雾，江上孤舟" \
  --ink light \
  --color monochrome \
  --ratio 16:9
```

Capture the JSON output. Use the language that best matches the user's request:
- Prefer `positive_en` for most generation models.
- Use `positive_zh` if the model explicitly supports strong Chinese prompt understanding (e.g. Seedream, qwen-image).

### Step 3 — Use Reference Examples

If the script cannot be executed, browse the `examples/` directory for hand-crafted prompts:

- `examples/character/` — scholar, lady, monk, hermit
- `examples/scene/` — mountain, river, temple, pavilion
- `examples/nature/` — bamboo, plum, orchid, crane
- `examples/creature/` — dragon, phoenix, tiger
- `examples/poetry/` — moonlit, snow, autumn, spring moods

Each example includes:
- The full prompt (Chinese + English)
- The accompanying reference image
- Recommended aspect ratio
- Notes on ink treatment

### Step 4 — Merge Negative Terms

The `ImageGen` and `VideoGen` tools do not expose a separate negative-prompt field. Append relevant negative terms with "avoid" phrasing:

```text
<positive prompt>. Avoid: 3D rendering, photorealistic, CGI, modern elements, cars, smartphones, Western architecture, neon lights, anime cel-shading, Pixar, Disney, plastic texture, harsh saturated colors, hard shadows...
```

Full negative prompt list: `references/negative-prompts.md`

### Step 5 — Inform User About Credits

Before calling generation tools, tell the user:
- ImageGen: roughly 5-10 credits per image.
- VideoGen: roughly 50-100 credits per 5-second video.

### Step 6 — Generate

For **images**:
- `prompt`: assembled prompt.
- `size`: `3:4` → `1024x1536`, `16:9` → `1536x1024`, `9:16` → `1024x1536`, `1:1` → `1024x1024`.
- `quality`: `medium` for drafts, `high` for finals.

For **videos**:
- `prompt`: assembled prompt.
- `resolution`: `720P` default.
- `seconds`: default 5.

### Step 7 — Present the Result

Use `present_files` to show the generated image or video.

## Style DNA (核心视觉基因)

The full DNA is documented in `references/visual-dna.md`. Key pillars:

1. **手绘笔触 (Hand-painted brushwork)** — visible strokes, dry-brush breaks, wet blooms
2. **宣纸质感 (Rice paper texture)** — paper fibers, aged hue, absorbent quality
3. **极致留白 (Vast negative space)** — open paper is part of composition
4. **墨色浓淡 (Ink density variation)** — from light wash to solid black
5. **诗意意境 (Poetic atmosphere)** — restrained, refined, contemplative
6. **东方哲学 (Eastern philosophy)** — Zen simplicity, yin-yang balance

## Reference Materials

- `references/visual-dna.md` — Full visual definition, ink levels, color palettes
- `references/brush-techniques.md` — Traditional brush stroke types and their visual results
- `references/negative-prompts.md` — Complete negative prompt checklist
- `references/model-recommendations.md` — Model-specific tweaks (Seedream / GPT-image / qwen)
- `examples/` — Hand-crafted prompts with reference images

## Important Style Rules

- **Never use 3D rendering** — this skill is strictly 2D hand-painted.
- **Never add modern elements** — no cars, modern buildings, smartphones, neon lights.
- **Embrace negative space** — vast empty areas are intentional and essential.
- **Restraint over abundance** — less is more, leave room for imagination.
- **Restrained color** — primarily monochrome, with limited color accents.
- **Hand-painted imperfection** — slight asymmetry and brush variation are features, not bugs.

## Output Defaults

When the user provides only a vague request ("generate an ink wash image"):
- Category: `scene` (most common)
- Ink: `medium`
- Color: `monochrome`
- Media: `image`
- Aspect ratio: `16:9` (landscape, suits ink wash style)

Ask the user to confirm before generating if cost > 10 credits.