# 负面词清单 / Negative Prompts — film-ambient

> 负面词是"高级感"的另一半。**本清单与 `3d-realistic` / `ink-wash` 不通用** ——
> 那两套要避开的正是本画法要的东西（照片写实、胶片质感）。

---

## 1. 用法

`ImageGen` / `VideoGen` 没有独立的 negative 字段，把负面词用 `Avoid: ` 拼到提示词末尾：

```
<positive_en> ... Avoid: studio hanfu photoshoot, xianxia glow effects, anime, CGI, ...
```

**GPT Image 2.5 用英文版**（`--style film-ambient` 输出的 `negative_en`）。

> ⚠️ 不要堆成 60 个词的长列表。模型对超长负面清单的响应会衰减，
> 而且部分词反而会把概念"拉"进画面。**下表 8 组高价值词就够了**，
> `build_prompt.py` 输出的已经压缩过。

---

## 2. 高价值负面词组（8 组）

| 组 | 中文 | English | 治什么病 |
|---|------|---------|---------|
| **影楼味** | 影楼汉服写真，正经摆拍，证件照构图，正面平光 | studio hanfu photoshoot, stiff posing, ID-photo framing, flat frontal light | 摆拍感、"在演"、平光 |
| **仙侠味** | 仙侠玄幻光效，发光粒子，法阵，CG 感 | xianxia glow effects, glowing particles, magic circles, CGI | 廉价玄幻、塑料发光 |
| **二次元** | 二次元，3D 渲染，游戏原画 | anime, 3D render, game concept art | 画风跑偏、非实拍 |
| **假脸** | 网红脸，幼态娃娃脸，过度磨皮，假皮肤 | influencer face, doll-like childish face, over-smoothed skin, fake skin | 塑料感、网红脸（本画法最大的敌人） |
| **过头饰** | 复杂发冠，满头珠钗，夸张妆容 | elaborate hair crown, heavy hair ornaments, heavy makeup | 造型从"素净"变"华丽" |
| **过曝** | 过曝脸部，强 HDR，高饱和糖果色，鲜艳大红大绿 | blown-out face, heavy HDR, oversaturated candy colors, garish red and green | 毁掉低饱和胶片调 |
| **现代** | 现代元素 | modern elements | 现代物件穿帮 |
| **手** | 手指畸形，多余手指 | deformed hands, extra fingers | 模型画手必翻（本风格常有持物动作） |

---

## 3. 视频额外负面词

```
动作僵硬，镜头呆板，人物变形，画面过锐
stiff motion, static camera, warped subject, over-sharpened frame
```

---

## 4. 注意：有些"负面词"其实是正面要求

本画法有两条要求**不能只靠负面词**，必须正面写进 prompt（`build_prompt.py` 已内置）：

- **不是摆拍** → 正面写"像摄影师突然叫住她的一瞬间"比"避免摆拍"有效得多
- **皮肤要真实** → 正面写"保留真实肌肤纹理、轻微胶片颗粒"，而不是只写"不要磨皮"

> 经验：**模型对"是什么"的响应，永远强于"不是什么"。**
> 负面词只用来堵漏，不用来塑形。
