# 古风美人 · AI 出图 Skill 集

> `guofeng-meiren` = 中国朝代风格 AI 出图 Skill 包。
>
> 「一张主题，出一张稳出该朝代美学的图」。
> 共享骨架 + 每个朝代单独 SKILL.md（人物 / 服饰 / 色彩 / 场景），agent 出图前读对应朝代的 SKILL.md + references/。

---

## 🎯 设计目标

> 「把中式审美变成可以反复使用的创作工具」
> 想到一句诗、一个季节、或一个生活片段，就能把它变成画面。
> 不需要每次重新解释什么是该朝代审美。

---

## 🚀 快速使用

### 命令行出图（推荐：用 `museav` CLI，仓库自带 wrapper 脚本）
```bash
# 默认宋韵 + 3:4 竖版（视频号 / 小红书）
./dynasties/song/scripts/generate.py \
  --subject "春日庭院，少女倚栏观花，海棠初开，微风拂动衣袖"

# 唐代（盛唐华贵）
./dynasties/tang/scripts/generate.py \
  --subject "盛唐宫廷仕女，立于牡丹花丛中" \
  --ratio 3:4

# 魏晋（飘逸出尘）
./dynasties/wei-jin/scripts/generate.py \
  --subject "魏晋名士，松下抚琴，衣袂飘举" \
  --ratio 16:9
```

输出默认存到 `/Volumes/AI素材资源/图片素材/山鬼映画/古风美人/{朝代}/{日期}-{主题}.jpg`（你的外部硬盘，AI 素材统一盘）。

### 给大模型一句画面
```
春日庭院，少女倚栏观花，海棠初开，微风拂动衣袖。
```
agent 读取 `dynasties/song/SKILL.md` + `references/prompt-core.md`，按宋韵骨架整理成可用的图像生成 prompt。

### 在 Claude Code / Cursor / Codex 等 agent 里
把本仓库路径（或 `SKILL.md` 链接）告诉 agent，agent 会读取对应朝代的 SKILL.md + references 自动组织 prompt。

---

## 🏛️ 当前覆盖的朝代

| 朝代 | 风格核心 | SKILL.md | 完整度 | 备注 |
|------|---------|---------|--------|------|
| **宋** | 清雅克制 / 淡到极致 | [dynasties/song/SKILL.md](dynasties/song/SKILL.md) | 🟢 **深** | 你调了几十组的稳出参数沉淀 |
| **唐** | 丰腴雍容 / 张扬华贵 | [dynasties/tang/SKILL.md](dynasties/tang/SKILL.md) | 🟡 骨架 | 等你补调参经验 |
| **魏晋** | 飘逸出尘 / 名士风骨 | [dynasties/wei-jin/SKILL.md](dynasties/wei-jin/SKILL.md) | 🟡 骨架 | 等你补调参经验 |

> 计划扩展：明（端庄大气）/ 清（旗装）/ 汉（曲裾深衣）/ 唐宋之间（五代十国）。

---

## 📦 仓库结构

```
guofeng-meiren/
├─ README.md                  ← 你在这里
├─ LICENSE                    ← MIT
├─ shared/
│  └─ common-prompt-base.md  ← 跨朝代通用骨架（人物 5 元素 / 场景 4 / 光影 3 / 质感 4 + 反面清单）
└─ dynasties/
   ├─ tang/                  ← 盛唐华贵
   │  ├─ SKILL.md            ← 唐入口 + 5 元素 + 模板 + 反面
   │  ├─ references/
   │  │  ├─ prompt-core.md   ← TODO：等你给调参经验
   │  │  ├─ style-tokens.md  ← TODO
   │  │  └─ scene-matrix.md  ← TODO（可参考宋的结构）
   │  ├─ scripts/
   │  │  └─ generate.py      ← TODO：museav wrapper 唐朝专属部分
   │  └─ examples/            ← TODO：跑成功后的示范输出
   ├─ song/                  ← 宋韵美人（完整）
   │  ├─ SKILL.md            ← 完整宋韵入口
   │  ├─ references/
   │  │  ├─ prompt-core.md   ← 宋韵 token 库（人物 / 场景 / 光影 / 质感 + 反面 + 完整模板）
   │  │  ├─ style-tokens.md  ← 服饰 / 色彩 / 发型 / 妆容 / 园林 / 季节物候
   │  │  └─ scene-matrix.md  ← 4 季 × 5 空间 × 3 姿态 = 60 组合基线
   │  ├─ scripts/
   │  │  └─ generate.py      ← museav wrapper（宋完整版）
   │  └─ examples/            ← TODO
   └─ wei-jin/               ← 魏晋风骨
      ├─ SKILL.md            ← 魏晋入口 + 5 元素 + 模板 + 反面（骨架）
      ├─ references/         ← TODO
      ├─ scripts/            ← TODO
      └─ examples/            ← TODO
```

---

## 🎯 跨朝代差异速查（看一眼就懂差异在哪）

| 维度 | 唐 | 宋 | 魏晋 |
|------|----|----|------|
| **色彩** | 🔴 浓艳撞色（石榴红 / 鹅黄 / 翠绿）| ⚪ 低饱和素雅（藕荷 / 月白 / 茶白）| 🔵 冷色玄青（玄色 / 天青 / 鹤灰）|
| **身形** | 丰腴雍容 | 清瘦端庄 | 清瘦飘逸 |
| **发型** | 高髻 / 满头金翠 | 低盘发 + 素簪 | 飞天髻 + 素纱飘带 |
| **服饰** | 齐胸襦裙 + 大袖纱罗 | 对襟薄纱褙子 | 杂裾垂髾服 + 宽袖 |
| **场景** | 满画面 / 华堂 / 牡丹 | 留白 / 园林 / 廊亭 | 自然山水 / 松竹 / 月 |
| **光影** | 暖黄明亮 / 清晰锐利 | 傍晚黄金侧逆 / 漫射 | 晨昏柔光 / 月色 |
| **代表物** | 牡丹 / 团扇 / 步摇 | 荷塘 / 园林 / 素簪 | 松竹 / 古琴 / 玄学 |
| **气质** | 盛 / 华贵 / 张扬 | 清 / 克制 / 松弛 | 逸 / 超然 / 隐逸 |

---

## 🔒 反面清单（任何朝代都不能出现）

```
❌ 不要：浓妆 / 网红脸 / 亮片闪粉 / 高光滤镜
❌ 不要：现代妆容 / 西式剪裁
❌ 不要：AI 滤镜词（"8k", "trending on artstation", "unreal engine"）
❌ 不要：脸崩 / 多手指 / 透视错误
❌ 不要：紧绷束身 / 现代内衣轮廓
```

具体朝代的反面清单见各朝代的 `SKILL.md`。

---

## 🛠️ 工具依赖

- **museav** CLI（已配置在 `~/.museav.json`）—— 出图中台
  - 测试：`museav whoami`
  - 安装：见 [Studio (MUSE AV)](https://docs.museav.top)
- **Python 3.10+**（脚本用）

---

## 🤝 贡献

1. 跑通一个朝代的 SKILL，把输出图传到 `examples/`（提 PR 或直接 commit）
2. 把你的调参经验沉淀到对应朝代的 `references/prompt-core.md`
3. 新增朝代（汉 / 明 / 清 等）：复制 `dynasties/song/` 改名字

---

## 📜 License

MIT
