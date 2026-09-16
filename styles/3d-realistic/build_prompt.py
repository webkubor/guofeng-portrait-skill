#!/usr/bin/env python3
"""
Build prompts for the Donghua 3D Realistic style (国漫 3D 写实 · 古风美人).

本画法**只画女性** —— 这个 skill 是「古风美人」，不做男性角色。

重写于 v3.5.0 —— 旧版固定层只有一句"PBR材质，皮肤有呼吸感…唯美空灵"，
没有任何脸型 / 年龄 / 骨相 / 比例约束，导致模型自由发挥成**幼态娃娃脸 + 塑料皮
+ 满头堆砌 + 满屏荧光**。新版把「审美签名」写死：

  70% 真人质感 + 30% 国漫理想化   ← 最关键的一句
  20 岁左右成年东方少女骨相（不是幼童、不是御姐）

固定层（FEMALE_FIXED / MALE_FIXED）包含永不改变的审美签名：
  比例（70/30）· 年龄与骨相（成年，小鹅蛋脸，下巴短小圆润）· 五官规格（圆润杏眼、
  真实虹膜晶体层次、樱粉唇）· 皮肤（SSS + 微毛孔 + 克制高光，不磨皮不蜡像）·
  发（strand-based，碎发）· 发饰克制不堆砌 · 技术栈（PBR/RT/GI/85mm f/1.4/film grading）

可换槽位（四维）：
  --scene   场景（黄昏庭院 / 云雾山巅 / 竹林 / 雪中古寺 ...）
  --light   光位（暖金侧逆光 / 柔和窗光 / 灯笼暖光 / 月华冷光 ...）
  --framing 景别（超近头肩肖像 / 头肩 / 半身 / 全身 / 侧脸特写）
  --mood    情绪（轻轻靠近 / 安静 / 清冷 / 坚定 / 浅笑）

命名风格（PRESETS）：
  heroine-closeup 国漫女主特写 ⭐ 基准    heroine-lantern 灯下少女
  bamboo-quiet 竹林静女                  snow-temple 雪寺清影
  swordsman-night 月下剑修（男）          sect-master 宗门宗主（男）

Example:
  python scripts/build_prompt.py --style 3d-realistic \
      --category character-female --preset heroine-closeup \
      --subject "轻轻向镜头靠近，直视镜头"

输出为 stdout 的 JSON：
  {
    "style": "3d-realistic", "preset": "...", "category": "character-female",
    "scene": "...", "light": "...", "framing": "...", "mood": "...",
    "media": "image", "ratio": "3:4", "subject": "...",
    "positive_zh": "...", "positive_en": "...",
    "negative_zh": "...", "negative_en": "...", "recommended_size": "1024x1536"
  }
"""

import argparse
import json
import sys


# ============================================================
# 固定层：审美签名（永不改变）
#
# 这两段是整个画法的命门 —— 旧版就败在这里。改动前务必想清楚：
# 去掉「70% 真人质感 + 30% 国漫理想化」或「成年少女骨相」，
# 画面会立刻退回幼态娃娃脸。
# ============================================================

FEMALE_FIXED_ZH = (
    "高级中国国漫电影级 CGI，美型但保留真人骨相，70% 真人质感 + 30% 国漫理想化；"
    "20 岁左右成年东方女性，精致鹅蛋脸，但骨相与比例明确是成年人的（不是儿童比例），"
    "面中饱满、下颌结构清晰，下颌线流畅，下巴圆润不尖不长；"
    "清澈的暖棕色杏仁眼，与脸型比例协调、不过大，眼型圆润但不二次元夸张，"
    "虹膜具有真实晶体层次与细密纹理，"
    "湿润自然的眼神高光，细长自然睫毛；眉形柔和自然；小巧挺直鼻梁，鼻头圆润精致；"
    "柔软饱满的樱粉色嘴唇，唇峰自然，嘴角轻微放松；"
    "皮肤白皙通透但有真实血色，脸颊只有极淡的自然血色（不是浓重腮红），"
    "细腻真实皮肤纹理与可见毛孔，"
    "柔和次表面散射，鼻尖、眼下、脸颊有克制的自然高光，不磨皮、不塑料、不蜡像；"
    "乌黑浓密长发，发丝逐根清晰，额前与脸颊有纤细自然碎发；"
    "发饰小巧精致、克制不堆砌；"
    "高级东方审美，精致、灵动、自然、有生命感"
)

