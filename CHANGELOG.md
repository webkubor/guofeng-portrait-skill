# 更新日志 / Changelog

## v3.5.0（2026-09-15）

**重建 `3d-realistic`** —— 旧版产出幼态娃娃脸 + 塑料皮 + 满头堆砌 + 满屏荧光。

### 背景（Why）

旧版固定层只有一句虚的描述（"PBR材质，皮肤有呼吸感…唯美空灵"），
**没有任何脸型 / 年龄 / 骨相 / 比例约束**，负面词也只堵"动漫大眼"而不堵幼童脸。
结果：模型自由发挥出幼态娃娃脸、磨砂塑料皮、满头银冠链条、满屏蓝色荧光粒子 ——
`AESTHETIC.md` 警告过的每一条，旧版全犯了。

### 新增（Added）

- **核心比例写死进固定层**：`70% 真人质感 + 30% 国漫理想化` +
  **20 岁左右成年少女骨相**（精致小鹅蛋脸、面中饱满、下颌线流畅、下巴短小圆润不尖不长）+
  圆润杏眼与**真实虹膜晶体层次**、樱粉唇 + SSS 皮肤与微毛孔
  （不磨皮 / 不塑料 / 不蜡像）+ 发饰克制不堆砌 +
  PBR / subsurface scattering / ray tracing / GI / strand-based hair / 85mm f/1.4 / film color grading
- **四个槽位**：`--scene` 9 种 · `--light` 6 种 · `--framing` 5 种 · `--mood` 5 种
- **6 个命名风格**：`heroine-closeup`（基准）· `heroine-lantern` · `bamboo-quiet` ·
  `snow-temple` · `swordsman-night` · `sect-master`
- **负面词重建**：新增「幼态组」（幼童 / 儿童脸 / 过度婴儿肥 / 圆饼脸 / 尖锥脸 /
  成熟御姐 / 欧美骨相）与「整容脸组」（网红脸 / 韩式整容脸 / 蛇精脸），
  并补上旧版病灶组（仙侠荧光粒子 / 魔法光带 / 满天飞光 / 发饰堆砌 / 满头珠翠 / 通用云海背景）
- **基准范例** `styles/3d-realistic/examples-zh/characters/heroine-closeup.md` ——
  作者手写 prompt 全文 + 逐条对照 `AESTHETIC.md` + 8 种常见失败归因表

### 变更（Changed）

- `references/visual-dna.md`：新增 **§0 核心比例（70/30）** 与 **§0.1 旧版病灶解剖**
  （六条症状 → 根因 → 违反哪条原理），并把 `immortal-fairy.jpg` 明确标为反例保留
- `README.md` 作品区：**撤下 6 张旧版样张**（幼态 / 塑料 / 堆砌 / 荧光），
  换成 4 张验收级作品 —— 女主特写基准 + 亭台托腮 + 庭前持花 + 执卷回眸
- `SKILL.md` 与路由说明：画法描述从"仙侠光效、体积光"改为"70/30、成年骨相、克制"

### 诊断口诀（Diagnosis）

> **"大眼但不精致" = 缺骨相约束；"漂亮但塑料" = 缺皮肤正面规格。**

已写进 `visual-dna.md` §0.1，防复发。

---

## v3.4.0（2026-09-15）

新增**审美判断层** —— 这个 skill 从"提示词库"升级为"教 AI 怎么把古风图做漂亮"。

### 背景（Why）

21 个命名预设解决的是"查表"，但**提示词是答案，判断力是解题方法**。
答案会过时（模型换代、术语失效），方法不会。遇到表里没有的新题材、
或出图不理想时，只有预设的 skill 会失灵 —— 它只会让你换一个预设再抽一次。

### 新增（Added）

