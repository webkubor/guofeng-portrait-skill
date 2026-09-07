# 更新日志 / Changelog

## v2.1.0（2026-09-07）

收窄为**纯人像 skill**。

### 移除（Removed）

- `3d-realistic`：`scene` / `weapon` / `action` 三个 category，及其
  assets（4 张）、examples（3 组）、中文 examples（2 组）
- `ink-wash`：`scene` / `nature` / `creature` / `poetry` 四个 category，及其
  assets（8 张）、examples（4 组）
- 中文提示词库删掉「场景提示词模板」「武器法宝提示词」两章，后续章节顺移
- `visual-dna.md` 删掉「核心场景」列举，该节改为「人像的环境与构图」——
  环境只服务于人物，不把场景当主体

### 保留（Kept）

「战斗/动态角色」这类主体仍是人的内容全部保留（"白衣剑修全身动态图"是人像，
不是战斗场面）；空间纵深与构图原则保留，它们决定人像的背景怎么处理。

### 理由

定位模糊的工具没人用得顺手。一个 skill 同时管人物、场景、器物、花鸟，
提示词体系会互相稀释，agent 每次还得先问「你要画哪类」。

## v2.0.0（2026-09-07）

三个重叠的提示词仓库合并为一个，主题重新定位为**古风人像**。

### 变更（Changed）

- **仓库更名** `donghua-3d-skill` → `guofeng-portrait-skill`，slug
  `donghua-3d-realistic` → `guofeng-portrait`。GitHub 会自动重定向旧地址。
- **主线从「国漫 3D 风格」收窄为「古风人像」**：人物是主打，
  场景 / 器物 / 自然题材保留为配景（人像需要环境，删掉是净损失）。
- **按风格分目录**：原 `references/` `examples/` `assets/` 移入
  `styles/3d-realistic/`，git 历史保留。
- **`scripts/build_prompt.py` 改为薄分发器**，按 `--style` 转给
  `styles/<风格>/build_prompt.py`。原脚本原样移入 3D 风格目录。
  不带 `--style` 默认 `3d-realistic`，旧调用方式只差一个参数。

### 新增（Added）

- **`styles/ink-wash/`** —— 国风水墨写意风格，来自 `guoman-ink-wash-skill`：
  10 张参考图、5 组示例、`brush-techniques.md`（笔法墨法）、完整 visual-dna
  与负面词表、独立的 build_prompt.py。
- **`styles/3d-realistic/prompt-library-zh.md`** —— 中文提示词库全文（349 行，
  关键词表 / 组合公式 / 避坑），来自 `guoman-3d-skill`。
- **`styles/3d-realistic/examples-zh/`** —— 中文示例 4 组（人物男女、场景、武器）。
- **`CONTRIBUTING.md`** —— 贡献指南，同样来自 `guoman-3d-skill`。

### 合并说明

`guoman-3d-skill` 与本仓库是**同一主题的两个版本**（slug 都是 `*-3d-realistic`），
一个是 skill 包格式、一个是提示词库格式，各自演进互不知情。
合并时两边内容全部保留，没有删改；`guoman-ink-wash-skill` 的原始 SKILL.md
留在 `styles/ink-wash/SKILL-original.md` 备查。

**两种风格的提示词体系互不相通**（一个讲渲染材质，一个讲笔触留白），
所以不做内容层面的融合，各自保留完整一套，顶层只做路由。

## v1.0.0（2026-09-02）

初始发布。基于实测验证的国漫 3D 写实风格 Skill 框架。

### 新增（Added）

- **Skill 框架**：完整 SKILL.md + references/ + scripts/ + examples/ 标准结构
- **5 大分类示例**：
  - 男性角色：剑修、宗主、魔尊（3 例）
  - 女性角色：仙子、妖女（2 例）
  - 场景：仙门山门、修炼洞府、古战场（3 例）
  - 武器法宝：飞剑、魔刀、灵珠（3 例）
  - 战斗动作：剑修出招、施法（2 例）
- **完整中英双语提示词**：每个示例都附中英两个版本
- **9 张实测参考样图**：所有样图都是用 museav 出图生成的真实结果
- **`scripts/build_prompt.py`**：中英双语提示词自动生成脚本
- **references/ 文档**：
  - `visual-dna.md` — 视觉基因（色彩 / 光影 / 角色）
  - `camera-lenses.md` — 镜头与光影手册
  - `negative-prompts.md` — 负向提示词清单
  - `model-recommendations.md` — 模型选型建议
- **`manifest.yaml`** 元数据 + **`LICENSE`** MIT + **`README.md`** 项目说明

### 验证（Verified）

- ✅ Seedream（火山）—— 国漫脸型最正
- ✅ gpt-image-2 —— 光影氛围最佳
- ✅ qwen-image-3.0 —— 中文理解稳定
- ✅ 所有样图都是真实生成结果（非占位）

### 设计原则

1. **3D 写实**为核心，区别于日漫 2D / 古风水墨
2. **东方审美**为基调，区别于好莱坞 3D
3. **可复制可调整**，每个提示词都是完整可用的
4. **开源可商用**，MIT 协议