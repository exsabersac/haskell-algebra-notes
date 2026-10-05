# -*- coding: utf-8 -*-
"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S7Haskell": ["s_adj", "s_state", "s_store", "s_lens"],
}
SNIP_FILE = {k: "XiongCi.hs" for k in SNIPS["S7Haskell"]}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("伴随 L ⊣ R", "adjunction L ⊣ R"),
    ("hom 集自然同构", "natural isomorphism of hom-sets"),
    ("单位 η / 余单位 ε", "unit η / counit ε"),
    ("三角恒等式", "triangle identities"),
    ("转置（伴随同构）", "transpose (adjunct)"),
    ("笛卡尔闭范畴 CCC", "cartesian closed category"),
    ("柯里化伴随 (−, s) ⊣ (s → −)", "currying adjunction"),
    ("单子 T = R∘L · μ = RεL", "monad from adjunction"),
    ("余单子 W = L∘R · δ = LηR", "comonad from adjunction"),
    ("State / Store（余状态）", "State / Store (costate) comonad"),
    ("lens = Store 余代数", "lens as Store-coalgebra"),
]


def script_md():
    L = []
    L.append("# 道可道 · 进阶深讲 11 —— 知其雄，守其雌\n")
    L.append("*伴随、单位/余单位、State、Store、lens｜Adjunctions, State, Store, lens — Advanced Deep Dive 11*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已完成入门深讲 01–06 与进阶 07–10；先范畴论陈述，再短 Haskell。\n"
             "- 结构：道德经钩子 → 伴随：hom 同构 → 单位、余单位与三角 → R∘L：State → L∘R：Store → 知其雄守其雌与 lens → 短 Haskell → 下集无为而无不为。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-11.srt`。\n"
             "- 屏幕代码摘自 `haskell/src/XiongCi.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。\n"
             "- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。印章语出《道德经》第二十八章，与本集钩子同章。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>\n")
    L.append("\n| 段落 | DaoFP | CTFP |\n|---|---|---|\n"
             "| 钩子 / 知其雄守其雌 | 10 Adjunctions | 3.2 Adjunctions |\n"
             "| 伴随：hom 同构 | 10 Adjunction between functors；The Currying Adjunction | 3.2 |\n"
             "| 单位、余单位与三角 | 10 Unit and Counit；Triangle identities | 3.2 |\n"
             "| R∘L：State | 16 Monads from Adjunctions；currying → state | 3.6 Monads Categorically |\n"
             "| L∘R：Store | 17 Comonads from Adjunctions；Costate | 3.7 The Store Comonad |\n"
             "| 知其雄守其雌 / lens | 16–17；17 Comonad coalgebras；Lenses | 3.6 / 3.7 |\n"
             "| 短 Haskell | 10 / 16 / 17 · 本集 XiongCi.hs | 3.2 / 3.6 / 3.7 |\n"
             "| 下集预告 | 米田 / Kan | 3.3–3.4 |\n")
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
             "- 伴随 L ⊣ R：C(L x, y) ≅ D(x, R y)，对 x、y 自然；转置互称 adjunct。\n"
             "- 单位 η_x = φ(id_{L x}) : x → R(L x)；余单位 ε_y = φ⁻¹(id_{R y}) : L(R y) → y。\n"
             "- 三角恒等式：(ε L) · (L η) = id_L；(R ε) · (η R) = id_R。有 η/ε+三角 ⇔ 有自然同构。\n"
             "- 任意伴随给出单子 T = R∘L，μ = R ε L；余单子 W = L∘R，δ = L η R。\n"
             "- 柯里化伴随 (−, s) ⊣ (s → −)：R(L a) = s → (a, s) = State s a；L(R c) = (s → c, s) = Store s c。\n"
             "- lens 作为 Store-余代数：φ : s → Store a s ≅ (get, set)，满足 set s (get s) = s、get (set s a) = a、set (set s a) a′ = set s a′。\n"
             "- 每个单子都可拆成伴随（Kleisli / Eilenberg–Moore），拆法不唯一；List 等常来自离开 Hask 的 Free ⊣ U。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。\n"
             "- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {
        "S0Title": "开场：知其雄，守其雌",
        "S1Hook": "一 道德经钩子",
        "S2Adjunction": "二 伴随：hom 同构",
        "S3UnitCounit": "三 单位、余单位与三角",
        "S4State": "四 R∘L：State 单子",
        "S5Store": "五 L∘R：Store 余单子",
        "S6XiongCi": "六 知其雄，守其雌",
        "S7Haskell": "七 短 Haskell",
        "S8Next": "结语：下集无为而无不为",
    }
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "知其雄守其雌：伴随、State、Store 与 lens | 进阶深讲 11"
    desc = f"""进阶深讲第十一集。伴随作为 hom 集自然同构；单位/余单位与三角恒等式；R∘L → State；L∘R → Store；lens 是 Store 余代数。

· 钩子：知其雄，守其雌，为天下溪（伴随 = 半个等价）
· 伴随 L ⊣ R：C(Lx, y) ≅ D(x, Ry)，自然；左映出、右映入
· 单位 η、余单位 ε 与三角恒等式；两种定义等价
· R∘L 生单子：柯里化给出 State；μ = RεL
· L∘R 生余单子：柯里化给出 Store；δ = LηR；extend / 元胞自动机
· 雄 State · 雌 Store · 同一对 η/ε；lens = Store 余代数
· 短 Haskell：adjunction / State / Store / _1
· 下集：无为而无不为 · 米田与 Kan 扩张

章节
{chap}

参考（释义改写，非照录）
· DaoFP ch.10 Adjunctions；ch.16 Monads from Adjunctions；ch.17 Comonads —— https://github.com/BartoszMilewski/DaoFP
· CTFP 3.2 Adjunctions；3.6 Monads；3.7 Store —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第二十八章

系列：道可道 · 进阶深讲。上一集《反者道之动》；下一集《无为而无不为》。
代码：片中 Haskell 均可 GHC 编译。制作：Manim · edge-tts zh-CN-YunxiNeural · 无 BGM。

#范畴论 #Haskell #道德经 #知其雄守其雌 #伴随 #adjunction #State #Store #lens #道可道
"""
    tags = ["范畴论", "Haskell", "道德经", "知其雄守其雌", "伴随", "adjunction", "State", "Store",
            "lens", "comonad", "monad", "unit counit", "category theory",
            "Bartosz Milewski", "Dao of Functional Programming", "Manim", "进阶深讲"]
    md = f"""# YouTube 发布信息（草案）— 进阶深讲 11 知其雄守其雌

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
- 字幕：画面已烧录中文；`final/tao-category-detail-11.srt` 可作 YouTube 字幕轨（建议默认关），或用 `*-nosubs.mp4` + 上传 SRT。
- 分类：教育；语言：中文（简体）。
- 系列：道可道进阶深讲；上一集《反者道之动》；下一集《无为而无不为》。入门深讲见 01–06。
"""
    os.makedirs(f"{ROOT}/final", exist_ok=True)
    open(f"{ROOT}/final/youtube.md", "w").write(md)


if __name__ == "__main__":
    script_md()
    youtube_md()
    print("docs ok")
