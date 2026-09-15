---
name: guofeng-portrait
slug: guofeng-portrait
version: 3.0.0
description: 生成古风人像图像与短视频，只做人物。两个维度自由组合——画法：国漫 3D 写实 / 国风水墨写意；朝代形制：唐 / 宋 / 魏晋。适用于角色立绘、头像、人物海报。
author: 山鬼映画
category: 内容创作
tags:
  - 古风
  - 人像
  - 唐制
  - 宋制
  - 魏晋
  - 国漫
  - 3D写实
  - 水墨
  - 仙侠
  - guofeng
  - portrait
triggers:
  - 古风人像
  - 古风头像
  - 古风美人
  - 唐制美人
  - 宋韵美人
  - 魏晋风骨
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

生成**古风人像**（角色立绘、头像、人物海报）的图像与短视频。
**这是一个纯人像 skill —— 只画人**，不做场景概念图、器物法宝、花鸟山水。
人物所处的环境只作为背景服务于人像。

两个**正交维度**，自由组合：**画法**（怎么画）× **朝代**（画哪个年代的形制）。
"宋韵美人的水墨画法" = `--style ink-wash` + `dynasties/song/`。

## 维度一：画法（必选）

| 风格 | 对标作品 / 质感来源 | 特征 | 目录 |
|---|---|---|---|
| **`3d-realistic`** 国漫 3D 写实 | 斗罗大陆、斗破苍穹、灵笼、完美世界、一念永恒 | UE5 电影级渲染、皮肤毛孔与发丝可见、仙侠光效、体积光 | `styles/3d-realistic/` |
| **`ink-wash`** 国风水墨写意 | 大鱼海棠、中国奇谭、天书奇谭、山水情 | 手绘笔触、宣纸质感、极致留白、写意而非写实 | `styles/ink-wash/` |
| **`film-ambient`** 古风氛围胶片人像 | 日系胶片扫描 × 东方电影摄影、真人抓拍 | 低饱和青绿月白、侧逆光斑驳树影、胶片颗粒、清冷易碎情绪 | `styles/film-ambient/` |

三种画法的提示词体系**互不相通**——一个讲渲染与材质，一个讲笔触与留白，
一个讲摄影语言与胶片质感，所以各自保留完整的一套 references / examples /
assets / build_prompt.py，本文只做路由。
**混用三套关键词，会让画面同时不像 3D、不像水墨、也不像照片。**

## 维度二：朝代形制（可选，但强烈建议指定）

不指定朝代时，模型画出来的"汉服"多半是杂糅形制——各朝代的衣领、袖型、
腰线混在一起，懂的人一眼看出不对。指定朝代能拿到具体的服饰 token 与配色。

| 朝代 | 审美核心 | 适合 | 目录 |
|---|---|---|---|
| **`tang`** 唐 | 华贵丰腴、色彩浓烈 | 宫廷仕女、盛世气象 | `dynasties/tang/` |
| **`song`** 宋 | "淡到极致才是宋韵"，清雅低饱和 | 江南园林、庭院、肖像特写 | `dynasties/song/`（最完整） |
| **`wei-jin`** 魏晋 | 飘逸出尘、褒衣博带 | 名士、洛神、松下抚琴 | `dynasties/wei-jin/` |

用法：读 `dynasties/<朝代>/SKILL.md` 取服饰形制与配色 token，拼进 `--subject`。
每个朝代目录下：

- `SKILL.md` — 该朝代的人物 / 服饰 / 色彩 / 气质定义
- `references/scene-matrix.md` — 场景 × 人物的组合矩阵（宋另有 `style-tokens.md` 服饰 token 速查、`prompt-core.md`）
- `scripts/generate.py` — 直接调 museav 出图的 wrapper（与 `scripts/build_prompt.py` 是两条路：前者出图，后者只出提示词）

跨朝代通用的 4 段式骨架（主体 + 场景 + 光影 + 质感）在
`dynasties/common-prompt-base.md`，三个朝代只在服饰 / 色彩 / 气质上分支。

## When to Use This Skill

- "画个古风人像 / 古风头像"
- "斗罗大陆风格的剑修" / "灵笼风格的角色"
- "水墨风格的白衣书生" / "写意人物画"
- "Chinese 3D donghua portrait" / "ink wash portrait"
- 任何「古风 / 仙侠 / 国风」+ 人物 + 出图的请求