FEMALE_FIXED_EN = (
    "high-end Chinese animation cinematic CGI, idealized yet retaining real human bone structure, "
    "70% photoreal texture + 30% donghua idealization; "
    "East Asian woman in her early twenties, refined oval face with distinctly ADULT facial proportions "
    "and bone structure (NOT childlike proportions), full midface, defined jaw, smooth jawline, "
    "rounded chin — neither pointed nor elongated; "
    "clear warm-brown almond eyes, proportionate to the face rather than oversized, "
    "rounded but not exaggeratedly anime, iris with real crystalline "
    "depth and fine texture, moist natural catchlights, fine natural lashes; soft natural brows; "
    "small straight nose with a refined rounded tip; soft pale-pink lips, natural shape without "
    "exaggeration, neither glossy nor plump, gently relaxed corners; "
    "fair translucent skin with real blood tone, only the faintest natural flush on the "
    "cheeks (NOT heavy blush), fine real skin texture with visible pores, soft subsurface scattering, "
    "restrained natural "
    "highlights on the nose tip, under the eyes and on the cheeks — not airbrushed, not plastic, not waxen; "
    "thick black hair with individually resolved strands and fine loose wisps at the forehead and cheeks; "
    "small refined hair ornaments, restrained, never piled up; "
    "refined oriental aesthetics, delicate, lively, natural, alive"
)

# 通用技术栈与镜头规格（决定"电影级 CGI"的质感下限）
TECH_ZH = (
    "realistic CGI portrait，PBR skin shader，subsurface scattering，ray tracing，"
    "global illumination，realistic iris，strand-based hair，film color grading，"
    "85mm 人像镜头，f/1.4，极浅景深，柔和电影级散景，电影截图感"
)

TECH_EN = (
    "realistic CGI portrait, PBR skin shader, subsurface scattering, ray tracing, "
    "global illumination, realistic iris, strand-based hair, film color grading, "
    "85mm portrait lens, f/1.4, very shallow depth of field, soft cinematic bokeh, "
    "cinematic still"
)

CATEGORIES = {
    "character-female": {"zh": FEMALE_FIXED_ZH, "en": FEMALE_FIXED_EN},
}


# ============================================================
# 槽位一：场景（scene）—— 背景必须"完全虚化"，只留氛围信息
# ============================================================

SCENES = {
    "dusk-courtyard": {
        "zh": "黄昏古代庭院背景，木质建筑与暖黄色灯笼光斑，背景完全虚化",
        "en": "dusk in an ancient Chinese courtyard, wooden architecture and warm yellow lantern "
              "bokeh, background fully blurred",
    },
    "mist-mountain": {
        "zh": "云雾山巅，远山层叠，空气透视明显，背景虚化",
        "en": "misty mountain summit, layered distant ridges, strong atmospheric perspective, "
              "background blurred",
    },
    "bamboo-grove": {
        "zh": "竹林与木屋，竹叶层次分明，背景虚化",
        "en": "bamboo grove beside a wooden hut, layered bamboo leaves, background blurred",
    },
    "palace-hall": {
        "zh": "深色木质殿堂内部，烛台与帷幔，背景虚化",
        "en": "interior of a dark wooden hall, candle stands and hanging drapes, background blurred",
    },
    "lantern-street": {
        "zh": "古代灯市长街，成排灯笼延伸向远处，背景虚化",
        "en": "an ancient lantern-lit street, rows of lanterns receding into the distance, "
              "background blurred",
    },
    "snow-temple": {
        "zh": "雪中古寺，屋檐覆雪，冷调空气，背景虚化",
        "en": "an old temple in snow, snow-covered eaves, cool air, background blurred",
    },
    "plum-garden": {
        "zh": "梅林花影，枝干与花簇形成前景层次，背景虚化",
        "en": "a plum grove, branches and blossoms layering the foreground, background blurred",
    },
    "study-room": {
        "zh": "书斋内部，书架、卷轴与笔架，背景虚化",
        "en": "a scholar's study, bookshelves, scrolls and a brush rack, background blurred",
    },
    "moonlit-terrace": {
        "zh": "月下石台，栏杆与远处屋脊剪影，背景虚化",
        "en": "a stone terrace under moonlight, railing and distant roof silhouettes, background blurred",
    },
}