- **`AESTHETIC.md`（审美核心）** —— 跨三套画法通用的判断层：
  - **§2 六条第一性原理**：克制法则 / 暗示优于直给 / 光必须有出处 /
    情绪浓度 > 造型精度 / 真实感来自不完美 / 对比度预算是有限的
    —— 每条都带**判据**（可自检）与**推论**（可执行）
  - **§3 推导链**：情绪 → 光 → 色 → 构图 → 质感 → 镜头（后一步是前一步的函数，
    每步附判据与常见误判）
  - **§4 诊断回路**：8 类症状 → 归因维度 → 处方（出图不理想时定位失败维度，**不抽卡**）
  - **§5 反例解剖**：影楼汉服写真为什么一眼俗（七条逐项归因）、
    仙侠光效为什么廉价、3D 渲染感为什么塑料
  - **§6 生成前必答 5 问** + **§7 自我训练法**

### 变更（Changed）

- `SKILL.md`：新增「审美优先：先想清楚，再查参数」章节；工作流插入
  **Step 0 — 审美判断（不能跳）**；参考资料表把 `AESTHETIC.md` 置顶。
- `README.md`：重新定位为「**先教审美判断，再给落地参数**」，
  新增「审美核心讲了什么」章节（六条原理 + 推导链 + 诊断 + 反例）。
- 三套画法的 `visual-dna.md` 顶部都加了指向 `AESTHETIC.md` 的指针
  （本文是通用层在该媒介上的落地）。

### 不变（Unchanged）

21 个命名预设与槽位机制**保留**，继续作为入口与"已验证案例"；
但文档明确了它的定位：**供校准判断，不是查表替代推理**。

---

## v3.3.0（2026-09-15）

给 `film-ambient` 建**命名风格库** —— 把槽位取值从"零件"变成"能直接点的菜"。

### 新增（Added）

- **21 个命名风格**（`--preset`）—— 每个是一套调好的槽位组合 + 一句美学定位：

  | 气质 | 风格 |
  |---|---|
  | 🌸 花木与春夏 | 花影柔光 `blossom-veil` · 落英慵卧 `petal-recline` · 荷塘盛夏 `lotus-summer` · 春雪寻梅 `spring-plum` · 绿意回眸 `green-glance` |
  | ❄️ 雪与寒 | 雪落庭院 `snow-court` · 雪原独行 `snow-walk` |
  | 🎋 竹绿与山野 | 竹影清茶 `bamboo-tea` · 松间晨雾 `pine-dawn` · 山巅风起 `peak-wind` |
  | 🏮 夜与灯 | 灯下夜读 `lamp-reading` · 提灯夜行 `lantern-walk` · 烛影摇红 `candle-night` · 月下独坐 `moon-court` |
  | 🌊 水与远行 | 湖畔暮光 `lake-glow` · 舟头望水 `boat-gaze` · 回廊听雨 `corridor-rain` |
  | ⚔️ 江湖与侠气 | 江湖冷调 `jianghu-cold` · 月下横剑 `moon-blade` |
  | 🍂 秋与静室 | 秋庭落笺 `autumn-letter` · 书斋静读 `library-quiet` |

  标 ⭐ 的前 9 个出自标杆九宫格，逐格命名。
- **`references/style-presets.md`** —— 完整菜单：分组表 + 按情绪倒推选风格 + 加新风格的约束。
- **槽位扩充**：环境 8→16、光型 7→12、情绪 6→10、机位 6→7（新增仰拍 `low-angle`），
  槽位取值合计 36→54。

### 变更（Changed）

- `build_prompt.py`：新增 `PRESETS` / `DEFAULT_SLOTS` / `resolve_slots()`
  （覆盖优先级：**显式槽位 > 预设 > 全局默认**）；新增 `--preset`；
  `--list` 现在同时打印风格库与槽位表；JSON 输出新增 `preset` 字段。
- `scripts/generate.py`：新增 `--preset`；槽位参数默认值改为 `None` 以支持预设覆盖。
- `SKILL.md` / `README.md`：把"**先点风格，再谈调参**"作为 film-ambient 的推荐入口；
  README 画廊第 9 节加 21 风格分组表。

### 为什么（Why）

