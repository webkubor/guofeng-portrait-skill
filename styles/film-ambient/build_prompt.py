#!/usr/bin/env python3
"""
Build prompts for the film-ambient (古风氛围胶片人像) style.

和另外两套画法的根本区别：这里不画"画"，是**用电影摄影拍真人**。
所以提示词由两层组成 —— 一层永不变（风格锚点），一层换着玩（场景槽位）。
"稳定出图"靠的就是这个分层：变的东西越少，出的图越像同一个人拍的。

固定层（FIXED_ZH / FIXED_EN）包含七维审美指纹里的六维：
  色彩（低饱和青绿月白、高光泛白、阴影灰绿）
  光（自然日光侧逆、发丝轮廓光）
  质感（日系胶片扫描 + 东方电影摄影、颗粒、光晕、浅景深）
  造型（半披半束长黑发、细窄丝带、素色纱衣、无繁复头饰）
  情绪（真人抓拍、空气感、电影静帧）
  负面（影楼味、仙侠光效、网红脸、塑料皮肤 —— 见 NEGATIVE_*）

可换槽位（五维）：
  --scene   环境（竹林庭院 / 雪庭 / 湖畔暮色 / 书案灯下 / 花影 / 夜色提灯 ...）
  --light   光型（斑驳树影 / 雪天散射 / 竹叶漏光 / 灯火暖调 / 暮色逆光 ...）
  --mood    情绪（安静疏离 / 易碎 / 怅惘 / 慵懒 / 温柔 / 清冷）
  --shot    机位与景别（抓拍半身 50mm f/1.8 / 抓拍特写 85mm f/1.4 / 俯拍 ...）
  --era     朝代形制（宋 / 唐 / 魏晋，与 dynasties/ 维度对齐，不指定则不加约束）
  --subject 具体主体描述（唯一必须自由发挥的部分）

Example:
  python scripts/build_prompt.py --style film-ambient \
      --subject "轻轻蹲坐在青石旁，一只手随意拿着一小枝竹叶" \
      --scene bamboo-garden --light dappled-sun \
      --mood quiet-aloof --shot candid-half --era song --ratio 3:4

输出为 stdout 的 JSON：
  {
    "style": "film-ambient", "scene": "...", "light": "...", "mood": "...",
    "shot": "...", "era": "...", "media": "image", "ratio": "3:4",
    "subject": "...", "positive_zh": "...", "positive_en": "...",
    "negative_zh": "...", "negative_en": "...", "recommended_size": "1024x1536"
  }

模型选择：本风格首选 **GPT Image 2.5**（英文 prompt 更稳，皮肤微纹理是它的强项），
中文 `positive_zh` 留给 qwen-image / Seedream。理由与调法见
references/model-recommendations.md。
"""

import argparse
import json
import sys


# ============================================================
# 固定风格层 —— 每次出图都必须原样带上（这是"稳定"的来源）
# ============================================================

FIXED_ZH = (
    "真实摄影人像，非 CG 非二次元；20 岁左右年轻东亚女性，清透自然的古典美人气质，"
    "鹅蛋脸，五官精致但真实，皮肤白皙通透且保留真实肌肤纹理，自然淡粉唇；"
    "乌黑长发半披半束，发型简洁，仅用细窄浅色丝带固定，几缕碎发被微风吹过脸颊；"
    "素色轻薄飘逸的古风纱衣，面料带细腻丝织纹理，轻盈宽袖；"
    "清透色调，低饱和，高光微微泛白，阴影呈灰绿色；"
    "日系胶片扫描质感结合东方电影摄影，轻微胶片颗粒，柔和高光晕染，"
    "真实镜头光学感，浅景深，前景轻微虚化，背景柔和散景；"
    "真人抓拍感、空气感、电影静帧感、真实摄影质感"
)

