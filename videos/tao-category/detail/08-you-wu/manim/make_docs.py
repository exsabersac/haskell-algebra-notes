# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S6Haskell": ["s_wu", "s_you", "s_units", "s_probe", "s_demo"],
}
SNIP_FILE = {k: "YouWu.hs" for k in ["s_wu", "s_you", "s_units", "s_probe", "s_demo"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("始对象 / 终对象", "initial / terminal object"),
    ("对偶范畴 Cᵒᵖ", "opposite category"),
    ("和（余积）/ 积", "sum (coproduct) / product"),
    ("全局元素", "global element"),
    ("否定 Not a", "negation (a → Void)"),
    ("普遍性质", "universal property"),
    ("Void / 单元类型 ()", "Void / unit type ()"),
]


def script_md():
    L = []
    L.append("# 道可道 · 进阶深讲 08 —— 有无相生\n")
    L.append("*始/终对偶、积与余积、探针与否定｜Initial/terminal duality — Advanced Deep Dive 08*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已完成入门深讲 01–06 与进阶 07；先范畴论陈述，再短 Haskell。\n"
             "- 结构：道德经钩子 → 始与终 → 对偶范畴 → 积与余积 → 探针与否定 → 短 Haskell → 下集道生一。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-08.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/YouWu.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。比入门 02 更深：对偶范畴、积/余积、探针与否定。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 阴阳 | 1 Clean Slate（Yin and Yang） | 1.5 |\n"
             "| 始与终 | 1 Elements | 1.5 Initial / Terminal |\n"
             "| 对偶范畴 | 1 Yin and Yang | 1.5 dual / opposite |\n"
             "| 积与余积 | 1 | 1.5 Products and Coproducts；1.6 |\n"
             "| 探针与否定 | 1 Elements | 1.5 / 1.6 |\n"
             "| 短 Haskell | 1 / 本集 YouWu.hs | 1.6 |\n"
             "| 下集预告 | 7 Recursion | 3.8 F-Algebras |\n")
    L.append("\n## 术语表\n\n| 中文 | English |\n|---|---|\n" + "".join(f"| {a} | {b} |\n" for a, b in GLOSSARY))
    for s in SCENES:
        off, d = A["offsets"][s["id"]]
        tm = json.load(open(f"{ROOT}/build/timings/{s['id']}.json"))
        L.append(f"\n---\n\n## {s['title']}　`{ts(off)}–{ts(off + d)}`\n")
        if s["quote"]:
            L.append(f"\n> **{s['quote']}**　——{s['chapter']}\n")
        if s["refs"]:
            L.append("\n参考：" + "；".join(s["refs"]) + "\n")
        L.append("\n| 时间 | 旁白 | 画面 / 代码 |\n|---|---|---|\n")
        for k, b in enumerate(s["beats"]):
            L.append(f"| {ts(off + tm['starts'][k])} | {b['say']} | {b.get('note', '')} |\n")
        for nm in SNIPS.get(s["id"], []):
            L.append(f"\n屏幕代码 `{nm}`（`haskell/src/{SNIP_FILE[nm]}`）：\n\n```haskell\n" + "\n".join(load_snip(nm)) + "\n```\n")
    L.append("\n---\n\n## 数学校对备注\n\n"
             "- 依 CTFP 惯例在 Hask 中忽略 ⊥（`Void` 作为始对象、`a -> Void` 作为否定都在此约定下成立）。\n"
             "- 始/终按 Hom-集唯一性定义；对偶范畴 Cᵒᵖ 使 0_C = 1_{Cᵒᵖ}。\n"
             "- 积/余积以普遍性质对偶陈述；Void / () 分别为余积 / 积的单位。\n"
             "- 全局元素 = 1 → a；Not a = a → Void。入门 02 已覆盖 Void/() 直觉，本集加深对偶与积/余积。\n"
             "- 下集预告：道生一（初始代数）——不在本集展开。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：有无相生",
        "S1Hook": "一 道德经钩子",
        "S2InitialTerminal": "二 始与终",
        "S3Opposite": "三 对偶范畴",
        "S4ProdCoprod": "四 积与余积",
        "S5ProbeNegation": "五 探针与否定",
        "S6Haskell": "六 短 Haskell",
        "S7Next": "结语：下集道生一",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "有无相生：始/终对偶与积余积 | 进阶深讲 08"
    desc = f"""进阶深讲第八集。比入门 02 更深：对偶范畴、积与余积、全局元素与否定。

· 钩子：有无相生（DaoFP 阴阳）
· 始与终：Hom 唯一性
· 对偶范畴 Cᵒᵖ：无是倒过来的有
· 积 ↔ 余积；Void / () 为单位
· 探针 ()→a 与否定 a→Void
· 短 Haskell：wu / you / units / element / Not
· 下集：道生一 · 初始代数

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.1 Clean Slate（Yin and Yang / Elements） —— https://github.com/BartoszMilewski/DaoFP
· CTFP 1.5–1.6 —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第二章

系列：道可道 · 进阶深讲。上一集《道可道》；下一集《道生一》。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #有无相生 #对偶 #积 #余积 #道可道
"""
    tags = ["范畴论", "Haskell", "道德经", "有无相生", "对偶", "始对象", "终对象",
            "积", "余积", "category theory", "initial object", "terminal object",
            "Bartosz Milewski", "Dao of Functional Programming", "Manim", "进阶深讲"]
    md = f"""# YouTube 发布信息（草案）— 进阶深讲 08 有无相生

## 标题
{title}

（{len(title)} 字符，YouTube 上限 100）

## 说明
```
{desc}```

## 章节（与成片实际时间一致，成片总长 {ts(A['total'])}）
```
{chap}
```

## 标签
{", ".join(tags)}

## 其他
- 缩略图：`final/thumbnail.png`（1280×720）
- 字幕：画面已烧录中文；`final/tao-category-detail-08.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道进阶深讲；上一集《道可道》；下一集《道生一》。入门深讲见 01–06。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
