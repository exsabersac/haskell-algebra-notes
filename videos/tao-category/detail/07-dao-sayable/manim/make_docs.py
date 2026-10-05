# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Haskell": ["s_dao", "s_speak", "s_hear", "s_demo"],
}
SNIP_FILE = {k: "DaoSayable.hs" for k in ["s_dao", "s_speak", "s_hear", "s_demo"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("对象 / 箭头（态射）", "object / arrow (morphism)"),
    ("可道 / 不可道", "sayable / ineffable"),
    ("全局元素（本集仅对照）", "global element"),
    ("续体传递 / Speak", "continuation-passing / Speak a"),
    ("自然性", "naturality"),
    ("米田引理（一句预告）", "Yoneda lemma (tease)"),
    ("米田嵌入（后集）", "Yoneda embedding"),
]


def script_md():
    L = []
    L.append("# 道可道 · 进阶深讲 07 —— 道可道\n")
    L.append("*对象不可道，箭头可道；Yoneda 一句｜Objects ineffable, arrows speakable — Advanced Deep Dive 07*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已完成入门深讲 01–06；先范畴论陈述，再短 Haskell。\n"
             "- 结构：道德经钩子 → 对象不可道 → 箭头可道 → 自然性铺垫 / Yoneda 一句 → 短 Haskell → 下集有无相生。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-07.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/DaoSayable.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。本集为进阶深讲开篇。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 道可道 | 1 Clean Slate（Types） | 1.1, 1.2 |\n"
             "| 对象不可道 | 1 Types and Functions | 1.1 |\n"
             "| 箭头可道 | 3 Isomorphism（At the arrows look!） | 1.2 |\n"
             "| 自然性 / 米田一句 | 3 / 9 Yoneda tease | 2.5–2.6（仅预告） |\n"
             "| 短 Haskell | 1 Speak / abstract type | — |\n"
             "| 下集预告 | 1 Yin and Yang | 1.5 |\n")
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
             "- 依 CTFP 惯例在 Hask 中忽略 ⊥。\n"
             "- 本集讲认识论层：对象不可道 / 箭头可道；Speak 作续体风格收集器。\n"
             "- 米田引理仅一句预告，不写证明、不展开嵌入；自然性作「说法对齐」直觉。\n"
             "- `newtype Dao` 不导出构造子；`hear` 为 Yoneda 侧最小种子。\n"
             "- 下集预告：有无相生（始/终对象）——不在本集展开。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：进阶深讲开篇",
        "S1Hook": "一 道德经钩子",
        "S2Object": "二 对象不可道",
        "S3Arrow": "三 箭头可道",
        "S4Yoneda": "四 自然性 / 米田一句",
        "S5Haskell": "五 短 Haskell",
        "S6Next": "结语：下集有无相生",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "道可道：对象不可道，箭头可道 | 进阶深讲 07"
    desc = f"""入门深讲收束后，进阶篇开篇。第七集钉牢认识论：对象不可道，箭头可道；米田一句先挂上。

· 钩子：道可道，非常道
· 对象不可道：公理里没有「打开内部」
· 箭头可道：At the arrows look!
· 自然性铺垫 / 米田一句：对象被 Hom(a,−) 刻画（不写证明）
· 短 Haskell：Dao / Speak / hear
· 下集：有无相生 · 始对象与终对象

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.1 Clean Slate；ch.3 Isomorphism —— https://github.com/BartoszMilewski/DaoFP
· CTFP 1.1–1.2 —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第一章

系列：道可道 · 进阶深讲。上一阶段入门深讲 01–06；下一集《有无相生》。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #米田引理 #Yoneda #道可道
"""
    tags = ["范畴论", "Haskell", "道德经", "道可道", "米田引理", "Yoneda",
            "category theory", "对象", "箭头", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "进阶深讲"]
    md = f"""# YouTube 发布信息（草案）— 进阶深讲 07 道可道

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
- 字幕：画面已烧录中文；`final/tao-category-detail-07.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道进阶深讲开篇；下一集《有无相生》。入门深讲见 01–06。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
