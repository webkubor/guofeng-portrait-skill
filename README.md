# 古风人像 / Guofeng Portrait Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](./CHANGELOG.md)
[![Styles](https://img.shields.io/badge/Styles-2-green.svg)](#-两种风格)

> 🎨 古风人像提示词库与 Agent Skill —— 国漫 3D 写实 + 国风水墨写意，两种风格一套工具

---

## 📋 这是什么？

生成**古风人像**（角色立绘、头像、海报）的提示词库。主线是人物，
场景 / 器物 / 自然题材作为配景一并提供。

## 🌟 两种风格

### `3d-realistic` —— 国漫 3D 写实

对标《斗罗大陆》《斗破苍穹》《灵笼》《完美世界》《一念永恒》《凡人修仙传》。

不是日漫 2D，不是好莱坞 3D，是**国漫特有的东方审美 + 写实渲染 + 仙侠光效**：
UE5 Nanite/Lumen 级渲染、皮肤毛孔与发丝可见、体积光与灵气粒子、电影级景深。

题材：`character-male` / `character-female` / `scene` / `weapon` / `action`

### `ink-wash` —— 国风水墨写意

对标《大鱼海棠》《中国奇谭》《天书奇谭》《山水情》。

手绘笔触（飞白、湿墨晕染）、宣纸质感、**极致留白**——留白是构图的一部分，
不是没画完。写意而非写实。

题材：`character` / `creature` / `nature` / `poetry` / `scene`

> ⚠️ **两套提示词互不相通**。3D 那套讲渲染与材质，水墨这套讲笔触与留白，
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

- `styles/3d-realistic/examples/` — 英文提示词，按题材分目录
- `styles/3d-realistic/examples-zh/` — 中文提示词，更细
- `styles/3d-realistic/prompt-library-zh.md` — 中文提示词库全文（关键词表、组合公式、避坑）
- `styles/ink-wash/examples/` — 水墨示例

每个示例带完整提示词（中英）、参考图、推荐画幅。

---

## 📁 目录结构

```
SKILL.md                    Agent 入口（风格路由 + 工作流）
manifest.yaml               与 SKILL.md frontmatter 同步
scripts/build_prompt.py     薄分发器，按 --style 转给对应风格
styles/
  3d-realistic/
    build_prompt.py         该风格完整的提示词构建器
    prompt-library-zh.md    中文提示词库全文
    references/             visual-dna / camera-lenses / negative-prompts / model-recommendations
    examples/  examples-zh/ 示例提示词（英 / 中）
    assets/                 参考图
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

前两个是**同一主题的两个版本**（slug 都是 `*-3d-realistic`），一个是 skill 包格式、
一个是提示词库格式，各自演进互不知情——正是"一个项目两个仓库"的典型。
合并时两边内容全部保留，没有删改。

## 📄 License

MIT