# ============================================================
# 槽位二：光位（light）—— 必须有出处，且保留立体骨相
# ============================================================

LIGHTS = {
    "warm-backlight": {
        "zh": "暖金色夕阳从人物左后方照射，形成柔和金色发丝轮廓光，"
              "脸部为自然柔光，冷暖平衡，面部不过曝，柔和阴影保留立体骨相，空气中轻微暖色雾感",
        "en": "warm golden sunset light from behind-left, soft golden rim light on the hair, "
              "gentle natural fill on the face, balanced warm-cool, face not overexposed, "
              "soft shadows preserving three-dimensional bone structure, faint warm haze in the air",
    },
    "soft-window": {
        "zh": "柔和窗光侧照，明暗过渡自然，面部立体感保留，不过曝",
        "en": "soft window light from the side, natural falloff, facial structure preserved, not overexposed",
    },
    "lantern-glow": {
        "zh": "灯笼暖光作为主光源，暖金光晕，暗部保留细节，冷暖对比",
        "en": "warm lantern light as the key source, golden glow, shadow detail preserved, warm-cool contrast",
    },
    "moonlight-cool": {
        "zh": "月华冷光侧照，银蓝冷调，暗部通透，人物轮廓被冷光勾出",
        "en": "cool moonlight from the side, silver-blue cast, luminous shadows, silhouette edged by cold light",
    },
    "candle-warm": {
        "zh": "烛火暖点光，大面积暗部，面部受光集中在近光源一侧",
        "en": "warm candlelight as a point source, large dark areas, light concentrated on the side nearest the flame",
    },
    "overcast-soft": {
        "zh": "阴天柔和散射光，低对比，无硬阴影，质感干净",
        "en": "soft overcast diffusion, low contrast, no hard shadows, clean rendering",
    },
}


# ============================================================
# 槽位三：景别（framing）
# ============================================================

FRAMINGS = {
    "closeup-head": {
        "zh": "超近距离头肩肖像，脸部占画面约 70%-80%，正面微微偏侧",
        "en": "extreme close-up head-and-shoulders portrait, face filling about 70-80% of the frame, "
              "front-facing with a slight turn",
    },
    "head-shoulder": {
        "zh": "头肩肖像，脸部占画面约 50%-60%，构图留出呼吸空间",
        "en": "head-and-shoulders portrait, face filling about 50-60% of the frame, "
              "composition leaves breathing room",
    },
    "half-body": {
        "zh": "半身像，人物占画面约 60%，服装形制与手部动作可见",
        "en": "half-body portrait, subject filling about 60% of the frame, costume silhouette and "
              "hand gesture visible",
    },
    "full-body": {
        "zh": "全身立绘，人物占画面约 40%，环境与衣料垂坠可见",
        "en": "full-body portrait, subject filling about 40% of the frame, environment and fabric drape visible",
    },
    "profile-closeup": {
        "zh": "侧脸特写，强调鼻梁、下颌线与颈部线条",
        "en": "profile close-up, emphasising the nose bridge, jawline and neck line",
    },
}


# ============================================================
# 槽位四：情绪（mood）
# ============================================================

