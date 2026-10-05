"""Generate script.md and final/youtube.md from content.py + Haskell snippets + actual render timings."""
import json, os, re
from content import SCENES
from common import load_snip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(f"{ROOT}/build/assembly_hq.json"))
SNIPS = {
    "S1Dao": ["s1"], "S2YouWu": ["s2wu", "s2you", "s2b", "s2c"], "S3Fix": ["s3a", "s3b", "s3c"],
    "S4Hylo": ["s4a", "s4b"], "S5Adjunction": ["s5a", "s5b", "s5c", "s5d"], "S6Yoneda": ["s6a", "s6b"],
}
SNIP_FILE = {"s1": "Seg1Dao.hs", "s2": "Seg2YouWu.hs", "s3": "Seg3Fix.hs", "s4": "Seg4Hylo.hs", "s5": "Seg5Adjunction.hs",
             "s6": "Seg6Yoneda.hs"}


def ts(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


GLOSSARY = [
    ("对象 / 箭头（态射）", "object / arrow (morphism)"), ("始对象 / 终对象", "initial / terminal object"),
    ("对偶范畴 Cᵒᵖ", "opposite category"), ("和（余积）/ 积", "sum (coproduct) / product"),
    ("全局元素", "global element"), ("函子 / 自然变换 / 自然性", "functor / natural transformation / naturality"),
    ("代数 / 载体 / 结构映射", "algebra / carrier / structure map"), ("初始代数 / 终余代数", "initial algebra / terminal coalgebra"),
    ("不动点（最小 μF / 最大 νF）", "fixed point (least / greatest)"), ("兰贝克引理", "Lambek's lemma"),
    ("余极限 / ω-链", "colimit / ω-chain"), ("折叠 cata / 展开 ana / 合态射 hylo", "catamorphism / anamorphism / hylomorphism"),
    ("伴随 L ⊣ R / 单位 η / 余单位 ε", "adjunction / unit / counit"), ("柯里化伴随", "currying adjunction"),
    ("单子 / 余单子", "monad / comonad"), ("Store（costate）余单子", "store (costate) comonad"),
    ("余单子余代数", "comonad coalgebra"), ("米田引理 / 米田嵌入（满忠实）", "Yoneda lemma / Yoneda embedding (fully faithful)"),
    ("续体传递风格", "continuation-passing style (CPS)"), ("右 Kan 扩张", "right Kan extension"),
]


def script_md():
    L = []
    L.append("# 道可道 · 范畴之道 —— 解说稿\n")
    L.append("*用六句《道德经》重读范畴论与 Haskell｜The Dao of Categories*\n")
    L.append(f"- 成片时长：**{ts(A['total'])}**（{A['total']:.1f} 秒），1920×1080，30 fps\n"
             "- 受众：已熟悉 Haskell、读过 CTFP / DaoFP（入门范畴论已知）。跳过基本定义，只给新视角。\n"
             "- 结构：每段 = 《道德经》原文 → 范畴论陈述 → 几行 Haskell。哲学只是钩子，数学必须正确。\n"
             "- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category.srt`。\n"
             "- 屏幕上的全部代码都直接摘自 `haskell/src/*.hs`（以 `-- {{snip:…}}` 标记抽取），并经 GHC 9.14.1 `-Wall` 编译通过。\n")
    L.append("\n## 主要参考与致谢\n")
    L.append("本片的叙述框架与 Haskell 写法以 Bartosz Milewski 的两本书为主要参照（释义、改写，不做长段照录）：\n\n"
             "- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>\n"
             "- **CTFP** — *Category Theory for Programmers*（hmemcpy 编排版），<https://github.com/hmemcpy/milewski-ctfp-pdf>\n\n"
             "DaoFP 自身的“道”式框架被直接借用：第 1 章把老子首句改写为 *“The type that can be described is not the eternal type”*，"
             "并以“Yin and Yang”一节引入始/终对象；第 2 章称恒等箭头为 *wu wei*；第 3 章 *“Master Yoneda says: At the arrows look!”*；"
             "第 7 章《Recursion》以“道生一……”开篇；第 20 章以 Mac Lane 的 *“All concepts are Kan extensions”* 引入 Kan 扩张。\n")
    L.append("\n| 段落 | DaoFP 章节 | CTFP 章节 |\n|---|---|---|\n"
             "| 一 道可道 | 1 Clean Slate（Types and Functions, Elements）；3 Isomorphism（Reasoning with Arrows） | 1.1, 1.2 |\n"
             "| 二 有无相生 | 1 Clean Slate（Yin and Yang, Elements） | 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types |\n"
             "| 三 道生一 | 7 Recursion；11 Algebras（Initial algebra, Lambek's Lemma and Fixed Points, Catamorphisms, Initial Algebra as a Colimit） | 3.8 F-Algebras |\n"
             "| 四 反者道之动 | 12 Coalgebras（Anamorphisms, Infinite data structures, Hylomorphisms, The impedance mismatch） | 3.8 F-Algebras（Coalgebras） |\n"
             "| 五 知其雄 | 10 Adjunctions（The Currying Adjunction; Unit and Counit）；16 Monads and Adjunctions（currying adjunction and the state monad）；17 Comonads（Costate comonad; Lenses） | 3.2 Adjunctions；3.6 Monads Categorically；3.7 Comonads |\n"
             "| 六 无为 | 2 Composition（Identity）；9 Natural Transformations（The Yoneda Lemma; Yoneda lemma in programming）；20 Kan Extensions（Right Kan extension in Haskell） | 2.5 The Yoneda Lemma；2.6 Yoneda Embedding；3.11 Kan Extensions |\n")
    L.append("\n与 Milewski 保持一致的写法：`newtype Fix f = Fix { unFix :: f (Fix f) }`、`type Algebra f a = f a -> a`、"
             "`cata alg = alg . fmap (cata alg) . unFix`、`ana coa = Fix . fmap (ana coa) . coa`、`hylo`；"
             "`unit = curry id` / `counit = uncurry id`；`data Store s c = St (s -> c) s`；`join mma = State (fmap (uncurry runState) (runState mma))`；"
             "`duplicate (St f s) = St (St f) s`；`Lens s a = s -> Store a s`；`newtype Ran g h a = Ran (forall b. (a -> g b) -> h b)`。\n")
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
        if s["id"] == "S6Yoneda":
            L.append("\n另：屏幕上 `fmap h (Yoneda g) = Yoneda (\\k -> g (k . h))` 为 `Seg6Yoneda.hs` 中 `Functor (Yoneda f)` 实例；"
                     "`Ran` 与 `Yoneda f ≅ Ran Identity f` 的双向转换 `yonedaToRan` / `ranToYoneda` 亦在该文件中。\n")
        if s["id"] == "S4Hylo":
            L.append("\n另：屏幕上 `nats = ana (\\n -> StreamF n (n + 1)) 0` 摘自 `Seg4Hylo.hs`（惰性下同一个 `Fix` 承载无限流）。\n")
    L.append("\n---\n\n## 数学校对备注\n\n"
             "- 依 CTFP 惯例在 Hask 中忽略 ⊥（`Void` 作为始对象、`a -> Void` 作为否定都在此约定下成立）。\n"
             "- 第三段：Adámek 定理要求 f 保持 ω-链余极限（多项式函子如 `Maybe`、`ListF e` 满足）；`Maybeⁿ Void` 恰有 n 个值，故“无、一、二、三”是精确的计数。\n"
             "- 第四段：在 Set 中 μF ⊊ νF（例如恒等函子：∅ 与单点集）；Haskell 因惰性用同一个 `Fix f` 承载二者，"
             "代价是 hylo 在展开不终止时发散（DaoFP 12 “impedance mismatch”）。\n"
             "- 第五段：State = R∘L，Store = L∘R，`join = R ε L`，`duplicate = L η R`；合法 lens 恰为 Store 余单子的余代数（DaoFP 17）。\n"
             "- 第六段：`forall x. (a -> x) -> f x ≅ f a` 是 Hask 中（参数性下）的米田引理；f = Identity 给出 `a ≅ forall x. (a -> x) -> x`（CPS）；"
             "米田嵌入满忠实 ⇒ a ≅ b ⟺ C(a,−) ≅ C(b,−)；`Yoneda f ≅ Ran Identity f`。\n")
    L.append("\n## 制作说明\n\n"
             "- 画面：Manim Community 0.21（Cairo），白底渲染后与程序生成的宣纸纹理做 multiply 合成；唯一红色为印章「知白守黑」（第二十八章）。\n"
             "- 字体：原文书法 Ma Shan Zheng（OFL）；正文/字幕 霞鹜文楷 LXGW WenKai（OFL）；代码 IBM Plex Mono（OFL）；英文引文 EB Garamond（OFL）。\n"
             "- 构建：`manim/tts.py` → `manim/scenes.py`（每拍时间写入 `build/timings`）→ `manim/assemble.py`（按实际帧时刻放置音频、生成字幕）→ ffmpeg 合成。\n")
    open(f"{ROOT}/script.md", "w").write("".join(L))


def youtube_md():
    names = {"S0Title": "开场：六句话，一件事", "S1Dao": "一 道可道：对象不可道，箭头可道", "S2YouWu": "二 有无相生：始对象与终对象",
             "S3Fix": "三 道生一：初始代数、兰贝克引理与 cata", "S4Hylo": "四 反者道之动：余代数、ana 与 hylo",
             "S5Adjunction": "五 知其雄，守其雌：伴随生出 State 与 Store", "S6Yoneda": "六 无为而无不为：米田引理与 Kan 扩张",
             "S7Ending": "结语：看箭头"}
    chap = "\n".join(f"{ts(A['offsets'][s['id']][0])} {names[s['id']]}" for s in SCENES)
    title = "道可道：用《道德经》读范畴论与 Haskell | The Dao of Categories: Fixpoints, Adjunctions & Yoneda"
    desc = f"""用六句《道德经》，重读范畴论里最核心的几件事：始对象与终对象、初始代数与兰贝克引理、代数与余代数的对偶、伴随（State 与 Store），以及米田引理。每一段都是同一个节奏：先读原文，再给出范畴论的陈述，最后落到几行 Haskell。

老子是钩子，数学是正文。本片面向已经会 Haskell、读过《程序员的范畴论》（CTFP）或《函数式编程之道》（DaoFP）的观众，跳过基本定义，只讲新的视角：
· 对象不可道，只有箭头可道——直到米田引理把这句话赎回来
· 道生一，一生二，二生三：从 Void 出发反复作用 Maybe，恰好得到 0、1、2、3 个值，这条链的余极限就是自然数（Adámek 定理）
· 道法自然：Fix f ≅ f (Fix f)，道是它自己的不动点
· 反者道之动：翻转箭头，cata 变成 ana；hylo 先生后归，生而不有
· 知其雄，守其雌：同一个柯里化伴随 (,) s ⊣ (->) s，一面是 State 单子，一面是 Store 余单子
· 无为而无不为：forall x. (a -> x) -> f x ≅ f a

章节
{chap}

参考（本片框架主要参照 Bartosz Milewski 的两本书，叙述为释义改写）
· The Dao of Functional Programming（DaoFP）：第 1 章 Clean Slate、第 2 章 Composition、第 3 章 Isomorphism、第 7 章 Recursion、第 9 章 Natural Transformations（Yoneda）、第 10 章 Adjunctions、第 11 章 Algebras、第 12 章 Coalgebras、第 16 章 Monads and Adjunctions、第 17 章 Comonads、第 20 章 Kan Extensions —— https://github.com/BartoszMilewski/DaoFP
· Category Theory for Programmers（CTFP）：1.5、1.6、2.5 Yoneda Lemma、2.6 Yoneda Embedding、3.2 Adjunctions、3.6 Monads Categorically、3.7 Comonads、3.8 F-Algebras、3.11 Kan Extensions —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第一、二、二十八、三十七、四十、四十二章

代码：片中全部 Haskell 代码均可用 GHC 编译运行（仓库链接待补）。
制作：Manim Community · 旁白 Microsoft Edge 神经语音（zh-CN-YunxiNeural）· 字体 霞鹜文楷 / Ma Shan Zheng / IBM Plex Mono / EB Garamond（均为 SIL OFL）。无背景音乐。

#范畴论 #Haskell #道德经
"""
    tags = ["范畴论", "Haskell", "道德经", "老子", "函数式编程", "米田引理", "Yoneda lemma", "伴随", "adjunction",
            "初始代数", "initial algebra", "兰贝克引理", "Lambek lemma", "catamorphism", "anamorphism", "hylomorphism",
            "递归模式", "recursion schemes", "State monad", "Store comonad", "Kan extension", "category theory",
            "Bartosz Milewski", "Dao of Functional Programming", "Category Theory for Programmers", "Manim"]
    md = f"""# YouTube 发布信息（草案）

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
- 字幕：画面已烧录中文字幕；`final/tao-category.srt` 可作为 YouTube 中文字幕轨上传（便于搜索与自动翻译；如上传，建议默认关闭以免与烧录字幕重叠），或改用无烧录版本 `final/tao-category-nosubs.mp4` + 上传 SRT。
- 分类建议：教育（Education）；语言：中文（简体）。
"""
    open(f"{ROOT}/final/youtube.md", "w").write(md)


script_md()
youtube_md()
print("docs ok")
