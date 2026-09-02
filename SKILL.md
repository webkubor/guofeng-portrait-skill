---
name: donghua-3d-realistic
slug: donghua-3d-realistic
version: 1.0.0
description: 生成国产 3D 动漫（斗罗大陆/斗破苍穹/灵笼/完美世界）写实风格的图像。适用于仙侠玄幻角色立绘、场景概念图、宣传海报、头像壁纸等。
author: 山鬼映画
category: 内容创作
tags:
  - 国漫
  - 3D写实
  - 仙侠
  - 玄幻
  - Donghua
  - 3D Anime
triggers:
  - 国漫风格
  - 国漫3D
  - 灵笼风格
  - 斗破风格
  - donghua style
  - 国漫仙侠
  - generate donghua image
homepage: https://github.com/webkubor/donghua-3d-skill
license: MIT
permissions:
  - image_generation
  - video_generation
---

# 国漫 3D 写实风格 / Donghua 3D Realistic

## Overview

Generate still images or short videos in the visual style associated with mainstream Chinese 3D donghua (animated series) such as *Douluo Dalu* (斗罗大陆), *Doupo Cangqiong* (斗破苍穹), *Ling Long* (灵笼), *Wanmei Shijie* (完美世界), and *Yinian Yongheng* (一念永恒).

The style is characterized by:
- **High-end Unreal Engine 5 / PBR cinematic render** with cinematic 3D lighting
- **Next-gen character render** with visible skin pores, hair strands, and material reflections
- **Xianxia / xuanhuan fantasy aesthetics** with Eastern color palettes
- **Atmospheric particles, volumetric light, motion effects** to convey cultivation and spiritual energy
- **Cinematic depth of field**, golden hour rim light, back-lit silhouettes

Always confirm whether the user wants a **character portrait**, **scene/environment**, **weapon/artifact**, or **action/battle** shot before generating.

## When to Use This Skill

Use this skill when the user asks for anything like:
- "用国漫 3D 风格生成一张图"
- "斗罗大陆风格的剑修"
- "灵笼风格的角色"
- "完美世界风格的海报"
- "Chinese 3D donghua style"
- "Doupo style swordsman portrait"
- Any request involving Chinese 3D anime / xianxia / xuanhuan content combined with image generation.

## Required Decisions Before Generating

1. **Subject category**
   - `character-male` — swordsman, sect master, demon lord, young hero, old master
   - `character-female` — immortal fairy, enchantress, demoness, female warrior, maiden
   - `scene` — sect mountain gate, cultivation cave, ancient battlefield, heavenly realm, bamboo forest
   - `weapon` — flying sword, demon blade, spirit pearl, mystical instrument
   - `action` — battle slash, spell casting, flying technique, cultivation breakthrough

2. **Media**
   - `image` — static picture
   - `video` — short AI-generated video clip
   - If only "content" or "visual" is mentioned, default to `image`.

3. **Aspect ratio**
   - `3:4` (portrait) — character portraits, posters
   - `16:9` (landscape) — scenes, panoramas, action shots
   - `9:16` (mobile portrait) — wallpapers, mobile-optimized posters
   - `1:1` (square) — weapon showcases, avatars

4. **Subject description**
   - Always ask for concrete subject, e.g. "冷峻的青年剑修，月下山巅"
   - Or accept existing prompt and re-style it.

## Workflow

### Step 1 — Gather Inputs

Confirm the user's choices:
- Subject category (see above)
- Media: image or video
- Aspect ratio
- Subject description (Chinese or English)

### Step 2 — Build the Prompt

Run the bundled prompt builder script from the skill root directory:

```bash
python scripts/build_prompt.py \
  --subject "<subject description>" \
  --category <character-male|character-female|scene|weapon|action> \
  --ratio <3:4|16:9|9:16|1:1> \
  [--media image]
```

Example:

```bash
python scripts/build_prompt.py \
  --subject "冷峻的青年剑修，月下山巅，黑色长发高束" \
  --category character-male \
  --ratio 3:4
```

Capture the JSON output. Use the language that best matches the user's request:
- Prefer `positive_en` for most generation models.
- Use `positive_zh` if the model explicitly supports strong Chinese prompt understanding (e.g. Seedream, qwen-image).

