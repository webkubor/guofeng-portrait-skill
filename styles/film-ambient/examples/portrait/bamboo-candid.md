# 范例 01 · 竹林抓拍 · 宋韵青绿 (`bamboo-garden` + `dappled-sun`)

> **这是本画法的基准范例** —— 由作者手写，作为"什么叫做对了"的参照物。
> 出图偏离这张太远时，回 `visual-dna.md` 逐条比对。

---

## 槽位映射

| 槽位 | 取值 |
|------|------|
| `--scene` | `bamboo-garden` 竹林庭院（青石、古树、庭院植物，夏末湿润空气） |
| `--light` | `dappled-sun` 斑驳树影（阳光穿叶，不规则光影落在脸与衣料） |
| `--mood` | `quiet-aloof` 安静疏离（清澈、略带好奇，不露齿笑） |
| `--shot` | `candid-half` 抓拍半身（50mm f/1.8，机位略高于视线，占画面 ~65%） |
| `--era` | `song` 宋制（低饱和青绿 + 月白，轻薄丝织） |

**一句话出提示词**：

```bash
python scripts/build_prompt.py --style film-ambient \
  --subject "轻轻蹲坐在青石旁，一只手随意拿着一小枝竹叶，另一只手自然垂落，微微抬头看向镜头，像摄影师突然叫住她的一瞬间" \
  --scene bamboo-garden --light dappled-sun \
  --mood quiet-aloof --shot candid-half --era song --ratio 3:4
```

---

## 作者手写原版提示词（中文，完整基准）

> 保留原样作为"审美锚点"。它比脚本输出更细，写新场景时可以照这个密度仿写。
> 给 GPT Image 2.5 时建议改用脚本输出的 `positive_en`（英文更稳）。

```text
一位20岁左右的年轻东亚女性，清透自然的古典美人气质，五官精致但真实，鹅蛋脸，清澈有神的眼睛，
自然鼻梁，柔软淡粉唇，皮肤白皙通透但保留真实肌肤纹理，不要网红脸，不要过度磨皮，不要塑料感。

身穿轻薄飘逸的宋制古风服饰，低饱和青绿色与月白色搭配，面料带细腻丝织纹理，轻盈宽袖。
乌黑长发，半披半束的自然古风发型，发型简洁，不要复杂盘发，不要夸张头饰，仅用细窄浅色丝带固定，
几缕碎发被微风吹过脸颊，丝带随风自然飘动。

人物置身真实中式自然环境中，竹林、古树、青石、庭院植物形成前后景层次。阳光穿过树叶，
在人物脸部、衣服和地面形成不规则斑驳光影，空气中有轻微夏日湿润感。

人物没有刻意摆拍，身体自然放松，轻轻蹲坐在青石旁，一只手随意拿着一小枝竹叶，
另一只手自然垂落，微微抬头看向镜头，像摄影师突然叫住她的一瞬间。
眼神安静、清澈，略带一点疏离和好奇，嘴唇自然放松，不露齿笑。

摄影机略高于人物视线，从斜上方俯拍，50mm人像镜头，f/1.8，人物占画面约65%，
脸部清晰，前景竹叶轻微虚化，背景柔和散景，浅景深。

自然日光摄影，清透青绿色调，低饱和，高光微微泛白，阴影呈灰绿色，肤色保持自然暖白，
绿色环境与人物肤色形成柔和对比。日系胶片扫描质感结合东方电影摄影，轻微胶片颗粒，
柔和高光晕染，真实镜头光学感。

重点：真人抓拍感、自然风吹发丝、斑驳树影、清透肤色、东方含蓄情绪、空气感、电影静帧感、真实摄影质感。

避免：影楼汉服写真、仙侠、玄幻、二次元、CG感、网红脸、幼态娃娃脸、过度磨皮、假皮肤、夸张妆容、
复杂发冠、满头珠钗、刻意摆拍、正面证件照构图、过曝脸部、强HDR、廉价古装摄影。
```

---

## 英文版（给 GPT Image 2.5 · 可直接用）

```text
real-photography portrait, not CGI, not anime; East Asian woman in her early 20s,
clear natural classical beauty, egg-shaped face, refined but real features,
luminous translucent skin with visible real skin texture, soft pale-pink lips;
long black hair half-loose, simple styling held by a single thin pale ribbon,
a few wisps of hair blown across her cheek; sheer flowing Song-dynasty silk robe,
low-saturation celadon green and moon white, fine woven texture, light wide sleeves;
a real Chinese garden environment, bamboo grove with old trees, mossy stones and
garden plants layering the foreground and midground, faint summer humidity in the air;
sunlight filtering through leaves, irregular dappled shadows across her face,
clothing and the ground, rim light on her hair;
candid, not posed, body relaxed, crouching beside a mossy stone, one hand casually
holding a small bamboo sprig, the other arm hanging naturally, chin lifted slightly
toward the lens, the instant a photographer calls out to her;
quiet clear gaze with a touch of distance and curiosity, relaxed lips, no teeth showing;
candid waist-up framing, 50mm portrait lens at f/1.8, camera slightly above eye level,
subject filling about 65% of the frame, face tack-sharp, slightly blurred foreground,
soft background bokeh, shallow depth of field;
clean color grading, low saturation, slightly blown highlights, grey-green shadows,
natural warm-white skin, gentle contrast between green environment and skin tone;
Japanese film-scan texture meets East Asian cinematography, subtle film grain,
soft halation, true lens optics; candid documentary feel, airy atmosphere,
cinematic still, real photographic texture.
Avoid: studio hanfu photoshoot, xianxia, fantasy glow effects, anime, CGI, 3D render,
influencer face, doll-like childish face, over-smoothed skin, plastic skin, fake skin,
heavy makeup, elaborate hair crown, heavy hair ornaments, stiff posing,
ID-photo framing, blown-out face, heavy HDR, cheap costume photography,
oversaturated colors, modern elements, deformed hands, extra fingers.
```

---

## 出图命令（带锁脸）

```bash
./styles/film-ambient/scripts/generate.py \
  --subject "轻轻蹲坐在青石旁，一只手随意拿着一小枝竹叶，另一只手自然垂落，微微抬头看向镜头，像摄影师突然叫住她的一瞬间" \
  --scene bamboo-garden --light dappled-sun --mood quiet-aloof \
  --shot candid-half --era song --ratio 3:4 \
  --ref ~/refs/face-anchor.jpg
```

---

## 这张为什么是"对的"

- **色彩**：青绿 + 月白 + 冷灰，饱和度压到极低，红色只留在唇
- **光**：斑驳树影是"不规则"的 —— 规则圆斑一眼假
- **构图**：竹林/古树/青石三层景深，人物只占 65%，留白给空气
- **情绪**：抓拍瞬间 + 疏离好奇 + 不露齿笑 —— 本画法的分水岭
- **质感**：明确写"保留真实肌肤纹理" + "日系胶片扫描"，双向夹住塑料感