FIXED_EN = (
    "real-photography portrait, not CGI, not anime; East Asian woman in her early 20s, "
    "clear natural classical beauty, egg-shaped face, refined but real features, "
    "luminous translucent skin with visible real skin texture, soft pale-pink lips; "
    "long black hair half-loose, simple styling held by a single thin pale ribbon, "
    "a few wisps of hair blown across her cheek; "
    "sheer flowing period silk robe in muted tones, fine woven texture, light wide sleeves; "
    "clean color grading, low saturation, slightly blown highlights, grey-green shadows; "
    "Japanese film-scan texture meets East Asian cinematography, subtle film grain, "
    "soft halation, true lens optics, shallow depth of field, "
    "slightly blurred foreground, soft background bokeh; "
    "candid documentary feel, airy atmosphere, cinematic still, real photographic texture"
)


# ============================================================
# 槽位一：环境（scene）
# ============================================================

SCENES = {
    "bamboo-garden": {
        "zh": "置身真实中式自然环境，竹林、古树、青石与庭院植物形成前后景层次，空气中有轻微夏日湿润感",
        "en": "a real Chinese garden environment, bamboo grove with old trees, mossy stones "
              "and garden plants layering the foreground and midground, faint summer humidity in the air",
    },
    "snow-court": {
        "zh": "雪后中式庭院，屋檐与枯枝覆雪，地面薄雪留有踩痕",
        "en": "a Chinese courtyard after snowfall, tiled eaves and bare branches under fresh snow, "
              "faint footprints in the thin snow on the ground",
    },
    "lakeside-dusk": {
        "zh": "湖畔暮色，远山轮廓与平静水面，芦苇在风里轻晃",
        "en": "a lakeside at dusk, distant hill silhouettes and still water, reeds swaying in the wind",
    },
    "study-lamp": {
        "zh": "深色木质书案与卷轴笔架，一盏旧油灯，室内暗调",
        "en": "a dark wooden desk with scrolls and a brush rack, one old oil lamp, dim interior",
    },
    "blossom-shadow": {
        "zh": "花枝掩映的中式庭院，粉白花瓣在光线里浮动，花影落在衣料上",
        "en": "a Chinese courtyard veiled by flowering branches, pale pink petals drifting in the light, "
              "flower shadows falling across the fabric",
    },
    "night-lantern": {
        "zh": "夜色中的中式庭院，手提纸灯笼，远处有零星光点",
        "en": "a Chinese courtyard at night, holding a paper lantern, scattered points of light in the distance",
    },
    "pine-terrace": {
        "zh": "松石亭台，木栏杆与石阶，远景是淡去的山",
        "en": "a pine and rock terrace with a wooden railing and stone steps, hills fading into the distance",
    },
    "river-wind": {
        "zh": "江畔旷野，风穿过草木，衣料与发丝被吹起",
        "en": "open riverside wilderness, wind moving through grass and trees, fabric and hair lifted by the breeze",
    },
}


# ============================================================
# 槽位二：光型（light）—— 逆光是本风格的骨架，永远有来源、有方向
# ============================================================

LIGHTS = {
    "dappled-sun": {
        "zh": "阳光穿过树叶，在人物脸部、衣服和地面形成不规则斑驳光影，发丝有轮廓光",
        "en": "sunlight filtering through leaves, irregular dappled shadows across her face, "
              "clothing and the ground, rim light on her hair",
    },
    "snow-diffuse": {
        "zh": "雪天散射柔光，低对比，冷调，面部受光均匀而无硬阴影",
        "en": "soft diffused light from snow, low contrast, cool tone, even light on the face without hard shadows",
    },
    "bamboo-leak": {
        "zh": "竹叶漏光，细碎光斑落在面部与肩头，明暗交界柔和",
        "en": "light leaking through bamboo leaves, fine specks of light on her face and shoulder, "
              "soft transition between light and shade",
    },
    "lamp-warm": {
        "zh": "单侧暖灯作主光，暖金光晕，暗部保留细节不死黑",
        "en": "a single warm lamp as key light, warm golden glow, shadow detail preserved without crushing blacks",
    },
    "dusk-backlight": {
        "zh": "暮色侧逆光，发丝与薄纱衣料透光，轮廓被光勾出",
        "en": "dusk backlight from the side, light passing through hair and sheer fabric, "
              "the silhouette outlined by light",
    },
    "lantern-night": {
        "zh": "夜色中手提灯笼的暖光，面部半明半暗，背景沉入深蓝",
        "en": "warm lantern light at night, her face half-lit and half in shadow, "
              "background sinking into deep blue",
    },
    "cold-window": {
        "zh": "冷调窗光侧照，柔和阴影呈灰绿，室内低调",
        "en": "cool window light from the side, soft grey-green shadows, low-key interior",
    },
}


