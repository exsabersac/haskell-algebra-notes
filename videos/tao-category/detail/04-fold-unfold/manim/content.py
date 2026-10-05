# -*- coding: utf-8 -*-
"""Single source of truth for narration — 深讲第 4 集：构造与折叠。

Audience: knows some programming; Haskell optional.
Expand beginner points on fold/unfold into ~8–12 min. CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Void", "Void"),
    ("Maybe", "Maybe"),
    ("Nothing", "Nothing"),
    ("Just", "Just"),
    ("Nil", "Nil"),
    ("Cons", "Cons"),
    ("List", "List"),
    ("foldr", "fold r"),
    ("fold", "fold"),
    ("unfoldr", "unfold r"),
    ("unfold", "unfold"),
    ("cata", "cata"),
    ("ana", "ana"),
    ("hylo", "hylo"),
    ("Functor", "Functor"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="构造与折叠", quote="", chapter="", refs=[],
         beats=[
             dict(say="夫物芸芸，各复归其根。欢迎来到「道可道」深讲第四集。",
                  note="宣纸背景，圆相一笔画出；标题「构造与折叠」浮现"),
             dict(say="上一集把 Maybe 和列表生出来了：构造子往外长。这一集，我们把方向反过来——沿着构造的逆方向，把结构收成一个值。生，与归，是同一枚硬币的两面。",
                  note="小字：深讲 03 → 04；提纲 构造 / 折叠 / 展开"),
             dict(say="范畴论里，这叫沿着代数去折叠：构造子是引入，折叠是消解。先把话说明白，再落到几行 Haskell。不着急写代码。",
                  note="三行：构造代数 · cata / foldr · ana 浅提"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》讲代数与余代数的那几章，以及《程序员的范畴论》里 F-代数那一节。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》讲代数与余代数的那几章，以及《程序员的范畴论》里 F 代数那一节。片中表述都是释义，不是照录。",
                  note="DaoFP ch.11–12 · CTFP 3.8；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 各复归其根", quote="夫物芸芸，各复归其根。", chapter="《道德经》第十六章",
         refs=["DaoFP ch.11 Algebras（Catamorphisms，直觉层）",
               "CTFP 3.8 F-Algebras（fold 直觉）"],
         beats=[
             dict(say="夫物芸芸，各复归其根。", note="竖排书法原文，右起"),
             dict(say="入门篇扫过折叠与展开；深讲第三集只把「生」看清楚。这一集，我们把「收回去」单独拉开。生出来之后，还要能归回去。",
                  note="小字：入门篇 → 深讲 04；生 → 归"),
             dict(say="先问范畴论的问题：一个递归类型，有哪些构造方式？每种构造子对应一条引入规则。消解，则是沿着这些规则往回走——不是另起炉灶，而是原路返还。",
                  note="引入 / 消解 对照"),
             dict(say="列表要么空，要么头加尾。折叠就是：遇到空，给一个起点；遇到头加尾，说清如何把头和已折叠的尾合成一步。两句话，就定下整条折法。",
                  note="Nil → init；Cons → step"),
             dict(say="你没有写循环——你只说清了一步，递归替你走完全程。慢一点，先把「代数」这两个字看明白；后面的 fold，都站在它上面。",
                  note="书法小字：只说清一步"),
         ]),

    dict(id="S2Algebra", title="二 · 构造代数", quote="", chapter="",
         refs=["DaoFP ch.11 Algebras；CTFP 3.8 F-Algebras（直觉，不引入 Lambek）"],
         beats=[
             dict(say="构造子合在一起，就是一份代数：它告诉你，怎么从「零件」拼出「成品」。对列表来说，零件是单元，或「一个元素加上已有列表」。形状先于值。",
                  note="代数 = 构造方式的集合；Nil / Cons"),
             dict(say="Nil 不吃任何东西，直接交出空列表。Cons 吃一个头、一个尾，交出更长的列表。两支合起来，就是列表的代数——引入规则的全体。",
                  note="Nil :: 1 → List；Cons :: A × List → List"),
             dict(say="Milewski 提醒：代数不只是「数据结构」。它是一套操作——把形状里的洞填上，得到目标类型里的一个值。洞可以是空位，也可以是递归的子结构。",
                  tts="米列夫斯基提醒：代数不只是「数据结构」。它是一套操作——把形状里的洞填上，得到目标类型里的一个值。洞可以是空位，也可以是递归的子结构。",
                  note="小字：algebra = 填洞的操作"),
             dict(say="举例：若目标是数字，空对应零，头加尾对应「头加上已折好的尾」——这就是求和代数。同一形状，换一套操作，就变成求积、求长、拼接。结构不变，菜谱变。",
                  note="同一 List 形状 · 不同代数 → sum / product / length"),
             dict(say="所以折叠不是魔法关键字。它是：拿着一份代数，沿着构造子的逆方向，把整棵树——或整条列表——收成代数所指定的那个值。一步对应一个构造子。",
                  note="fold = 用代数消费结构"),
             dict(say="日常比喻：代数像一份菜谱。构造给出食材的摆法；折叠按菜谱一步步做完，桌上只剩一道菜——那个结果值。看懂菜谱，比背菜名有用。",
                  note="菜谱隐喻：结构 → 结果"),
         ]),

    dict(id="S3Cata", title="三 · 折叠 cata", quote="", chapter="",
         refs=["DaoFP ch.11 Catamorphisms；CTFP 3.8（cata / foldr 直觉）"],
         beats=[
             dict(say="范畴论里，这种「沿着代数往回折」的唯一箭头，常叫 catamorphism，简称 cata。名字吓人，直觉很素：就是 fold。对列表，你每天都在用。",
                  note="cata = catamorphism ≈ fold"),
             dict(say="对列表，Haskell 里最熟的是 foldr：先给空列表一个起点，再给「头与已折尾」一个二元步骤。从右往左折，形状与 Cons 对齐——这不是巧合，是设计。",
                  note="foldr step init；与 Cons 对齐"),
             dict(say="看求和：空是零；非空是头加上尾的总和。写成 foldr，就是把加号和零交给它——结构由列表保管，你只负责一步。一、二、三，折完是六。",
                  note="sum = foldr (+) 0；动画 1:2:3:[] → 6"),
             dict(say="再看求积：空是一；非空是头乘以尾的积。同一条列表，换代数，结果就变。形状不变，操作变——这正是「代数」二字的用处。",
                  note="product = foldr (*) 1"),
             dict(say="为什么说「唯一」？因为递归类型由构造子生成：一旦你规定了每个构造子对应哪一步，从根到叶的折叠路径就被钉死了——没有别的合法折法。今天只讲直觉，不写 Lambek。",
                  note="小字：由构造唯一决定（直觉，非 Lambek 证明）"),
             dict(say="入门篇那句仍在：道生一，三生万物；折叠则是万物各归其根。构造往外长，cata 往回收。生与归，合在一处。",
                  note="书法：各复归其根"),
         ]),

    dict(id="S4Ana", title="四 · 展开 ana（浅提）", quote="", chapter="",
         refs=["DaoFP ch.12 Coalgebras（Anamorphisms——直觉层）；CTFP 3.8 Coalgebras"],
         beats=[
             dict(say="方向一翻，故事就变了。折叠是消费结构；展开是生成结构。范畴论里对应的是 anamorphism，简称 ana——跟 cata 对偶。今天只浅提，不深挖余代数。",
                  note="fold ← ⟷ → unfold；cata ⟷ ana"),
             dict(say="消费像拆快递：打开一层，处理里头的东西，再对剩下的箱子做同样的事。生成像种树：看着手里的种子，决定「现在结一个果，还剩下一颗更小的种子」，直到种子耗尽。",
                  note="拆箱 / 种树 对照"),
             dict(say="比如从数字 n 展开：若 n 是零就停止；否则结出 n，留下 n 减一。于是五、四、三、二、一，整条链就长出来了。种子在左手，列表在右手。",
                  note="动画：5 → 5:4:3:2:1:[]"),
             dict(say="有了展开，有了折叠，就能接起来：先展开，再折叠。中间那条列表被生出，又立刻被消费。先生，而后归——有人叫它 hylo，合态射。今天只点到这里，知道方向即可。",
                  note="种子 ─ana→ 列表 ─cata→ 结果；hylo 浅提"),
             dict(say="反者道之动：同一套结构，箭头一翻，消费变成生成。对偶不是修辞，是一种省力的思考方式——每学会一个方向，就白得相反的那个。折与展，是一对。",
                  note="小字：fold ⟷ unfold · 反者道之动"),
         ]),

    dict(id="S5Haskell", title="五 · 落到代码", quote="", chapter="",
         refs=["DaoFP ch.11–12；CTFP 3.8"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。先手写列表，再写出 foldr 风格的求和与求积——同一形状，两套代数。类型写在前，递归藏在匹配里。",
                  note="代码块：s_cata"),
             dict(say="sumList 遇到 Nil 回零，遇到 Cons 头加尾；productList 空是一，非空是乘法。你只说清一步，递归走完全程——cata 的手写版。",
                  note="高亮 sumList / productList"),
             dict(say="再用标准库的 foldr 写一遍乘积，对照看出：手写递归与 foldr，说的是同一件事——cata 的两种写法。一个显式，一个浓缩。",
                  note="代码 s_foldr；foldProduct = foldr (*) 1"),
             dict(say="展开这边：countdown 用 unfoldr，种子为零则停，否则结出当前数、留下减一。从五展开，得到五到一。ana 的日常面目。",
                  note="代码 s_ana；5 → [5,4,3,2,1]"),
             dict(say="接上折叠：fact 先 countdown 再 foldProduct，就是十的阶乘。愿意的话，两步合成一步，中间列表不落地——hylo 直觉。屏幕代码都能编译。",
                  note="fact / factHylo；3628800"),
             dict(say="图对齐了，代码只是把图念出来。更深的 Fix、Lambek，留给以后；今天只把直觉钉牢。看构造，再看折叠。",
                  note="对照：图 ⟷ 代码；不引入 Fix"),
         ]),

    dict(id="S6Next", title="结 · 各复归其根", quote="", chapter="",
         refs=["DaoFP / CTFP Functor；下一集函子"],
         beats=[
             dict(say="今天钉牢三件事：构造子合起来是代数；沿着代数往回折是 cata，也就是 fold；方向一翻，ana 从种子长出结构。生与归，都从构造子出发。",
                  note="三句回顾环绕圆相"),
             dict(say="下一集，我们把「形状」本身提出来：Functor——在结构上描画箭头，而不拆掉结构。映射，是折叠之前的那一层薄纱。fmap 会登场。",
                  note="预告：Functor · fmap；小字「深讲 05」"),
             dict(say="借 Milewski 的提醒：先看构造，再看折叠。各复归其根。我们下集见。",
                  tts="借米列夫斯基的提醒：先看构造，再看折叠。各复归其根。我们下集见。",
                  note="「各复归其根」书法；印章；谢谢观看"),
         ]),
]
