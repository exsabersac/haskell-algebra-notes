# -*- coding: utf-8 -*-
"""Single source of truth for narration — 深讲第 2 集：Void 与 ()。

Audience: knows some programming; Haskell optional.
Expand beginner point 2 (有无相生) into ~8–12 min. CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Void", "Void"),
    ("absurd", "absurd"),
    ("Either", "Either"),
    ("Maybe", "Maybe"),
    ("id，", "I D，"), ("id。", "I D。"),
    ("id 是", "I D 是"), ("叫 id", "叫 I D"), ("用 id", "用 I D"),
    ("写作 id", "写作 I D"), ("函数 id", "函数 I D"),
    ("id 跟", "I D 跟"),
    ("const", "const"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="Void 与 ()", quote="", chapter="", refs=[],
         beats=[
             dict(say="有无相生。欢迎来到「道可道」深讲第二集。",
                  note="宣纸背景，圆相一笔画出；标题「Void 与 ()」浮现"),
             dict(say="上一集铺平了门口：类型是对象，函数是箭头；复合与恒等，撑起整座范畴。这一集，我们只谈一对极端——完全空的类型，和只有一个值的类型。",
                  note="小字：深讲 01 → 02；提纲 Void / ()"),
             dict(say="范畴论里，它们分别叫始对象与终对象。先把话说清楚，再落到几行 Haskell。慢一点，只把这一对镜子看明白。",
                  note="三行：始对象 · 终对象 · 对偶"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第一章的阴阳与元素，以及《程序员的范畴论》里积与余积那一章。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第一章的阴阳与元素，以及《程序员的范畴论》里积与余积那一章。片中表述都是释义，不是照录。",
                  note="DaoFP ch.1 Yin and Yang · CTFP 1.5/1.6；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 有无相生", quote="有无相生，难易相成，长短相形，高下相倾。", chapter="《道德经》第二章",
         refs=["DaoFP ch.1 Clean Slate（Yin and Yang, Elements）",
               "CTFP 1.5 Products and Coproducts"],
         beats=[
             dict(say="有无相生，难易相成，长短相形，高下相倾。", note="竖排书法原文，右起"),
             dict(say="老子说，有和无互相生成。《函数式编程之道》把这一节叫作阴与阳。程序里也有一对极端：一个值都没有的类型，和恰好一个值的类型。",
                  note="左「无 Void」右「有 ()」；中间竖直镜面虚线"),
             dict(say="别急着谈实现。先问范畴论的问题：从它出发，有几条箭头？通向它，又有几条箭头？答案一旦唯一，这个对象就特别——它成了整座范畴的标尺。",
                  note="出射 / 入射计数示意；「唯一」加粗"),
             dict(say="始对象：对每个对象，从它出发有且仅有一条箭头。终对象：对每个对象，通向它有且仅有一条箭头。定义里不谈「里面有什么」，只谈箭头怎么数。",
                  note="卡片：始对象 / 终对象 定义并排"),
             dict(say="在 Haskell 的类型范畴里——依惯例先忽略底——始对象就是 Void，终对象就是单元类型，写作一对空括号。有无相生，从这对定义开始。",
                  note="标注 Hask：Void = 0，() = 1"),
         ]),

    dict(id="S2Void", title="二 · Void：无出射", quote="", chapter="",
         refs=["DaoFP ch.1 Elements（Void）", "CTFP 1.5 Initial object；1.6"],
         beats=[
             dict(say="先看无。Void 一个值都没有。你没法构造出一个 Void，就像没法从空屋里拿出一张椅子。没有值，就没有旅客可以上路。",
                  note="空屋 / 空圆；标注「零个值」"),
             dict(say="可是箭头不需要旅客先存在，也能被声明。从 Void 到任意类型 a，仍然可以写一条箭头。Haskell 里它叫 absurd：类型是 Void 箭头 a。",
                  note="Void → A / B / C；标签 absurd"),
             dict(say="为什么叫荒谬？因为你永远拿不出一个 Void 的值来喂给它。这条路合法，却永远不会被真正走完。没有输入，就无需说任何话——输出可以是任何类型。",
                  note="小字：never called；信封空"),
             dict(say="关键不在于「能不能调用」，而在于「有几条」。从 Void 到任意 a，恰好有一条。两条不同的实现？在忽略底的世界里，它们被迫相等——因为没有输入可以区分它们。",
                  note="唯一性：Hom(Void, a) 恰有一元"),
             dict(say="这正是始对象的定义：对每个对象 a，从始对象出发的箭头存在且唯一。Void 就是这座范畴的起点——不是时间上的起点，是箭头计数上的零。",
                  note="书法小字：始对象 · initial"),
             dict(say="日常比喻：Void 像一封永远寄不出去的空信封——里面没东西可寄。路可以画在地图上，邮差却永远等不到那封信。",
                  note="空信封示意"),
         ]),

    dict(id="S3Unit", title="三 · ()：唯一入", quote="", chapter="",
         refs=["DaoFP ch.1 Elements（Unit）", "CTFP 1.5 Terminal object"],
         beats=[
             dict(say="再看有。单元类型写作一对空括号。它只有一个值，就是它自己——那个空括号。不多不少，恰好一点。",
                  note="() 圆点；标注「一个值」"),
             dict(say="从任意类型 a 到它，都有一条箭头：不管给你什么，都丢掉，只回那个唯一的点。Haskell 里写作 const 单元，或者干脆写成下划线箭头空括号。",
                  note="A / B / C → ()；标签 const ()"),
             dict(say="为什么唯一？因为终点只有一个值可选。两条从 a 到单元的函数，对任何输入都只能交出同一个结果——所以它们是同一条箭头。",
                  note="唯一性：Hom(a, ()) 恰有一元"),
             dict(say="这正是终对象的定义：对每个对象 a，通向终对象的箭头存在且唯一。单元类型是万物归一的那个点——箭头计数上的一。",
                  note="书法小字：终对象 · terminal"),
             dict(say="日常比喻：单元类型像一个公用邮筒——不管你塞什么信，结果都是「已投递」。信息被丢掉，只留下「到达过」这一件事。",
                  note="邮筒示意"),
         ]),

    dict(id="S4Dual", title="四 · 对偶", quote="", chapter="",
         refs=["DaoFP ch.1 Yin and Yang", "CTFP 1.5（initial ↔ terminal dual）"],
         beats=[
             dict(say="看见了吗？两个定义几乎是镜像。始对象管出射：从它出发，通往万物，各恰好一条。终对象管入射：从万物出发，归于一点，各恰好一条。",
                  note="左右对照图：出射扇 / 入射汇"),
             dict(say="箭头方向一翻，无就变成了有。范畴论把这种「整张图翻个面」叫做对偶：把每条箭头掉头，始对象就变成终对象，定义一字不改，只换方向。",
                  note="镜面翻转动画；标注 duality"),
             dict(say="它们还各守一种运算。Void 是「或者」的单位：Either Void a 跟 a 一样——空的那一支永远用不上。单元类型是「并且」的单位：跟谁配对，都不增加信息。",
                  note="Either Void a ≅ a；((), a) ≅ a"),
             dict(say="所以有无相生，不只是修辞。空与满、零与一、始与终，是同一枚硬币的两面。学会看见这一对，后面的积、余积、Maybe，都会从这面镜子里长出来。",
                  note="硬币两面；预告积 / 余积"),
             dict(say="Milewski 提醒：先把这一对极端钉牢。它们是类型代数的零与一——加减乘除还没上场，标尺已经立好了。",
                  tts="米列夫斯基提醒：先把这一对极端钉牢。它们是类型代数的零与一——加减乘除还没上场，标尺已经立好了。",
                  note="小字：0 与 1 in the algebra of types"),
         ]),

    dict(id="S5Haskell", title="五 · 落到代码", quote="", chapter="",
         refs=["DaoFP ch.1；CTFP 1.6 Simple Algebraic Data Types"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。先从 Data.Void 取出 Void 和 absurd；再写出万物归一的那条箭头。",
                  note="代码块：wu / you"),
             dict(say="wu 的类型是 Void 箭头 a；实现就是 absurd。you 的类型是 a 箭头单元；实现就是 const 单元。类型写在前，唯一性藏在类型里。",
                  note="高亮 wu 与 you 签名"),
             dict(say="再看一对单位律。sumUnit 吃掉 Either Void a，用 absurd 处理左支，用 id 放行右支——结果只剩 a。空的「或者」消失了。",
                  note="代码 sumUnit；Either 图左支淡出"),
             dict(say="prodUnit 吃掉一对：单元和 a。取第二个分量就够了——单元没带来新信息。「并且」上的单位，就是这样看不见自己。",
                  note="代码 prodUnit；配对图 () 淡出"),
             dict(say="你不必真的构造 Void。这些函数的意义，在于它们证明箭头存在，并且类型系统保证你写不出第二条。唯一性，是类型在替你说话。",
                  note="小字：existence + uniqueness via types"),
             dict(say="屏幕上的代码都能直接编译。自己写一遍 absurd 与 const，是为了看见始与终；用库函数，是为了日常省事。图对齐了，代码只是把图念出来。",
                  note="对照：图 ⟷ 代码"),
         ]),

    dict(id="S6Next", title="结 · 有无相生", quote="", chapter="",
         refs=["DaoFP ch.7 Recursion；CTFP 1.6 / 下一集 Maybe·List"],
         beats=[
             dict(say="今天只钉牢一对镜子：Void 是始对象，出射唯一；单元是终对象，入射唯一。箭头一翻，有无相生。零与一，立在类型代数的两端。",
                  note="三句回顾环绕圆相"),
             dict(say="下一集，我们从「无」里生出东西来：Maybe，和列表。Nothing 是一；再包一层是二；一层层包下去，就是三生万物。折叠，则把万物收回去。",
                  note="预告：Maybe / List；小字「深讲 03」"),
             dict(say="借 Milewski 的提醒：看箭头。有无相生。我们下集见。",
                  tts="借米列夫斯基的提醒：看箭头。有无相生。我们下集见。",
                  note="「看箭头」书法；印章；谢谢观看"),
         ]),
]
