# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S4Haskell": ["s_yoneda", "s_redeem", "s_ran"],
}
SNIP_FILE = {k: "WuWei.hs" for ks in SNIPS.values() for k in ks}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("可表函子 / 表示元", "representable functor / representing object"),
    ("米田引理", "Yoneda lemma"),
    ("米田嵌入（满忠实）", "Yoneda embedding (fully faithful)"),
    ("自然变换族 Nat", "natural transformations Nat"),
    ("续体传递 / Speak", "continuation-passing / Speak a"),
    ("右/左 Kan 扩张 Ran / Lan", "right/left Kan extension"),
    ("沿恒等的右 Kan 扩张", "Ran along Identity ≅ Yoneda"),
]


def script_md():
    L = []
    L.append("# 道可道 · 进阶深讲 12 —— 无为而无不为（系列终章）\n")
    L.append("*米田引理、可表函子、Kan 扩张｜Yoneda lemma, representable functors, Kan extensions — Advanced Deep Dive 12 (FINAL)*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已完成入门深讲 01–06 与进阶 07–11；先范畴论陈述，再短 Haskell。\n"
             "- 结构：钩子 → 可表函子 → 米田引理（对象由箭头决定）→ Haskell Yoneda/forall → Kan 扩张（Ran/Lan）→ 系列收束回到道可道。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-12.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/WuWei.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。本集赎回进阶 07 的米田预告。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 无为 | 2 Composition（Identity = wu wei） | — |\n"
             "| 可表函子 | 9 Representable Functors | 2.5（前置） |\n"
             "| 米田引理 | 9 The Yoneda Lemma | 2.5 / 2.6 |\n"
             "| Haskell Yoneda / Speak | 9 Yoneda lemma in programming | 2.5 |\n"
             "| Kan 扩张 Ran/Lan | 20 Kan Extensions | 3.11 |\n"
             "| 系列收束 | Master Yoneda: At the arrows look! | — |\n")
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
             "- 米田引理：Nat(C(a,−), F) ≅ F(a)；α ↦ α_a(id_a)；ξ ↦ (h ↦ F(h)(ξ))。\n"
             "- Hask 中 `forall x. (a -> x) -> f x ≅ f a` 依赖参数性；按 CTFP 惯例忽略 ⊥。\n"
             "- f = Identity ⇒ `forall x. (a -> x) -> x ≅ a`（CPS / Speak）；redeem = ($ id)。\n"
             "- 米田嵌入满忠实 ⇒ a ≅ b ⟺ C(a,−) ≅ C(b,−)。\n"
             "- Ran_p f a ≅ ∫_b [B(a, p b), f b]；Haskell：`Ran g h a = forall b. (a -> g b) -> h b`。\n"
             "- Yoneda f ≅ Ran Identity f；Mac Lane: “All concepts are Kan extensions.”\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：无为而无不为",
        "S1Hook": "一 道德经钩子",
        "S2Representable": "二 可表函子",
        "S3Yoneda": "三 米田引理",
        "S4Haskell": "四 Haskell：Yoneda 与 forall",
        "S5Kan": "五 Kan 扩张：Ran 与 Lan",
        "S6Close": "结语：回到道可道（系列完结）",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "无为而无不为：米田引理与 Kan 扩张 | 进阶深讲 12（终章）"
    desc = f"""进阶深讲第十二集（系列终章）。赎回第七集的米田预告：可表函子、米田引理、Haskell Yoneda/forall、Kan 扩张 Ran/Lan，回到道可道。

· 钩子：道常无为而无不为（id = wu wei）
· 可表函子 Hom(a,−)；表示元
· 米田引理：Nat(Hom(a,−), F) ≅ F a；嵌入满忠实
· Haskell：Yoneda / fromYoneda = g id；Speak ≅ a；fmap 熔合
· Kan：Ran / Lan；Yoneda ≅ Ran Identity；Mac Lane
· 系列收束：看箭头 · 道可道，非常道

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.2 / 9 / 20 —— https://github.com/BartoszMilewski/DaoFP
· CTFP 2.5 / 2.6 / 3.11 —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第三十七章

系列：道可道 · 进阶深讲终章。上一集《知其雄，守其雌》。入门深讲见 01–06。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #无为而无不为 #米田引理 #Yoneda #Kan扩张 #道可道
"""
    tags = ["范畴论", "Haskell", "道德经", "无为而无不为", "米田引理", "Yoneda", "Kan扩张",
            "Kan extension", "representable", "category theory", "Bartosz Milewski",
            "Dao of Functional Programming", "Manim", "进阶深讲", "系列终章"]
    md = f"""# YouTube 发布信息（草案）— 进阶深讲 12 无为而无不为（系列终章）

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
- 字幕：画面已烧录中文；`final/tao-category-detail-12.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道进阶深讲终章；上一集《知其雄，守其雌》。入门深讲见 01–06。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
