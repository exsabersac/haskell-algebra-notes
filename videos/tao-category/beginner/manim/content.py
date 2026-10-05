# -*- coding: utf-8 -*-
"""Single source of truth for narration — BEGINNER episode.

Audience: knows some programming, may know a little Haskell or none.
Slow pace, everyday metaphors, fewer formulas, more intuition.
Same six 道德经 hooks as the advanced episode, with swapped topics.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"), ("fmap", "f map"),
    ("Haskell", "哈斯凯尔"), ("id，", "I D，"), ("id。", "I D。"),
    ("id 是", "I D 是"), ("叫 id", "叫 I D"), ("用 id", "用 I D"),
    ("map id", "map I D"), ("bind", "bind"),
    ("Functor", "函子"), ("Applicative", "Applicative"),
    ("Monad", "单子"), ("hylo", "海罗"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="道可道 · 范畴入门", quote="", chapter="", refs=[],
         beats=[
             dict(say="道可道，非常道。这期视频，用六句《道德经》，带你入门范畴论。",
                  note="宣纸背景，毛笔圆相（ensō）一笔画出；标题书法字浮现"),
             dict(say="不需要提前读过范畴论，也不必先会 Haskell。你会写一点程序——变量、函数、列表——就够了。屏幕上的代码，我们会一行一行念。",
                  note="六个章节名竖排列出，逐一淡入；标注「入门」"),
             dict(say="每一段都是同样的节奏：先读一句老子，再用日常比喻讲清楚，最后落到几行代码。老子是钩子，直觉是正文。",
                  note="节奏示意：原文 → 比喻 → 代码"),
             dict(say="框架上，我们会不断回到 Bartosz Milewski 的两本书：《程序员的范畴论》和《函数式编程之道》。更深入的一集——不动点、伴随、米田——留给进阶篇。",
                  tts="框架上，我们会不断回到巴托什·米列夫斯基的两本书：《程序员的范畴论》和《函数式编程之道》。更深入的一集——不动点、伴随、米田——留给进阶篇。",
                  note="两本书名 CTFP / DaoFP；朱红印章「知白守黑」；小字「进阶篇另见」"),
         ]),

    dict(id="S1Compose", title="一 · 道可道", quote="道可道，非常道；名可名，非常名。", chapter="《道德经》第一章",
         refs=["DaoFP ch.1 Clean Slate（Types and Functions）", "DaoFP ch.2 Composition（Identity）",
               "CTFP 1.1 Category: The Essence of Composition", "CTFP 1.2 Types and Functions"],
         beats=[
             dict(say="道可道，非常道；名可名，非常名。", note="竖排书法原文，右起"),
             dict(say="先忘掉抽象。想象一张地图：城市是点，公路是箭头。范畴论就是这样看世界的：对象是点，箭头是从一点到另一点的路。",
                  note="左「对象 = 点」右「箭头 = 路」；简单两点一箭头图"),
             dict(say="在程序里，类型就是对象：整数、字符串、布尔。函数就是箭头：把一种类型变成另一种。整数变成字符串，字符串变成整数——都是箭头。",
                  note="Int、String、Bool 三个圆点；箭头 toString、length"),
             dict(say="两段路可以接起来。先走 f，再走 g，合起来就是 g 圆点 f。这叫复合。注意顺序：先写的 g 其实后走——像管道，从右往左读。",
                  note="三点 A→B→C；标注 g ∘ f"),
             dict(say="复合有个规矩：三段路，先接左边再接右边，和先接右边再接左边，结果一样。这叫结合律。你不必加括号去想先算谁。",
                  note="结合律：(h∘g)∘f = h∘(g∘f)"),
             dict(say="每个城市还有一条什么也不做的环路：从自己回到自己。这叫恒等箭头，Haskell 里写作 id。它是复合的单位：跟谁接，都不改变对方。",
                  note="自环 id；代码 identity / compose"),
             dict(say="举个例子：toString 把整数变成字符串，strlen 量字符串长度。把它们接起来，得到从整数到整数的箭头——输入四十二，输出二，因为四十二有两个字符。",
                  note="代码 shout = compose strlen toString；示例 42 ↦ 2"),
             dict(say="Milewski 在《程序员的范畴论》第一章说：范畴的本质，就是复合。可道者，是箭头怎样接；对象本身，只是箭头的端点。",
                  tts="米列夫斯基在《程序员的范畴论》第一章说：范畴的本质，就是复合。可道者，是箭头怎样接；对象本身，只是箭头的端点。",
                  note="引文 Composition is the essence of category"),
             dict(say="所以第一句可以这样读：能说清楚的，是箭头怎样走；说不清楚的，是对象本身——它只存在于箭头的关系里。",
                  note="书法小字：可道者箭头也"),
         ]),

    dict(id="S2YouWu", title="二 · 有无相生", quote="有无相生，难易相成，长短相形，高下相倾。", chapter="《道德经》第二章",
         refs=["DaoFP ch.1 Clean Slate（Yin and Yang, Elements）",
               "CTFP 1.5 Products and Coproducts", "CTFP 1.6 Simple Algebraic Data Types"],
         beats=[
             dict(say="有无相生，难易相成，长短相形，高下相倾。", note="竖排原文"),
             dict(say="老子说，有和无互相生成。《函数式编程之道》把这一节叫作阴与阳。程序里也有一对极端：完全空的类型，和只有一个值的类型。",
                  note="左「无 Void」右「有 ()」；中间竖直镜面虚线"),
             dict(say="空的类型叫 Void。它一个值都没有。你没法构造出一个 Void，就像没法从空屋里拿出一张椅子。",
                  note="空屋示意；Void 标注「零个值」"),
             dict(say="从 Void 出发到任何类型，都有唯一一个函数，叫 absurd。它永远不会被真正调用——因为你拿不出一个 Void 的值来喂给它。没有输入，就无需说任何话。",
                  note="Void 向 A、B、C 发出箭头（absurd）"),
             dict(say="另一个极端是单元类型，写作一对空括号。它只有一个值，就是它自己。从任何类型到它，都有唯一一个函数：const 单元——不管给你什么，都丢掉，只回那个唯一的点。",
                  note="A、B、C 汇入 ()（const ()）"),
             dict(say="看见了吗？两个定义几乎是镜像：一个是「从无出发，通往万物」；一个是「从万物出发，归于一点」。箭头方向一翻，无就变成了有。",
                  note="左图沿镜面翻转、箭头反向，与右图重合"),
             dict(say="日常比喻：Void 像一封永远寄不出去的空信封——里面没东西可寄。单元类型像一个公用邮筒——不管你塞什么信，结果都是「已投递」。",
                  note="信封 / 邮筒示意；代码 wu / you"),
             dict(say="它们还各守一种运算：Void 是「或者」的单位——Either Void a 跟 a 一样，空的那一支永远用不上。单元类型是「并且」的单位——跟谁配对，都不增加信息。",
                  note="代码 sumUnit / prodUnit"),
             dict(say="有无相生：空与满、无与有，是同一枚硬币的两面。下一句，我们从「无」里生出东西来。",
                  note="小字预告：道生一 →"),
         ]),

    dict(id="S3Maybe", title="三 · 道生一", quote="道生一，一生二，二生三，三生万物。", chapter="《道德经》第四十二章",
         refs=["DaoFP ch.7 Recursion（以此句开篇）", "DaoFP ch.11 Algebras（Catamorphisms，直觉层）",
               "CTFP 1.6 Simple Algebraic Data Types", "CTFP 3.8 F-Algebras（fold 直觉）"],
         beats=[
             dict(say="道生一，一生二，二生三，三生万物。", note="竖排原文"),
             dict(say="《函数式编程之道》讲递归的那一章，正是以这句话开篇的。我们用程序员最熟的两样东西来读它：Maybe，和列表。",
                  note="小字：DaoFP ch.7；Maybe / List 图标"),
             dict(say="Maybe a 表示「也许有一个 a，也许没有」。它有两个构造子：Nothing，什么都没有；Just x，装着一个 x。像一个可能空的盒子。",
                  note="代码 data Maybe；Nothing / Just 图示"),
             dict(say="从「无」开始想：Maybe 作用于 Void，只能是 Nothing——这是一。再包一层，有两个可能：Nothing，或 Just Nothing——这是二。再一层，三个可能——这是三。",
                  note="链：Void → Maybe Void → Maybe² → Maybe³；点数 0 1 2 3；书法「无 一 二 三」"),
             dict(say="每包一层，就多一个「在这一层停住」的选择。一层层包下去，选择越来越多——三生万物的感觉，就在这里。",
                  note="层数与值的个数对齐动画"),
             dict(say="列表也是这样长出来的：要么是空列表，要么是「一个元素，再加上另一份列表」。空是无；接一个元素是一；再接一个是二。万物，就是任意长的列表。",
                  note="[] / (1:[]) / (1:2:[]) 展开"),
             dict(say="生出来之后，还要能收回去。折叠，就是沿着构造的逆方向走：遇到空，给一个起点；遇到「头加尾」，说清如何把头和已折叠的尾合成一步。",
                  note="折纸隐喻：打开的列表 → 一步步折起"),
             dict(say="求和就是最熟的折叠：空列表是零；非空列表是「头，加上尾的总和」。你没有写循环——你只说清了一步，递归会替你走完全程。",
                  note="代码 sumList；动画 1:2:3:[] → 6"),
             dict(say="道生一，三生万物；折叠则是万物各归其根。下一句，我们把「生」和「归」反过来看。",
                  note="书法小字：夫物芸芸，各复归其根"),
         ]),

    dict(id="S4FoldUnfold", title="四 · 反者道之动", quote="反者道之动，弱者道之用。", chapter="《道德经》第四十章",
         refs=["DaoFP ch.12 Coalgebras（Anamorphisms, Hylomorphisms——直觉层）",
               "CTFP 3.8 F-Algebras（Coalgebras）"],
         beats=[
             dict(say="反者道之动，弱者道之用。", note="竖排原文"),
             dict(say="上一句我们把列表折起来，变成一个数。现在反过来：从一个种子，长出列表。方向一翻，故事就变了。",
                  note="折叠箭头 ← 与展开箭头 → 对照"),
             dict(say="消费列表，像拆快递：打开一层，处理里头的东西，再对剩下的箱子做同样的事——这是 fold，折叠。",
                  note="拆箱示意；foldr 代码"),
             dict(say="生成列表，像种树：看着手里的种子，决定「现在结一个果，还剩下一颗更小的种子」，直到种子耗尽——这是 unfold，展开。",
                  note="种子→果+种子 示意；unfoldr 代码"),
             dict(say="比如从数字 n 展开：若 n 是零就停止；否则结出 n，留下 n 减一。于是五、四、三、二、一，整条链就长出来了。",
                  note="动画：5 → 5:4:3:2:1:[]"),
             dict(say="有了展开，有了折叠，就能接起来：先展开，再折叠。中间那条列表被生出，又立刻被消费。先生，而后归。",
                  note="种子 ─unfold→ 列表 ─fold→ 结果"),
             dict(say="阶乘就是例子：先把 n 展开成 n 到一，再把它们乘起来。十的阶乘，是三百六十二万八千八百。",
                  note="代码 fact；结果 3628800"),
             dict(say="如果你愿意，可以把这两步合成一步，中间列表从不完整出现——有人叫它 hylo，合态射。入门只需记住八个字：先生后归，生而不有。",
                  note="代码 factHylo；书法「生而不有」"),
             dict(say="反者道之动：同一套结构，箭头一翻，消费变成生成。对偶不是修辞，是一种省力的思考方式——每学会一个方向，就白得相反的那个。",
                  note="小字：fold ⟷ unfold"),
         ]),

    dict(id="S5Functor", title="五 · 知其雄，守其雌", quote="知其雄，守其雌，为天下溪。", chapter="《道德经》第二十八章",
         refs=["CTFP 1.7 Functors", "CTFP 1.8 Functoriality and Functors",
               "DaoFP 相关 Functor 铺垫；Applicative 见 DaoFP 14 / CTFP"],
         beats=[
             dict(say="知其雄，守其雌，为天下溪。", note="竖排原文"),
             dict(say="前面出现了 Maybe、列表。它们有一个共同点：都是「在某个形状里，装着一些值」。盒子可以不同，但都是盒子。",
                  note="Maybe 盒子 / 列表盒子 并排"),
             dict(say="函子，说的就是：你能在不拆盒子的前提下，改里面的值。形状不变，内容可换。Haskell 里，这个动作叫 fmap，或者就是大家熟悉的 map。",
                  note="盒子外形固定；内部 a → b；代码 fmap"),
             dict(say="对 Maybe：若是 Nothing，map 之后还是 Nothing——空的还是空的。若是 Just 三，加上一，就变成 Just 四。盒子还在，只是贴纸换了。",
                  note="Nothing ↦ Nothing；Just 3 ↦ Just 4"),
             dict(say="对列表：map 就是对每个元素施同一个函数，列表的长短、顺序都不动。一、二、三，乘以二，变成二、四、六。",
                  note="[1,2,3] map (*2) → [2,4,6]；标注「形不变」"),
             dict(say="雄，是那个主动出击的函数 f；雌，是守住形状的盒子。函数再猛，也不能把列表变成 Maybe——形状由函子守着。",
                  note="左「雄 · 函数」右「雌 · 形状」"),
             dict(say="函子有两条必须守住的规矩，像诚信条款：map id，等于什么都不做；连续 map 两次，等于 map 它们的复合。不守规矩，就不是函子。",
                  note="两条定律：fmap id = id；fmap (g∘f) = fmap g ∘ fmap f"),
             dict(say="再往前半步：Applicative。它让你把「盒子里的函数」应用到「盒子里的值」。pure 把一个普通值抬进盒子；尖括号星号负责应用。Just 加一，作用于 Just 三，得到 Just 四。",
                  note="代码：pure / (<*>)；Just (+1) <*> Just 3 = Just 4"),
             dict(say="知其雄，守其雌，为天下溪。函数是雄，容器是雌。函子让它们共处而不互相破坏；Applicative 更让盒子里的函数也能发挥作用。形状，是那条容纳一切的溪床。",
                  note="两栏之间一道墨线（溪）"),
         ]),

    dict(id="S6Monad", title="六 · 无为而无不为", quote="道常无为而无不为。", chapter="《道德经》第三十七章",
         refs=["DaoFP ch.2 Composition（Identity = wu wei）", "DaoFP ch.15 Monads（入门直觉）",
               "CTFP 3.4 Kleisli Categories", "CTFP 3.6 Monads Categorically（bind / join 直觉）"],
         beats=[
             dict(say="道常无为而无不为。", note="竖排原文"),
             dict(say="函子能改盒子里的值，但有件事它做不到：若你的函数自己会返回一个新盒子，fmap 之后会变成「盒子里套盒子」。Just 套 Just，两层皮。",
                  note="f :: a → Maybe b；fmap f (Just x) :: Maybe (Maybe b)"),
             dict(say="单子，多了一步：把套叠的盒子摊平。这一步，Haskell 里叫 bind，写作大于大于等号；或者用 join 先摊平，再 fmap。两层变一层。",
                  note="Maybe (Maybe a) → Maybe a；代码 (>>=)"),
             dict(say="日常比喻：你吩咐助手「去问问前台，房间号是多少」。助手回来时，不会交给你「另一个助手手里的字条」，而是直接把字条给你——bind 就是那位会拆套的助手。",
                  note="助手拆套示意"),
             dict(say="举个例子：half 只对偶数动手，奇数就返回 Nothing。八 bind half bind half，得到 Just 二；七 bind half，直接是 Nothing。",
                  note="代码 half / chain；8→4→2，7→Nothing"),
             dict(say="有了 bind，就可以按顺序排好几件可能失败的事：先读配置，再开文件，再解析。任何一步是 Nothing，后面自动跳过。你不用满屏写 if。",
                  note="三步管道；旁注「一步失败则全体短收」"),
             dict(say="这就是 do 记法：看起来像命令式，一行接一行；底下仍是 bind 在串盒子。你没有强迫每一步立刻交出普通值——你只描述顺序，让盒子自己处理失败。",
                  note="代码 do 块与等价的 >>= 对照"),
             dict(say="无为：不强行把效果从盒子里掏出来。无不为：一旦排好顺序，该做的事都能做完。单子是「在效果里编程」，而不是「先消灭效果再编程」。",
                  note="书法小字：无为而无不为"),
             dict(say="今天停在这里。进阶篇会走得更深：Fix 与不动点、伴随、米田引理——把「可道」与「不可道」彻底说圆。若你刚入门，先把箭头、有无、折叠、函子、单子这五块摸熟，就已经握住溪流的源头了。",
                  note="指向「进阶篇」；五块回顾小字"),
         ]),

    dict(id="S7Ending", title="结 · 看箭头", quote="", chapter="", refs=[],
         beats=[
             dict(say="从对象与箭头，到有与无；从生与归，到形与效。六句话，其实只说了一件事：顺着箭头看。",
                  note="六句原文小字环绕圆相"),
             dict(say="借 Milewski 的提醒：看箭头。道可道，非常道。谢谢观看。进阶篇见。",
                  tts="借米列夫斯基的提醒：看箭头。道可道，非常道。谢谢观看。进阶篇见。",
                  note="「看箭头」书法大字；印章；谢谢观看；小字进阶篇"),
         ]),
]
