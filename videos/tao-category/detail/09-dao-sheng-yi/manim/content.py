# -*- coding: utf-8 -*-
"""Single source of truth for narration — 进阶深讲第 9 集：道生一.

Audience: finished beginner 01–06 and advanced 07–08.
Deeper than beginner ep03 (Maybe/List counting) and ep04 (fold intuition, "no Lambek today"):
F-algebras and their category, initial algebra = catamorphism, Lambek's lemma, Fix, Adámek colimit, Church Mu.
CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Adámek", "阿达梅克"),
    ("DaoFP", "道 F P"),
    ("CTFP", "C T F P"),
    ("unFix", "un Fix"),
    ("fmap", "f map"),
    ("ExprF", "Expr F"),
    ("ListF", "List F"),
    ("μF", "缪 F"),
    ("Mu", "缪"),
    ("ι", "约塔"),
    ("α", "阿尔法"),
    ("β", "贝塔"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="道生一", quote="", chapter="", refs=[],
         beats=[
             dict(say="道生一。欢迎来到「道可道」进阶深讲——第九集。",
                  note="宣纸背景，圆相一笔画出；标题「道生一」浮现"),
             dict(say="上一集立起了始对象：从它出发，到谁都恰有一支箭头。今天把同一句话搬进另一个范畴——F-代数的范畴。那里的始对象，就是「一」：初始代数。",
                  note="小字：进阶 08 → 09；始对象 → 初始代数"),
             dict(say="本集四根钉子：代数与同态；初始代数与 cata；兰贝克引理与不动点；从无出发的余极限。入门三、四集给了直觉；今天把定理写正式。",
                  note="四行提纲"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第七章递归与第十一章代数，以及《程序员的范畴论》F-代数那一节。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第七章递归与第十一章代数，以及《程序员的范畴论》F 代数那一节。片中表述都是释义，不是照录。",
                  note="DaoFP ch.7 / ch.11 · CTFP 3.8；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道德经钩子", quote="道生一，一生二，二生三，三生万物。", chapter="《道德经》第四十二章",
         refs=["DaoFP ch.7 Recursion（以此句开篇）", "DaoFP ch.11 Algebras"],
         beats=[
             dict(say="道生一，一生二，二生三，三生万物。", note="竖排书法原文，右起"),
             dict(say="《函数式编程之道》讲递归的那一章，就以这句话开篇。入门篇把它读成计数：Maybe 套在 Void 上，一层、两层、三层。那是现象。",
                  note="入门 03：计数是现象"),
             dict(say="进阶篇要问背后的结构：为什么一层层套下去，会停在一个确定的类型上？为什么从这个类型出发，折叠恰好只有一种？",
                  note="两个问题：为何收敛 · 为何唯一"),
             dict(say="答案是一个普遍性质。递归类型不是被「写出来」的，而是被刻画出来的：它是一类代数里的始对象。刻画一旦成立，递归、折叠、同构，全都跟着来。",
                  note="递归类型 = 代数范畴的始对象"),
             dict(say="Milewski 把问题拆成两半：递归的机关，和可插拔的零件。零件是一个函子，机关只写一次。今天就把这台机关拆开看。",
                  tts="米列夫斯基把问题拆成两半：递归的机关，和可插拔的零件。零件是一个函子，机关只写一次。今天就把这台机关拆开看。",
                  note="递归机关 ‖ 可插拔零件"),
         ]),

    dict(id="S2Algebras", title="二 · 代数与同态", quote="", chapter="",
         refs=["DaoFP ch.11 Algebras from Endofunctors；Category of Algebras", "CTFP 3.8 F-Algebras"],
         beats=[
             dict(say="先定零件。一个自函子 F，描述「一层」形状，用洞标出子结构该放的位置。比如表达式：要么是一个整数叶子，要么是一个加号，下面挂两个洞。",
                  note="ExprF x = ValF Int | PlusF x x"),
             dict(say="F-代数是一对东西：一个载体 a，和一支结构映射 α，从 F a 到 a。读法是：假设洞里已经装好了算完的结果，这一步怎么收尾。",
                  note="(a, α : F a → a)"),
             dict(say="同一个形状可以有许多代数。载体取整数，加号就做加法——这是求值。载体取字符串，加号就做拼接——这是打印。不评判哪一个更合理；每一种选择都是一份代数。",
                  note="eval : F Int → Int；pretty : F String → String"),
             dict(say="代数之间的箭头，叫代数同态：载体之间的一支 f，要和两边的结构映射交换。先在 F 层用 F f 搬运，再用 β 收尾；或者先用 α 收尾，再用 f 搬运——两条路必须相等。",
                  note="交换方块：f ∘ α = β ∘ F f"),
             dict(say="函子保持恒等与复合，所以恒等是同态，方块可以拼接。代数和同态组成一个范畴。条件很苛刻：show 就不是从求值到打印的同态。",
                  note="Alg(F) 是范畴；show 不交换"),
         ]),

    dict(id="S3Initial", title="三 · 初始代数与 cata", quote="", chapter="",
         refs=["DaoFP ch.11 Initial algebra；Catamorphisms", "CTFP 3.8"],
         beats=[
             dict(say="现在把上一集的定义原样搬过来。代数范畴里的始对象，叫初始代数，记作 i 和 ι：对任意代数 a 和 α，从它出发的同态存在且唯一。",
                  note="(i, ι)：∀(a, α) ∃! 同态"),
             dict(say="这支唯一的同态，就叫 catamorphism，简称 cata，有时写成香蕉括号包住 α。入门第四集说「cata 就是 fold」；现在知道它的身份：初始对象的唯一出射。",
                  note="⦇α⦈ = cata α；虚线 ∃!"),
             dict(say="存在给你算法：任选一份代数，就有一条折法。唯一给你证明原则：两个函数只要都满足同一个方块，它们就相等。不用归纳，不用逐项比较。",
                  note="存在 = 算法 · 唯一 = 证明原则"),
             dict(say="取 F 为 Maybe。一份 Maybe 代数，等于两样东西：Nothing 对应的起点，和 Just 对应的一步。初始代数的 cata，正是自然数的递归子——给起点、给一步，路就定了。",
                  note="Maybe a → a ≅ (a, a → a)；Nat 递归子"),
             dict(say="取列表的形状函子 ListF：代数等于空表的起点，加上「头与已折尾」的一步。cata 就是 foldr。所有递归类型的折叠，都是同一个定理的特例。",
                  note="ListF e：cata = foldr"),
         ]),

    dict(id="S4Lambek", title="四 · 兰贝克引理", quote="", chapter="",
         refs=["DaoFP ch.11 Lambek's Lemma and Fixed Points", "CTFP 3.8"],
         beats=[
             dict(say="兰贝克引理：初始代数的结构映射 ι，一定是同构。F i 与 i，是同一个东西。",
                  note="ι : F i ≅ i"),
             dict(say="证明只靠一个观察：代数是自相似的。把 F 再作用一次，F i 配上 F ι，又是一份代数。由初始性，存在唯一同态 h，从 i 到 F i。",
                  note="代数 (F i, F ι)；∃! h : i → F i"),
             dict(say="把 h 的方块和一个显然交换的方块拼在一起：ι 复合 h，就是从初始代数到它自己的同态。可恒等也是这样的同态。唯一性一锤定音：ι 复合 h，等于恒等。",
                  note="拼接方块；ι ∘ h = id"),
             dict(say="再读 h 的方块：h 复合 ι，等于 F ι 复合 F h，也就是 F 作用在「ι 复合 h」上——恒等被 F 送到恒等。所以 h 就是 ι 的逆。",
                  note="h ∘ ι = F(ι ∘ h) = id"),
             dict(say="所以 i 是 F 的不动点：再作用一次 F，它不变。而且它是最小的那个——因为任何不动点本身也是一份代数，初始代数到它总有一支箭头。记作 μF。",
                  note="i = μF（最小不动点）"),
             dict(say="《道德经》说，道法自然。「自然」二字的本义，是自己如此。初始代数正是这样：它不靠外物定义，展开一层，还是它自己。",
                  note="书法：道法自然 = 自己如此"),
         ]),

    dict(id="S5Fix", title="五 · Fix 与 cata 的来历", quote="", chapter="",
         refs=["DaoFP ch.11 Fixed point in Haskell；Catamorphisms", "CTFP 3.8"],
         beats=[
             dict(say="Haskell 直接写出这个不动点：Fix f。构造子 Fix，从 F 作用在 Fix f 上，收成 Fix f——它就是结构映射 ι。unFix 剥掉一层——它就是兰贝克给出的逆。",
                  note="Fix = ι；unFix = ι⁻¹"),
             dict(say="现在 cata 的定义不再是凭空背下来的。把 cata 的方块里朝上的 ι 换成 unFix：先剥一层，再用 fmap 把 cata 递归地伸进每个洞，最后用代数收尾。沿着箭头读一遍，就是定义。",
                  note="cata α = α ∘ fmap (cata α) ∘ unFix"),
             dict(say="这一刀切得很干净：递归全部关在 Fix 和 cata 里，只写一次。使用者只提供两样不递归的东西——形状函子，和一份代数。复杂的问题，拆成了简单的零件。",
                  note="递归只写一次；用户给 F 与 α"),
             dict(say="一句诚实的附注。在集合范畴里，Fix 对应最小不动点 μF。Haskell 是惰性的，Fix 还能装下无穷的值，最小与最大不动点在那里重合——最大不动点，是下一集的故事。",
                  note="Set：Fix = μF；Hask：惰性 → 亦含无穷值（νF 下集）"),
             dict(say="另外，Fix 对任何类型构造子都能写，但要真正从无生出东西，形状里必须有不依赖洞的「叶子」。没有叶子，就没有起点。",
                  note="需要叶子：Nothing / NilF / ValF"),
         ]),

    dict(id="S6Colimit", title="六 · 从无出发：余极限", quote="", chapter="",
         refs=["DaoFP ch.11 Initial Algebra as a Colimit；Initial Algebra from Universality"],
         beats=[
             dict(say="初始代数从哪里来？从无出发。把 F 作用在始对象零上：零里什么也没有，所以 F 零里只剩叶子。再作用一次，叶子可以挂进节点；再一次，树更高一层。",
                  note="0 → F0 → F²0 → F³0 → ⋯"),
             dict(say="这些对象排成一条链，箭头是始对象的唯一出射，被 F 一层层抬上去。链的余极限，把所有有限阶段粘在一起。",
                  note="ω-链；箭头 !, F!, F²!"),
             dict(say="这是 Adámek 定理：只要 F 保持这种链的余极限，链的余极限就是初始代数。多项式函子在集合范畴里都满足；Maybe 和 ListF 都在其中。无穷加一，还是无穷。",
                  note="Adámek：F 保持 ω-余极限 ⇒ colim = μF"),
             dict(say="取 F 为 Maybe：零、一、二、三，链的余极限就是自然数。取列表：一、加 a、加 a 乘 a，一直加下去——Milewski 戏称的几何级数，在这里有了严格的意义。",
                  note="Nat；L = 1 + a + a² + ⋯"),
             dict(say="还有另一种看法：一个初始代数的值，等价于它对所有代数的折法。对一切载体 a，给我一份代数，我就交出一个 a。这就是 Church 编码，Mu f。「一」，是全部归途的总和。",
                  note="Mu f = ∀a. (F a → a) → a"),
         ]),

    dict(id="S7Haskell", title="七 · 短 Haskell", quote="", chapter="",
         refs=["DaoFP ch.11；CTFP 3.8；本集 haskell/src/DaoShengYi.hs"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。Fix、Algebra、cata，三行就是全部机关；最后一行，是沿着方块读出来的定义。",
                  note="代码 s_fix"),
             dict(say="零件：ExprF 是一层表达式的形状。eval 和 pretty 是同一形状上的两份代数。cata eval 把 e9 折成九；cata pretty 折成「二加三加四」。",
                  note="代码 s_expr / s_algs"),
             dict(say="兰贝克引理也能写成代码：把 fmap Fix 当作代数——这正是提升后的 F ι——它的 cata 就是那支 h。可以检验，它和 unFix 一模一样。",
                  note="代码 s_lambek"),
             dict(say="自然数是 Maybe 的不动点；toInt 用 maybe 零 加一 作代数。Mu 把值存成「全部折法」：fromMu 只需把 Fix 本身当作代数交进去。",
                  note="代码 s_nat / s_mu"),
             dict(say="跑一下：e9 求值得九，打印得二加三加四；兰贝克检验为真；三个后继得三；一到十的 Mu 列表求和，五十五。图怎么说，代码就怎么应。",
                  note="demo 输出"),
         ]),

    dict(id="S8Next", title="结 · 下集反者道之动", quote="", chapter="",
         refs=["下集预告：反者道之动 · 余代数与 ana"],
         beats=[
             dict(say="今天钉牢四件事：代数与同态组成范畴；初始代数的唯一出射就是 cata；兰贝克说结构映射是同构，所以它是最小不动点；Adámek 说，它是从无出发那条链的余极限。",
                  note="四句回顾环绕圆相"),
             dict(say="下一集《反者道之动》：把箭头全部掉头。代数变余代数，始对象变终对象，cata 变 ana——从种子展开出无穷的结构，最大不动点登场。",
                  note="预告：余代数 · ana · νF"),
             dict(say="借 Milewski 的提醒：机关只写一次，零件随你插。道生一。进阶篇，我们下集见。",
                  tts="借米列夫斯基的提醒：机关只写一次，零件随你插。道生一。进阶篇，我们下集见。",
                  note="「道生一」书法；印章；谢谢观看"),
         ]),
]