# ============================================================
# 槽位三：情绪（mood）—— 姿态一律静态内敛，没有大笑与强动作
# ============================================================

MOODS = {
    "quiet-aloof": {
        "zh": "眼神安静清澈，略带疏离与好奇，嘴唇自然放松，不露齿笑",
        "en": "quiet clear gaze with a touch of distance and curiosity, relaxed lips, no teeth showing",
    },
    "fragile": {
        "zh": "易碎感，微垂眼睫，呼吸很轻，像随时会被风带走",
        "en": "a fragile presence, lowered lashes, barely-there breath, as if the wind could carry her away",
    },
    "wistful": {
        "zh": "怅惘，望向画外，似有心事未说",
        "en": "wistful, gazing off-frame, a quiet preoccupation left unspoken",
    },
    "lazy": {
        "zh": "慵懒，身体完全放松，重心自然偏斜",
        "en": "languid, body fully relaxed, weight naturally shifted",
    },
    "tender": {
        "zh": "温柔，神情浅淡柔和，唇角有极轻的弧度",
        "en": "tender, soft understated expression, the faintest curve at the corner of her mouth",
    },
    "cold-steel": {
        "zh": "清冷克制，下颌微抬，眼神带一点危险感",
        "en": "cool and restrained, chin slightly raised, a hint of danger in her eyes",
    },
}


# ============================================================
# 槽位四：机位与景别（shot）—— 抓拍，不是摆拍
# ============================================================

SHOTS = {
    "candid-half": {
        "zh": "抓拍半身，50mm 人像镜头 f/1.8，机位略高于视线，人物占画面约 65%，"
              "脸部清晰，前景轻微虚化，背景柔和散景，浅景深",
        "en": "candid waist-up framing, 50mm portrait lens at f/1.8, camera slightly above eye level, "
              "subject filling about 65% of the frame, face tack-sharp, slightly blurred foreground, "
              "soft background bokeh, shallow depth of field",
    },
    "candid-close": {
        "zh": "抓拍特写，85mm 人像镜头 f/1.4，极浅景深，面部细节与皮肤肌理清晰",
        "en": "candid close-up, 85mm portrait lens at f/1.4, very shallow depth of field, "
              "face detail and skin texture clearly rendered",
    },
    "full-figure": {
        "zh": "全身自然站姿或坐姿，35mm 镜头 f/2，环境在画面里占更大比重",
        "en": "full figure in a natural stance, 35mm lens at f/2, environment taking a larger share of the frame",
    },
    "high-angle": {
        "zh": "机位略高于人物视线，从斜上方俯拍，人物微微抬头看向镜头",
        "en": "camera slightly above eye level looking down, subject tilting her head up toward the lens",
    },
    "candid-turned": {
        "zh": "像摄影师突然叫住她的一瞬间，身体正在微微回头，动作停在半途",
        "en": "the instant a photographer calls out to her, caught mid-turn, the movement frozen halfway",
    },
    "back-view": {
        "zh": "背影或侧背影，发丝与衣料随风，人物面向环境深处",
        "en": "back or three-quarter-back view, hair and fabric caught by the wind, facing into the depth of the scene",
    },
}


