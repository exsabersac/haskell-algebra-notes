# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Haskell": ["s_maybe", "s_count", "s_list"],
}
SNIP_FILE = {k: "MaybeList.hs" for k in ["s_maybe", "s_count", "s_list"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("Maybe / 列表", "Maybe / list"),
    ("代数数据类型", "algebraic data type (ADT)"),
    ("构造子 / 引入规则", "constructor / introduction rule"),
    ("余积 / 求和", "coproduct / sum type"),
    ("递归类型", "recursive type"),
    ("折叠 / 展开", "fold / unfold"),
]


def script_md():
    L = []
    L.append("# 道可道 · 深讲 03 —— Maybe 与 List\n")
    L.append("*从无生长的代数数据类型｜Maybe and List — Deep Dive 03*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。\n"
             "- 结构：道生一钩子 → Maybe = 1+A → List 递归 → 从无生长 → 代码 → 预告构造与折叠。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-03.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/MaybeList.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 道生一 | 7 Recursion（开篇） | 1.6 |\n"
             "| Maybe = 1+A | 7；4 Sum Types | 1.6 Maybe ≅ Either () a |\n"
             "| List 递归 | 7 Lists | 1.6 recursive ADT |\n"
             "| 从无生长 | 7；入门篇计数 | 1.6 |\n"
             "| 下一集预告 | 11 Algebras / 12 Coalgebras | 3.8 F-Algebras |\n")
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
             "- Maybe a ≅ Either () a ≅ 1 + A（类型代数直觉）；不引入 Yoneda、伴随、Lambek。\n"
             "- `Maybeⁿ Void` 恰有 n 个值（n=0 时 Void 有 0 个）；列表为 Nil | Cons 递归 ADT。\n"
             "- 本集只点到折叠预告；fold / unfold / catamorphism 留给深讲 04。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：深讲第三集",
        "S1Hook": "一 道生一：构造子",
        "S2Maybe": "二 Maybe = 1 + A",
        "S3List": "三 List：递归",
        "S4Grow": "四 从无生长",
        "S5Haskell": "五 落到 Haskell",
        "S6Next": "结语：下集构造与折叠",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "Maybe 与 List：从无生长 | 道可道深讲 03"
    desc = f"""入门篇扫过「道生一」。深讲第三集把 Maybe 与列表单独拉开。

· 道生一钩子：构造子即引入规则
· Maybe = 1 + A：Either () a；Nothing / Just
· List：Nil | Cons 递归；有限求和对上无限递归
· 从无生长：Maybeⁿ Void 恰有 n 个值
· Haskell：互转、计数、sumList 预告
· 下集预告：构造与折叠 · fold / unfold

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.7 Recursion —— https://github.com/BartoszMilewski/DaoFP
· CTFP 1.6 Simple Algebraic Data Types —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第四十二章

系列：道可道 · 深讲。上一集《Void 与 ()》；入门总览见入门篇。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #Maybe #List #代数数据类型
"""
    tags = ["范畴论", "Haskell", "道德经", "Maybe", "List", "代数数据类型", "递归",
            "category theory", "algebraic data type", "coproduct", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "深讲"]
    md = f"""# YouTube 发布信息（草案）— 深讲 03 Maybe 与 List

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
- 字幕：画面已烧录中文；`final/tao-category-detail-03.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道深讲；下集《构造与折叠》。上一集《Void 与 ()》；入门总览见同系列入门篇。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
