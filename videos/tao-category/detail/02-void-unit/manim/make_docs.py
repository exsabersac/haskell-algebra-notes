# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Haskell": ["s_wu", "s_you", "s_sum", "s_prod"],
}
SNIP_FILE = {k: "VoidUnit.hs" for k in ["s_wu", "s_you", "s_sum", "s_prod"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("始对象 / 终对象", "initial / terminal object"),
    ("Void / 单元类型 ()", "Void / unit type ()"),
    ("出射 / 入射", "outgoing / incoming morphism"),
    ("对偶", "duality"),
    ("absurd / const", "absurd / const"),
]


def script_md():
    L = []
    L.append("# 道可道 · 深讲 02 —— Void 与 ()\n")
    L.append("*始对象、终对象与对偶直觉｜Void and Unit — Deep Dive 02*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。\n"
             "- 结构：有无相生钩子 → Void 无出射 → () 唯一入 → 对偶 → 代码 → 预告 Maybe/List。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-02.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/VoidUnit.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 阴阳 | 1 Clean Slate（Yin and Yang） | 1.5 |\n"
             "| Void / 始对象 | 1 Elements（Void） | 1.5 Initial；1.6 |\n"
             "| () / 终对象 | 1 Elements（Unit） | 1.5 Terminal |\n"
             "| 对偶 / 单位律 | 1 Yin and Yang | 1.5 dual；1.6 |\n"
             "| 下一集预告 | 7 Recursion | 1.6 Maybe / List |\n")
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
             "- 始/终对象按 Hom-集唯一性定义；不引入 Yoneda、伴随。\n"
             "- `wu` 即 `absurd`；`you` 即 `const ()`；单位律对应 Either/× 的单位同构（直觉层）。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：深讲第二集",
        "S1Hook": "一 有无相生：始与终",
        "S2Void": "二 Void：无出射 · 始对象",
        "S3Unit": "三 ()：唯一入 · 终对象",
        "S4Dual": "四 对偶：有无相生",
        "S5Haskell": "五 落到 Haskell：absurd 与 const",
        "S6Next": "结语：下集 Maybe / List",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "Void 与 ()：始对象、终对象与对偶 | 道可道深讲 02"
    desc = f"""入门篇扫过「有无相生」。深讲第二集把 Void 与单元类型 () 单独拉开。

· 有无相生钩子：始对象与终对象的箭头计数定义
· Void：零个值；absurd 出射唯一 —— 始对象
· ()：一个值；const () 入射唯一 —— 终对象
· 对偶：箭头掉头，无变有；Either / 配对上的单位律
· Haskell：wu、you、sumUnit、prodUnit
· 下集预告：Maybe 与列表

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.1 Yin and Yang / Elements —— https://github.com/BartoszMilewski/DaoFP
· CTFP 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第二章

系列：道可道 · 深讲。上一集《类型与箭头》；入门总览见入门篇。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #Void #始对象 #终对象
"""
    tags = ["范畴论", "Haskell", "道德经", "Void", "单元类型", "始对象", "终对象", "对偶",
            "category theory", "initial object", "terminal object", "absurd", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "深讲"]
    md = f"""# YouTube 发布信息（草案）— 深讲 02 Void 与 ()

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
- 字幕：画面已烧录中文；`final/tao-category-detail-02.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道深讲；下集《道生一：Maybe 与列表》。上一集《类型与箭头》；入门总览见同系列入门篇。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
