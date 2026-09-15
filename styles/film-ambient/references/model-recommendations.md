# 模型调法 / Model Recommendations — film-ambient

> 本画法的成败 90% 在质感，所以**模型选择比提示词更重要**。

---

## 1. 首选：GPT Image 2.5

| 项目 | 说明 |
|------|------|
| **为什么选它** | 皮肤微纹理、发丝、光影层次是它的强项 —— 恰好是本画法的命门（真实肌理 vs 塑料磨皮） |
| **语言** | **用英文 `positive_en`**。它是 OpenAI 系，中文长句会有衰减 |
| **质量档** | 定稿 `-q high`；摸槽位组合时先 `-q low` 省钱 |
| **比例** | 人像一律 `-r 3:4`（1024×1536） |
| **负面词** | 用 `Avoid: ` 拼在提示词末尾，见 `negative-prompts.md` |

```bash
museav gen \
  --prompt "<positive_en> ... Avoid: <negative_en>" \
  --ratio 3:4 --quality high \
  --ref ~/refs/face-anchor.jpg
```

**中文 `positive_zh` 给谁用**：qwen-image / Seedream 这类中文理解强的模型，
以及需要快速批量摸草稿时。

---

## 2. 「稳定出图」的四件事（缺一件就不稳）

### ① 风格锚点固化 ✅ 已内置

不要每次现编提示词 —— 现编 = 每次都不一样。
`build_prompt.py` 的固定层（`FIXED_ZH` / `FIXED_EN`）包含七维指纹里的六维，
**每次出图原样带上**，你只换槽位。

```bash
python scripts/build_prompt.py --style film-ambient \
  --subject "..." --scene bamboo-garden --light dappled-sun \
  --mood quiet-aloof --shot candid-half --era song
```

### ② 垫图锁脸（最关键，也最容易被忽略）⭐

**提示词锁不住脸。** 不锁脸的话，每次都会换一个人 —— 这就是"不稳定"的最大来源。

做法：挑一张满意的出图当**脸部母版**，之后每张都垫它：

```bash
museav gen --prompt "..." --ref ~/refs/face-anchor.jpg --ratio 3:4
```

- `--ref` 可重复传（最多 5 张），顺序对应提示词里的「图片1、图片2…」
- 组合建议：**1 张脸 + 1 张色调参考 + 1 张构图参考** = 最稳
- 提示词里显式写 `same face as image 1` 效果更好

### ③ 槽位化：变的东西越少，越像同一个人拍的

五槽中最多同时换两个。**光型和机位一次只调一个**，
一次全换等于重新抽卡。

### ④ 自检回路：不靠抽卡，靠打分

出图后按 `visual-dna.md` 第 7 节的 7 条自检清单打分（可用本地 VLM 批量跑），
不达标就**改槽位重出**，而不是多抽几张碰运气。

---

## 3. 常见失败与修法

| 症状 | 根因 | 修法 |
|------|------|------|
| **塑料感 / 磨皮** | 模型默认美化 | 正面写 `visible skin texture, subtle film grain`；负面加 `over-smoothed skin`；换 `-q high` |
| **网红脸** | 训练数据偏向 | 负面必须带 `influencer face, doll-like face`；用 `--ref` 垫真实感的脸 |
| **仙侠味** | 关键词串味 | 检查有没有混进 3d-realistic 的光效词；负面加 `xianxia glow effects` |
| **摆拍感** | 姿态描述太"演" | 改用 `--shot candid-turned`；主体写"像摄影师突然叫住她的一瞬间" |
| **脸部过曝** | 逆光没处理好 | 加 `face clearly lit`；或从 `dusk-backlight` 换 `dappled-sun` |
| **高饱和 / 糖果色** | 色彩约束不够 | 固定层已带 `low saturation`，再确认没混进 ink-wash / 3d 的调色词 |
| **画面太平（无层次）** | 缺前景 | 场景槽位必须带前景遮挡；补 `slightly blurred foreground` |
| **手画坏** | 模型通病 | 负面加 `deformed hands, extra fingers`；主体写"手指自然放松" |
| **肤色发灰** | 冷光过强 | 补 `natural warm-white skin` 做冷暖对比 |
| **每张脸不一样** | 没垫图 | 上 `--ref` 锁脸（见 ②） |

---

## 4. 和其它模型搭配

| 模型 | 定位 | 用法 |
|------|------|------|
| **GPT Image 2.5** | 定稿首选 | 英文提示词 + `-q high` + 垫图 |
| **qwen-image** | 批量摸槽位组合 | 中文提示词，`-q low`，快速出多版看构图 |
| **museav 模板** | 固定题材复用 | 把满意的槽位组合存成模板，见 README 的画廊模板表 |
