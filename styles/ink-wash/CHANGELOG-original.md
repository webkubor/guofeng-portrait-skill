# 更新日志 / Changelog

## v1.0.0（2026-09-03）

初始发布。基于实测验证的国风水墨风格 Skill 框架。

### 新增（Added）

- **Skill 框架**：完整 SKILL.md + references/ + scripts/ + examples/ 标准结构
- **5 大分类示例**：
  - 人物：古代学者、古装仕女（2 例）
  - 山水场景：远山、江面、月下楼阁（3 例）
  - 花鸟：仙鹤、竹影（2 例）
  - 瑞兽：神龙（1 例）
  - 诗意场景：秋日枫林、雪中寒梅（2 例）
- **10 张实测参考样图**：所有样图都是用 museav 出图生成的真实结果
- **`scripts/build_prompt.py`**：中英双语提示词自动生成脚本
  - 5 个分类参数
  - 3 档墨色（light / medium / bold）
  - 3 档色彩（monochrome / accent-red / accent-gold）
  - 4 档比例
- **references/ 文档**：
  - `visual-dna.md` — 视觉基因（墨色 / 笔触 / 构图）
  - `brush-techniques.md` — 13 种传统笔法详解
  - `negative-prompts.md` — 负向提示词清单
  - `model-recommendations.md` — 模型选型建议
- **`manifest.yaml`** 元数据 + **`LICENSE`** MIT + **`README.md`** 项目说明

### 验证（Verified）

- ✅ Seedream（火山）—— 国风水墨首选
- ✅ gpt-image-2 —— 细节氛围最佳
- ✅ qwen-image-3.0 —— 中文理解稳定
- ✅ 所有样图都是真实生成结果（非占位）

### 设计原则

1. **2D 手绘**为核心，**永不 3D**
2. **写意意境**为基调，**不要写实**
3. **极致留白**是构图的一部分，**不要过满**
4. **墨色浓淡**变化，**不要均匀**
5. **可复制可调整**，每个提示词都是完整可用的
6. **开源可商用**，MIT 协议