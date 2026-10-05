# -*- coding: utf-8 -*-
"""Single source of truth for narration — 进阶深讲第 11 集：知其雄，守其雌.

Audience: finished beginner 01–06 and advanced 07–10.
Adjunctions as natural hom-set isomorphisms; unit/counit + triangle identities;
every adjunction L ⊣ R gives a monad R∘L (μ = RεL) and a comonad L∘R (δ = LηR);
currying adjunction (−, s) ⊣ (s → −)  ⇒  State / Store; lens = Store coalgebra.
CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("DaoFP", "道 F P"),
    ("CTFP", "C T F P"),
    ("Kleisli", "克莱斯利"),
    ("Eilenberg–Moore", "艾伦伯格-摩尔"),
    ("runState", "run State"),
    ("fmap", "f map"),
    ("hom", "Hom"),
    ("R∘L", "R 复合 L"),
    ("L∘R", "L 复合 R"),
    ("s′", "s 撇"),
    ("η", "伊塔"),
    ("ε", "艾普西隆"),
    ("μ", "缪"),
    ("δ", "德尔塔"),
    ("_1", "下划线一"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="知其雄，守其雌", quote="", chapter="", refs=[],
         beats=[
             dict(say="知其雄，守其雌。欢迎来到「道可道」进阶深讲——第十一集。",
                  note="宣纸背景，圆相一笔画出；标题「知其雄，守其雌」浮现"),
             dict(say="前两集一生一归：初始代数与 cata，终余代数与 ana。今天换一种普遍性：不在一个对象上，而在两个方向相反的函子之间。它叫伴随。",
                  note="小字：进阶 10 → 11；对象的普遍性 → 函子之间的伴随"),
             dict(say="本集四根钉子：伴随是 hom 集之间的自然同构；单位、余单位与三角恒等式；R∘L 生出单子，柯里化给出 State；L∘R 生出余单子，柯里化给出 Store，顺带认出 lens。",
                  note="四行提纲"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》与《程序员的范畴论》里伴随、单子、余单子各章。片中都是释义，不是照录。印章「知白守黑」，恰好出自同一章。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》与《程序员的范畴论》里伴随、单子、余单子各章。片中都是释义，不是照录。印章「知白守黑」，恰好出自同一章。",
                  note="DaoFP ch.10 / 16 / 17 · CTFP 3.2 / 3.6 / 3.7；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道德经钩子", quote="知其雄，守其雌，为天下溪。", chapter="《道德经》第二十八章",
         refs=["DaoFP ch.10 Adjunctions", "CTFP 3.2 Adjunctions"],
         beats=[
             dict(say="知其雄，守其雌，为天下溪。", note="竖排书法原文，右起"),
             dict(say="雄与雌，不是两样东西争高下，而是同一条溪的两岸：一岸向外流，一岸向内收。伴随正是这样：两个方向相反的函子，谁也不是谁的逆，却彼此知道得清清楚楚。",
                  note="两岸 · 一溪；L 与 R 方向相反"),
             dict(say="同构：来回一圈，回到原处。等价：回到一个与原处同构的地方。伴随更松：回不到原处，只留下两支见证箭头——单位与余单位。Milewski 称之为「半个等价」。",
                  tts="同构：来回一圈，回到原处。等价：回到一个与原处同构的地方。伴随更松：回不到原处，只留下两支见证箭头——单位与余单位。米列夫斯基称之为「半个等价」。",
                  note="同构 = · 等价 ≅ · 伴随 η / ε"),
             dict(say="伴随无处不在。和与积，都是对角函子的伴随；极限与余极限也是；自由与遗忘也是。一旦认出 hom 集之间的这种同构，你会发现它到处冒头。",
                  note="+ ⊣ Δ ⊣ ×；colim ⊣ Δ ⊣ lim；Free ⊣ U"),
             dict(say="今天只抓最朴素的一对：与 s 配对，以及从 s 出发的函数。每个 Haskell 程序员天天在用它，只是叫它 curry。从这一对里，会流出 State 与 Store 两条支流。",
                  note="(−, s) ⊣ (s → −) ⇒ State · Store"),
         ]),

    dict(id="S2Adjunction", title="二 · 伴随：hom 集的同构", quote="", chapter="",
         refs=["DaoFP ch.10 Adjunction between functors；The Currying Adjunction", "CTFP 3.2 Adjunctions"],
         beats=[
             dict(say="定义。两个范畴 C 与 D：左函子 L 从 D 到 C，右函子 R 从 C 到 D。伴随 L ⊣ R 说：从 L x 出发到 y 的箭头，与从 x 出发到 R y 的箭头，一一对应。",
                  tts="定义。两个范畴 C 与 D：左函子 L 从 D 到 C，右函子 R 从 C 到 D。伴随 L 左伴随于 R，是说：从 L x 出发到 y 的箭头，与从 x 出发到 R y 的箭头，一一对应。",
                  note="C(L x, y) ≅ D(x, R y)；L ⊣ R"),
             dict(say="这一族双射，要对 x 和 y 都自然。比如对 y 自然：在左边先用 f 后复合、再转置，和先转置、再用 R f 后复合，结果一样。对应的两支箭头，互称转置。",
                  note="自然性方块：φ(f ∘ g) = R f ∘ φ(g)"),
             dict(say="读法很重要：左边是映出——从 L x 出去；右边是映入——进入 R y。左伴随擅长映出，右伴随擅长映入。所以左伴随保持余极限，右伴随保持极限。",
                  note="映出 / 映入；L 保余极限 · R 保极限"),
             dict(say="最经典的例子是指数。从 e 与 a 之积到 b 的箭头，对应从 e 到 b 的 a 次方的箭头。左函子是乘以 a，右函子是取 a 次方。对所有 a 都有这对伴随的范畴，叫笛卡尔闭范畴。",
                  note="C(e × a, b) ≅ C(e, bᵃ)；(− × a) ⊣ (−)ᵃ；CCC"),
             dict(say="到了 Haskell，把 a 改名为 s：从 a 与 s 的配对到 b 的函数，等同于从 a 到「从 s 到 b」的函数。两个方向，正是 curry 与 uncurry。左伴随是与 s 配对，右伴随是从 s 出发的函数。",
                  note="((a, s) → b) ≅ (a → s → b)；(,) s ⊣ (->) s"),
         ]),

    dict(id="S3UnitCounit", title="三 · 单位、余单位与三角", quote="", chapter="",
         refs=["DaoFP ch.10 Unit and Counit of an Adjunction；Triangle identities", "CTFP 3.2 Adjunction and Unit/Counit Pair"],
         beats=[
             dict(say="伴随还有第二张面孔。在同构里把 y 取成 L x，左边有一支现成的箭头：恒等。它的转置，是从 x 到 R L x 的箭头，叫单位 η。拿恒等去换——这是米田式的老技巧。",
                  note="η_x = φ(id_{Lx}) : x → R(L x)"),
             dict(say="对偶地，把 x 取成 R y，右边的恒等转置回来，是从 L R y 到 y 的箭头，叫余单位 ε。η 是从恒等函子到 R∘L 的自然变换；ε 是从 L∘R 到恒等函子的自然变换。",
                  note="ε_y = φ⁻¹(id_{Ry})；η : Id → R∘L；ε : L∘R → Id"),
             dict(say="它们满足三角恒等式：对 L，先用 η 插入一对 R L，再用 ε 消去一对 L R，等于什么都没做；对 R 也一样。插入再消去，归于无为。",
                  note="(εL)·(Lη) = id_L；(Rε)·(ηR) = id_R"),
             dict(say="反过来，有了 η、ε 和三角恒等式，就能还原同构：从 x 到 R y 的 f，先用 L 抬升，再用 ε 收尾；另一方向，用 R 抬升，前面接上 η。两种定义等价。",
                  note="φ⁻¹ f = ε ∘ L f；φ g = R g ∘ η"),
             dict(say="落到柯里化伴随上：单位是 curry 作用在恒等上，把 a 变成「等一个 s，就配成一对」；余单位是 uncurry 作用在恒等上，也就是求值：手里有函数和一个 s，作用上去。",
                  note="η = curry id；ε = uncurry id = eval"),
         ]),

    dict(id="S4State", title="四 · R∘L：State 单子", quote="", chapter="",
         refs=["DaoFP ch.16 Monads from Adjunctions；The currying adjunction and the state monad", "CTFP 3.6 Monads Categorically"],
         beats=[
             dict(say="现在把两个函子接起来。先走 L 再走 R，得到 D 上的自函子 T，等于 R∘L。关键事实：对任何伴随，T 都是单子。单位就是伴随的单位 η；乘法 μ，是把余单位夹在中间：R ε L。",
                  note="T = R∘L；η；μ = R ε L : RLRL → RL"),
             dict(say="为什么成立？两条单位律，正是两个三角恒等式；结合律，来自 ε 的自然性。Milewski 用弦图画得最清楚：T 的弦拆成并排的 L 与 R，μ 就是中间一对被 ε 收口。",
                  tts="为什么成立？两条单位律，正是两个三角恒等式；结合律，来自艾普西隆的自然性。米列夫斯基用弦图画得最清楚：T 的弦拆成并排的 L 与 R，缪就是中间一对被艾普西隆收口。",
                  note="弦图：L R L R → L R，中间 ε 收口"),
             dict(say="代入柯里化伴随：先配上 s，再变成从 s 出发的函数。R L a，就是从 s 到 a 与 s 之配对的函数——State s a。单位 η 把 a 原样配上当前状态，这正是 State 的 return。",
                  note="R(L a) = s → (a, s) = State s a；return = η"),
             dict(say="join 呢？R ε L 翻译成 Haskell，就是 fmap 余单位：外层拿到状态 s，跑出一个内层 State 和新状态 s′；余单位把内层作用到 s′ 上。这正是 uncurry runState。",
                  note="join = fmap counit；join mma = State (fmap (uncurry runState) (runState mma))"),
             dict(say="多数单子来自离开 Hask 的伴随，比如 List 来自自由幺半群与遗忘函子；柯里化伴随却两边都留在 Hask 里。反过来，每个单子也都能拆成伴随——Kleisli 与 Eilenberg–Moore 是两种拆法，并不唯一。",
                  note="List ⇐ Free ⊣ U；任何单子 = 某个伴随（Kleisli / EM，不唯一）"),
         ]),

    dict(id="S5Store", title="五 · L∘R：Store 余单子", quote="", chapter="",
         refs=["DaoFP ch.17 Comonads from Adjunctions；Costate comonad", "CTFP 3.7 The Store Comonad"],
         beats=[
             dict(say="反过来，先走 R 再走 L，得到 C 上的自函子 W，等于 L∘R。对偶的事实：它是余单子。余单位就是伴随的余单位 ε；余乘法 δ，是把单位夹在中间：L η R。",
                  note="W = L∘R；ε；δ = L η R : LR → LRLR"),
             dict(say="代入柯里化：先变成从 s 出发的函数，再配上一个 s。L R c，就是一个从 s 到 c 的函数，加上一个 s——Store s c。它也叫余状态余单子。",
                  note="L(R c) = (s → c, s) = Store s c；costate comonad"),
             dict(say="读法：那个函数是一整张以 s 为下标的表，那个 s 是当前位置。extract 就是余单位：在当前位置上把表查一下。",
                  note="Store = 全表 + 焦点；extract = ε"),
             dict(say="duplicate 就是 L η R：位置不动，把表的每一格都换成「以那一格为焦点的 Store」。于是得到一张由视角组成的表：每个位置看到的整个世界。",
                  note="duplicate (St f s) = St (St f) s"),
             dict(say="有了 duplicate，就有 extend：把一条只看邻域的局部规则，推到每一个位置。s 取整数，就是一维卷积或元胞自动机——DaoFP 的一一零号规则，CTFP 的生命游戏。惰性只算你真正看的格子。",
                  note="extend k = fmap k ∘ duplicate；rule 110 / 生命游戏"),
         ]),

    dict(id="S6XiongCi", title="六 · 知其雄，守其雌", quote="", chapter="",
         refs=["DaoFP ch.16–17；ch.17 Comonad coalgebras；Lenses", "CTFP 3.6, 3.7"],
         beats=[
             dict(say="把两边并排。State 是雄：主动向外，Kleisli 箭头从 a 到 State s b，产生效果、改写状态。Store 是雌：接纳向内，余 Kleisli 箭头从 Store s a 到 b，守着焦点、消费语境。",
                  note="雄 · State · a → State s b ｜ 雌 · Store · Store s a → b"),
             dict(say="而喂养它们的，是同一对箭头。η 在 State 里是 return，在 Store 里藏在 duplicate 中间；ε 在 Store 里是 extract，在 State 里藏在 join 中间。一对 η 与 ε，两种结构。",
                  note="η / ε × State / Store 对照表"),
             dict(say="知其雄，守其雌，为天下溪。单子与余单子不是两套理论，而是同一条溪流的两岸；那条溪，就是伴随本身。",
                  note="两栏之间一道墨线（溪），标注 L ⊣ R"),
             dict(say="顺带认出一位老朋友。Store 余单子的余代数，是从 s 到 Store a s 的箭头；拆开，就是一对 get 与 set。这就是 lens：s 是整体，a 是焦点。",
                  note="φ : s → Store a s ≅ (get, set)"),
             dict(say="余代数的两条定律翻译过来：把当前焦点原样写回，什么都不变；写进去再读，读到刚写的；连写两次，只留后一次。第十集的余代数又出现了，这次带着定律。",
                  note="set s (get s) = s；get (set s a) = a；set (set s a) a′ = set s a′"),
         ]),

    dict(id="S7Haskell", title="七 · 短 Haskell", quote="", chapter="",
         refs=["DaoFP ch.10 / 16 / 17；CTFP 3.2 / 3.6 / 3.7；本集 haskell/src/XiongCi.hs"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。leftAdjunct 是 curry，rightAdjunct 是 uncurry；unit 是 curry id，counit 是 uncurry id。伴随的四个零件，四行写完。",
                  note="代码 s_adj"),
             dict(say="State 就是 R 套 L。join 只有一行：先跑外层，再用 uncurry runState 把内层作用到新状态上——那就是夹在中间的余单位。",
                  note="代码 s_state"),
             dict(say="Store 就是 L 套 R。extract 是求值；duplicate 让每一格都成为焦点；extend 由它和 fmap 拼成；sum3 是一条只看邻域的规则。",
                  note="代码 s_store"),
             dict(say="lens 是 Store 的余代数。_1 聚焦在配对的第一个分量上；get 和 set，都从这一个函数里读出来。",
                  note="代码 s_lens"),
             dict(say="跑一下：两个三角恒等式在样例上成立；tick 三次，从零数到三；在平方数纸带上做邻域求和；把配对的第一项换成九，三条 lens 定律都为真。代码怎么写，伴随就怎么说。",
                  note="demo 输出"),
         ]),

    dict(id="S8Next", title="结 · 下集无为而无不为", quote="", chapter="",
         refs=["下集预告：无为而无不为 · 米田引理与 Kan 扩张"],
         beats=[
             dict(say="今天钉牢四件事：伴随是 hom 集的自然同构；单位、余单位与三角恒等式是它的第二张面孔；R∘L 给出单子 State；L∘R 给出余单子 Store，lens 是它的余代数。",
                  note="四句回顾环绕圆相"),
             dict(say="下一集《无为而无不为》：米田引理与 Kan 扩张。不碰对象，只看箭头，就能知道一切。",
                  note="预告：米田 · Kan 扩张"),
             dict(say="借 Milewski 的提醒：伴随一旦被认出，就到处都是。知其雄，守其雌。进阶篇，我们下集见。",
                  tts="借米列夫斯基的提醒：伴随一旦被认出，就到处都是。知其雄，守其雌。进阶篇，我们下集见。",
                  note="「知其雄，守其雌」书法；印章；谢谢观看"),
         ]),
]