36 个槽位取值 = 十万种理论组合，**对使用者等于没有菜单**。
命名风格把验证过的组合固化，让"懂你的审美"从"需要调参"变成**一条命令**。

---

## v3.2.0（2026-09-15）

给 `film-ambient` 加**胶片型号锚点** —— 把"胶片感"从形容词变成硬锚点。

### 新增（Added）

- **`--film` 槽位**（第六个槽）—— 5 个取值，默认 `pro400h`：
  - `pro400h` Fujifilm Pro 400H：青绿偏冷、通透薄荷调、肤色干净不发黄（**本画法招牌色**）
  - `portra400` Kodak Portra 400：暖调奶油肤、宽容度高（配灯火 / 暮色）
  - `superia` Fujifilm Superia：轻微偏青、颗粒明显、生活化的不精致（纪实感）
  - `cinestill800t` CineStill 800T：钨丝灯夜景、高光 halation、暗部深蓝（配提灯夜行）
  - `none`：通用"日系胶片扫描质感"（保底）

### 变更（Changed）

- `build_prompt.py`：固定层里的泛词"日系胶片扫描质感"抽出来做成 `--film` 槽
  （默认 `pro400h`，比原泛词更具体、更可复现）；JSON 输出新增 `film` 字段。
- `scripts/generate.py` 新增 `--film` 透传。
- `references/visual-dna.md` 新增「胶片型号锚点」章节（选型逻辑 + 一次只用一个型号）。
- `references/light-patterns.md` 组合规则新增第 4 条：**光型 × 胶片型号配对表**
  （斑驳树影 / 竹叶漏光 / 雪天 → `pro400h`；灯火 / 暮色 → `portra400`；
  提灯夜行 → `cinestill800t`）。
- `references/model-recommendations.md`：槽位化一节补"胶片型号是性价比最高的锚点"。
- `SKILL.md` / `README.md` / 基准范例：槽位数 5 → 6，命令与示例补 `--film`。

### 为什么（Why）

模型对**具体胶片名**的响应，远强于"film grain / 胶片质感"这类泛词 ——
一个型号名同时锁定了色彩倾向、宽容度、高光行为与颗粒粗细。
这是本画法"稳定出图"里成本最低、收益最高的一步。

---

## v3.1.0（2026-09-15）

新增第三套画法 **`film-ambient` 古风氛围胶片人像** —— 真实摄影，不是渲染。

前两套画法（3D 写实 / 水墨）都是"画"，这套是**用电影的摄影语言拍古装少女**：
低饱和青绿月白、侧逆光斑驳树影、胶片颗粒、清冷易碎的情绪。
重心在**氛围与情绪浓度**，不在形制考究。

### 新增（Added）

- **`styles/film-ambient/`** —— 完整的第三套画法，与前两套平级：
  - `build_prompt.py` —— **五槽位**提示词构建器（`--scene` 环境 8 种 ×
    `--light` 光型 7 种 × `--mood` 情绪 6 种 × `--shot` 机位 6 种 × `--era` 朝代），
    `--list` 可打印全部取值。**固定风格层永不变，只换槽位** —— 这是稳定出图的根本。
  - `scripts/generate.py` —— **端到端出图 wrapper**（整理提示词 → 调 museav → 落盘），
    支持 `--ref` 垫图锁脸与 `--batch` 批量。
  - `references/visual-dna.md` —— **七维审美指纹**：色彩 / 光 / 质感 / 构图 / 造型 /
    情绪 / 抓拍感，含与另外两套画法的边界对照、出图后的 7 条自检清单。
  - `references/light-patterns.md` —— 7 种光型库（斑驳树影 / 雪天散射 / 竹叶漏光 /
    灯火暖调 / 暮色逆光 / 提灯夜行 / 冷调窗光），逐条附适用场景与坑。
  - `references/camera-recipes.md` —— 焦段机位配方（35/50/85mm）、构图三规则、抓拍姿态库。
  - `references/negative-prompts.md` —— 8 组高价值负面词（影楼味 / 仙侠味 / 二次元 /
    假脸 / 过头饰 / 过曝 / 现代 / 手）。
  - `references/model-recommendations.md` —— GPT Image 2.5 调法、稳定出图四件事、
    10 种常见失败的修法表。
  - `examples/portrait/bamboo-candid.md` —— 手写基准范例（竹林抓拍 · 宋韵青绿），
    含完整中英提示词与"这张为什么是对的"逐条拆解。
  - `assets/gallery-9grid.jpg` —— 标杆九宫格（审美锚点，166KB）。

