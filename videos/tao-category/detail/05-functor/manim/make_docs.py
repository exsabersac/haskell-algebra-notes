# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Haskell": ["s_class", "s_maybe", "s_list", "s_demo"],
}
SNIP_FILE = {k: "FunctorIntuition.hs" for k in ["s_class", "s_maybe", "s_list", "s_demo"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("函子 / Functor", "functor"),
    ("保形 / 不撕裂", "shape-preserving / no-tearing"),
    ("fmap / 抬升", "fmap / lifting"),
    ("类型构造子", "type constructor"),
    ("单位定律", "identity law"),
    ("复合定律", "composition law"),
    ("自函子（浅提）", "endofunctor (mention)"),
]


def script_md():
    L = []
    L.append("# 道可道 · 深讲 05 —— Functor 直觉\n")
    L.append("*保形、fmap、定律；Maybe / List｜Functor Intuition — Deep Dive 05*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。\n"
             "- 结构：钩子 → 函子保形 → fmap / 交换图 → 定律 → Maybe/List 代码 → 预告 Monad。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-05.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/FunctorIntuition.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 大制不割 | 8 Functors（保形） | 1.7 Functors（no-tearing） |\n"
             "| 函子保形 | 8 Functors between categories | 1.7 |\n"
             "| fmap / 交换图 | 8 fmap | 1.7 lifting |\n"
             "| 定律 | 8 preserve id & ∘ | 1.7 laws |\n"
             "| Maybe / List | 8 instances | 1.7 Maybe Functor |\n"
             "| 下一集预告 | 15 Monads | 3.4–3.6 Monads |\n")
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
             "- 本集讲函子的**直觉层**（保形 / fmap / 定律）；不引入 Bifunctor、Contravariant、Profunctor、Yoneda。\n"
             "- 用手写 `class Functor` 避免与 Prelude 混谈；实例覆盖 Maybe 与 []。\n"
             "- 「自函子」仅在叙述中作为 Hask→Hask 的背景，不单独展开。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：深讲第五集",
        "S1Hook": "一 大制不割",
        "S2Shape": "二 函子保形",
        "S3Fmap": "三 fmap / 交换图",
        "S4Laws": "四 函子定律",
        "S5Haskell": "五 Maybe 与 List",
        "S6Next": "结语：下集 Monad",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "Functor 直觉：保形与 fmap | 道可道深讲 05"
    desc = f"""入门篇扫过 Functor。深讲第五集把「映射而不撕裂」单独拉开。

· 钩子：大制不割
· 函子保形：对象与箭头一起映；不撕破结构
· fmap / 交换图：把箭头抬到外壳上
· 定律：单位与复合，写成契约
· Haskell：Maybe / List 的 fmap
· 下集预告：Monad · do

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.8 Functors —— https://github.com/BartoszMilewski/DaoFP
· CTFP 1.7–1.8 Functors —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第二十八章

系列：道可道 · 深讲。上一集《构造与折叠》；入门总览见入门篇。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #Functor #fmap #函子
"""
    tags = ["范畴论", "Haskell", "道德经", "Functor", "fmap", "函子",
            "category theory", "Maybe", "List", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "深讲"]
    md = f"""# YouTube 发布信息（草案）— 深讲 05 Functor 直觉

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
- 字幕：画面已烧录中文；`final/tao-category-detail-05.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道深讲；下集《Monad / do》。上一集《构造与折叠》；入门总览见同系列入门篇。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
