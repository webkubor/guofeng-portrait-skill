# 更新日志 / Changelog

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