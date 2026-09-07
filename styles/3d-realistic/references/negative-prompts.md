# 负向提示词清单 / Negative Prompts

> 直接复制粘贴到生成指令后，用「avoid」或「no」句式引入。

---

## 中文版（推荐用于 Seedream / 国产模型）

```
avoid: 2D动漫，赛璐璐，二次元眼睛，水墨画，工笔，平面卡通，
日漫风格，皮克斯，迪士尼，
现代元素，手机，汽车，摩天大楼，
西方元素，西式盔甲，欧洲城堡，
塑料皮肤，磨皮过度，毛孔不可见，
头发糊成一片，发丝不分明，
手部畸形，六根手指，手部穿模，
武器比例失调，剑太长或太短，
服饰混搭，中西混杂，
过度饱和，糖果色，廉价光效，
低多边形，卡通渲染，粗糙建模，
壁纸感，业余摄影，
模糊不清，像素化，低分辨率
```

## English Version (for global models)

```
avoid: 2D anime, cel-shading, watercolor, ink wash, flat cartoon,
Japanese anime style, Pixar, Disney,
modern elements, smartphones, cars, skyscrapers,
Western elements, European armor, Gothic castle,
plastic skin, over-smoothed, no visible pores,
hair blending into one mass, no visible strands,
deformed hands, six fingers, hand clipping,
incorrect weapon proportions, sword too long or short,
mixed costume styles, East-meets-West chaos,
oversaturated, candy colors, cheap light effects,
low-poly, cartoon rendering, crude modeling,
wallpaper feel, amateur photography,
blurry, pixelated, low resolution
```

---

## 按场景分类的负向清单

### 角色生成专用
```
避免：卡通大眼、扁平脸型、纸片人身材、棒球棍般的手臂、
塑料感头发、粗糙皮肤纹理、儿童画风
```

### 场景生成专用
```
避免：现代建筑、电子产品、汽车、霓虹灯、英文招牌、
高楼大厦、玻璃幕墙、合成感背景
```

### 武器生成专用
```
避免：变形比例、漂浮不自然、缺少阴影、光效过曝、
廉价塑料质感、不符合设定的纹样
```

### 战斗场面专用
```
避免：动作僵直、构图松散、人物重叠混乱、特效堆积、
动作不到位、缺少动感模糊
```

---

## 通用必加约束（不可省略）

### 必须加（中文）
```
1. 手部自然，手指数量正确
2. 发丝根根分明，有光泽变化
3. 服饰符合古代形制，不要混搭
4. 禁止出现现代元素
5. 保持东方美学，不要西方化
6. 人物比例正常，符合人体结构
```

### 必须加（English）
```
1. natural hands, correct finger count
2. individual hair strands visible with sheen
3. historically consistent costumes, no mixing
4. no modern elements
5. maintain Eastern aesthetics, avoid Westernization
6. normal human proportions, anatomically correct
```

---

## 高级避坑（可选）

### 防止"日本化"
```
additionally avoid: Japanese school uniform, sailor uniform, modern Japanese architecture, anime-specific eye styles, kawaii expressions
```

### 防止"好莱坞化"
```
additionally avoid: Western superhero proportions, spandex suits, Hollywood color grading, American comic book style
```

### 防止"网页游戏化"
```
additionally avoid: mobile game UI, gacha game style, MMORPG armor, MMO weapon design, pay-to-win aesthetic
```

---

*完整负向清单参考 niulai-style 的 v1.3 修复经验，针对国漫 3D 风格专门优化。*