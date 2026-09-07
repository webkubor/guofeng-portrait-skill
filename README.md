# 古风人像 / Guofeng Portrait Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-3.0.0-blue.svg)](./CHANGELOG.md)
[![Styles](https://img.shields.io/badge/画法-2-green.svg)](#-维度一画法)
[![Dynasties](https://img.shields.io/badge/朝代-3-orange.svg)](#-维度二朝代形制)

> 🎨 古风**人像**提示词库与 Agent Skill —— 画法（3D 写实 / 水墨）× 朝代（唐 / 宋 / 魏晋）自由组合

---

## 📋 这是什么？

生成**古风人像**（角色立绘、头像、人物海报）的提示词库。

**只做人物。** 不做场景概念图、器物法宝、花鸟山水——人物所处的环境只作为
背景服务于人像。要那些题材请另找 skill，混在一起会让提示词失焦。

两个**正交维度**自由组合：**画法**（怎么画）× **朝代**（画哪个年代的形制）。
"宋韵美人的水墨画法" = `--style ink-wash` + `dynasties/song/`。

## 🌟 维度一：画法

### `3d-realistic` —— 国漫 3D 写实

对标《斗罗大陆》《斗破苍穹》《灵笼》《完美世界》《一念永恒》《凡人修仙传》。

不是日漫 2D，不是好莱坞 3D，是**国漫特有的东方审美 + 写实渲染 + 仙侠光效**：
UE5 Nanite/Lumen 级渲染、皮肤毛孔与发丝可见、体积光与灵气粒子、电影级景深。

题材：`character-male` / `character-female`

### `ink-wash` —— 国风水墨写意

对标《大鱼海棠》《中国奇谭》《天书奇谭》《山水情》。

手绘笔触（飞白、湿墨晕染）、宣纸质感、**极致留白**——留白是构图的一部分，
不是没画完。写意而非写实。

题材：`character`

### 📜 维度二：朝代形制

不指定朝代时，模型画的"汉服"多半是杂糅形制——各朝代的衣领、袖型、腰线混在一起，
懂的人一眼看出不对。指定朝代能拿到具体的服饰 token 与配色：

| 朝代 | 审美核心 | 适合 |
|---|---|---|
| **唐 `tang`** | 华贵丰腴、色彩浓烈 | 宫廷仕女、盛世气象 |
| **宋 `song`** | "淡到极致才是宋韵"，清雅低饱和 | 江南园林、庭院、肖像特写（资料最全） |
| **魏晋 `wei-jin`** | 飘逸出尘、褒衣博带 | 名士、洛神、松下抚琴 |

跨朝代通用的 4 段式骨架（主体 + 场景 + 光影 + 质感）在
`dynasties/common-prompt-base.md`，三个朝代只在服饰 / 色彩 / 气质上分支。
每个朝代还带一个 `scripts/generate.py`，直接调 museav 出图。

```bash
./dynasties/song/scripts/generate.py --dynasty song \
  --subject "春日庭院，少女倚栏观花，海棠初开" --ratio 3:4
```

> ⚠️ **两套画法的提示词互不相通**。3D 那套讲渲染与材质，水墨这套讲笔触与留白，
> 混用会让画面既不像 3D 也不像水墨。所以两边各自保留完整的
> references / examples / assets / build_prompt.py，顶层脚本只做路由。

---

## 🚀 三种用法

### 一、装成 Agent Skill（推荐）

把整个仓库放进 agent 的 skills 目录，`SKILL.md` 就是入口，
agent 会自己问清风格与题材再出图。

### 二、命令行生成提示词

```bash
# 国漫 3D 写实 · 男性角色 · 人像画幅
python scripts/build_prompt.py --style 3d-realistic \
  --subject "冷峻的青年剑修，月下山巅，黑色长发高束" \
  --category character-male --ratio 3:4

# 国风水墨 · 人物
python scripts/build_prompt.py --style ink-wash \
  --subject "白衣书生，竹林独坐" \
  --category character --ratio 3:4
```

输出 JSON，含 `positive_zh` / `positive_en` / `negative_*` / `recommended_size`。
不带 `--style` 默认 `3d-realistic`。

### 三、直接抄示例

- `styles/3d-realistic/examples/character-male|character-female/` — 英文提示词
- `styles/3d-realistic/examples-zh/characters/` — 中文提示词，更细
- `styles/3d-realistic/prompt-library-zh.md` — 中文人像提示词库全文（关键词表、镜头参数、组合公式、避坑）
- `styles/ink-wash/examples/character/` — 水墨人物示例

每个示例带完整提示词（中英）、参考图、推荐画幅。

---

## 📁 目录结构

```
SKILL.md                    Agent 入口（风格路由 + 工作流）
manifest.yaml               与 SKILL.md frontmatter 同步
scripts/build_prompt.py     薄分发器，按 --style 转给对应风格
dynasties/
  common-prompt-base.md     跨朝代 4 段式通用骨架
  tang/ song/ wei-jin/      各朝代的 SKILL.md + references/ + scripts/generate.py
styles/
  3d-realistic/
    build_prompt.py         该风格完整的提示词构建器
    prompt-library-zh.md    中文提示词库全文
    references/             visual-dna / camera-lenses / negative-prompts / model-recommendations
    examples/  examples-zh/ 人像示例提示词（英 / 中）
    assets/                 人像参考图
  ink-wash/
    build_prompt.py
    references/             visual-dna / brush-techniques / negative-prompts / model-recommendations
    examples/  assets/
    SKILL-original.md       合并前的独立版本，保留备查
```

---

## 📜 由三个仓库合并而来

v2.0.0 之前这是三个独立仓库，主题互相重叠：

| 原仓库 | 内容 | 去处 |
|---|---|---|
| `donghua-3d-skill` | 国漫 3D 写实 skill（英文，结构完整） | 本仓库（保留 git 历史） |
| `guoman-3d-skill` | 同主题的中文提示词库版本 | `styles/3d-realistic/prompt-library-zh.md` + `examples-zh/` |
| `guoman-ink-wash-skill` | 国风水墨 skill | `styles/ink-wash/` |
| `guofeng-meiren` | 古风美人 skill 集（唐/宋/魏晋朝代形制） | `dynasties/` |

前两个是**同一主题的两个版本**（slug 都是 `*-3d-realistic`），一个是 skill 包格式、
一个是提示词库格式，各自演进互不知情——正是"一个项目两个仓库"的典型。

v2.1.0 进一步收窄为**纯人像**：场景、器物、自然、诗意题材的素材与提示词全部移除，
两份 `build_prompt.py` 的对应 category 一并删掉。定位模糊的工具没人用得顺手。

v3.0.0 并入 `guofeng-meiren`——它同样是古风人像出图 skill，只是切分维度不同
（按朝代而非按画法）。两者正交互补：原来只说"形制统一的汉服"却没有朝代知识，
现在补上了唐/宋/魏晋的具体服饰 token 与配色。

## 📄 License

MIT
