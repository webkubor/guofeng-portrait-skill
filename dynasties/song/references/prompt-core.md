# 宋 · Prompt 核心词组库

> 这是从 SKILL.md「宋韵核心 5 元素」展开的**可直接复用的词组库**。每个 token 列出英文 + 中文，agent 出图时挑 1-2 个组合进 prompt。
> 来源：调参几十组 + 永泰公主墓壁画（对比）+ 南宋黄昇墓实物 + 顾恺之《女史箴图》。

---

## 1. 人物 · Prompt Token

### 发型（一定要「低盘 + 碎发 + 素簪」组合）
| Token | 中文 |
|-------|------|
| `low chignon with loose strands` | 低盘发 + 几缕碎发 |
| `low twisted bun with wispy fringe` | 低盘髻 + 细碎刘海 |
| `low knotted hair, two wisps falling by the temples` | 低盘发 + 鬓边两缕碎发 |
| `simple jade hairpin, minimal ornamentation` | 一支素色玉簪，极简 |
| `no headpiece, only a wooden hairpin` | 无头饰，只有木簪 |

### 服饰（褙子为主，**不要大袖蓬蓬**）
| Token | 中文 |
|-------|------|
| `sheer silk beizi (Song dynasty outer robe)` | 薄纱褙子（宋代外衫） |
| `cross-collared beizi in sheer silk gauze` | 对襟褙子，薄丝绸纱感 |
| `pleated inner robe (jiaoling) under sheer beizi` | 交领内衫 + 薄纱褙子 |
| `unlined silk, light and flowing` | 无里丝，轻盈飘逸 |
| `soft cream / oat / moonwhite base color` | 米白 / 燕麦 / 月白底色 |

### 神态（"松弛感"是古意来源）
| Token | 中文 |
|-------|------|
| `soft smile gazing into the distance` | 浅笑望向远方 |
| `relaxed sideways glance, half-lidded eyes` | 放松的侧目，眼睑半垂 |
| `serene, almost meditative expression` | 安宁、近乎入定的表情 |
| `wind tugging at the sleeve` | 风拂过衣袂 |
| `half-leaned against the pillar, weight on one hip` | 半倚在柱上，重心在一侧髋 |

---

## 2. 场景 · Prompt Token

### 空间（永远只取「一角」，不要全景）
| Token | 中文 |
|-------|------|
| `corner of waterside pavilion (langting)` | 廊亭水榭的一角 |
| `scholar's garden in Suzhou/Hangzhou` | 苏州/杭州文人之园 |
| `half-covered wooden walkway by a lotus pond` | 荷塘边被遮半面的木廊 |
| `open window of a study, soft daylight` | 书房半开的窗，柔日光 |
| `covered corridor with light filtering through lattice` | 透光格栅的回廊 |

### 前景遮挡（必带，遮约 1/4 画面）
| Token | 中文 |
|-------|------|
| `lotus leaf in foreground framing the scene` | 前景荷叶取景框 |
| `drooping willow branch at top corner` | 画面顶部垂柳枝 |
| `carved wooden balustrade in foreground` | 前景雕花木栏杆 |
| `bamboo screen partially revealing figure` | 半遮的竹帘露人身 |
| `lotus stem cutting diagonally across frame` | 莲梗斜穿画面 |

### 远景（朦胧水墨，不要清晰细节）
| Token | 中文 |
|-------|------|
| `soft silhouette of distant pavilions` | 远景亭台柔和剪影 |
| `water-reflected light, blurred` | 水面反光，模糊化 |
| `distant mountain in ink-wash mist` | 远山水墨雾气 |
| `trees reflected on still pond surface` | 静水面倒树影 |
| `moon half-obscured by thin cloud` | 薄云遮半月 |

---

## 3. 光影 · Prompt Token

| Token | 中文 | 用法 |
|-------|------|------|
| `soft golden backlight at dusk` | 傍晚柔和金色逆光 | 主光 |
| `rim light on hair and hem` | 发梢衣边柔光金边 | 镶边效果 |
| `thin atmospheric haze, low contrast` | 薄雾漫射，低对比 | 压 AI 塑料感 |
| `warm apricot + lotus-leaf green palette` | 暖杏 + 荷绿色系 | 统一色调 |
| `soft window light from left` | 左侧柔窗光 | 室内场景用 |
| `dappled light through tree canopy` | 树冠筛下斑驳光斑 | 园林场景用 |

---

## 4. 质感 · Prompt Token

| Token | 中文 | 用法 |
|-------|------|------|
| `85mm portrait lens` | 85mm 人像镜头 | 必带 |
| `low saturation, no high-saturation colors` | 低饱和，不要高饱和色 | 必带 |
| `subtle film grain, museum-quality composition` | 细微胶片颗粒，博物馆级构图 | 必带 |
| `realistic skin texture, no AI plastic look` | 真实皮肤纹理，无 AI 塑料感 | 反 AI |
| `unlined silk, visible weave` | 无里丝，可见织纹 | 宋制工艺细节 |

---

## 5. 反面清单（直接过滤）

```
-filter --exclude "8k, 4k, trending on artstation, unreal engine, octane render, hyperrealistic, 3d render, plastic skin, glossy, anime, illustration, painting, sketch, vibrant colors, oversaturated"
```

agent 出图时建议：
- 把以上 token 加到 negative prompt（如支持）
- 或者在主体 prompt 里**避免出现**这些词

---

## 6. 完整 Prompt 模板（宋韵最终版，可直接复制用 `museav gen`）

```
Southern Song Dynasty noblewoman, [人物姿态: leaning on wooden rail of waterside pavilion in scholar's garden / sitting by open window reading / plucking plum branch / pouring tea], low chignon with loose strands at temples and simple jade hairpin, sheer silk beizi (Song outer robe) in oat / moonwhite, soft cream inner robe underneath, relaxed sideways glance half-lidded, soft serene expression, [场景: Jiangnan scholar's garden / waterside pavilion corner / wooden corridor / lotus pond], foreground [前景遮挡: lotus leaf / willow branch / wooden balustrade / bamboo screen] partially framing the figure, half the frame left as breathing empty space, distant pavilions and lotus pond in soft misty silhouette, soft golden backlight at dusk creating rim light on hair and hem, thin atmospheric haze softening all shadows, realistic skin texture, 85mm portrait lens, low saturation palette of warm apricot and lotus-leaf green, subtle film grain, museum-quality composition
```

---

## 7. 完整 Negative Prompt（宋韵版）

```
anime, illustration, painting, sketch, 3d render, cgi, plastic skin, glossy skin, airbrushed, oversaturated, vibrant neon colors, heavy makeup, modern hairstyle, western dress, fantasy armor, blurry eyes, extra fingers, mutated hands, deformed face, text, watermark, low quality, worst quality, blurry, jpeg artifacts
```

---

## 8. 调参经验笔记（TODO 待补充）

> 你之前「反复调了几十组参数摸透稳出逻辑」的**具体参数**（model / sampler / steps / CFG / seed / lora 权重）还没写进来。等你**贴 1-2 个跑成功过的完整 prompt + 输出图**，我直接结构化进本文件。

预期包含：
- museav / MJ / SD 各家适配
- steps / cfg 推荐值
- 哪些 seed 区间稳
- 任何反 AI 塑料感的负面 prompt 细节