# ============================================================
# 槽位五：朝代形制（era）—— 与 dynasties/ 维度对齐，只注入服饰与色彩 token
# ============================================================

ERAS = {
    "none": {"zh": "", "en": ""},
    "song": {
        "zh": "宋制形制：低饱和青绿与月白配色，轻薄丝织对襟褙子，细窄缘边",
        "en": "Song-dynasty styling: low-saturation celadon green and moon white, "
              "sheer silk front-buttoned beizi with narrow trim",
    },
    "tang": {
        "zh": "唐制形制：齐胸襦裙，披帛轻盈，色彩可略丰润",
        "en": "Tang-dynasty styling: high-waisted ruqun with a light silk shawl, slightly richer color",
    },
    "wei-jin": {
        "zh": "魏晋形制：褒衣博带，杂裾垂髾，衣料飘举出尘",
        "en": "Wei-Jin styling: loose robes with wide sashes and trailing panels, fabric lifting as if airborne",
    },
}


# ============================================================
# 负面词 —— 决定"高级感"的另一半，与另外两套画法不通用
# ============================================================

NEGATIVE_BASE_ZH = (
    "影楼汉服写真，仙侠玄幻光效，发光粒子，法阵，二次元，CG 感，3D 渲染，游戏原画，"
    "网红脸，幼态娃娃脸，过度磨皮，塑料皮肤，假皮肤，夸张妆容，"
    "复杂发冠，满头珠钗，正经摆拍，证件照构图，正面平光，过曝脸部，强 HDR，"
    "廉价古装摄影，高饱和糖果色，鲜艳大红大绿，现代元素，手指畸形，多余手指"
)

NEGATIVE_BASE_EN = (
    "studio hanfu photoshoot, xianxia glow effects, glowing particles, magic circles, "
    "anime, CGI, 3D render, game concept art, "
    "influencer face, doll-like childish face, over-smoothed skin, plastic skin, fake skin, "
    "heavy makeup, elaborate hair crown, heavy hair ornaments, stiff posing, ID-photo framing, "
    "flat frontal light, blown-out face, heavy HDR, cheap costume photography, "
    "oversaturated candy colors, garish red and green, modern elements, deformed hands, extra fingers"
)

NEGATIVE_VIDEO_ZH = "，动作僵硬，镜头呆板，人物变形，画面过锐"
NEGATIVE_VIDEO_EN = ", stiff motion, static camera, warped subject, over-sharpened frame"


# ============================================================
# 画幅 → 推荐像素尺寸
# ============================================================

RATIO_TO_SIZE = {
    "3:4": "1024x1536",
    "9:16": "1024x1536",
    "16:9": "1536x1024",
    "1:1": "1024x1024",
}


