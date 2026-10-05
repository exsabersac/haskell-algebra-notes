# -*- coding: utf-8 -*-
"""Single source of truth for narration — 深讲第 6 集：Monad 与 do 记法。

Audience: knows some programming; Haskell optional.
Last beginner deep-dive. CT first, then short Haskell.
Points to advanced series: fixed points, adjunctions, Yoneda.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Functor", "Functor"),
    ("Monad", "Monad"),
    ("Maybe", "Maybe"),
    ("Nothing", "Nothing"),
    ("Just", "Just"),
    ("List", "List"),
    ("Kleisli", "克莱斯利"),
    ("Yoneda", "米田"),
    ("fmap", "f map"),
    ("bind", "bind"),
    ("return", "return"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="Monad 与 do 记法", quote="", chapter="", refs=[],
         beats=[
             dict(say="道生一。欢迎来到「道可道」深讲第六集——也是入门深讲的最后一集。",
                  note="宣纸背景，圆相一笔画出；标题「Monad 与 do 记法」浮现"),
             dict(say="上一集钉牢函子：保形、抬箭头。这一集，在函子之上接「效应」——把一步一步的计算，串成一条能失败、能分支的链。函子管形状；Monad 管「下一步怎么走」。",
                  note="小字：深讲 05 → 06；提纲 bind / 定律 / do"),
             dict(say="范畴论里，这叫 Monad：有注入，有绑定；还有鱼子复合。先把话说明白，再落到几行 Haskell，以及 do 记法。",
                  note="三行：bind · 定律 · do"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第十五章，以及《程序员的范畴论》里 Monad 那几节。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第十五章，以及《程序员的范畴论》里 Monad 那几节。片中表述都是释义，不是照录。",
                  note="DaoFP ch.15 · CTFP 3.4–3.6；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道生一", quote="道生一。", chapter="《道德经》第四十二章",
         refs=["DaoFP ch.15 Monads（效应链）",
               "CTFP 3.4–3.5 Monads / Kleisli"],
         beats=[
             dict(say="道生一。", note="竖排书法原文，右起"),
             dict(say="入门篇扫过 Monad；深讲第五集刚把函子钉牢。这一集，我们把「效应如何串联」单独拉开。函子改内容；Monad 还要决定下一步往哪走。映射是一层；串联，是另一层。",
                  note="小字：入门篇 → 深讲 06；效应串联"),
             dict(say="先问范畴论的问题：手里有一块带着效应的值，和下一步「吃纯值、交回效应」的箭头——能不能接成更长的一条？能，就叫它 Monad。",
                  note="效应值 + 下一步 → 更长的链"),
             dict(say="Milewski 的画面：函子是外套；Monad 还多一枚钮扣——能把「外套里的外套」解开一层，接到下一段旅程。",
                  tts="米列夫斯基的画面：函子是外套；Monad 还多一枚钮扣——能把「外套里的外套」解开一层，接到下一段旅程。",
                  note="小字：join / bind · 道生一"),
             dict(say="慢一点。先把 bind 与鱼子看明白；后面的定律与 do，都站在它们上面。一生二，二生三——链，就这样长出来。",
                  note="书法小字：绑定"),
         ]),

    dict(id="S2Bind", title="二 · bind 与鱼子", quote="", chapter="",
         refs=["DaoFP ch.15 bind / Kleisli；CTFP 3.4 fish operator"],
         beats=[
             dict(say="Monad 先做两件事。第一，注入：把一个纯值 a，放进效应壳，得到 m a。Haskell 里常叫 return，也叫 pure。",
                  note="return :: a → m a"),
             dict(say="第二，绑定 bind：手里有一块 m a，和一条「从 a 交回 m b」的箭头。bind 把它们接起来，交出 m b。效应不拆掉，只往前走。",
                  note="(>>=) :: m a → (a → m b) → m b"),
             dict(say="对照函子：fmap 吃的是「纯箭头」a 到 b；bind 吃的是「带效应的箭头」a 到 m b。多出来的那一层效应，正是链式的关键。",
                  note="fmap vs bind"),
             dict(say="把两条带效应的箭头首尾相接，就得到鱼子运算符：大于等于大于。先跑 f，再把结果交给 g。这是克莱斯利范畴里的复合。",
                  tts="把两条带效应的箭头首尾相接，就得到鱼子运算符：大于等于大于。先跑 f，再把结果交给 g。这是克莱斯利范畴里的复合。",
                  note="(>=>) 鱼子 / Kleisli"),
             dict(say="日常比喻：函子是换衬衫；Monad 是「按说明书走下一步」——说明书本身也可能失败，也可能分出多条岔路。失败走 Maybe；分岔走列表。同一接口，两种脾气。",
                  note="下一步可能失败 / 分支"),
             dict(say="所以 Monad 不是「再写一个 map」。它是：在效应的形状上，把计算接成链。形状仍先于操作——只是形状里，多了「如何继续」的记忆。",
                  note="效应上的链式复合"),
         ]),

    dict(id="S3Laws", title="三 · 定律浅讲", quote="", chapter="",
         refs=["DaoFP ch.15 monad laws；CTFP 3.5–3.6"],
         beats=[
             dict(say="Monad 不止要有 return 与 bind，还要守三条定律。定律写不进类型，却写进责任：左单位、右单位、结合律。",
                  note="三条定律：左单位 · 右单位 · 结合"),
             dict(say="左单位：return 一个值，再 bind 上 f，必须等于直接对那个值施 f。注入不能偷偷加料。",
                  note="return a >>= f  =  f a"),
             dict(say="右单位：一块效应值 bind 上 return，必须原样回来。结尾不能无故拆掉或加厚外壳。",
                  note="m >>= return  =  m"),
             dict(say="结合律：先 bind f 再 bind g，必须等于一次 bind「f 鱼子 g」。链式怎么加括号，结果一样——结合，才叫一条道。括号可以挪，终点不许偷偷改。",
                  note="(m >>= f) >>= g  =  m >>= (f >=> g)"),
             dict(say="为什么要定律？没有它们，bind 只是同名函数——可以乱序、吞步骤、把失败变成成功。有了定律，效应链才可组合、可替换。",
                  note="无定律 = 不合法 Monad"),
             dict(say="道生一：单位是「生」的干净起点；结合是「生」可以一直生下去。条文三条，分量不轻。今天只浅讲，进阶篇还会从伴随回头看。",
                  note="书法：道生一"),
         ]),

    dict(id="S4Do", title="四 · do 记法", quote="", chapter="",
         refs=["DaoFP ch.15 do-notation；CTFP 3.4"],
         beats=[
             dict(say="链式 bind 写多了，尖括号会淹过人话。Haskell 给了一层语法糖：do 记法——看起来像顺序语句，语义仍是 bind。糖熔掉，底下还是那条链。",
                  note="do = >>= 的语法糖"),
             dict(say="箭头左边的名字，是从效应壳里取出的纯值；下一行可以继续用。最后一行往往是 return，或另一块效应。",
                  note="x <- mx  ·  return …"),
             dict(say="重要提醒：do 不引入新语义。它不会让纯函数突然有副作用；它只是把已有的 Monad 实例，写得更像人话。",
                  note="无新语义 · 可读性"),
             dict(say="看到 do，心里应还原成 bind 链；看到 bind，也可以写成 do。两种字体，同一条道。考试也好，阅读也好，都要能来回翻译。",
                  note="do ⟷ >>="),
             dict(say="还有一行只有效应、不绑名字的写法，对应小小的双大于号——先做前一步，丢掉它的纯值，只保留效应顺序。今天点到为止。",
                  note=">> 顺序 · 浅提"),
             dict(say="do 是入门的梯子，不是终点。梯子稳了，再去看变换器、IO、解析器——都还是同一套 return 与 bind。",
                  note="梯子 · 同一套接口"),
         ]),

    dict(id="S5Haskell", title="五 · Maybe 与 List", quote="", chapter="",
         refs=["DaoFP ch.15 Maybe / List monads；CTFP 3.4–3.5"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。先声明 Monad 类型类，再写鱼子，再写 Maybe 与列表的实例。类型写在前，匹配藏在里头。图怎么说，代码就怎么应。",
                  note="代码块：s_class / s_fish"),
             dict(say="Maybe 的 bind：遇到 Nothing 整条链停；遇到 Just，把里头的值交给下一步。失败会短路——这是效应最直观的一种。",
                  note="代码 s_maybe；高亮 instance"),
             dict(say="列表的 bind：对每个元素展开下一步，再拼平。一变多、多再变多——不确定计算，或者「搜索所有可能」。",
                  note="代码 s_list；nondeterminism"),
             dict(say="试一下：Just 二十，加一，再乘二，得到 Just 四十二；列表一对二，每个再分出自身与十倍，得到一、十、二、二十。",
                  note="demoMaybe / demoList"),
             dict(say="同一条链，用 do 再写一遍：名字一行行绑下来，最后 return。结果与尖括号版相同——糖，熔掉还是糖。",
                  note="代码 s_do"),
             dict(say="再抽查定律：左单位、右单位、结合，屏幕代码都能编译。图对齐了，代码只是把图念出来。",
                  note="三条定律抽检"),
         ]),

    dict(id="S6Next", title="结 · 道生一", quote="", chapter="",
         refs=["进阶篇预告：不动点 · 伴随 · 米田"],
         beats=[
             dict(say="今天钉牢四件事：bind 把效应接成链；鱼子是克莱斯利复合；三条定律写成契约；do 是人话写法。入门深讲六集，从类型到函子再到效应，到此收束。",
                  note="四句回顾环绕圆相"),
             dict(say="下一阶段，进入进阶篇：不动点——折叠与生成的不动点；伴随——左右两侧的最优翻译；米田——对象被它出发的箭头所认识。深讲是底，进阶往上长。三条线，各自成章。",
                  tts="下一阶段，进入进阶篇：不动点——折叠与生成的不动点；伴随——左右两侧的最优翻译；米田——对象被它出发的箭头所认识。深讲是底，进阶往上长。三条线，各自成章。",
                  note="预告：不动点 · 伴随 · 米田"),
             dict(say="借 Milewski 的提醒：先看形状，再看映射，再看效应如何串联。道生一。我们进阶篇见。",
                  tts="借米列夫斯基的提醒：先看形状，再看映射，再看效应如何串联。道生一。我们进阶篇见。",
                  note="「道生一」书法；印章；谢谢观看"),
         ]),
]
