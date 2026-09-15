# 命名风格库 / Style Presets — film-ambient

> **21 个命名风格**，每个都是一套调好的槽位组合 + 一句美学定位。
>
> 为什么需要它：36 个槽位取值 = 十万种理论组合，**对使用者等于没有菜单**。
> 这里把验证过的组合命名固化 —— 一条 `--preset` 直接出图，不用再想"该配什么光"。
>
> 标 ⭐ 的 9 个出自标杆九宫格 [`assets/gallery-9grid.jpg`](../assets/gallery-9grid.jpg)。

---

## 1. 用法

```bash
# 直接点一个风格
./scripts/generate.py --preset blossom-veil --subject "凑近花枝，微微侧脸"

# 风格 + 覆盖单个槽位（其余沿用预设）
./scripts/generate.py --preset snow-court --subject "抬头看雪" --shot candid-close

# 只看提示词
python scripts/build_prompt.py --style film-ambient --preset bamboo-tea --subject "..."

# 看全部风格
python scripts/build_prompt.py --style film-ambient --list
```

**覆盖优先级**：显式传入的单槽位参数 **>** 预设 **>** 全局默认。
所以 `--preset snow-court --shot candid-close` = 雪落庭院的一切，只把机位换成抓拍特写。

---

## 2. 风格菜单

### 🌸 花木与春夏

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| ⭐ **花影柔光** | `blossom-veil` | 花枝掩面，光落成影 —— 最柔的一张 | blossom-shadow · dappled-sun · tender · pro400h · candid-close · song |
| ⭐ **落英慵卧** | `petal-recline` | 落瓣满身，懒得起身 | blossom-shadow · dappled-sun · lazy · pro400h · candid-half · song |
| **荷塘盛夏** | `lotus-summer` | 盛夏荷风，眼睫低垂 | lotus-pond · dappled-sun · serene · pro400h · candid-half · song |
| **春雪寻梅** | `spring-plum` | 梅开在残雪里，她凑近看 | snow-court · dappled-sun · curious · pro400h · candid-close · song |
| ⭐ **绿意回眸** | `green-glance` | 绿意深处，忽然回头 —— 像被谁叫了一声 | bamboo-garden · bamboo-leak · quiet-aloof · pro400h · candid-turned · song |

### ❄️ 雪与寒

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| ⭐ **雪落庭院** | `snow-court` | 雪落无声，人比雪静 | snow-court · snow-diffuse · fragile · pro400h · candid-half · song |
| **雪原独行** | `snow-walk` | 天地之间只剩她一个 | snow-field · snow-diffuse · fragile · pro400h · back-view · none |

### 🎋 竹绿与山野

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| ⭐ **竹影清茶** | `bamboo-tea` | 竹影扫阶，一盏清茶，人不想动 | bamboo-garden · bamboo-leak · lazy · pro400h · candid-half · song |
| **松间晨雾** | `pine-dawn` | 雾里松针在滴水 | pine-mist · mist-dawn · serene · pro400h · full-figure · none |
| **山巅风起** | `peak-wind` | 风从谷底上来，衣角和草一起倒 | mountain-peak · mist-dawn · resolute · superia · full-figure · none |

### 🏮 夜与灯

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| ⭐ **灯下夜读** | `lamp-reading` | 一灯如豆，书页半掩，暗部留得住 | study-lamp · lamp-warm · wistful · portra400 · candid-close · song |
| ⭐ **提灯夜行** | `lantern-walk` | 一盏灯笼，只照亮半张脸 | night-lantern · lantern-night · quiet-aloof · cinestill800t · candid-turned · none |
| **烛影摇红** | `candle-night` | 烛火一跳，影子跟着晃 | study-lamp · candle-flutter · dreamy · cinestill800t · candid-close · none |
| **月下独坐** | `moon-court` | 月色很凉，人很静 | moonlit-court · moonlight · serene · pro400h · full-figure · none |

### 🌊 水与远行

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| ⭐ **湖畔暮光** | `lake-glow` | 暮色落水，人影快要成剪影 | lakeside-dusk · dusk-backlight · wistful · portra400 · back-view · none |
| **舟头望水** | `boat-gaze` | 舟行水上，人在想别的事 | boat-river · mist-dawn · dreamy · pro400h · back-view · none |
| **回廊听雨** | `corridor-rain` | 檐外雨声很大，人没动 | corridor-rain · rain-soft · wistful · pro400h · candid-half · song |

### ⚔️ 江湖与侠气

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| ⭐ **江湖冷调** | `jianghu-cold` | 天地不仁，衣袂带霜 | river-wind · overcast-silver · cold-steel · superia · low-angle · none |
| **月下横剑** | `moon-blade` | 剑未出鞘，人已经冷了 | mountain-peak · moonlight · resolute · superia · low-angle · none |

### 🍂 秋与静室

| 风格 | `--preset` | 一句话 | 槽位组合 |
|------|-----------|--------|---------|
| **秋庭落笺** | `autumn-letter` | 一叶落在信纸上，谁也没捡 | autumn-court · dappled-sun · wistful · portra400 · candid-half · song |
| **书斋静读** | `library-quiet` | 满墙旧书，一个人，没有声音 | study-lamp · cold-window · serene · superia · candid-half · song |

---

## 3. 不知道选哪个？按情绪倒推

| 想要的感觉 | 直接点 |
|-----------|--------|
| 最柔、最讨喜 | `blossom-veil` |
| 清冷、疏离、易碎 | `snow-court` / `snow-walk` / `jianghu-cold` |
| 安静、不怕留白 | `moon-court` / `pine-dawn` / `library-quiet` |
| 慵懒、生活化 | `bamboo-tea` / `petal-recline` |
| 怅惘、有故事 | `lake-glow` / `corridor-rain` / `autumn-letter` |
| 夜戏、电影感最强 | `lantern-walk` / `candle-night` / `lamp-reading` |
| 气场、侠气 | `jianghu-cold` / `moon-blade` / `peak-wind` |
| 抓拍、像被叫住 | `green-glance` / `lantern-walk`（都是 `candid-turned`） |

---

## 4. 加新风格

风格库就是 `build_prompt.py` 里的 `PRESETS` 字典，加一条即可：

```python
"my-style": {
    "zh": "中文名",
    "line": "一句话美学定位",
    "slots": {"scene": "...", "light": "...", "mood": "...",
              "film": "...", "shot": "...", "era": "..."},
},
```

约束：
1. **`slots` 里的值必须是已有的槽位取值**（见 `--list`），否则 `resolve_slots` 会报错
2. **一次只动一个变量** —— 新风格应该跟已有风格有明显差异，别只换个 `--shot`
3. **光型 × 胶片要配对**（见 `light-patterns.md` 组合规则第 4 条），否则会串味
4. 加完在 `--list` 里检查一遍，再补进本文档的菜单表