def build_prompt(scene, light, mood, shot, era, subject, media, ratio):
    """把固定风格层与五个槽位拼成中英双版提示词。"""
    for name, value, table in (
        ("scene", scene, SCENES),
        ("light", light, LIGHTS),
        ("mood", mood, MOODS),
        ("shot", shot, SHOTS),
        ("era", era, ERAS),
    ):
        if value not in table:
            raise ValueError(f"未知 {name}: {value}")

    scene_zh, scene_en = SCENES[scene]["zh"], SCENES[scene]["en"]
    light_zh, light_en = LIGHTS[light]["zh"], LIGHTS[light]["en"]
    mood_zh, mood_en = MOODS[mood]["zh"], MOODS[mood]["en"]
    shot_zh, shot_en = SHOTS[shot]["zh"], SHOTS[shot]["en"]
    era_zh, era_en = ERAS[era]["zh"], ERAS[era]["en"]

    # 顺序遵循 dynasties/common-prompt-base.md 的 4 段式：
    # 主体 + 场景 + 光影 + 质感/规格，风格锚点贴身跟在主体之后
    parts_zh = [FIXED_ZH, subject]
    parts_en = [FIXED_EN, subject]
    if era_zh:
        parts_zh.append(era_zh)
        parts_en.append(era_en)
    parts_zh += [scene_zh, light_zh, mood_zh, shot_zh]
    parts_en += [scene_en, light_en, mood_en, shot_en]

    if media == "video":
        parts_zh.append("真人实拍动态，发丝与衣料在风里自然流动，轻微手持呼吸感")
        parts_en.append("live-action motion, hair and fabric drifting naturally in the wind, "
                        "a slight handheld breathing feel")
        negative_zh = NEGATIVE_BASE_ZH + NEGATIVE_VIDEO_ZH
        negative_en = NEGATIVE_BASE_EN + NEGATIVE_VIDEO_EN
    else:
        negative_zh = NEGATIVE_BASE_ZH
        negative_en = NEGATIVE_BASE_EN

    return {
        "style": "film-ambient",
        "scene": scene,
        "light": light,
        "mood": mood,
        "shot": shot,
        "era": era,
        "media": media,
        "ratio": ratio,
        "subject": subject,
        "positive_zh": "，".join(p for p in parts_zh if p),
        "positive_en": "; ".join(p for p in parts_en if p),
        "negative_zh": negative_zh,
        "negative_en": negative_en,
        "recommended_size": RATIO_TO_SIZE.get(ratio, "1024x1536"),
        "note": "negative 没有独立字段：把 negative_en 用 'Avoid: ' 拼到提示词末尾（GPT Image 2.5 用英文版）",
    }


def print_presets():
    """打印所有槽位取值，方便人和 agent 选。"""
    print("film-ambient 槽位一览 / available slots\n")
    for title, table in (
        ("--scene  环境", SCENES),
        ("--light  光型", LIGHTS),
        ("--mood   情绪", MOODS),
        ("--shot   机位景别", SHOTS),
        ("--era    朝代形制", ERAS),
    ):
        print(f"{title}")
        for key, value in table.items():
            brief = value["zh"].split("，")[0]
            print(f"    {key:<16} {brief}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Build film-ambient (古风氛围胶片人像) generation prompts.",
    )
    parser.add_argument("--subject", help="具体主体描述与姿态，例如：轻轻蹲坐在青石旁，手里拿着一小枝竹叶")
    parser.add_argument("--scene", choices=list(SCENES.keys()), default="bamboo-garden",
                        help="环境槽位（默认 bamboo-garden 竹林庭院）")
    parser.add_argument("--light", choices=list(LIGHTS.keys()), default="dappled-sun",
                        help="光型槽位（默认 dappled-sun 斑驳树影）")
    parser.add_argument("--mood", choices=list(MOODS.keys()), default="quiet-aloof",
                        help="情绪槽位（默认 quiet-aloof 安静疏离）")
    parser.add_argument("--shot", choices=list(SHOTS.keys()), default="candid-half",
                        help="机位与景别槽位（默认 candid-half 抓拍半身 50mm f/1.8）")
    parser.add_argument("--era", choices=list(ERAS.keys()), default="none",
                        help="朝代形制槽位（默认 none，不注入形制约束）")
    parser.add_argument("--media", choices=["image", "video"], default="image",
                        help="生成媒介：image 静态图片（默认）/ video 视频片段")
    parser.add_argument("--ratio", choices=list(RATIO_TO_SIZE.keys()), default="3:4",
                        help="画面比例：3:4 竖版人像（默认）/ 9:16 / 16:9 / 1:1")
    parser.add_argument("--list", action="store_true", help="只打印所有槽位取值，不出提示词")
    args = parser.parse_args()

    if args.list:
        print_presets()
        return 0

    if not args.subject:
        parser.error("--subject 是必填的（除非用 --list 看槽位）")

    result = build_prompt(
        args.scene, args.light, args.mood, args.shot, args.era,
        args.subject, args.media, args.ratio,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