### Step 3 — Use Reference Examples

If the script cannot be executed, or the user wants a more specific style, browse the `examples/` directory for hand-crafted prompts grouped by category:

- `examples/character-male/` — male character prompts (swordsman, sect master, demon lord)
- `examples/character-female/` — female character prompts (fairy, enchantress, warrior)
- `examples/scene/` — environment prompts (sect gate, cave, battlefield)
- `examples/weapon/` — weapon/artifact prompts (sword, blade, pearl)
- `examples/action/` — battle/action prompts

Each example includes:
- The full prompt (Chinese + English versions)
- The accompanying reference image
- Recommended aspect ratio
- Notes on style tweaks

### Step 4 — Merge Negative Terms

The `ImageGen` and `VideoGen` tools do not expose a separate negative-prompt field. Append the relevant negative terms directly into the prompt with "avoid" or "no" phrasing:

```text
<positive prompt>. Avoid: traditional 2D anime, watercolor, ink wash, cel-shading, flat cartoon, modern elements, smartphones, cars, Western fantasy armor, oversized weapons, deformed hands, plastic skin...
```

The full negative prompt list lives in `references/negative-prompts.md`.

### Step 5 — Inform User About Credits

Before calling generation tools, tell the user:
- ImageGen (portrait): roughly 5-10 credits per image.
- ImageGen (landscape/panorama): roughly 8-12 credits per image.
- VideoGen: roughly 50-100 credits per 5-second video.

### Step 6 — Generate

For **images**, call `ImageGen`:
- `prompt`: the assembled prompt.
- `size`: map `3:4` → `1024x1536`, `16:9` → `1536x1024` (or `1024x576` for low-cost), `9:16` → `1024x1536`, `1:1` → `1024x1024`.
- `quality`: `medium` for drafts, `high` for final renders (high costs ~3× more credits).

For **videos**, call `VideoGen`:
- `prompt`: the assembled prompt.
- `resolution`: `720P` default; use `1080P` only if the user requests higher resolution.
- `seconds`: default to 5 unless the user specifies otherwise.

### Step 7 — Present the Result

Use `present_files` to show the generated image or video to the user.

## Style DNA (核心视觉基因)

The style DNA is fully documented in `references/visual-dna.md`. Key pillars:

1. **Cinematic UE5 render** — Nanite geometry, Lumen global illumination, PBR materials
2. **Visible micro-detail** — skin pores, individual hair strands, fabric weave, metal reflections
3. **Xianxia color palette** — ice blue, deep red, jade green, royal gold, ink black, misty white
4. **Atmospheric effects** — volumetric fog, spiritual light particles, sword qi, glowing auras
5. **Cinematic lighting** — golden hour rim light, back-lit silhouettes, volumetric god rays, Rembrandt lighting
6. **Dynamic motion** — flowing hair, billowing robes, dynamic poses, particle trails

## Reference Materials

- `references/visual-dna.md` — Full visual definition, color palette, lighting rules
- `references/camera-lenses.md` — Camera, lens, focal length, and lighting recipes
- `references/negative-prompts.md` — Complete negative prompt checklist
- `references/model-recommendations.md` — Model-specific tweaks (Seedream / GPT-image / qwen / Midjourney)
- `examples/` — Hand-crafted prompt examples grouped by category with reference images

## Important Style Rules

- **Never mix 2D watercolor / cel-shading** — this skill is strictly 3D rendered.
- **Keep Eastern aesthetics** — no modern elements (cars, smartphones, modern buildings).
- **Hand correctness** — explicitly request "anatomically correct hands, five fingers" since AI models commonly deform them.
- **Hair detail** — request "individual hair strands visible" to avoid plastic look.
- **Clothing consistency** — request "historically consistent hanfu / warrior robes" to avoid anachronism.
- **Weapon proportions** — request "proportionally correct weapons" since swords tend to be too long or too short.

## Output Defaults

Default behavior when the user provides only a vague request ("generate a donghua image"):
- Category: `character-male` (most common starting point)
- Media: `image`
- Aspect ratio: `3:4` (portrait, best for character)
- Quality: `medium` (cost-conscious default)

Ask the user to confirm before generating if cost > 10 credits.