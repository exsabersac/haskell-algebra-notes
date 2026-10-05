# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Haskell": ["s_cata", "s_foldr", "s_ana"],
}
SNIP_FILE = {k: "FoldUnfold.hs" for k in ["s_cata", "s_foldr", "s_ana"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("构造 / 代数", "constructor / algebra"),
    ("折叠 / catamorphism", "fold / catamorphism (cata)"),
    ("展开 / anamorphism", "unfold / anamorphism (ana)"),
    ("合态射 / hylo", "hylomorphism (hylo)"),
    ("引入 / 消解", "introduction / elimination"),
    ("F-代数（直觉）", "F-algebra (intuition)"),
]


def script_md():
    L = []
    L.append("# 道可道 · 深讲 04 —— 构造与折叠\n")
    L.append("*从代数到 cata / foldr，浅提 ana｜Fold and Unfold — Deep Dive 04*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。\n"
             "- 结构：钩子 → 构造代数 → 折叠 cata/foldr → 展开 ana（浅提）→ 代码 → 预告 Functor。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-04.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/FoldUnfold.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 各复归其根 | 11 Algebras（cata 直觉） | 3.8 F-Algebras |\n"
             "| 构造代数 | 11 Algebras | 3.8 |\n"
             "| 折叠 cata / foldr | 11 Catamorphisms | 3.8 |\n"
             "| 展开 ana（浅提） | 12 Coalgebras | 3.8 Coalgebras |\n"
             "| 下一集预告 | Functor 相关 | 1.7–1.8 Functors |\n")
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
             "- 本集讲 F-代数 / cata / ana 的**直觉层**；不引入 Fix、Lambek 引理、Adámek 定理。\n"
             "- foldr 与手写递归同为列表上的 catamorphism 写法；unfoldr 为 anamorphism 浅提。\n"
             "- hylo = ana 后接 cata，仅点到；不展开融合证明。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：深讲第四集",
        "S1Hook": "一 各复归其根",
        "S2Algebra": "二 构造代数",
        "S3Cata": "三 折叠 cata / foldr",
        "S4Ana": "四 展开 ana（浅提）",
        "S5Haskell": "五 落到 Haskell",
        "S6Next": "结语：下集 Functor",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "构造与折叠：cata / fold 直觉 | 道可道深讲 04"
    desc = f"""入门篇扫过折叠与展开。深讲第四集把「收回去」单独拉开。

· 钩子：夫物芸芸，各复归其根
· 构造代数：构造子合起来是代数
· 折叠 cata ≈ foldr：同一形状，不同操作
· 展开 ana 浅提：种子长出列表；hylo 点到
· Haskell：sumList / foldr / unfoldr
· 下集预告：Functor · fmap

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.11 Algebras / ch.12 Coalgebras —— https://github.com/BartoszMilewski/DaoFP
· CTFP 3.8 F-Algebras —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第十六章

系列：道可道 · 深讲。上一集《Maybe 与 List》；入门总览见入门篇。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #fold #cata #代数
"""
    tags = ["范畴论", "Haskell", "道德经", "fold", "unfold", "catamorphism", "代数",
            "category theory", "F-algebra", "foldr", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "深讲"]
    md = f"""# YouTube 发布信息（草案）— 深讲 04 构造与折叠

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
- 字幕：画面已烧录中文；`final/tao-category-detail-04.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道深讲；下集《函子 Functor》。上一集《Maybe 与 List》；入门总览见同系列入门篇。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