**不适用**：纯场景概念图、器物法宝特写、花鸟山水、无人物的意境图 —— 这个 skill 不做这些。

## Required Decisions Before Generating

1. **风格**（最重要，先问这个）
   - `3d-realistic` — 想要电影感、写实、有光效 → 默认
   - `ink-wash` — 想要手绘感、留白、意境
   - `film-ambient` — 想要**真人实拍感、氛围感、胶片质感**（"像照片，不像画"）

2. **题材**
   - `3d-realistic`：`character-male` / `character-female`
   - `ink-wash`：`character`
   - `film-ambient`：六个槽位 `--scene` / `--light` / `--mood` / `--film` /
     `--shot` / `--era`，先 `--list` 看全部取值
     （默认：竹林庭院 + 斑驳树影 + 安静疏离 + Pro 400H + 抓拍半身）

3. **朝代**（可选）：`tang` / `song` / `wei-jin`，不指定则不加朝代形制约束

4. **媒介**：`image`（默认）/ `video`

5. **画幅**：`3:4` 人像立绘（默认）/ `9:16` 手机壁纸 / `16:9` 横构图 / `1:1` 头像

6. **主体描述**：要具体，例如「冷峻的青年剑修，月下山巅，黑色长发高束」。

## Workflow

### Step 1 — 确认输入

风格、题材、媒介、画幅、主体描述。用户只说"画个古风人像"时，
按 `3d-realistic` + `character-male` + `image` + `3:4` 走。

### Step 2 — 构建提示词

```bash
# 3d-realistic / ink-wash：单命令
python scripts/build_prompt.py --style <3d-realistic|ink-wash> \
  --subject "<主体描述>" \
  --category <见上方题材> \
  --ratio <3:4|16:9|9:16|1:1> \
  [--media image]

# film-ambient：六个槽位，默认值已是最通用的起点
python scripts/build_prompt.py --style film-ambient \
  --subject "<主体描述>" \
  --scene <bamboo-garden|snow-court|lakeside-dusk|...> \
  --light <dappled-sun|snow-diffuse|bamboo-leak|...> \
  --mood <quiet-aloof|fragile|wistful|...> \
  --film <pro400h|portra400|superia|cinestill800t|none> \
  --shot <candid-half|candid-close|candid-turned|...> \
  --era <none|song|tang|wei-jin> \
  --ratio 3:4
```

不带 `--style` 默认 `3d-realistic`。输出是 JSON，取 `positive_en` 或
`positive_zh`（Seedream / qwen-image 这类中文理解强的模型用后者）。

**`film-ambient` 额外说明**：首选 **GPT Image 2.5**，用 `positive_en`（英文更稳）；
出图必须`--ref` 垫图锁脸，否则每次换人 —— 详见
`styles/film-ambient/references/model-recommendations.md`。该风格另有端到端 wrapper
（整理提示词 → 出图 → 落盘）：

```bash
./styles/film-ambient/scripts/generate.py \
  --subject "<主体描述>" --scene bamboo-garden --light dappled-sun \
  --film pro400h --mood quiet-aloof --shot candid-half --era song \
  --ref ~/refs/face-anchor.jpg
```

### Step 3 — 参考已有示例

脚本跑不了、或用户要更具体的风格时，翻对应风格的示例：

- `styles/3d-realistic/examples/character-male|character-female/` — 英文提示词
- `styles/3d-realistic/examples-zh/characters/` — 中文提示词，更细
- `styles/3d-realistic/prompt-library-zh.md` — 中文人像提示词库全文（关键词、镜头、公式、避坑）
- `styles/ink-wash/examples/character/` — 水墨人物示例
- `styles/film-ambient/examples/portrait/bamboo-candid.md` — **手写基准范例**
  （竹林抓拍 · 宋韵青绿），含完整中英提示词与"这张为什么是对的"逐条拆解

每个示例都带完整提示词（中英）、参考图、推荐画幅、调风格的注意事项。

### Step 4 — 合并负面词

`ImageGen` / `VideoGen` 没有独立的 negative 字段，把负面词用 "Avoid:" 拼进提示词末尾。
完整清单在各风格的 `references/negative-prompts.md` —— **三份不能混用**：
3D 风格要避开水墨和 2D，水墨风格要避开 3D 渲染和照片写实，
`film-ambient` 要避开影楼味、仙侠光效和塑料磨皮（它反过来**要**"照片写实 + 胶片质感"）。

