# 光型库 / Light Patterns — film-ambient

> 本画法 90% 的高级感来自光。**光必须有来源、有方向** —— 说不出光源的光不要。
>
> 9 张标杆图（`assets/gallery-9grid.jpg`）里 **7 张是逆光或侧逆光**。
> 正面平光是"影楼味"的第一来源，永不用。

---

## 1. 七种验证过的光型

| 光型 | `--light` | 光源 | 色彩后果 | 标杆图对应 |
|------|-----------|------|---------|-----------|
| **斑驳树影** | `dappled-sun` | 阳光穿过树叶 | 明暗碎块落满脸部与衣料，暖白高光 + 灰绿阴影 | ①花影柔光 ⑧落英慵卧 |
| **雪天散射** | `snow-diffuse` | 雪地反射的天光 | 低对比、冷调、几乎无硬阴影，皮肤通透 | ②雪落庭院 |
| **竹叶漏光** | `bamboo-leak` | 竹叶间隙的日光 | 细碎光斑，青绿环境色反到皮肤上 | ③竹影清茶 ⑤绿意回眸 |
| **灯火暖调** | `lamp-warm` | 单侧油灯 / 灯笼 | 暖金光晕，暗部不死黑，唯一允许的暖色 | ④灯下夜读 |
| **暮色逆光** | `dusk-backlight` | 落日 | 发丝与纱料透光，轮廓被勾亮，天光偏青 | ⑥湖畔逆光 |
| **提灯夜行** | `lantern-night` | 手中纸灯笼 | 面部半明半暗，背景沉入深蓝，暖冷强对比 | ⑨提灯夜行 |
| **冷调窗光** | `cold-window` | 窗 / 天光侧照 | 柔和灰绿阴影，低调，清冷 | ⑦江湖冷调 |

---

## 2. 逐条用法与坑

### `dappled-sun` 斑驳树影 ⭐ 最常用
- **关键词**：`sunlight filtering through leaves, irregular dappled shadows on face and clothing, rim light on hair`
- **适用**：竹林、庭院、花枝、夏日午后
- **坑**：容易糊成一片均匀亮斑 → 必须写 **irregular**（不规则），
  否则模型会画成规则的圆形光斑，一眼假

### `snow-diffuse` 雪天散射
- **关键词**：`soft diffused snow light, low contrast, cool tone, even light without hard shadows`
- **适用**：雪庭、冬日、极简构图
- **坑**：低对比容易出灰片 → 靠 **发丝轮廓光**和深色衣料保住层次，
  肤色要写 `luminous` 否则会发灰

### `bamboo-leak` 竹叶漏光
- **关键词**：`light leaking through bamboo leaves, fine specks of light on face and shoulder`
- **适用**：竹林、绿意、回眸
- **坑**：环境绿会串到肤色上，写 `natural warm-white skin` 把肤色拉回来

### `lamp-warm` 灯火暖调
- **关键词**：`single warm lamp as key light, warm golden glow, shadow detail preserved`
- **适用**：书案、夜读、室内
- **坑**：暖光容易过饱和变成橙黄滤镜 → 写 `low saturation` 压住，
  暖色只允许出现在光源与受光面

### `dusk-backlight` 暮色逆光 ⭐ 最容易出片
- **关键词**：`dusk backlight from the side, light passing through hair and sheer fabric, silhouette outlined by light`
- **适用**：湖畔、旷野、江边、山巅
- **坑**：逆光容易把脸压成剪影 → 要写 `face clearly lit` 或让面部有反射光，
  否则五官全丢

### `lantern-night` 提灯夜行
- **关键词**：`warm lantern light at night, face half-lit and half in shadow, background deep blue`
- **适用**：夜庭、石阶、回廊
- **坑**：夜景容易出噪点与死黑 → 写 `shadow detail preserved`，
  并要求背景有"零星光点"接住画面

### `cold-window` 冷调窗光
- **关键词**：`cool window light from the side, soft grey-green shadows, low-key interior`
- **适用**：室内、江湖冷调、清冷情绪
- **坑**：冷调过头会像恐怖片 → 肤色写 `natural warm-white` 做冷暖对比

---

## 3. 组合规则

1. **一张图只用一种主光源** —— 混两种光（灯火 + 天光）会立刻失去纪实感
2. **逆光时必配轮廓光** —— 发丝被勾亮是本画法的签名
3. **光型要匹配情绪**：
   - 清冷疏离 → `snow-diffuse` / `cold-window` / `lantern-night`
   - 温柔通透 → `dappled-sun` / `bamboo-leak`
   - 怅惘易碎 → `dusk-backlight` / `lamp-warm`
4. **光型要匹配胶片型号**（`--film`，见 `visual-dna.md` 的胶片锚点表）：

| 光型 | 推荐胶片 | 理由 |
|------|---------|------|
| `dappled-sun` / `bamboo-leak` / `snow-diffuse` | `pro400h` | 青绿通透调吃住绿意与冷光，是本画法招牌色 |
| `lamp-warm` / `dusk-backlight` | `portra400` | 暖奶油肤色接暖光，不会黄上加黄 |
| `lantern-night` | `cinestill800t` | 钨丝灯胶片专为夜戏而生，高光 halation 直接出电影感 |
| `cold-window` | `superia` 或 `pro400h` | 纪实轻微偏青 / 冷静通透，两种都成立 |
