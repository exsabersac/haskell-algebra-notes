# -*- coding: utf-8 -*-
"""Single source of truth for narration — 进阶深讲第 10 集：反者道之动.

Audience: finished beginner 01–06 and advanced 07–09.
Deeper than beginner ep04 (fold intuition, shallow ana): coalgebras and CoAlg(F),
terminal coalgebra = anamorphism, dual of Lambek, μF vs νF / impedance mismatch, hylo fusion.
CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("DaoFP", "道 F P"),
    ("CTFP", "C T F P"),
    ("unFix", "un Fix"),
    ("fmap", "f map"),
    ("ListF", "List F"),
    ("StreamF", "Stream F"),
    ("NilF", "Nil F"),
    ("ConsF", "Cons F"),
    ("μF", "缪 F"),
    ("νF", "纽 F"),
    ("ι", "约塔"),
    ("α", "阿尔法"),
    ("β", "贝塔"),
    ("γ", "伽马"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="反者道之动", quote="", chapter="", refs=[],
         beats=[
             dict(say="反者道之动。欢迎来到「道可道」进阶深讲——第十集。",
                  note="宣纸背景，圆相一笔画出；标题「反者道之动」浮现"),
             dict(say="上一集立起了初始代数：从它出发，到任何代数恰有一支同态，叫 cata。今天把每一支箭头都反过来。始变终，收拢变展开，砍树变种树。",
                  note="小字：进阶 09 → 10；初始代数 → 终余代数"),
             dict(say="本集四根钉子：余代数与同态；终余代数与 ana；μF 与 νF，以及 Haskell 里的阻抗失配；hylo——先生而后归。入门第四集浅提了展开；今天把对偶写正式。",
                  note="四行提纲"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第十二章余代数，以及《程序员的范畴论》F-代数那一节的对偶侧。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第十二章余代数，以及《程序员的范畴论》F 代数那一节的对偶侧。片中表述都是释义，不是照录。",
                  note="DaoFP ch.12 · CTFP 3.8；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道德经钩子", quote="反者道之动，弱者道之用。", chapter="《道德经》第四十章",
         refs=["DaoFP ch.12 Coalgebras", "CTFP 3.8 Coalgebras"],
         beats=[
             dict(say="反者道之动，弱者道之用。", note="竖排书法原文，右起"),
             dict(say="「反」不是否定，是掉头。范畴论里，把箭头全部翻转，几乎每个构造都会得到它的孪生兄弟。对偶不是修辞，而是一种机械的生产力。",
                  note="箭头翻转；定理 ⟷ 对偶定理"),
             dict(say="上一集的代数，是从 F a 到 a：收拢一层结构。反过来，余代数是从 a 到 F a：从一颗种子里，长出一层结构。Milewski 说得很干脆：cata 用来砍树，ana 用来种树。",
                  tts="上一集的代数，是从 F a 到 a：收拢一层结构。反过来，余代数是从 a 到 F a：从一颗种子里，长出一层结构。米列夫斯基说得很干脆：cata 用来砍树，ana 用来种树。",
                  note="f a → a 与 a → f a 上下对照"),
             dict(say="入门第四集已经让你见过 unfold：给一个种子，吐出列表。那是现象。今天要问：为什么展开恰好只有一种？为什么无穷的流也能被同一个 Fix 装下？",
                  note="入门 04：展开是现象；两个问题"),
             dict(say="答案仍是普遍性质——只是始对象换成了终对象。刻画一旦掉头，递归、展开、最大不动点，全都跟着来。",
                  note="终对象 → 终余代数 → ana"),
         ]),

    dict(id="S2Coalgebras", title="二 · 余代数与同态", quote="", chapter="",
         refs=["DaoFP ch.12 Coalgebras", "CTFP 3.8 Coalgebras"],
         beats=[
             dict(say="先定零件。还是那个自函子 F，描述「一层」形状。只是方向反了：现在不是把装好的结果收进来，而是从载体里观察出一层形状。",
                  note="自函子 F；观察 vs 收尾"),
             dict(say="F-余代数是一对东西：一个载体 a，和一支结构映射 γ，从 a 到 F a。读法是：给我一个种子，它这一步长出什么形状，洞里又留下什么种子。",
                  note="(a, γ : a → F a)"),
             dict(say="同一个形状可以有许多余代数。从整数展开出列表：零映到空，非零映到头与减一——这是阶乘的生。从整数展开出流：映到自身与加一——这是自然数流的种。",
                  note="range / nats 两份余代数"),
             dict(say="余代数之间的箭头，叫余代数同态：载体之间的一支 f，要和两边的结构映射交换。先用 γ 观察，再用 F f 搬运；或者先用 f 搬运，再用 δ 观察——两条路必须相等。",
                  note="交换方块：F f ∘ γ = δ ∘ f"),
             dict(say="函子保持恒等与复合，所以恒等是同态，方块可以拼接。余代数和同态组成一个范畴，记作 CoAlg(F)。它正是 Alg(F) 的对偶范畴。",
                  note="CoAlg(F) ≅ Alg(F)^op"),
         ]),

    dict(id="S3Terminal", title="三 · 终余代数与 ana", quote="", chapter="",
         refs=["DaoFP ch.12 Anamorphisms；Infinite data structures", "CTFP 3.8"],
         beats=[
             dict(say="现在把上一集的定义原样对偶过来。余代数范畴里的终对象，叫终余代数，记作 ν 和它的结构映射：对任意余代数 a 和 γ，通往它的同态存在且唯一。",
                  note="(ν, out)：∀(a, γ) ∃! 同态"),
             dict(say="这支唯一的同态，就叫 anamorphism，简称 ana。入门第四集说「ana 就是 unfold」；现在知道它的身份：终对象的唯一入射。",
                  note="ana γ；虚线 ∃!"),
             dict(say="存在给你算法：任选一份余代数，就有一条展法。唯一给你证明原则：两个函数只要都满足同一个方块，它们就相等。不用共归纳的逐项比较，方块替你说完。",
                  note="存在 = 算法 · 唯一 = 共归纳证明原则"),
             dict(say="兰贝克的对偶也成立：终余代数的结构映射一定是同构。ν 与 F ν 是同一个东西。所以 ν 是 F 的不动点——而且是最大的那个。记作 νF。",
                  note="out : ν ≅ F ν；ν = νF（最大不动点）"),
             dict(say="取 F 为 StreamF：没有空构造子，每一层都有头和尾。终余代数就是无穷流。取列表形状：终余代数在集合里比初始代数更大——它还允许「假无穷」的极限情况。",
                  note="Stream = ν StreamF；List 在 Set 中 μ ⊂ ν"),
         ]),

    dict(id="S4Flip", title="四 · 翻转：图与代码", quote="", chapter="",
         refs=["DaoFP ch.12 Anamorphisms", "CTFP 3.8"],
         beats=[
             dict(say="图也一样：把 cata 那张交换图的箭头全部翻转，就是 ana 的交换图。左边的 ι 朝上变成右边的 out 朝下；虚线的唯一出射，变成唯一入射。",
                  note="cata 方块 ↔ ana 方块；箭头逐一翻转"),
             dict(say="代码也一样。cata 是：先剥一层 unFix，再 fmap 递归，最后用代数收尾。把复合的顺序倒过来，unFix 换成 Fix，就是 ana：先用余代数观察，再 fmap 递归，最后用 Fix 封一层。",
                  note="代码 cata / ana 对照高亮"),
             dict(say="所以你不必另背一套定义。记住一张方块，掉头即得另一张；记住一行复合，倒序即得另一行。反者道之动——对偶是一种压缩。",
                  note="一图两读 · 一行两式"),
             dict(say="Haskell 里，构造子 Fix 同时扮演两边：作为代数的结构映射，它是 ι；作为余代数的逆，它是 out 的逆，把一层形状封回不动点。unFix 则是对面的那一支。",
                  note="Fix 兼任 ι 与 out⁻¹"),
             dict(say="这里藏着第二集与第九集的回声：初始代数从始对象，也就是无，一层层生长出来；终余代数则从终对象，也就是有，一层层逼近。有无相生，又出现了一次。",
                  note="0 → F0 → F²0 → …  与  1 ← F1 ← F²1 ← …"),
         ]),

    dict(id="S5MuNu", title="五 · μF 与 νF", quote="", chapter="",
         refs=["DaoFP ch.12 Infinite data structures；The impedance mismatch", "CTFP 3.8"],
         beats=[
             dict(say="在集合范畴里，最小不动点与最大不动点并不相同。μF 是从无长出来的全部有限阶段；νF 是从有逼近下来的全部相容体系。一般有 μF 真包含于 νF。",
                  note="Set：μF ⊂ νF"),
             dict(say="经典例子是恒等函子：最小不动点是空集，最大不动点是单点集。列表函子也一样：初始代数是有限列表；终余代数还装着「无限列表」的理想点。",
                  note="Id：∅ vs 1；List：有限 vs 含极限"),
             dict(say="但在 Haskell 里，因为惰性，同一个 Fix 既能折叠有限的结构，也能展开无限的流。最小与最大，在这里被揉成了一个类型。",
                  note="Hask：Fix 兼任 μF 与 νF"),
             dict(say="Milewski 把这种错位叫阻抗失配：范畴论在集合里分得很清的两样东西，到了惰性语言里共用一个语法。便利是真的，代价也是真的。",
                  tts="米列夫斯基把这种错位叫阻抗失配：范畴论在集合里分得很清的两样东西，到了惰性语言里共用一个语法。便利是真的，代价也是真的。",
                  note="impedance mismatch"),
             dict(say="代价之一：如果展开永不终止，依赖它的计算也会永远算下去。惰性让你写下无穷，却不替你保证停机。",
                  note="发散：ana 不终止 ⇒ 后续发散"),
         ]),

    dict(id="S6Hylo", title="六 · hylo：先生而后归", quote="", chapter="",
         refs=["DaoFP ch.12 Hylomorphisms", "CTFP 3.8"],
         beats=[
             dict(say="有了生，有了归，就可以把它们接起来：先用 ana 展开，再用 cata 折叠。这就是 hylo，合态射。先生，而后归。",
                  note="a ─ana→ Fix f ─cata→ b"),
             dict(say="妙处在于，hylo 的定义里没有不动点的影子：中间那个结构被生出，又在构造的同时被消费，从未完整存在于内存中。老子有一句话恰好描述这种融合：生而不有。",
                  note="中间 Fix f 渐隐；书法「生而不有」"),
             dict(say="比如阶乘：从 n 展开出 n、n 减一，一直到一；再把这条链乘起来。写成 hylo，生和归各是一份不递归的菜谱，递归机关只出现一次。",
                  note="fact = hylo alg coa"),
             dict(say="你也可以先 ana 再 cata，语义相同；但那会真的建出中间那棵树。hylo 把两趟合成一趟——这是融合律在代码里的样子。",
                  note="hylo = cata ∘ ana（融合后不建 Fix）"),
             dict(say="反者道之动：每证明一个关于代数的定理，翻转箭头，就白得一个关于余代数的定理。弱者道之用——余代数这一侧，往往用更弱的假设，换来对无穷结构的发言权。",
                  note="定理 ⟷ 对偶定理；弱者 = 共归纳"),
         ]),

    dict(id="S7Haskell", title="七 · 短 Haskell", quote="", chapter="",
         refs=["DaoFP ch.12；CTFP 3.8；本集 haskell/src/FanZhe.hs"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。Fix、Algebra、Coalgebra、cata、ana。后两行是同一张方块的两种读法。",
                  note="代码 s_fix"),
             dict(say="hylo 一行：没有 Fix 的影子。阶乘是 ListF 上的一份代数加一份余代数。",
                  note="代码 s_hylo / s_list"),
             dict(say="StreamF 没有空构造子。nats 从零展开，takeS 只取前几项——无穷被种下，有限被看见。",
                  note="代码 s_stream"),
             dict(say="ana 也能种有限树：range 把闭区间展开成列表，再交给 cata 求和。同一套机关，有限与无穷共用。",
                  note="代码 s_range"),
             dict(say="跑一下：五的阶乘是一百二十；自然数流前八项是零到七；一到十求和得五十五。图怎么说，代码就怎么应。",
                  note="demo 输出"),
         ]),

    dict(id="S8Next", title="结 · 下集知其雄守其雌", quote="", chapter="",
         refs=["下集预告：知其雄，守其雌 · 伴随与单子余单子"],
         beats=[
             dict(say="今天钉牢四件事：余代数与同态组成范畴；终余代数的唯一入射就是 ana；μF 与 νF 在集合里分家，在 Haskell 里共用 Fix；hylo 先生后归，中间不落地。",
                  note="四句回顾环绕圆相"),
             dict(say="下一集《知其雄，守其雌》：伴随登场。左伴随与右伴随，单位与余单位——同一条溪流的两岸，喂养出单子与余单子。",
                  note="预告：伴随 · State · Store"),
             dict(say="借 Milewski 的提醒：对偶不是修辞，而是生产力。反者道之动。进阶篇，我们下集见。",
                  tts="借米列夫斯基的提醒：对偶不是修辞，而是生产力。反者道之动。进阶篇，我们下集见。",
                  note="「反者道之动」书法；印章；谢谢观看"),
         ]),
]
