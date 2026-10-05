# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S7Haskell": ["s_fix", "s_expr", "s_algs", "s_lambek", "s_nat", "s_mu", "s_list"],
}
SNIP_FILE = {k: "DaoShengYi.hs" for k in SNIPS["S7Haskell"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("自函子 F", "endofunctor F"),
    ("F-代数 / 载体 / 结构映射", "F-algebra / carrier / structure map"),
    ("代数同态 · 代数范畴 Alg(F)", "algebra morphism · category of algebras"),
    ("初始代数 (i, ι)", "initial algebra"),
    ("折叠 cata ⦇α⦈", "catamorphism (banana brackets)"),
    ("兰贝克引理", "Lambek's lemma"),
    ("最小不动点 μF / 最大不动点 νF", "least / greatest fixed point"),
    ("余极限 / ω-链", "colimit / ω-chain"),
    ("Adámek 定理", "Adámek's theorem"),
    ("Church 编码 Mu", "Church encoding"),
]


def script_md():
    L = []
    L.append("# 道可道 · 进阶深讲 09 —— 道生一\n")
    L.append("*初始代数、兰贝克引理、Fix 与 cata｜Initial algebras, Lambek, Fix — Advanced Deep Dive 09*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已完成入门深讲 01–06 与进阶 07–08；先范畴论陈述，再短 Haskell。\n"
             "- 结构：道德经钩子 → 代数与同态 → 初始代数与 cata → 兰贝克引理 → Fix 与 cata 的来历 → 从无出发：余极限 → 短 Haskell → 下集反者道之动。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-09.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/DaoShengYi.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。比入门 03（Maybe/List 计数）与 04（fold 直觉、「今天不写 Lambek」）更深：代数范畴、初始性、兰贝克证明、Fix 的来历、Adámek 余极限、Church 编码。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 道生一 | 7 Recursion（以此句开篇）；11 导言（递归机关 vs 可插拔零件） | 3.8 |\n"
             "| 代数与同态 | 11 Algebras from Endofunctors；Category of Algebras | 3.8 F-Algebras |\n"
             "| 初始代数与 cata | 11 Initial algebra；Catamorphisms（Examples, Lists as initial algebras） | 3.8 |\n"
             "| 兰贝克引理 | 11 Lambek's Lemma and Fixed Points | 3.8 |\n"
             "| Fix 与 cata 的来历 | 11 Fixed point in Haskell；Catamorphisms | 3.8 |\n"
             "| 从无出发：余极限 | 11 Initial Algebra as a Colimit；Initial Algebra from Universality | 3.8 |\n"
             "| 短 Haskell | 11 / 本集 DaoShengYi.hs | 3.8 |\n"
             "| 下集预告 | 12 Coalgebras | 3.8 Coalgebras |\n")
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
             "- F-代数 (a, α : F a → a)；同态 f 满足 f ∘ α = β ∘ F f；恒等与复合由函子律保证，Alg(F) 成范畴。\n"
             "- 初始代数 (i, ι) 是 Alg(F) 的始对象；到 (a, α) 的唯一同态即 cata α（⦇α⦈）。存在＝定义，唯一＝证明原则（融合律的来源）。\n"
             "- 兰贝克：(F i, F ι) 是代数，得唯一 h : i → F i；拼接得 ι ∘ h 为 i 上的自同态，故 = id；再 h ∘ ι = F ι ∘ F h = F(ι ∘ h) = id。i ≅ F i，且为最小不动点 μF（任何不动点 (x, ξ) 都是代数，故有 i → x）。\n"
             "- Haskell：`Fix` 构造子＝ι，`unFix`＝ι⁻¹；`lambekOut = cata (fmap Fix)` 即证明中的 h，可检验与 `unFix` 一致。\n"
             "- 在 Set 中 Fix 对应 μF；Hask 因惰性，`Fix f` 亦含无穷值，最小与最大不动点重合（DaoFP ch.12 “impedance mismatch”）——下集展开 νF。\n"
             "- 初始代数未必存在；需要“叶子”（不依赖洞的构造子）。例：F x = Int × x 在 Set 中 μF = 0（空集是其初始代数载体）。\n"
             "- Adámek：若 F 保持 ω-链余极限，则 colim(0 → F0 → F²0 → ⋯) 是初始代数；Set 上多项式函子满足。Maybe ⇒ ℕ；1 + a × x ⇒ 列表 1 + a + a² + ⋯。\n"
             "- Church 编码 `Mu f = forall a. (f a -> a) -> a`；在 Haskell（参数性）下与 `Fix f` 同构（`toMu` / `fromMu`）。\n"
             "- 依 CTFP 惯例忽略 ⊥。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：道生一",
        "S1Hook": "一 道德经钩子",
        "S2Algebras": "二 代数与同态",
        "S3Initial": "三 初始代数与 cata",
        "S4Lambek": "四 兰贝克引理",
        "S5Fix": "五 Fix 与 cata 的来历",
        "S6Colimit": "六 从无出发：余极限",
        "S7Haskell": "七 短 Haskell",
        "S8Next": "结语：下集反者道之动",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "道生一：初始代数、兰贝克引理与 Fix | 进阶深讲 09"
    desc = f"""进阶深讲第九集。比入门 03/04 更深：F-代数的范畴、初始代数与 cata、兰贝克引理的证明、Fix 的来历、Adámek 余极限与 Church 编码。

· 钩子：道生一（DaoFP 第七章以此开篇）
· 代数 (a, α : F a → a) 与代数同态；范畴 Alg(F)
· 初始代数：唯一出射 = cata；存在即算法，唯一即证明原则
· 兰贝克引理：ι 同构，F i ≅ i，最小不动点 μF
· Fix = ι，unFix = ι⁻¹；cata 沿方块读出
· Adámek：0 → F0 → F²0 → ⋯ 的余极限；Mu 编码
· 短 Haskell：Fix / cata / ExprF / lambekOut / Nat / Mu
· 下集：反者道之动 · 余代数与 ana

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.7 Recursion；ch.11 Algebras —— https://github.com/BartoszMilewski/DaoFP
· CTFP 3.8 F-Algebras —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第四十二章、第二十五章（道法自然）

系列：道可道 · 进阶深讲。上一集《有无相生》；下一集《反者道之动》。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #道生一 #初始代数 #兰贝克引理 #catamorphism #道可道
"""
    tags = ["范畴论", "Haskell", "道德经", "道生一", "初始代数", "F-代数", "兰贝克引理",
            "不动点", "cata", "category theory", "initial algebra", "Lambek's lemma",
            "catamorphism", "Fix", "Bartosz Milewski", "Dao of Functional Programming", "Manim", "进阶深讲"]
    md = f"""# YouTube 发布信息（草案）— 进阶深讲 09 道生一

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
- 字幕：画面已烧录中文；`final/tao-category-detail-09.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道进阶深讲；上一集《有无相生》；下一集《反者道之动》。入门深讲见 01–06。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
