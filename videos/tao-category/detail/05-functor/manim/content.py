# -*- coding: utf-8 -*-
"""Single source of truth for narration — 深讲第 5 集：Functor 直觉。

Audience: knows some programming; Haskell optional.
Expand beginner Functor point into ~8–12 min. CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Functor", "Functor"),
    ("fmap", "f map"),
    ("Maybe", "Maybe"),
    ("Nothing", "Nothing"),
    ("Just", "Just"),
    ("List", "List"),
    ("Monad", "Monad"),
    ("endo", "endo"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="Functor 直觉", quote="", chapter="", refs=[],
         beats=[
             dict(say="大制不割。欢迎来到「道可道」深讲第五集。",
                  note="宣纸背景，圆相一笔画出；标题「Functor 直觉」浮现"),
             dict(say="上一集讲构造与折叠：生与归，都沿着构造子走。这一集，我们把「形状」本身提出来——在结构上描画箭头，而不拆掉结构。",
                  note="小字：深讲 04 → 05；提纲 保形 / fmap / 定律"),
             dict(say="范畴论里，这叫函子：对象映到对象，箭头映到箭头，还要保住复合与单位。先把话说明白，再落到几行 Haskell。",
                  note="三行：函子保形 · fmap · 定律"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第八章函子，以及《程序员的范畴论》里函子那两节。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第八章函子，以及《程序员的范畴论》里函子那两节。片中表述都是释义，不是照录。",
                  note="DaoFP ch.8 · CTFP 1.7–1.8；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 大制不割", quote="大制不割。", chapter="《道德经》第二十八章",
         refs=["DaoFP ch.8 Functors（保形直觉）",
               "CTFP 1.7 Functors（no-tearing）"],
         beats=[
             dict(say="大制不割。", note="竖排书法原文，右起"),
             dict(say="入门篇扫过 Functor；深讲第四集刚把折叠钉牢。这一集，我们把「映射而不撕裂」单独拉开。结构可以换里头的值，外壳不许被撕开。映射，不等于拆开重装。",
                  note="小字：入门篇 → 深讲 05；映射而不撕裂"),
             dict(say="先问范畴论的问题：一类结构，能不能把里头的箭头「抬」到外壳上，而外壳的形状不变？能，就叫它函子。不能，就还不是。",
                  note="抬箭头 · 保形"),
             dict(say="Milewski 有个画面：范畴像一张织好的网。函子可以压扁、可以粘合，但不许撕破。连续感，来自「不撕裂」。",
                  tts="米列夫斯基有个画面：范畴像一张织好的网。函子可以压扁、可以粘合，但不许撕破。连续感，来自「不撕裂」。",
                  note="小字：no-tearing · 大制不割"),
             dict(say="慢一点。先把「保形」看明白；后面的 fmap，都站在它上面。映射，是折叠之前的那一层薄纱。",
                  note="书法小字：保形"),
         ]),

    dict(id="S2Shape", title="二 · 函子保形", quote="", chapter="",
         refs=["DaoFP ch.8 Functors between categories；CTFP 1.7"],
         beats=[
             dict(say="函子做两件事：把对象映成对象，把箭头映成箭头。对类型来说，对象是类型，箭头是函数。类型构造子，先完成第一步——把 a 映成 F a。",
                  note="F : 对象 → 对象；Maybe a / List a"),
             dict(say="Maybe 把 a 变成「也许有一个 a」；列表把 a 变成「一串 a」。它们本身不是类型，是类型构造子——要喂进一个类型，才变成类型。",
                  note="type constructor ≠ type"),
             dict(say="第二步更要紧：手里有一条箭头 f，从 a 到 b。函子要交出一条新箭头，从 F a 到 F b。外壳还在，里头的值被 f 改写。",
                  note="f : a → b  ⇒  F f : F a → F b"),
             dict(say="这就是保形：结构记得自己怎么被造出来。你只改「内容」那一层记忆，不改构造的骨架。Just 还是 Just，空列表还是空列表。",
                  note="记得构造 · 只改内容"),
             dict(say="日常比喻：函子像一件外套。你换里头的衬衫，外套的剪裁不变。换衬衫是 fmap；剪裁是那个类型构造子。",
                  note="外套隐喻：剪裁不变"),
             dict(say="所以函子不是「随便一个 map」。它是：在同一张网的形状上，把箭头抬过去。形状先于操作——这话，跟上一集的代数遥相呼应。先认形状，再谈映射。",
                  note="形状先于操作"),
         ]),

    dict(id="S3Fmap", title="三 · fmap 与交换图", quote="", chapter="",
         refs=["DaoFP ch.8 fmap；CTFP 1.7（lifting / commuting square）"],
         beats=[
             dict(say="Haskell 里，把箭头抬上去的那一步，叫 fmap。类型写出来很素：吃一条 a 到 b，交出一条 F a 到 F b。",
                  note="fmap :: (a → b) → (F a → F b)"),
             dict(say="画成交换图更清楚：左边是原来的 f，右边是抬上去的 F f；上下是「放进结构」的虚线。两条路径，说的是同一件事——结构与箭头一起走。",
                  note="交换正方形：a→b 与 Fa→Fb"),
             dict(say="看 Maybe：空还是空；有值，就对里头那个值施 f，再包回 Just。外壳两支，一支不动，一支只动内容。",
                  note="Nothing 不动；Just x → Just (f x)"),
             dict(say="看列表：对每个元素施 f，长度与顺序都不动。一、二、三，乘二之后，仍是三个格子——二、四、六。保形，肉眼可见。",
                  note="动画 [1,2,3] → [2,4,6]"),
             dict(say="术语上，这叫 lifting：把在值上的计算，抬到结构里去做。你不用拆开结构自己循环——函子替你保管形状。",
                  note="lifting · 抬升"),
             dict(say="交换图不是装饰。它强迫你核对：先映射再装箱，与先装箱再映射，是否一致。一致，才叫函子；不一致，只是碰巧同名的函数。图在说话，代码在应和。",
                  note="路径一致 = 函子"),
         ]),

    dict(id="S4Laws", title="四 · 函子定律", quote="", chapter="",
         refs=["DaoFP ch.8（preserve composition & identity）；CTFP 1.7 laws"],
         beats=[
             dict(say="函子不止要有 fmap，还要守两条定律。定律写不进 Haskell 的类型，却写进你的责任：单位，与复合。",
                  note="两条定律：id · 复合"),
             dict(say="第一，单位：fmap id，等于 id。对结构施「什么都不做」，结构必须原样回来。Just 三还是 Just 三；列表不增不减。",
                  note="fmap id = id"),
             dict(say="第二，复合：先 fmap f 再 fmap g，必须等于一次 fmap「g 圆点 f」。抬两次，等于抬一次复合后的箭头。顺序不许偷偷调换。",
                  note="fmap (g ∘ f) = fmap g ∘ fmap f"),
             dict(say="为什么要定律？因为没有它们，fmap 只是个同名函数——可以撕破形状，可以乱序，可以吞掉元素。有了定律，保形才被钉死。",
                  note="无定律 = 不合法函子"),
             dict(say="Milewski 提醒：编译器认的是类型类实例；合法与否，要人来核对。坏的 map 也能过类型检查——所以定律不是口号，是契约。",
                  tts="米列夫斯基提醒：编译器认的是类型类实例；合法与否，要人来核对。坏的 map 也能过类型检查——所以定律不是口号，是契约。",
                  note="typeclass ≠ laws"),
             dict(say="大制不割：定律就是「不割」的条文。单位保真，复合保序。守住这两条，函子才名副其实。条文简单，分量不轻。",
                  note="书法：大制不割"),
         ]),

    dict(id="S5Haskell", title="五 · Maybe 与 List", quote="", chapter="",
         refs=["DaoFP ch.8 Maybe / List instances；CTFP 1.7"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。先声明 Functor 类型类，再写出 Maybe 与列表的实例。类型写在前，匹配藏在里头。",
                  note="代码块：s_class"),
             dict(say="Maybe 的 fmap：遇到 Nothing 原样返回；遇到 Just，对里头的值施 f。空不生有，有则改内容——保形的最小例子。",
                  note="代码 s_maybe；高亮 instance"),
             dict(say="列表的 fmap：空还是空；非空则头施 f，尾递归同样做。长度不变，顺序不变。你每天写的 map，就是它。",
                  note="代码 s_list"),
             dict(say="试一下：对 Just 四十一加一，得到 Just 四十二；对一、二、三乘二，得到二、四、六。外壳没动，数字动了。",
                  note="demoMaybe / demoList"),
             dict(say="再抽查定律：fmap id 不改 Just，不改列表；先加一再乘二，与一次复合再 fmap，结果相同。屏幕代码都能编译。",
                  note="id / 复合 抽检"),
             dict(say="图对齐了，代码只是把图念出来。Bifunctor、Contravariant，留给以后；今天只把协变函子的直觉钉牢。",
                  note="对照：图 ⟷ 代码；不引入反变"),
         ]),

    dict(id="S6Next", title="结 · 大制不割", quote="", chapter="",
         refs=["DaoFP ch.15 Monads；CTFP 3.4–3.6；下一集 Monad / do"],
         beats=[
             dict(say="今天钉牢三件事：函子保形，不撕裂结构；fmap 把箭头抬到外壳上；单位与复合两条定律，把保形写成契约。形状清楚了，效应才接得上。",
                  note="三句回顾环绕圆相"),
             dict(say="下一集，我们把「效应」接进来：Monad——在函子之上，多一层绑定与注入。do 记号会登场，把链式计算写成人话。函子是底，Monad 往上长。",
                  note="预告：Monad · do；小字「深讲 06」"),
             dict(say="借 Milewski 的提醒：先看形状，再看映射。大制不割。我们下集见。",
                  tts="借米列夫斯基的提醒：先看形状，再看映射。大制不割。我们下集见。",
                  note="「大制不割」书法；印章；谢谢观看"),
         ]),
]
