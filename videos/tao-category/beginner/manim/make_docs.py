# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S1Compose": ["s1"], "S2YouWu": ["s2wu", "s2you", "s2b"], "S3Maybe": ["s3maybe", "s3list"],
    "S4FoldUnfold": ["s4fold", "s4unfold", "s4hylo"], "S5Functor": ["s5fmap", "s5law", "s5app"],
    "S6Monad": ["s6bind", "s6do"],
}
SNIP_FILE = {
    "s1": "Seg1Compose.hs", "s2": "Seg2YouWu.hs", "s3": "Seg3Maybe.hs",
    "s4": "Seg4FoldUnfold.hs", "s5": "Seg5Functor.hs", "s6": "Seg6Monad.hs",
}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("对象 / 箭头（态射）", "object / arrow (morphism)"),
    ("复合 / 恒等", "composition / identity"),
    ("始对象 / 终对象", "initial / terminal object"),
    ("Void / 单元类型 ()", "Void / unit type ()"),
    ("Maybe / 列表", "Maybe / list"),
    ("折叠 fold / 展开 unfold", "fold / unfold"),
    ("合态射 hylo（轻提）", "hylomorphism (light mention)"),
    ("函子 / fmap / map", "functor / fmap / map"),
    ("Applicative / pure / (<*>)", "Applicative / pure / (<*>)"),
    ("单子 / bind / join / do 记法", "monad / bind / join / do-notation"),
]