MOODS = {
    "gentle-approach": {
        "zh": "轻轻向镜头靠近，直视镜头，眼神清澈直接，嘴唇自然放松",
        "en": "leaning gently toward the lens, looking straight into the camera, clear direct gaze, "
              "lips naturally relaxed",
    },
    "quiet": {
        "zh": "安静，情绪内敛，眼神落在画外",
        "en": "quiet, inward composure, gaze resting off-frame",
    },
    "cold": {
        "zh": "清冷克制，下颌微抬，神情疏离",
        "en": "cool and restrained, chin slightly raised, distant expression",
    },
    "resolute": {
        "zh": "坚定，目光沉稳，眉头舒展不怒",
        "en": "resolute, steady gaze, brow relaxed rather than fierce",
    },
    "soft-smile": {
        "zh": "浅淡的笑意，唇角微微上扬，不露齿",
        "en": "a faint smile, corner of the mouth slightly lifted, no teeth showing",
    },
}


# ============================================================
# 命名风格（presets）
# ============================================================

PRESETS = {
    "heroine-closeup": {
        "zh": "国漫女主特写 ⭐ 基准",
        "line": "70% 真人 + 30% 理想化，小鹅蛋脸成年少女骨相 —— 本画法的基准样张",
        "category": "character-female",
        "slots": {"scene": "dusk-courtyard", "light": "warm-backlight",
                  "framing": "closeup-head", "mood": "gentle-approach"},
    },
    "heroine-lantern": {
        "zh": "灯下少女",
        "line": "灯笼暖光做主光，暗部留住，冷暖对比",
        "category": "character-female",
        "slots": {"scene": "lantern-street", "light": "lantern-glow",
                  "framing": "head-shoulder", "mood": "quiet"},
    },
    "bamboo-quiet": {
        "zh": "竹林静女",
        "line": "竹林层次 + 柔和窗光般的散射，安静内敛",
        "category": "character-female",
        "slots": {"scene": "bamboo-grove", "light": "overcast-soft",
                  "framing": "half-body", "mood": "quiet"},
    },
    "snow-temple": {
        "zh": "雪寺清影",
        "line": "雪中古寺冷调，月华或散射光，清冷疏离",
        "category": "character-female",
        "slots": {"scene": "snow-temple", "light": "moonlight-cool",
                  "framing": "head-shoulder", "mood": "cold"},
    },
}


DEFAULT_SLOTS = {
    "scene": "dusk-courtyard",
    "light": "warm-backlight",
    "framing": "closeup-head",
    "mood": "gentle-approach",
}


def resolve_slots(preset=None, **overrides):
    """预设提供基础值 → 显式传入的槽位覆盖它 → 其余用全局默认。"""
    slots = dict(DEFAULT_SLOTS)
    if preset:
        if preset not in PRESETS:
            raise ValueError(f"未知预设 {preset!r}，可选：{' / '.join(PRESETS)}")
        slots.update(PRESETS[preset]["slots"])
    for key, value in overrides.items():
        if value is not None:
            slots[key] = value
    return slots


# ============================================================
# 负面词 —— 分两组：通用排雷 + 本画法专属（幼态 / 塑料 / 堆砌 / 荧光）
#
# 「幼态组」是旧版最大的漏洞：只写"避免 big anime eyes"却不堵幼童脸，
# 模型会默认滑向娃娃脸。这一组必须原样保留。
# ============================================================

