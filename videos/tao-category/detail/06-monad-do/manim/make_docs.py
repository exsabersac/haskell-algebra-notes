# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S5Haskell": ["s_class", "s_fish", "s_maybe", "s_list", "s_demo", "s_do"],
}
SNIP_FILE = {k: "MonadDo.hs" for k in ["s_class", "s_fish", "s_maybe", "s_list", "s_demo", "s_do"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("单子 / Monad", "monad"),
    ("绑定 / bind", "bind / (>>=)"),
    ("注入 / return", "return / pure / unit"),
    ("鱼子 / Kleisli 复合", "fish / (>=>) / Kleisli composition"),
    ("do 记法", "do-notation"),
    ("左 / 右单位定律", "left / right unit law"),
    ("结合律", "associativity"),
]


def script_md():
    L = []
    L.append("# 道可道 · 深讲 06 —— Monad 与 do 记法\n")
    L.append("*bind、鱼子、定律；do；Maybe / List｜Monad & do-notation — Deep Dive 06*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。\n"
             "- 结构：钩子 → bind / 鱼子 → 定律浅讲 → do 记法 → Maybe/List 代码 → 进阶篇预告。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-06.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/MonadDo.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。本集为入门深讲最后一集。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 道生一 | 15 Monads（效应链） | 3.4–3.5 Monads |\n"
             "| bind / 鱼子 | 15 bind / Kleisli | 3.4 fish |\n"
             "| 定律浅讲 | 15 monad laws | 3.5–3.6 |\n"
             "| do 记法 | 15 do-notation | 3.4 |\n"
             "| Maybe / List | 15 instances | 3.4–3.5 |\n"
             "| 进阶预告 | — | 不动点 / 伴随 / 米田 |\n")
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
             "- 本集讲 Monad 的**直觉层**（bind / 鱼子 / 定律 / do）；不引入 transformer、IO、Free、Codensity。\n"
             "- 用手写 `class Monad` 避免与 Prelude 混谈；实例覆盖 Maybe 与 []。\n"
             "- join / μ 仅在叙述中作为「解开外套」隐喻，不单独展开定义。\n"
             "- 进阶篇预告：不动点、伴随、米田——不在本集展开。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：深讲第六集",
        "S1Hook": "一 道生一",
        "S2Bind": "二 bind / 鱼子",
        "S3Laws": "三 定律浅讲",
        "S4Do": "四 do 记法",
        "S5Haskell": "五 Maybe 与 List",
        "S6Next": "结语：进阶篇",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "Monad 与 do 记法：bind 与效应链 | 道可道深讲 06"
    desc = f"""入门篇扫过 Monad。深讲第六集（入门深讲收束）把「效应如何串联」单独拉开。

· 钩子：道生一
· bind / 鱼子：效应链与克莱斯利复合
· 定律浅讲：左单位、右单位、结合
· do 记法：语法糖，语义仍是 bind
· Haskell：Maybe / List 小例子
· 进阶预告：不动点 · 伴随 · 米田

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.15 Monads —— https://github.com/BartoszMilewski/DaoFP
· CTFP 3.4–3.6 Monads —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第四十二章

系列：道可道 · 深讲。上一集《Functor 直觉》；入门总览见入门篇。下一阶段进阶篇。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #Monad #do记法 #单子
"""
    tags = ["范畴论", "Haskell", "道德经", "Monad", "do记法", "单子",
            "category theory", "Maybe", "List", "bind", "Bartosz Milewski",
            "Dao of Functional Programming", "Category Theory for Programmers", "Manim", "深讲"]
    md = f"""# YouTube 发布信息（草案）— 深讲 06 Monad 与 do 记法

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
- 字幕：画面已烧录中文；`final/tao-category-detail-06.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道深讲（入门深讲收束）；进阶篇：不动点 / 伴随 / 米田。上一集《Functor 直觉》；入门总览见同系列入门篇。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