def script_md():
    L = []
    L.append("# 道可道 · 范畴入门 —— 解说稿\n")
    L.append("*用六句《道德经》入门范畴论与 Haskell｜The Dao of Categories — Beginner*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：会一点编程；Haskell 零基础或略知即可。慢节奏、日常比喻、少公式、多直觉。\n"
             "- 结构：每段 = 《道德经》原文 → 日常比喻 → 几行 Haskell。哲学只是钩子，数学必须正确。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-beginner.srt`。\n"
             "- 屏幕上的全部代码都直接摘自 `haskell/src/*.hs`（以 `-- {{snip:…}}` 标记抽取），并经 GHC 9.14.1 `-Wall` 编译通过。\n"
             "- 与进阶篇同美学：宣纸留白、朱红印章「知白守黑」、同一套字体与组装管线。进阶篇见 `/workspace/tao-category-video/`。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("本片的叙述框架与 Haskell 写法以 Bartosz Milewski 的两本书为主要参照（释义、改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*（hmemcpy 编排版），<https://github.com/hmemcpy/milewski-ctfp-pdf>\n\n"
             "入门篇刻意避开 Yoneda、伴随深度、Lambek / Adámek 定理表述；对应主题改用对象/箭头/复合、Void/()、Maybe·列表与折叠、"
             "unfold/fold、Functor·Applicative、Monad·do。更深内容指向进阶篇。\n")
    L.append("\n| 段落 | DaoFP 章节 | CTFP 章节 |\n|---|---|---|\n"
             "| 一 道可道 | 1 Clean Slate（Types and Functions）；2 Composition（Identity） | 1.1, 1.2 |\n"
             "| 二 有无相生 | 1 Clean Slate（Yin and Yang, Elements） | 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types |\n"
             "| 三 道生一 | 7 Recursion；11 Algebras（Catamorphisms——直觉层） | 1.6；3.8 F-Algebras（fold 直觉） |\n"
             "| 四 反者道之动 | 12 Coalgebras（Anamorphisms, Hylomorphisms——直觉层） | 3.8（Coalgebras） |\n"
             "| 五 知其雄 | Functor / Applicative 铺垫（DaoFP 相关章；14 Applicatives） | 1.7 Functors；1.8 |\n"
             "| 六 无为 | 2 Composition（wu wei）；15 Monads（入门直觉） | 3.4 Kleisli；3.6 Monads（bind / join） |\n")
    L.append("\n## 术语表（全片统一）\n\n| 中文 | English |\n|---|---|\n" + "".join(f"| {a} | {b} |\n" for a, b in GLOSSARY))
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
            L.append(f"\n屏幕代码 `{nm}`（`haskell/src/{SNIP_FILE[nm[:2]]}`）：\n\n```haskell\n" + "\n".join(load_snip(nm)) + "\n```\n")
    L.append("\n---\n\n## 数学校对备注\n\n"
             "- 依 CTFP 惯例在 Hask 中忽略 ⊥（`Void` 作为始对象在此约定下成立）。\n"
             "- 第三段：`Maybeⁿ Void` 恰有 n 个值，故「无、一、二、三」是精确计数；不引入 Lambek / Adámek 命名。\n"
             "- 第四段：hylo 仅作「先生后归、中间不落地」的轻提，不展开阻抗失配。\n"
             "- 第五段：函子定律与 Applicative 直觉；不讲 State/Store 伴随。\n"
             "- 第六段：Monad = bind 串联效果 + do；明确不是 Yoneda；收束指向进阶篇。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community 0.21（Cairo），白底渲染后与程序生成的宣纸纹理做 multiply 合成；唯一红色为印章「知白守黑」。\n"
             "- 字体：原文书法 Ma Shan Zheng（OFL）；正文/字幕 霞鹜文楷 LXGW WenKai（OFL）；代码 IBM Plex Mono（OFL）；英文引文 EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：六句话，带你入门",
        "S1Compose": "一 道可道：对象、箭头与复合",
        "S2YouWu": "二 有无相生：Void 与单元类型",
        "S3Maybe": "三 道生一：Maybe、列表与折叠",
        "S4FoldUnfold": "四 反者道之动：展开与折叠",
        "S5Functor": "五 知其雄，守其雌：函子与 Applicative",
        "S6Monad": "六 无为而无不为：单子与 do 记法",
        "S7Ending": "结语：看箭头 · 进阶篇见",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "道可道：用《道德经》入门范畴论与 Haskell | The Dao of Categories — Beginner"
    desc = f"""用六句《道德经》，带你入门范畴论。不需要先读过范畴论，会一点编程就够。每一段：先读原文，再用日常比喻，最后落到几行 Haskell。

这是入门篇（慢节奏、多直觉）。进阶篇另讲 Fix、伴随、米田。
· 道可道：类型是对象，函数是箭头；复合与 id
· 有无相生：Void 与 ()，absurd 与 const ()
· 道生一：Maybe / 列表从无中生长；折叠求和
· 反者道之动：unfold 生成、fold 消费；轻提 hylo
· 知其雄，守其雌：Functor / map 保持形状；Applicative
· 无为而无不为：Monad · bind · do——在效果里编程

章节
{chap}

参考（本片框架主要参照 Bartosz Milewski 的两本书，叙述为释义改写）
· The Dao of Functional Programming（DaoFP）：第 1、2、7、12、14、15 章等 —— https://github.com/BartoszMilewski/DaoFP
· Category Theory for Programmers（CTFP）：1.1、1.2、1.5、1.6、1.7、1.8、3.4、3.6、3.8 —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第一、二、二十八、三十七、四十、四十二章

代码：片中全部 Haskell 代码均可用 GHC 编译运行。
制作：Manim Community · 旁白 Microsoft Edge 神经语音（zh-CN-YunxiNeural）· 字体 霞鹜文楷 / Ma Shan Zheng / IBM Plex Mono / EB Garamond（均为 SIL OFL）。无背景音乐。

#范畴论 #Haskell #道德经 #入门
"""
    tags = ["范畴论", "Haskell", "道德经", "老子", "函数式编程", "入门", "函子", "Functor",
            "单子", "Monad", "Maybe", "fold", "unfold", "Applicative", "do notation",
            "category theory", "Bartosz Milewski", "Dao of Functional Programming",
            "Category Theory for Programmers", "Manim", "面向对象", "函数复合"]
    md = f"""# YouTube 发布信息（草案）— 入门篇

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
- 字幕：画面已烧录中文字幕；`final/tao-category-beginner.srt` 可作为 YouTube 中文字幕轨上传（建议默认关闭以免与烧录字幕重叠），或改用 `final/tao-category-beginner-nosubs.mp4` + 上传 SRT。
- 分类建议：教育（Education）；语言：中文（简体）。
- 系列：进阶篇见同系列《道可道：范畴之道》（Fix / 伴随 / 米田）。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


# Only run when assembly exists
if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
