# 宋 · 宋韵美人 · Skill

> "淡到极致才是宋韵"——宋制的审美核心是「清」。
>
> 适用：南宋女性 / 江南园林 / 庭院群像 / 田园人物 / 肖像特写。
> 不适用：盛唐华贵（看 [../tang/SKILL.md](../tang/SKILL.md)）/ 魏晋飘逸（看 [../wei-jin/SKILL.md](../wei-jin/SKILL.md)）。
> 共享骨架：[../common-prompt-base.md](../common-prompt-base.md)

---

## 使用

### 1. 给大模型一句画面
```
春日庭院，少女倚栏观花，海棠初开，微风拂动衣袖。
```
skill 会帮你按宋韵骨架整理成可用的图像生成 prompt（人物 + 场景 + 光影 + 质感 4 段）。

### 2. 命令行直接出图（museav）
```bash
# 一键出图
./dynasties/song/scripts/generate.py --dynasty song --subject "少女倚栏观花，海棠初开" --ratio 3:4

# 指定输出路径
./dynasties/song/scripts/generate.py --dynasty song --subject "..." --out ~/Movies/guofeng-portrait/song/2026-09-01-haitang.jpg

# 直接给完整 prompt（绕过 skill 整理）
./dynasties/song/scripts/generate.py --raw --prompt "你的完整宋韵 prompt"
```

---

## 宋韵核心 5 元素（实测调出的"张张稳"逻辑）

### 人物：淡到极致才是宋韵
**别搞华丽妆造！** 宋制的审美核心是「清」。

- **发型**：低盘发 + 几缕碎发 + 一支素色小发簪点缀（不戴满头金翠步摇）
- **服饰**：对襟薄纱褙子（≈ 现代 H 形），面料要带半透纱感，微风拂过衣袂轻扬才灵动
- **神态**：浅笑侧目、放松望向远方，**松弛感才是古意来源**，别蹙眉别撑眼

### 场景：留白比堆砌更高级
**别把荷花、亭台、假山全塞进画面。**

- 选**园林水榭的廊亭一角**，人物斜倚木栏杆
- **前景一定要加遮挡**（一枝荷叶 / 一截垂柳 / 一片芭蕉），遮 1/4 画面
- 远景留**朦胧的池水与亭台剪影**
- 人物只占画面**一半**，空出来的留白才装得下中式园林的意境

### 光影：侧逆光柔雾是封神关键
**这步直接甩掉 "AI 塑料感"。**

- 锁定**傍晚黄金侧逆光**，光线从人物斜后方打过来，给发梢和衣边镶一层柔光金边
- 再加一层**薄雾漫射**效果，弱化所有生硬阴影
- 皮肤会透出自然的通透感，完全不会假脸假面

### 质感：低饱和 + 胶片感 = 写真级出片
- 整体色调统一在**暖杏 + 荷绿**的低饱和色系里，坚决避开高饱和亮色
- 最后叠一层细微**胶片颗粒**
- 搭配 **85mm 镜头**浅景深

---

## 反面清单（任何宋代 prompt 都不能出现）

```
❌ 不要：浓妆 / 网红脸 / 亮片闪粉
❌ 不要：高饱和大红 / 华丽头饰堆砌
❌ 不要：厚重大袖（宋代是薄纱褙子，不是唐的蓬蓬大袖）
❌ 不要：现代妆容 / 西式剪裁
❌ 不要：AI 滤镜词（"8k", "unreal engine", "trending on artstation"）
❌ 不要：脸崩 / 多手指 / 透视错误
```

---

## Prompt 模板（宋韵专用版）

```
[Song Dynasty lady] + [场景人物姿态] + [服饰：低盘发+素簪+碎发 / 对襟薄纱褙子 / 半透纱感面料] + [神态：浅笑侧目/松弛望向远方] + [场景：园林水榭廊亭一角/斜倚木栏杆/前景一枝荷叶遮挡/远景池水亭台剪影/人物占画面一半留白] + [光影：傍晚黄金侧逆光/发梢衣边镶柔光金边/薄雾漫射] + [85mm portrait / 暖杏荷绿低饱和 / 微妙胶片颗粒 / 写真级构图]
```

### 示例（完整版）
```
Southern Song Dynasty lady, leaning on wooden rail of waterside pavilion in Jiangnan scholar's garden, low chignon with loose strands and simple jade hairpin, sheer silk beizi over inner robe, soft smile gazing into the distance, lotus pond and pavilions in soft silhouette behind, foreground lotus leaf partially framing, half the frame left as breathing space, warm golden backlight at dusk creating soft rim on hair and hem, thin atmospheric haze, 85mm portrait lens, low saturation palette of warm apricot and lotus-leaf green, subtle film grain, museum quality composition
```

---

## 配件

- [prompt-core.md](references/prompt-core.md) — 完整宋韵 Prompt 词组 + 反面清单
- [style-tokens.md](references/style-tokens.md) — 服饰 / 色彩 / 发型 / 妆容的朝代专属 token
- [scene-matrix.md](references/scene-matrix.md) — 场景矩阵（4 季 × 4 场景）
- [generate.py](scripts/generate.py) — museav 出图 wrapper（支持 `--subject` → 自动套模板）

---

## 实测例子

| 主题 | 输出 | 备注 |
|------|------|------|
| 春日海棠 | [examples/春日海棠.jpg](examples/) | TODO: 跑通后填 |
| 夏日荷塘 | [examples/夏日荷塘.jpg](examples/) | TODO |
| 秋日庭桂 | [examples/秋日庭桂.jpg](examples/) | TODO |
| 冬日梅窗 | [examples/冬日梅窗.jpg](examples/) | TODO |
