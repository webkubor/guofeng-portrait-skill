#!/usr/bin/env python3
"""
Build prompts for the film-ambient (古风氛围胶片人像) style.

和另外两套画法的根本区别：这里不画"画"，是**用电影摄影拍真人**。
所以提示词由两层组成 —— 一层永不变（风格锚点），一层换着玩（场景槽位）。
"稳定出图"靠的就是这个分层：变的东西越少，出的图越像同一个人拍的。

固定层（FIXED_ZH / FIXED_EN）包含七维审美指纹里的六维：
  色彩（低饱和青绿月白、高光泛白、阴影灰绿）
  光（自然日光侧逆、发丝轮廓光）
  质感（东方电影摄影的镜头光学感、浅景深、柔焦）
  造型（半披半束长黑发、细窄丝带、素色纱衣、无繁复头饰）
  情绪（真人抓拍、空气感、电影静帧）
  负面（影楼味、仙侠光效、网红脸、塑料皮肤 —— 见 NEGATIVE_*）

命名风格库（PRESETS，21 个）—— 最省事的入口：
  --preset 花影柔光 blossom-veil / 雪落庭院 snow-court / 竹影清茶 bamboo-tea /
           灯下夜读 lamp-reading / 绿意回眸 green-glance / 湖畔暮光 lake-glow /
           江湖冷调 jianghu-cold / 落英慵卧 petal-recline / 提灯夜行 lantern-walk /
           回廊听雨 corridor-rain / 荷塘盛夏 lotus-summer / 月下独坐 moon-court /
           山巅风起 peak-wind / 雪原独行 snow-walk / 秋庭落笺 autumn-letter /
           舟头望水 boat-gaze / 松间晨雾 pine-dawn / 烛影摇红 candle-night /
           书斋静读 library-quiet / 月下横剑 moon-blade / 春雪寻梅 spring-plum
  完整菜单见 references/style-presets.md；--list 可打印全部。

可换槽位（六维）—— 显式传入会覆盖预设：
  --scene   环境（竹林庭院 / 雪庭 / 湖畔暮色 / 书案灯下 / 花影 / 夜色提灯 ...）
  --light   光型（斑驳树影 / 雪天散射 / 竹叶漏光 / 灯火暖调 / 暮色逆光 ...）
  --mood    情绪（安静疏离 / 易碎 / 怅惘 / 慵懒 / 温柔 / 清冷 ...）
  --film    胶片型号（Pro 400H 日系青绿 / Portra 400 暖奶油 / Superia 纪实 /
            CineStill 800T 夜景钨丝灯 / none 通用）
  --shot    机位与景别（抓拍半身 50mm f/1.8 / 抓拍特写 85mm f/1.4 / 俯拍 ...）
  --era     朝代形制（宋 / 唐 / 魏晋，与 dynasties/ 维度对齐，不指定则不加约束）
  --subject 具体主体描述（唯一必须自由发挥的部分）

Example（推荐：点风格 + 只改主体）:
  python scripts/build_prompt.py --style film-ambient \
      --preset blossom-veil --subject "凑近花枝，微微侧脸"

Example（手搭槽位）:
  python scripts/build_prompt.py --style film-ambient \
      --subject "轻轻蹲坐在青石旁，一只手随意拿着一小枝竹叶" \
      --scene bamboo-garden --light dappled-sun --film pro400h \
      --mood quiet-aloof --shot candid-half --era song --ratio 3:4

输出为 stdout 的 JSON：
  {
    "style": "film-ambient", "preset": "...", "scene": "...", "light": "...",
    "mood": "...", "shot": "...", "era": "...", "film": "...",
    "media": "image", "ratio": "3:4",
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
    "可见的 400 度胶片颗粒（是胶片颗粒，不是数码噪点），在暗部与中间调最明显；"
    "东方电影摄影的真实镜头光学感，浅景深，前景轻微虚化，背景柔和散景；"
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
    "visible 400-speed film grain (real film grain, not digital noise), most apparent in shadows and midtones; "
    "true lens optics of East Asian cinematography, shallow depth of field, "
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
    "corridor-rain": {
        "zh": "木质回廊檐下，雨幕垂落，青石地面泛着水光",
        "en": "under the eaves of a wooden corridor, curtains of rain falling, wet flagstones catching the light",
    },
    "lotus-pond": {
        "zh": "荷塘盛夏，荷叶与木栏，水面反光晃动",
        "en": "a lotus pond in high summer, lotus leaves and a wooden railing, reflections shifting on the water",
    },
    "moonlit-court": {
        "zh": "月下中式庭院，石阶与树影，夜色清冷",
        "en": "a Chinese courtyard under moonlight, stone steps and tree shadows, cool night air",
    },
    "mountain-peak": {
        "zh": "山巅云海，风起草伏，远景层叠山脊",
        "en": "a mountain summit above a sea of clouds, wind moving through grass, layered ridges beyond",
    },
    "snow-field": {
        "zh": "无垠雪原，枯树与远山，天地一片素白",
        "en": "an endless snowfield, bare trees and distant hills, the world reduced to white",
    },
    "autumn-court": {
        "zh": "秋日庭院，银杏与枫叶落满石径",
        "en": "an autumn courtyard, ginkgo and maple leaves scattered across a stone path",
    },
    "boat-river": {
        "zh": "江上小舟，船头望水，远岸淡去",
        "en": "a small boat on the river, standing at the bow, the far bank fading into haze",
    },
    "pine-mist": {
        "zh": "松林晨雾，石径半隐，光柱柔和",
        "en": "a pine forest in morning mist, a half-hidden stone path, soft shafts of light",
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
    "rain-soft": {
        "zh": "阴雨散射柔光，低对比，空气湿润发亮",
        "en": "soft diffused light in the rain, low contrast, humid air glowing",
    },
    "moonlight": {
        "zh": "月华侧照，银蓝冷调，暗部深沉而通透",
        "en": "moonlight from the side, silver-blue cast, deep yet luminous shadows",
    },
    "mist-dawn": {
        "zh": "晨雾漫射，光线柔和成柱，空气透视明显",
        "en": "dawn light diffused through mist, soft shafts, strong atmospheric depth",
    },
    "candle-flutter": {
        "zh": "烛火摇曳的暖点光，大面积暗部，暖冷对比强",
        "en": "flickering candlelight as a warm point source, large dark areas, strong warm-cool contrast",
    },
    "overcast-silver": {
        "zh": "阴天银调，无方向的高级灰柔光，电影感",
        "en": "overcast silver light, directionless soft grey, cinematic",
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
    "serene": {
        "zh": "恬静安然，呼吸匀长，眉眼舒展",
        "en": "serene and settled, unhurried breathing, softened brows",
    },
    "curious": {
        "zh": "抬眼探询，微微前倾，像在听什么",
        "en": "looking up in inquiry, leaning slightly in, as if listening to something",
    },
    "resolute": {
        "zh": "目光沉稳，下颌微收，不笑",
        "en": "steady unwavering gaze, chin slightly tucked, unsmiling",
    },
    "dreamy": {
        "zh": "半梦半醒，眼神失焦，神思在别处",
        "en": "half-awake, unfocused eyes, her mind somewhere else",
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
    "low-angle": {
        "zh": "机位略低于视线仰拍，气场与疏离感，天空或屋檐入画",
        "en": "camera slightly below eye level looking up, a sense of presence and distance, "
              "sky or eaves entering the frame",
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
# 槽位六：胶片型号（film）—— 把"胶片感"锚到具体型号，比形容词硬
#
# 模型对具体胶片名的响应，远强于"film grain / 胶片质感"这类泛词 ——
# 一个型号名同时锁定了色彩倾向、宽容度、高光行为与颗粒粗细。
# 默认 pro400h：它就是"日系胶片扫描"那个青绿通透调，最贴本画法的标杆九宫格。
# ============================================================

FILMS = {
    "none": {
        "zh": "日系胶片扫描质感，可见胶片颗粒，柔和高光晕染",
        "en": "Japanese film-scan texture, visible film grain, soft halation",
    },
    "pro400h": {
        "zh": "Fujifilm Pro 400H 胶片扫描质感：青绿偏冷的通透薄荷调，"
              "高光柔和溢出，真实可见的 400 度颗粒，肤色干净不发黄",
        "en": "Fujifilm Pro 400H film scan: airy mint-green cast with cool shadows, "
              "gently blooming highlights, visible 400-speed grain, clean non-yellowing skin tones",
    },
    "portra400": {
        "zh": "Kodak Portra 400 胶片扫描质感：暖调奶油肤色，宽容度高，"
              "阴影柔和通透，高光细腻不过曝",
        "en": "Kodak Portra 400 film scan: warm creamy skin tones, wide latitude, "
              "soft luminous shadows, delicate highlights that roll off without clipping",
    },
    "superia": {
        "zh": "Fujifilm Superia 胶片扫描质感：日常纪实感，轻微偏青，颗粒明显，"
              "生活化的不精致",
        "en": "Fujifilm Superia film scan: everyday documentary feel, slight cyan shift, "
              "pronounced grain, deliberately unpolished",
    },
    "cinestill800t": {
        "zh": "CineStill 800T 钨丝灯夜景胶片：高光周围有明显暖色 halation 光晕（光晕外扩，不是柔光），"
              "暗部偏深蓝，颗粒粗，夜戏电影感",
        "en": "CineStill 800T tungsten night film: pronounced warm halation blooming around "
              "highlights (halation spreading outward, not soft glow), deep blue shadows, "
              "coarse grain, night-scene cinematic feel",
    },
}


# ============================================================
# 命名风格库（presets）—— 把槽位组合固化成"能直接点的菜"
#
# 36 个槽位取值 = 十万种理论组合，对使用者等于没有菜单。
# 这里把验证过的组合命名固化：`--preset blossom-veil` 一条命令出图，
# 显式传入的单个槽位会覆盖预设（预设只提供基础值）。
#
# 前 9 个来自标杆九宫格（assets/gallery-9grid.jpg），后面是扩展。
# ============================================================

PRESETS = {
    # —— 以下 9 个对应标杆九宫格，逐格命名 ——
    "blossom-veil": {
        "zh": "花影柔光",
        "line": "花枝掩面，光落成影 —— 最柔的一张",
        "slots": {"scene": "blossom-shadow", "light": "dappled-sun", "mood": "tender",
                  "film": "pro400h", "shot": "candid-close", "era": "song"},
    },
    "snow-court": {
        "zh": "雪落庭院",
        "line": "雪落无声，人比雪静",
        "slots": {"scene": "snow-court", "light": "snow-diffuse", "mood": "fragile",
                  "film": "pro400h", "shot": "candid-half", "era": "song"},
    },
    "bamboo-tea": {
        "zh": "竹影清茶",
        "line": "竹影扫阶，一盏清茶，人不想动",
        "slots": {"scene": "bamboo-garden", "light": "bamboo-leak", "mood": "lazy",
                  "film": "pro400h", "shot": "candid-half", "era": "song"},
    },
    "lamp-reading": {
        "zh": "灯下夜读",
        "line": "一灯如豆，书页半掩，暗部留得住",
        "slots": {"scene": "study-lamp", "light": "lamp-warm", "mood": "wistful",
                  "film": "portra400", "shot": "candid-close", "era": "song"},
    },
    "green-glance": {
        "zh": "绿意回眸",
        "line": "绿意深处，忽然回头 —— 像被谁叫了一声",
        "slots": {"scene": "bamboo-garden", "light": "bamboo-leak", "mood": "quiet-aloof",
                  "film": "pro400h", "shot": "candid-turned", "era": "song"},
    },
    "lake-glow": {
        "zh": "湖畔暮光",
        "line": "暮色落水，人影快要成剪影",
        "slots": {"scene": "lakeside-dusk", "light": "dusk-backlight", "mood": "wistful",
                  "film": "portra400", "shot": "back-view", "era": "none"},
    },
    "jianghu-cold": {
        "zh": "江湖冷调",
        "line": "天地不仁，衣袂带霜",
        "slots": {"scene": "river-wind", "light": "overcast-silver", "mood": "cold-steel",
                  "film": "superia", "shot": "low-angle", "era": "none"},
    },
    "petal-recline": {
        "zh": "落英慵卧",
        "line": "落瓣满身，懒得起身",
        "slots": {"scene": "blossom-shadow", "light": "dappled-sun", "mood": "lazy",
                  "film": "pro400h", "shot": "candid-half", "era": "song"},
    },
    "lantern-walk": {
        "zh": "提灯夜行",
        "line": "一盏灯笼，只照亮半张脸",
        "slots": {"scene": "night-lantern", "light": "lantern-night", "mood": "quiet-aloof",
                  "film": "cinestill800t", "shot": "candid-turned", "era": "none"},
    },

    # —— 扩展风格 ——
    "corridor-rain": {
        "zh": "回廊听雨",
        "line": "檐外雨声很大，人没动",
        "slots": {"scene": "corridor-rain", "light": "rain-soft", "mood": "wistful",
                  "film": "pro400h", "shot": "candid-half", "era": "song"},
    },
    "lotus-summer": {
        "zh": "荷塘盛夏",
        "line": "盛夏荷风，眼睫低垂",
        "slots": {"scene": "lotus-pond", "light": "dappled-sun", "mood": "serene",
                  "film": "pro400h", "shot": "candid-half", "era": "song"},
    },
    "moon-court": {
        "zh": "月下独坐",
        "line": "月色很凉，人很静",
        "slots": {"scene": "moonlit-court", "light": "moonlight", "mood": "serene",
                  "film": "pro400h", "shot": "full-figure", "era": "none"},
    },
    "peak-wind": {
        "zh": "山巅风起",
        "line": "风从谷底上来，衣角和草一起倒",
        "slots": {"scene": "mountain-peak", "light": "mist-dawn", "mood": "resolute",
                  "film": "superia", "shot": "full-figure", "era": "none"},
    },
    "snow-walk": {
        "zh": "雪原独行",
        "line": "天地之间只剩她一个",
        "slots": {"scene": "snow-field", "light": "snow-diffuse", "mood": "fragile",
                  "film": "pro400h", "shot": "back-view", "era": "none"},
    },
    "autumn-letter": {
        "zh": "秋庭落笺",
        "line": "一叶落在信纸上，谁也没捡",
        "slots": {"scene": "autumn-court", "light": "dappled-sun", "mood": "wistful",
                  "film": "portra400", "shot": "candid-half", "era": "song"},
    },
    "boat-gaze": {
        "zh": "舟头望水",
        "line": "舟行水上，人在想别的事",
        "slots": {"scene": "boat-river", "light": "mist-dawn", "mood": "dreamy",
                  "film": "pro400h", "shot": "back-view", "era": "none"},
    },
    "pine-dawn": {
        "zh": "松间晨雾",
        "line": "雾里松针在滴水",
        "slots": {"scene": "pine-mist", "light": "mist-dawn", "mood": "serene",
                  "film": "pro400h", "shot": "full-figure", "era": "none"},
    },
    "candle-night": {
        "zh": "烛影摇红",
        "line": "烛火一跳，影子跟着晃",
        "slots": {"scene": "study-lamp", "light": "candle-flutter", "mood": "dreamy",
                  "film": "cinestill800t", "shot": "candid-close", "era": "none"},
    },
    "library-quiet": {
        "zh": "书斋静读",
        "line": "满墙旧书，一个人，没有声音",
        "slots": {"scene": "study-lamp", "light": "cold-window", "mood": "serene",
                  "film": "superia", "shot": "candid-half", "era": "song"},
    },
    "moon-blade": {
        "zh": "月下横剑",
        "line": "剑未出鞘，人已经冷了",
        "slots": {"scene": "mountain-peak", "light": "moonlight", "mood": "resolute",
                  "film": "superia", "shot": "low-angle", "era": "none"},
    },
    "spring-plum": {
        "zh": "春雪寻梅",
        "line": "梅开在残雪里，她凑近看",
        "slots": {"scene": "snow-court", "light": "dappled-sun", "mood": "curious",
                  "film": "pro400h", "shot": "candid-close", "era": "song"},
    },
}


# 不指定任何槽位时的兜底（也是最通用的起点）
DEFAULT_SLOTS = {
    "scene": "bamboo-garden",
    "light": "dappled-sun",
    "mood": "quiet-aloof",
    "film": "pro400h",
    "shot": "candid-half",
    "era": "none",
}


def resolve_slots(preset=None, **overrides):
    """预设提供基础值 → 显式传入的槽位覆盖它 → 其余用全局默认。

    overrides 里值为 None 表示"用户没传这个槽位"，不覆盖预设。
    """
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


def build_prompt(scene, light, mood, shot, era, film, subject, media, ratio, preset=None):
    """把固定风格层与六个槽位拼成中英双版提示词。"""
    for name, value, table in (
        ("scene", scene, SCENES),
        ("light", light, LIGHTS),
        ("mood", mood, MOODS),
        ("shot", shot, SHOTS),
        ("era", era, ERAS),
        ("film", film, FILMS),
    ):
        if value not in table:
            raise ValueError(f"未知 {name}: {value}")

    scene_zh, scene_en = SCENES[scene]["zh"], SCENES[scene]["en"]
    light_zh, light_en = LIGHTS[light]["zh"], LIGHTS[light]["en"]
    mood_zh, mood_en = MOODS[mood]["zh"], MOODS[mood]["en"]
    shot_zh, shot_en = SHOTS[shot]["zh"], SHOTS[shot]["en"]
    era_zh, era_en = ERAS[era]["zh"], ERAS[era]["en"]
    film_zh, film_en = FILMS[film]["zh"], FILMS[film]["en"]

    # 顺序遵循 dynasties/common-prompt-base.md 的 4 段式：
    # 主体 + 场景 + 光影 + 质感/规格，风格锚点贴身跟在主体之后。
    # film 落在"质感"段、shot（镜头规格）之前 —— 先定质感，再定镜头。
    parts_zh = [FIXED_ZH, subject]
    parts_en = [FIXED_EN, subject]
    if era_zh:
        parts_zh.append(era_zh)
        parts_en.append(era_en)
    parts_zh += [scene_zh, light_zh, mood_zh, film_zh, shot_zh]
    parts_en += [scene_en, light_en, mood_en, film_en, shot_en]

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
        "preset": preset,
        "scene": scene,
        "light": light,
        "mood": mood,
        "shot": shot,
        "era": era,
        "film": film,
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
    """打印命名风格库与所有槽位取值，方便人和 agent 选。"""
    print("=" * 72)
    print(f"film-ambient 命名风格库 / named styles（{len(PRESETS)} 个）")
    print("用法： --preset <slug>   显式传入的槽位会覆盖预设")
    print("=" * 72 + "\n")
    for key, value in PRESETS.items():
        s = value["slots"]
        print(f"  {key:<16} {value['zh']}")
        print(f"    {value['line']}")
        print(f"    scene={s['scene']}  light={s['light']}  mood={s['mood']}")
        print(f"    film={s['film']}  shot={s['shot']}  era={s['era']}\n")

    print("=" * 72)
    print("槽位一览 / available slots")
    print("=" * 72 + "\n")
    for title, table in (
        ("--scene  环境", SCENES),
        ("--light  光型", LIGHTS),
        ("--mood   情绪", MOODS),
        ("--film   胶片型号", FILMS),
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
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default=None,
                        help="命名风格（--list 看全部 21 个）；单槽位参数可覆盖预设")
    parser.add_argument("--scene", choices=list(SCENES.keys()), default=None,
                        help="环境槽位（默认 bamboo-garden 竹林庭院）")
    parser.add_argument("--light", choices=list(LIGHTS.keys()), default=None,
                        help="光型槽位（默认 dappled-sun 斑驳树影）")
    parser.add_argument("--mood", choices=list(MOODS.keys()), default=None,
                        help="情绪槽位（默认 quiet-aloof 安静疏离）")
    parser.add_argument("--shot", choices=list(SHOTS.keys()), default=None,
                        help="机位与景别槽位（默认 candid-half 抓拍半身 50mm f/1.8）")
    parser.add_argument("--era", choices=list(ERAS.keys()), default=None,
                        help="朝代形制槽位（默认 none，不注入形制约束）")
    parser.add_argument("--film", choices=list(FILMS.keys()), default=None,
                        help="胶片型号槽位（默认 pro400h = 日系青绿通透调；"
                             "夜景配 cinestill800t，暖调配 portra400）")
    parser.add_argument("--media", choices=["image", "video"], default="image",
                        help="生成媒介：image 静态图片（默认）/ video 视频片段")
    parser.add_argument("--ratio", choices=list(RATIO_TO_SIZE.keys()), default="3:4",
                        help="画面比例：3:4 竖版人像（默认）/ 9:16 / 16:9 / 1:1")
    parser.add_argument("--list", action="store_true",
                        help="只打印命名风格库与槽位取值，不出提示词")
    args = parser.parse_args()

    if args.list:
        print_presets()
        return 0

    if not args.subject:
        parser.error("--subject 是必填的（除非用 --list 看风格与槽位）")

    slots = resolve_slots(
        args.preset,
        scene=args.scene, light=args.light, mood=args.mood,
        film=args.film, shot=args.shot, era=args.era,
    )
    result = build_prompt(
        slots["scene"], slots["light"], slots["mood"], slots["shot"],
        slots["era"], slots["film"],
        args.subject, args.media, args.ratio, preset=args.preset,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
