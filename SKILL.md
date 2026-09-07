---
name: guofeng-portrait
slug: guofeng-portrait
version: 2.0.0
description: 生成古风人像图像与短视频。两种风格：国漫 3D 写实（斗罗大陆/斗破苍穹/灵笼/完美世界）与国风水墨写意（大鱼海棠/中国奇谭/天书奇谭）。适用于角色立绘、头像壁纸、宣传海报。
author: 山鬼映画
category: 内容创作
tags:
  - 古风
  - 人像
  - 国漫
  - 3D写实
  - 水墨
  - 仙侠
  - guofeng
  - portrait
triggers:
  - 古风人像
  - 古风头像
  - 国漫风格
  - 国漫3D
  - 灵笼风格
  - 斗破风格
  - 国风水墨
  - 水墨人物
  - 写意人物
  - donghua portrait
  - ink wash portrait
  - guofeng portrait
homepage: https://github.com/webkubor/guofeng-portrait-skill
license: MIT
permissions:
  - image_generation
  - video_generation
---

# 古风人像 / Guofeng Portrait

## Overview

生成**古风人像**（角色立绘、头像、海报）的图像与短视频，两种视觉风格：

| 风格 | 对标作品 | 特征 | 目录 |
|---|---|---|---|
| **`3d-realistic`** 国漫 3D 写实 | 斗罗大陆、斗破苍穹、灵笼、完美世界、一念永恒 | UE5 电影级渲染、皮肤毛孔与发丝可见、仙侠光效、体积光 | `styles/3d-realistic/` |
| **`ink-wash`** 国风水墨写意 | 大鱼海棠、中国奇谭、天书奇谭、山水情 | 手绘笔触、宣纸质感、极致留白、写意而非写实 | `styles/ink-wash/` |

两种风格的提示词体系**互不相通**——一个讲渲染与材质，一个讲笔触与留白，
所以各自保留完整的一套 references / examples / assets / build_prompt.py，
本文只做路由。**混用两套关键词会让画面既不像 3D 也不像水墨。**

主线是**人像**；场景、器物、自然、诗意题材的素材一并保留，用作人像的配景
（人像需要环境，删掉是净损失），但不是这个 skill 的主打。

## When to Use This Skill

- "画个古风人像 / 古风头像"
- "斗罗大陆风格的剑修" / "灵笼风格的角色"
- "水墨风格的白衣书生" / "写意人物画"
- "Chinese 3D donghua portrait" / "ink wash portrait"
- 任何「古风 / 仙侠 / 国风」+ 人物 + 出图的请求

## Required Decisions Before Generating

1. **风格**（最重要，先问这个）
   - `3d-realistic` — 想要电影感、写实、有光效 → 默认
   - `ink-wash` — 想要手绘感、留白、意境

2. **题材**（两种风格的取值不同）
   - `3d-realistic`：`character-male` / `character-female` / `scene` / `weapon` / `action`
   - `ink-wash`：`character` / `creature` / `nature` / `poetry` / `scene`

3. **媒介**：`image`（默认）/ `video`

4. **画幅**：`3:4` 人像立绘（默认）/ `9:16` 手机壁纸 / `16:9` 横构图 / `1:1` 头像

5. **主体描述**：要具体，例如「冷峻的青年剑修，月下山巅，黑色长发高束」。

## Workflow

### Step 1 — 确认输入

风格、题材、媒介、画幅、主体描述。用户只说"画个古风人像"时，
按 `3d-realistic` + `character-male` + `image` + `3:4` 走。

### Step 2 — 构建提示词

```bash
python scripts/build_prompt.py --style <3d-realistic|ink-wash> \
  --subject "<主体描述>" \
  --category <见上方题材> \
  --ratio <3:4|16:9|9:16|1:1> \
  [--media image]
```

不带 `--style` 默认 `3d-realistic`。输出是 JSON，取 `positive_en` 或
`positive_zh`（Seedream / qwen-image 这类中文理解强的模型用后者）。

### Step 3 — 参考已有示例

脚本跑不了、或用户要更具体的风格时，翻对应风格的示例：

- `styles/3d-realistic/examples/` — 英文提示词，按题材分目录
- `styles/3d-realistic/examples-zh/` — 中文提示词，更细
- `styles/3d-realistic/prompt-library-zh.md` — 中文提示词库全文（关键词、公式、避坑）
- `styles/ink-wash/examples/` — 水墨示例

每个示例都带完整提示词（中英）、参考图、推荐画幅、调风格的注意事项。

### Step 4 — 合并负面词

`ImageGen` / `VideoGen` 没有独立的 negative 字段，把负面词用 "Avoid:" 拼进提示词末尾。
完整清单在各风格的 `references/negative-prompts.md` —— **两份不能混用**：
3D 风格要避开水墨和 2D，水墨风格要避开 3D 渲染和照片写实。

### Step 5 — 告知消耗

- ImageGen 人像：约 5-10 积分/张
- ImageGen 横构图：约 8-12 积分/张
- VideoGen：约 50-100 积分 / 5 秒

超过 10 积分先让用户确认。

### Step 6 — 生成

**图片** `ImageGen`：`size` 映射 `3:4`→`1024x1536`、`16:9`→`1536x1024`、
`9:16`→`1024x1536`、`1:1`→`1024x1024`；`quality` 草稿用 `medium`，定稿用 `high`（贵约 3 倍）。

**视频** `VideoGen`：`resolution` 默认 `720P`，`seconds` 默认 5。

### Step 7 — 呈现

用 `present_files` 把结果给用户看。

## 两种风格的硬规则

**`3d-realistic`**
- 绝不混入 2D 水彩 / 赛璐璐 / 平涂卡通 —— 它是纯 3D 渲染
- 不要现代元素（汽车、手机、现代建筑）
- 手部要明确写「解剖正确的手，五指」——模型极易画坏
- 发丝要写「根根分明」，否则出塑料感
- 服装写「形制统一的汉服 / 战袍」避免年代混搭

**`ink-wash`**
- 留白是构图的一部分，不是没画完 —— 提示词里要主动要求留白
- 绝不要 3D 渲染 / 照片写实 / 厚涂 —— 那会毁掉写意
- 笔触要可见（飞白、湿墨晕染），细节见 `styles/ink-wash/references/brush-techniques.md`

## 参考资料

| 文件 | 内容 |
|---|---|
| `styles/<风格>/references/visual-dna.md` | 该风格的完整视觉定义、配色、光影规则 |
| `styles/<风格>/references/negative-prompts.md` | 负面词清单（**两风格不通用**） |
| `styles/<风格>/references/model-recommendations.md` | 各模型（Seedream / GPT-image / qwen / MJ）的调法 |
| `styles/3d-realistic/references/camera-lenses.md` | 镜头、焦段、布光配方 |
| `styles/ink-wash/references/brush-techniques.md` | 笔法、墨法、宣纸质感 |
| `styles/ink-wash/SKILL-original.md` | 水墨 skill 合并前的独立版本（保留备查） |
