# 模型选型建议 / Model Recommendations

> 不同模型对国风水墨风格的理解差异较大，这里给出实测验证过的推荐。

---

## 综合评分

| 模型 | 水墨表现 | 中文理解 | 成本 | 推荐指数 |
|------|---------|---------|------|---------|
| Seedream（火山）| ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.2-0.3 | ⭐⭐⭐⭐⭐ |
| gpt-image-2 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ¥0.38 | ⭐⭐⭐⭐ |
| qwen-image-3.0 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.18 | ⭐⭐⭐⭐ |
| Midjourney v6 | ⭐⭐⭐⭐ | ⭐⭐ | 订阅制 | ⭐⭐⭐⭐ |

---

## 模型详解

### 🥇 Seedream（火山方舟）—— **国风水墨首选**

**优势**：
- 东方美学调校最强
- 中文提示词理解最佳
- 写意风格表现稳定
- 价格适中

**劣势**：
- 工笔精细度略低
- 复杂场景偶尔跑偏

**推荐用法**：
```
museav gen --prompt "<中文提示词>" --model Seedream
```

**调优技巧**：
- 加 `传统国画` 强化风格
- 加 `写意笔法` 突出意趣
- 比例 16:9 山水表现最佳

---

### 🥈 gpt-image-2 —— **细节氛围之王**

**优势**：
- 细节质感、毛笔纹理优秀
- 写意留白处理最佳
- 适合工笔花鸟
- Medium 档性价比高

**劣势**：
- High 档成本高
- 中文理解略弱
- 写意风格不如国产模型

**推荐用法**：
```
museav gen --prompt "<英文提示词>" --model gpt-image-2 --quality medium
```

**调优技巧**：
- 用英文提示词效果更稳定
- 强调 `traditional Chinese ink wash, rice paper texture` 提升质感
- 适合花鸟、人物题材

---

### 🥉 qwen-image-3.0 —— **性价比之王**

**优势**：
- 价格最低（¥0.18/张）
- 中文理解稳定
- 适合批量出图试方向

**劣势**：
- 细节略逊
- 工笔精细度一般

**推荐用法**：
```
museav gen --prompt "<中文提示词>" --model qwen-image-3.0
```

**调优技巧**：
- 适合试稿阶段
- 简洁提示词效果更稳
- 跑出方向后再用精模精修

---

### 🎨 Midjourney v6 —— **创意灵感**

**优势**：
- 创意发散、艺术感强
- 水墨意境表现惊艳
- 适合找灵感

**劣势**：
- 中文理解弱
- 国风水墨还原度不稳定
- 订阅制

**推荐用法**：
```
museav gen --prompt "<英文提示词>" --model midjourney --quality high
```

**调优技巧**：
- 加 `--s 50` 降低风格化
- 加 `style raw` 减少 MJ 风格
- 适合前期灵感探索

---

## 出图工作流（推荐）

```
阶段 1：灵感探索
├─ qwen-image-3.0 × 4 张（试方向）
└─ 选出最佳构图 / 墨色

阶段 2：精修
├─ Seedream 或 gpt-image-2 × 2 张
└─ 中等质量档

阶段 3：终稿
└─ Seedream × 1 张
   └─ 高质量档
```

---

## 风格加成关键词

### Seedream 专属
```
传统国画，水墨写意，笔触可见，墨色浓淡变化，
宣纸质感，留白意境，诗意
```

### GPT-image-2 专属
```
traditional Chinese ink wash painting, hand-painted brushwork,
rice paper texture, visible brush strokes, ink wash,
poetic atmosphere, masterpiece
```

### qwen-image-3.0 专属
```
国画水墨，写意笔法，宣纸纹理，留白意境，诗意
```

### Midjourney 专属
```
traditional Chinese ink painting, hand-painted brushwork,
rice paper, ink wash, poetic, masterpiece --s 50 --style raw
```

---

## 通用建议

1. **批次策略**：每张图成本不同，建议先用低成本模型试方向
2. **提示词版本**：同一提示词在不同模型上需要微调
3. **质量档位**：Medium 已足够日常使用
4. **比例固定**：3:4 / 16:9 / 9:16 / 1:1 四大标准
5. **样图参考**：先用 seedream 出样图，再用 gpt-image 精修

---

*本模型选型指南基于实测验证整理，价格为参考值。*