NEGATIVE_ZH = (
    # —— 幼态 / 脸型（旧版最大漏洞）——
    "幼童，儿童脸，过度婴儿肥，圆饼脸，尖锥脸，长脸，成熟御姐，欧美骨相，"
    "网红脸，韩式整容脸，蛇精脸，娃娃脸，童颜，幼态，浓重腮红，油亮唇，玻尿酸唇，滤镜脸，眼睛过大，"
    # —— 五官失真 ——
    "眼睛巨大，动漫眼，眼距异常，斗鸡眼，死鱼眼，假睫毛过重，鼻梁过高，鼻头过尖，"
    "嘴巴过小，嘴歪，五官僵硬，假笑，"
    # —— 皮肤质感 ——
    "过度美颜，磨皮，塑料皮，蜡像，油光，过度锐化，廉价3D，游戏NPC，"
    # —— 画风跑偏 ——
    "二次元平涂，赛璐璐，日漫风格，皮克斯，迪士尼，水墨，工笔，平面卡通，"
    # —— 廉价堆砌 / 无出处光效（旧版病灶）——
    "仙侠荧光粒子，魔法光带，满天飞光，塑料发光，体积光滥用，高饱和糖果色，"
    "发饰堆砌，满头珠翠，复杂头冠，复杂背景，通用云海背景，"
    # —— 其他 ——
    "影楼古装写真，过曝，霓虹灯，现代元素，西方元素，文字，水印，logo，"
    "手部畸形，六根手指，服饰混搭，中西混杂"
)

NEGATIVE_EN = (
    "toddler, child face, excessive baby fat, round pancake face, sharp cone face, long face, "
    "mature femme fatale, Western bone structure, influencer face, Korean plastic-surgery face, "
    "v-shape snake face, baby face, childlike facial proportions, heavy blush, glossy lips, "
    "filler lips, beauty-filter face, oversized eyes, "
    "giant eyes, anime eyes, abnormal eye spacing, cross-eyed, dead fish eyes, heavy fake lashes, "
    "overly high nose bridge, overly pointed nose tip, tiny mouth, crooked mouth, stiff features, fake smile, "
    "over-retouched, airbrushed skin, plastic skin, wax figure, greasy shine, over-sharpened, "
    "cheap 3D, game NPC, "
    "2D flat shading, cel-shading, Japanese anime style, Pixar, Disney, ink wash, gongbi, flat cartoon, "
    "xianxia glow particles, magic light ribbons, floating light spam, plastic glow, volumetric light abuse, "
    "oversaturated candy colors, piled-up hair ornaments, heavy jeweled crown, cluttered background, "
    "generic sea-of-clouds backdrop, "
    "studio costume photoshoot, blown-out highlights, neon lights, modern elements, Western elements, "
    "text, watermark, logo, deformed hands, six fingers, mixed costumes, East-meets-West chaos"
)

NEGATIVE_VIDEO_ZH = "，动作僵硬，面部崩坏，肢体变形，镜头呆板"
NEGATIVE_VIDEO_EN = ", stiff motion, face morphing, limb deformation, static camera"


# ============================================================
# 画幅 → 推荐像素尺寸
# ============================================================

RATIO_TO_SIZE = {
    "3:4": "1024x1536",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "1:1": "1024x1024",
}