负面词**别堆成 60 个词的长列表** —— 模型对超长清单的响应会衰减，
部分词反而会把概念"拉"进画面。8 组高价值词就够，脚本输出的已压缩过。

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

## 三种风格的硬规则

**`3d-realistic`**
- 绝不混入 2D 水彩 / 赛璐璐 / 平涂卡通 —— 它是纯 3D 渲染
- 不要现代元素（汽车、手机、现代建筑）
- 手部要明确写「解剖正确的手，五指」——模型极易画坏
- 发丝要写「根根分明」，否则出塑料感
- 服装形制别含糊 —— 指定朝代后用 `dynasties/<朝代>/` 里的具体 token
  （如宋制的 `sheer silk beizi` 薄纱褙子），别只写「汉服」
- 环境只做背景：写「背景虚化」「浅景深」，别让场景抢走主体

**`ink-wash`**
- 留白是构图的一部分，不是没画完 —— 提示词里要主动要求留白
- 绝不要 3D 渲染 / 照片写实 / 厚涂 —— 那会毁掉写意
- 笔触要可见（飞白、湿墨晕染），细节见 `styles/ink-wash/references/brush-techniques.md`

**`film-ambient`**
- **它要"像照片"**：绝不要写 "render / illustration / anime"，负面词必须带影楼味、
  仙侠光效、塑料皮肤三组 —— 这三样是它最大的敌人
- **光必须有来源**：树叶、雪、灯笼、夕阳、窗户。说不出光源的光不要；
  **正面平光是"影楼味"的第一来源，永不使用**
- **必须垫图锁脸**：提示词锁不住脸，不 `--ref` 就会每次换人 —— 这是"不稳定"的最大来源
- **姿态要"被抓拍"**：静态内敛（倚 / 趴 / 蹲坐 / 回眸 / 仰望 / 垂眸），
  一句"像摄影师突然叫住她的一瞬间"比"自然、放松、不摆拍"三个词都有效
- **前景必须有一层遮挡**：花枝 / 竹叶 / 雪 / 落瓣 / 灯笼 / 剑 —— 没有前景 = 平面 = 影楼感
- **色彩只有三个色**：雾白 / 灰青 / 烛金，红色只留在唇；阴影是**灰绿**，不是死黑
- **用胶片型号当锚点**：具体型号名（`pro400h` / `portra400` / `cinestill800t`）
  同时锁定色彩倾向、宽容度、高光行为与颗粒粗细，比"胶片质感 / film grain"这类泛词硬得多；
  一次只用一个型号，混用会让模型两头不靠
- 一次只换两个槽位，光型和机位别同时调（一次全换 = 重新抽卡）

## 参考资料

| 文件 | 内容 |
|---|---|
| `styles/<风格>/references/visual-dna.md` | 该风格的完整视觉定义、配色、光影规则 |
| `styles/<风格>/references/negative-prompts.md` | 负面词清单（**两风格不通用**） |
| `styles/<风格>/references/model-recommendations.md` | 各模型（Seedream / GPT-image / qwen / MJ）的调法 |
| `styles/3d-realistic/references/camera-lenses.md` | 镜头、焦段、布光配方（特写 / 半身 / 全身） |
| `styles/ink-wash/references/brush-techniques.md` | 笔法、墨法、宣纸质感 |
| `styles/film-ambient/references/visual-dna.md` | **本画法的七维审美指纹**（色彩 / 光 / 质感 / 构图 / 造型 / 情绪 / 抓拍感） |
| `styles/film-ambient/references/light-patterns.md` | 7 种光型库（斑驳树影 / 雪天散射 / 竹叶漏光 / 灯火 / 暮色逆光 / 提灯 / 冷调窗光） |
| `styles/film-ambient/references/camera-recipes.md` | 焦段机位配方 + 抓拍姿态库 + 构图三规则 |
| `styles/film-ambient/assets/gallery-9grid.jpg` | **标杆九宫格** —— 出图偏离这张太远时回 visual-dna 比对 |
| `dynasties/common-prompt-base.md` | 跨朝代通用 4 段式骨架 |
| `dynasties/<朝代>/SKILL.md` | 该朝代的服饰 / 色彩 / 气质定义 |
| `styles/ink-wash/SKILL-original.md` | 水墨 skill 合并前的独立版本（保留备查） |
| `dynasties/README-original.md` | 古风美人 skill 集合并前的独立版本（保留备查） |
