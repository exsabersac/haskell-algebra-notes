# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S7Haskell": ["s_fix", "s_hylo", "s_list", "s_stream", "s_range"],
}
SNIP_FILE = {k: "FanZhe.hs" for k in SNIPS["S7Haskell"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("自函子 F", "endofunctor F"),
    ("F-余代数 / 载体 / 结构映射", "F-coalgebra / carrier / structure map"),
    ("余代数同态 · 余代数范畴 CoAlg(F)", "coalgebra morphism · category of coalgebras"),
    ("终余代数 (ν, out)", "terminal coalgebra"),
    ("展开 ana", "anamorphism (ana)"),
    ("合态射 hylo", "hylomorphism (hylo)"),
    ("最小不动点 μF / 最大不动点 νF", "least / greatest fixed point"),
    ("阻抗失配", "impedance mismatch"),
    ("共归纳", "coinduction"),
    ("融合律", "fusion law"),
]


def script_md():
    L = []
    L.append("# 道可道 · 进阶深讲 10 —— 反者道之动\n")
    L.append("*余代数、ana、hylo、μF/νF｜Coalgebras, ana, hylo — Advanced Deep Dive 10*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已完成入门深讲 01–06 与进阶 07–09；先范畴论陈述，再短 Haskell。\n"
             "- 结构：道德经钩子 → 余代数与同态 → 终余代数与 ana → 翻转：图与代码 → μF 与 νF → hylo → 短 Haskell → 下集知其雄守其雌。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-10.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/FanZhe.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。比入门 04（fold 直觉、浅提 ana）更深：余代数范畴、终余代数、对偶兰贝克、μF/νF 与阻抗失配、hylo 融合。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 反者道之动 | 12 Coalgebras | 3.8 Coalgebras |\n"
             "| 余代数与同态 | 12 Coalgebras | 3.8 |\n"
             "| 终余代数与 ana | 12 Anamorphisms；Infinite data structures | 3.8 |\n"
             "| 翻转：图与代码 | 12 Anamorphisms | 3.8 |\n"
             "| μF 与 νF | 12 Infinite data structures；The impedance mismatch | 3.8 |\n"
             "| hylo | 12 Hylomorphisms | 3.8 |\n"
             "| 短 Haskell | 12 / 本集 FanZhe.hs | 3.8 |\n"
             "| 下集预告 | 10 Adjunctions | 3.2 Adjunctions |\n")
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
             "- F-余代数 (a, γ : a → F a)；同态 f 满足 F f ∘ γ = δ ∘ f；CoAlg(F) ≅ Alg(F)^op。\n"
             "- 终余代数 (ν, out) 是 CoAlg(F) 的终对象；从 (a, γ) 出发的唯一同态即 ana γ。存在＝算法，唯一＝共归纳证明原则。\n"
             "- 兰贝克对偶：终余代数的 out 是同构，ν ≅ F ν，且为最大不动点 νF（任何不动点都是余代数，故有 x → ν）。\n"
             "- ana 由交换方块读出：ana γ = Fix ∘ fmap (ana γ) ∘ γ；与 cata 复合顺序对偶。\n"
             "- Set 中一般 μF ⊂ νF（例：Id 的 ∅ ⊂ 1；列表的有限列表 ⊂ 含极限点）。Hask 因惰性，`Fix f` 兼任二者（DaoFP ch.12 “impedance mismatch”）。\n"
             "- hylo alg coa = alg ∘ fmap (hylo alg coa) ∘ coa；语义等于 cata alg ∘ ana coa，但定义中无 Fix，中间结构边生边消（融合）。\n"
             "- 若 coa 不终止，hylo 发散。依 CTFP 惯例忽略 ⊥。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：反者道之动",
        "S1Hook": "一 道德经钩子",
        "S2Coalgebras": "二 余代数与同态",
        "S3Terminal": "三 终余代数与 ana",
        "S4Flip": "四 翻转：图与代码",
        "S5MuNu": "五 μF 与 νF",
        "S6Hylo": "六 hylo：先生而后归",
        "S7Haskell": "七 短 Haskell",
        "S8Next": "结语：下集知其雄守其雌",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "反者道之动：余代数、ana 与 hylo | 进阶深讲 10"
    desc = f"""进阶深讲第十集。比入门 04 更深：余代数范畴、终余代数与 ana、对偶兰贝克、μF/νF 与阻抗失配、hylo 融合。

· 钩子：反者道之动（箭头掉头 = 对偶）
· 余代数 (a, γ : a → F a) 与余代数同态；范畴 CoAlg(F)
· 终余代数：唯一入射 = ana；存在即算法，唯一即共归纳
· 翻转：cata 方块 ↔ ana 方块；复合倒序
· Set：μF ⊂ νF；Hask：Fix 兼任二者（阻抗失配）
· hylo：先生后归，中间不落地（生而不有）
· 短 Haskell：ana / hylo / fact / nats / range
· 下集：知其雄，守其雌 · 伴随

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.12 Coalgebras —— https://github.com/BartoszMilewski/DaoFP
· CTFP 3.8 F-Algebras（Coalgebras） —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第四十章；第十章（生而不有）

系列：道可道 · 进阶深讲。上一集《道生一》；下一集《知其雄，守其雌》。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #反者道之动 #余代数 #anamorphism #hylomorphism #道可道
"""
    tags = ["范畴论", "Haskell", "道德经", "反者道之动", "余代数", "coalgebra", "ana", "hylo",
            "anamorphism", "hylomorphism", "不动点", "category theory", "terminal coalgebra",
            "Bartosz Milewski", "Dao of Functional Programming", "Manim", "进阶深讲"]
    md = f"""# YouTube 发布信息（草案）— 进阶深讲 10 反者道之动

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
- 字幕：画面已烧录中文；`final/tao-category-detail-10.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道进阶深讲；上一集《道生一》；下一集《知其雄，守其雌》。入门深讲见 01–06。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
