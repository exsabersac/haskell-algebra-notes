# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Identity": ["s_id"],
    "S6Haskell": ["s_id", "s_compose", "s_shout"],
    "S3Types": ["s_sig", "s_bool"],
}
SNIP_FILE = {k: "TypesArrows.hs" for k in ["s_id", "s_compose", "s_sig", "s_shout", "s_bool"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("对象 / 箭头（态射）", "object / arrow (morphism)"),
    ("类型 / 函数", "type / function"),
    ("复合 / 恒等", "composition / identity"),
    ("类型签名", "type signature"),
    ("结合律", "associativity"),
]


def script_md():
    L = []
    L.append("# 道可道 · 深讲 01 —— 类型与箭头\n")
    L.append("*对象、态射、复合与恒等｜Types and Arrows — Deep Dive 01*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。\n"
             "- 结构：道德经钩子 → 对象不可道、箭头可道 → 类型=对象、函数=态射 → 恒等与复合 → 代码 → 预告 Void/()。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-01.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/TypesArrows.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 对象与箭头 | 1 Clean Slate（Types and Functions） | 1.1, 1.2 |\n"
             "| 复合 | 2 Composition | 1.1 |\n"
             "| 恒等 | 2 Identity（wu wei） | 1.2 |\n"
             "| 下一集预告 | 1 Yin and Yang | — |\n")
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
             "- 本集不引入始/终对象、Yoneda、伴随；仅对象/箭头/复合/恒等。\n"
             "- `identity` 与 Prelude `id` 同义；`compose` 与 `(.)` 同义，片中并陈以利对照。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：深讲第一集",
        "S1Hook": "一 道可道：对象不可道，箭头可道",
        "S2Map": "二 地图：点与路",
        "S3Types": "三 类型是对象，函数是箭头",
        "S4Compose": "四 复合与结合律",
        "S5Identity": "五 恒等：无为的环路",
        "S6Haskell": "六 落到 Haskell：id 与 (.)",
        "S7Next": "结语：看箭头 · 下集 Void/()",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "类型与箭头：对象、态射、复合与恒等 | 道可道深讲 01"
    desc = f"""入门篇用六句话扫过范畴论。深讲系列把每一块单独拉开——本集只谈「类型与箭头」。

· 对象不可道，箭头可道（道德经钩子）
· 类型是对象，函数是态射；类型签名就是箭头声明
· 复合 g∘f 与结合律；Haskell 的 (.)
· 恒等 id：复合的单位，无为
· 小例子：id、compose、shout 42 = 2
· 下集预告：Void 与 ()

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.1 Clean Slate；ch.2 Composition / Identity —— https://github.com/BartoszMilewski/DaoFP
· CTFP 1.1 Category: The Essence of Composition；1.2 Types and Functions —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第一章

系列：道可道 · 深讲（入门点逐集展开）。上一集总览见入门篇。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #类型 #函数复合
"""
    tags = ["范畴论", "Haskell", "道德经", "类型", "函数", "复合", "恒等", "id",
            "category theory", "composition", "identity", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "深讲"]
    md = f"""# YouTube 发布信息（草案）— 深讲 01 类型与箭头

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
- 字幕：画面已烧录中文；`final/tao-category-detail-01.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道深讲；下集《有无相生：Void 与 ()》。入门总览见同系列入门篇。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