def build_prompt(category, media, subject, ratio,
                 scene=None, light=None, framing=None, mood=None, preset=None):
    """把固定层（审美签名）+ 四个槽位 + 主体描述拼成中英双版提示词。"""
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")

    slots = resolve_slots(preset, scene=scene, light=light, framing=framing, mood=mood)


    for name, value, table in (
        ("scene", slots["scene"], SCENES),
        ("light", slots["light"], LIGHTS),
        ("framing", slots["framing"], FRAMINGS),
        ("mood", slots["mood"], MOODS),
    ):
        if value not in table:
            raise ValueError(f"未知 {name}: {value}")

    # 顺序：固定层（审美签名）→ 主体 → 景别 → 情绪 → 场景 → 光位 → 技术栈
    # 技术栈放最后 —— 它是规格，不是内容（同 dynasties/common-prompt-base.md 的 4 段式）
    parts_zh = [
        CATEGORIES[category]["zh"],
        subject,
        FRAMINGS[slots["framing"]]["zh"],
        MOODS[slots["mood"]]["zh"],
        SCENES[slots["scene"]]["zh"],
        LIGHTS[slots["light"]]["zh"],
        TECH_ZH,
    ]
    parts_en = [
        CATEGORIES[category]["en"],
        subject,
        FRAMINGS[slots["framing"]]["en"],
        MOODS[slots["mood"]]["en"],
        SCENES[slots["scene"]]["en"],
        LIGHTS[slots["light"]]["en"],
        TECH_EN,
    ]

    if media == "video":
        parts_zh.append("电影级动态，发丝与衣料自然流动")
        parts_en.append("cinematic motion, hair and fabric moving naturally")
        negative_zh = NEGATIVE_ZH + NEGATIVE_VIDEO_ZH
        negative_en = NEGATIVE_EN + NEGATIVE_VIDEO_EN
    else:
        negative_zh = NEGATIVE_ZH
        negative_en = NEGATIVE_EN

    return {
        "style": "3d-realistic",
        "preset": preset,
        "category": category,
        "scene": slots["scene"],
        "light": slots["light"],
        "framing": slots["framing"],
        "mood": slots["mood"],
        "media": media,
        "ratio": ratio,
        "subject": subject,
        "positive_zh": "，".join(p for p in parts_zh if p),
        "positive_en": ", ".join(p for p in parts_en if p),
        "negative_zh": negative_zh,
        "negative_en": negative_en,
        "recommended_size": RATIO_TO_SIZE.get(ratio, "1024x1024"),
        "note": "negative 无独立字段：用 'Avoid: ' 把 negative_en 拼到提示词末尾",
    }


def print_presets():
    """打印命名风格与槽位取值。"""
    print("=" * 72)
    print(f"3d-realistic 命名风格 / named styles（{len(PRESETS)} 个）")
    print("用法： --preset <slug>   显式传入的槽位会覆盖预设")
    print("=" * 72 + "\n")
    for key, value in PRESETS.items():
        s = value["slots"]
        print(f"  {key:<18} {value['zh']}  [{value['category']}]")
        print(f"    {value['line']}")
        print(f"    scene={s['scene']}  light={s['light']}  framing={s['framing']}  mood={s['mood']}\n")

    print("=" * 72)
    print("槽位一览 / available slots")
    print("=" * 72 + "\n")
    for title, table in (
        ("--scene   场景", SCENES),
        ("--light   光位", LIGHTS),
        ("--framing 景别", FRAMINGS),
        ("--mood    情绪", MOODS),
    ):
        print(title)
        for key, value in table.items():
            print(f"    {key:<18} {value['zh'].split('，')[0]}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Build donghua 3D realistic (国漫 3D 写实) generation prompts.",
    )
    parser.add_argument("--category", choices=list(CATEGORIES.keys()), default="character-female",
                        help="主体分类：仅 character-female（本 skill 只画女性）")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default=None,
                        help="命名风格（--list 看全部）；单槽位参数可覆盖预设")
    parser.add_argument("--scene", choices=list(SCENES.keys()), default=None, help="场景槽位")
    parser.add_argument("--light", choices=list(LIGHTS.keys()), default=None, help="光位槽位")
    parser.add_argument("--framing", choices=list(FRAMINGS.keys()), default=None, help="景别槽位")
    parser.add_argument("--mood", choices=list(MOODS.keys()), default=None, help="情绪槽位")
    parser.add_argument("--media", choices=["image", "video"], default="image",
                        help="生成媒介：image 静态图片（默认）/ video 视频片段")
    parser.add_argument("--subject", help="主体描述与姿态")
    parser.add_argument("--ratio", choices=list(RATIO_TO_SIZE.keys()), default="3:4",
                        help="画面比例：3:4 竖版（默认）/ 16:9 / 9:16 / 1:1")
    parser.add_argument("--list", action="store_true", help="只打印命名风格与槽位取值")
    args = parser.parse_args()

    if args.list:
        print_presets()
        return 0

    if not args.subject:
        parser.error("--subject 是必填的（除非用 --list 看风格与槽位）")

    result = build_prompt(
        args.category, args.media, args.subject, args.ratio,
        scene=args.scene, light=args.light, framing=args.framing,
        mood=args.mood, preset=args.preset,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
