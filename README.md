# 国漫 3D 写实风格 / Donghua 3D Realistic Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](./CHANGELOG.md)
[![Categories](https://img.shields.io/badge/Categories-5-green.svg)](#-能力概览)

> 🎨 为 AI 创作者提供**斗罗大陆 / 斗破苍穹 / 灵笼 / 完美世界**风格的国产 3D 动漫提示词库与 Agent Skill

---

## 📋 这是什么？

本 Skill 用于生成**国产 3D 动漫（国漫）写实风格**的图像与短视频，风格定位对标：

- 🎬 《斗罗大陆》——角色塑造、武魂特效
- 🎬 《斗破苍穹》——火焰特效、热血战斗
- 🎬 《灵笼》——末日废土、机甲融合
- 🎬 《完美世界》——仙气飘逸、山水意境
- 🎬 《一念永恒》——水墨意境、幽默感
- 🎬 《凡人修仙传》——写实细腻、暗黑风

不是日漫 2D，不是好莱坞 3D，是**国漫特有的东方审美 + 写实渲染 + 仙侠光效**。

---

## 🌟 三种使用方式

### 方式一：一键复制给 AI（最简单）

直接复制下面文字发给任意桌面 Agent：

```
帮我安装这个 Skill：https://github.com/webkubor/donghua-3d-skill
```

支持从 GitHub 链接直接装 Skill 的客户端会自动拉取生效。

### 方式二：本地克隆到 Skill 目录

```bash
# 找到你客户端的 skills 目录
git clone https://github.com/webkubor/donghua-3d-skill.git
```

克隆完成后重启客户端即可使用「国漫风格」「donghua style」等调用。

### 方式三：手动下载 ZIP

1. 打开 https://github.com/webkubor/donghua-3d-skill
2. 点 `Code → Download ZIP`
3. 解压到客户端 skills 目录

---

## ✨ 能力概览

| 分类 | 数量 | 说明 |
|------|------|------|
| 男性角色 | 3 | 剑修、宗主、魔尊 |
| 女性角色 | 2 | 仙子、妖女 |
| 场景 | 3 | 仙门、洞府、战场 |
| 武器法宝 | 3 | 飞剑、魔刀、灵珠 |
| 战斗动作 | 2 | 剑修出招、施法 |

每个分类都有：
- ✅ 完整中英双语提示词
- ✅ 实测参考样图
- ✅ 推荐出图参数
- ✅ 模型选型建议

---

## 🚀 快速上手

### 安装 Skill 后，对 Agent 说：

```
用国漫 3D 风格生成一张图：冷峻的青年剑修，月下山巅，黑色长发高束
```

```
Donghua style: a cold young swordsman portrait, moonlit mountain peak
```

```
用国漫 3D 风格生成一张战斗海报：白衣剑修挥剑出招，悬崖边
```

### Agent 会自动：

1. 选择 `character-male` 分类
2. 调用 `scripts/build_prompt.py` 生成提示词
3. 应用负向约束
4. 调用生成工具
5. 返回结果

---

## 🎨 风格速览

### 核心特征

- **UE5 Nanite + Lumen 渲染** —— 几何 + 光照的电影级质感
- **PBR 材质** —— 皮肤毛孔、发丝纹理、衣物反射
- **东方美学** —— 仙侠玄幻、气势磅礴
- **电影光影** —— 侧逆光、体积光、粒子特效

### 视觉对比

| 风格 | 特征 |
|------|------|
| ❌ 日漫 2D | 平面、赛璐璐、大眼卡通 |
| ❌ 好莱坞 3D | 西方审美、动作捕捉感 |
| ❌ 古风 2D | 工笔、写意、水墨 |
| ✅ **国漫 3D** | 东方审美 + 写实渲染 + 仙侠光效 |

---

## 📁 文件结构

```
donghua-3d-skill/
├── README.md                      # 本文件
├── SKILL.md                       # Skill 入口与使用说明（Agent 读取）
├── CHANGELOG.md                   # 版本更新日志
├── manifest.yaml                  # 元数据（名称 / 触发词 / 权限）
├── LICENSE                        # MIT
├── scripts/
│   └── build_prompt.py            # 提示词生成脚本（中英双语）
├── references/
│   ├── visual-dna.md              # 视觉基因（色彩 / 光影 / 角色）
│   ├── camera-lenses.md           # 镜头与光影手册
│   ├── negative-prompts.md        # 负向提示词清单
│   └── model-recommendations.md   # 模型选型建议
├── examples/
│   ├── character-male/            # 男性角色示例（带样图）
│   ├── character-female/          # 女性角色示例（带样图）
│   ├── scene/                     # 场景示例（带样图）
│   ├── weapon/                    # 武器法宝示例（带样图）
│   └── action/                    # 战斗动作示例（带样图）
└── assets/                        # 参考样图
    ├── character-male/
    ├── character-female/
    ├── scene/
    ├── weapon/
    └── action/
```

---

## 🛠 提示词脚本用法

```bash
python scripts/build_prompt.py \
  --category <character-male|character-female|scene|weapon|action> \
  --media <image|video> \
  --subject "<主体描述>" \
  --ratio <3:4|16:9|9:16|1:1>
```

**参数说明**：
- `--category`：主体分类（必填）
- `--media`：生成媒介（默认 `image`）
- `--subject`：具体主体，如「冷峻的青年剑修，月下山巅」
- `--ratio`：画面比例（默认 `3:4`）

**输出**：JSON 含 `positive_zh` / `positive_en` / `negative_zh` / `negative_en` / `recommended_size`

**示例**：

```bash
python scripts/build_prompt.py \
  --category character-male \
  --subject "冷峻的青年剑修，月下山巅，黑色长发高束" \
  --ratio 3:4
```

---

## 📊 模型选型建议

| 模型 | 国漫 3D 表现 | 中文理解 | 成本 | 推荐 |
|------|-------------|---------|------|------|
| Seedream（火山）| ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.2-0.3 | 🥇 |
| gpt-image-2 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ¥0.38 | 🥈 |
| qwen-image-3.0 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.18 | 🥉 性价比 |
| Midjourney v6 | ⭐⭐⭐ | ⭐⭐ | 订阅制 | 灵感 |

详细对比见 `references/model-recommendations.md`

---

## 💬 使用案例（可直接复制）

### 案例 A：生成角色图

```
用国漫 3D 风格生成一张图：冷峻的青年剑修，月下山巅
```

### 案例 B：生成场景图

```
Donghua style landscape: ancient sect mountain gate floating above cloud sea, golden hour
```

### 案例 C：生成战斗场面

```
用国漫 3D 风格生成一张战斗海报：白衣剑修挥剑出招，悬崖边
```

### 案例 D：生成武器展示

```
国漫风格飞剑：剑身泛冰蓝灵光，龙纹雕刻，灵气粒子环绕
```

---

## ⚠️ 注意事项

- **效果因模型而异**：不同生图模型对提示词理解不同，结果有差别是正常的。
- **手部/发丝**：AI 最容易翻车的两个点，必须在提示词中显式约束。
- **历史服饰**：避免混搭，指定朝代（汉 / 唐 / 宋 / 明）。
- **现代元素**：必须显式排除（手机、汽车、玻璃幕墙等）。
- **版权说明**：本 Skill 基于公开动画作品视觉特征整理，仅供个人学习 / 二次创作参考，请勿用于侵权商用。

---

## 🎬 参考作品

| 作品 | 风格特色 |
|------|----------|
| 《斗罗大陆》| 角色塑造、武魂特效 |
| 《斗破苍穹》| 火焰特效、热血战斗 |
| 《灵笼》| 末日废土、机甲融合 |
| 《完美世界》| 仙气飘逸、山水意境 |
| 《一念永恒》| 水墨意境、幽默感 |
| 《凡人修仙传》| 写实细腻、暗黑风 |

---

## 📄 License

[MIT](./LICENSE) © 2026 webkubor

---

## 🌟 Star History

如果这个 Skill 对你有帮助，请给个 ⭐ Star 支持一下！

---

## 📞 联系方式

- GitHub: [@webkubor](https://github.com/webkubor)
- 小红书：山鬼映画

---

**🤝 欢迎贡献！** 提交 Issue 或 PR 一起完善这个 Skill。