# 负向提示词清单 / Negative Prompts — 国风水墨

> 直接复制粘贴到生成指令后，用「avoid」或「no」句式引入。

---

## 中文版（推荐用于 Seedream / 国产模型）

```
avoid: 3D渲染，CGI，立体感，电影级光影，UE5，PBR材质，
photorealistic，写实照片，数字绘画，CG感，
日漫风格，赛璐璐，二次元眼睛，线稿风格，皮克斯，迪士尼，
现代元素，手机，汽车，摩天大楼，霓虹灯，
高饱和度，糖果色，鲜艳红黄蓝绿，
均匀笔触，平滑边缘，完美对称，
过多样式，过多细节，画面拥挤，
塑料质感，金属质感，玻璃质感，
hard shadows，硬阴影，hdr效果，
anime风格，cel-shading，flat color，
油画风格，水彩风格（除非指定），
anime eyes，漫画风格
```

## English Version (for global models)

```
avoid: 3D rendering, CGI, photorealistic, digital painting,
UE5, PBR materials, cinematic lighting, volumetric light,
Japanese anime style, cel-shading, line art, anime eyes,
Pixar, Disney, Studio Ghibli (unless requested),
modern elements, smartphones, cars, skyscrapers, neon lights,
oversaturated colors, candy colors, bright primary colors,
uniform brushstrokes, smooth edges, perfect symmetry,
cluttered composition, plastic texture, metallic texture,
hard shadows, HDR effect,
oil painting style, watercolor style (unless specified),
anime, manga, comic book style
```

---

## 按主题分类的负向清单

### 山水画专用
```
避免：明亮饱和，鲜艳花朵，现代建筑，立体山脉，
塑料山峰，塑料树木，塑料河流
```

### 人物画专用
```
避免：立体五官，现代服饰，西方面孔，二次元大眼，
塑料皮肤，赛璐璐上色，勾线轮廓明显
```

### 花鸟画专用
```
避免：写实摄影，3D渲染，立体花鸟，
工业产品感，塑料光泽，过分鲜艳
```

---

## 通用必加约束（不可省略）

### 必须加（中文）
```
1. 笔触可见，不可过于均匀
2. 大量留白，避免画面过满
3. 墨色浓淡变化，不要均匀
4. 宣纸质感，保留纸张纹理
5. 写意为主，不要过于写实
6. 禁止现代元素
7. 保持东方意境，不要西方化
```

### 必须加（English）
```
1. visible brushstrokes, not too uniform
2. vast negative space, avoid cluttered composition
3. ink density variation, not uniform
5. expressive rather than photorealistic
6. no modern elements
7. maintain Eastern aesthetic, avoid Westernization
8. rice paper texture visible
```

---

## 高级避坑（可选）

### 防止"日漫化"
```
additionally avoid: Japanese school uniform, manga style eyes, cel-shading, big anime eyes, kawaii expressions
```

### 防止"3D 化"
```
additionally avoid: 3D render, CGI, octane render, volumetric fog, Unreal Engine, ray tracing, depth of field blur
```

### 防止"油画化"
```
additionally avoid: oil painting, thick impasto, western realism, renaissance art
```

### 防止"商业插画化"
```
additionally avoid: commercial illustration, K-Pop aesthetic, Instagram style, modern digital art
```

---

## 与「国漫 3D」负向的对比

| ❌ 国漫 3D 要避免 | ❌ 国风水墨要避免 |
|------------------|------------------|
| 2D 平面风格 | 3D 立体风格 |
| 日漫风 | 日漫风 |
| 水墨画 | 油画 / 商业插画 |
| 赛璐璐上色 | 高饱和度色彩 |
| 线稿 | 数字绘画 |
| 卡通形象 | 写实摄影 |

两者都强调：**避免日漫、避免现代元素、避免西方化**。

---

*完整负向清单基于传统水墨画美学特征整理。*