### 变更（Changed）

- `scripts/build_prompt.py` 路由加入 `film-ambient`，"两种风格"改为"三种风格"。
- `SKILL.md`：画法表加第三行；`Required Decisions` 与 `Workflow` 补 film-ambient 的
  五槽位用法与端到端 wrapper；硬规则一节从两条变三条。
- `README.md`：画法 badge 2 → 3，画廊新增第 9 节（含槽位速查表与稳定出图三件事），
  矩阵速查表加一行，目录结构补 film-ambient。
- `manifest.yaml`：`version` → 3.1.0，补 `氛围感 / 胶片感 / 实拍人像 / film-look`
  tags 与对应 triggers。

### 设计说明（Notes）

本画法的分水岭是最后两条指纹：**情绪**（清冷、易碎、疏离，姿态静态内敛）与
**抓拍感**（"像摄影师突然叫住她的一瞬间"）。色彩光影做得再对，少了这两条，
出来的也只是"精致的摆拍"。

**稳定出图 ≠ 写好一段魔法提示词**，要靠四件事：风格锚点固化 → `--ref` 垫图锁脸
（提示词锁不住脸）→ 槽位化（一次最多换两个槽）→ 出图后按七维自检打分改槽重出。

---

## v3.0.0（2026-09-07）

并入 `guofeng-meiren`（古风美人 skill 集），新增**朝代**维度。

### 新增（Added）

- **`dynasties/`** —— 唐 / 宋 / 魏晋三个朝代的形制知识，每个朝代含
  `SKILL.md`（人物 / 服饰 / 色彩 / 气质）、`references/scene-matrix.md`
  （场景 × 人物组合矩阵）、`scripts/generate.py`（直接调 museav 出图）。
  宋另有 `style-tokens.md` 服饰 token 速查与 `prompt-core.md`，资料最全。
- **`dynasties/common-prompt-base.md`** —— 跨朝代通用的 4 段式骨架
  （主体 + 场景 + 光影 + 质感），三个朝代只在服饰 / 色彩 / 气质上分支。

### 变更（Changed）

- SKILL.md 重组为**两个正交维度**：画法（必选，3D 写实 / 水墨）× 朝代（可选，
  唐 / 宋 / 魏晋）。"宋韵美人的水墨画法" = `--style ink-wash` + `dynasties/song/`。
- 硬规则里「服装写形制统一的汉服」改为「指定朝代后用具体 token」——
  不指定朝代时模型画的"汉服"多半是杂糅形制，各朝代的衣领袖型腰线混在一起。
- 原 `shared/common-prompt-base.md` 提到 `dynasties/` 同级，链接少一层。
- `guofeng-meiren` CLI 已不存在（仓库并入），朝代 SKILL.md 里的调用改为
  仓库自带的 `./dynasties/<朝代>/scripts/generate.py`，输出目录改为
  `~/Movies/guofeng-portrait/`。

### 修复（Fixed）

- v2.1.0 只改了本文件，`SKILL.md` / `manifest.yaml` 的 `version` 字段
  还停在 2.0.0，本次一并修正。

### 为什么并

`guofeng-meiren` 同样是「古风人像出图 skill」，只是按朝代切分而非按画法。
两者正交互补：这边有渲染风格体系却没有朝代形制知识，那边正好相反。
一个项目一个仓库 —— 同一件事不该长成两个仓。

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