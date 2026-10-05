# -*- coding: utf-8 -*-
"""Single source of truth for narration — 深讲第 1 集：类型与箭头.

Audience: knows some programming; Haskell optional.
Expand beginner point 1 into ~8–12 min. CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("id，", "I D，"), ("id。", "I D。"),
    ("id 是", "I D 是"), ("叫 id", "叫 I D"), ("用 id", "用 I D"),
    ("写作 id", "写作 I D"), ("函数 id", "函数 I D"),
    ("id 跟", "I D 跟"), ("idA", "I D A"), ("idB", "I D B"),
    ("(.).", "圆点。"), ("(.) ", "圆点 "),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="类型与箭头", quote="", chapter="", refs=[],
         beats=[
             dict(say="道可道，非常道。欢迎来到「道可道」深讲系列。",
                  note="宣纸背景，圆相一笔画出；标题「类型与箭头」浮现"),
             dict(say="入门篇用六句话，把范畴论扫了一遍。从这一集起，我们把每一块单独拉开：慢一点，讲透一点。不赶进度，只把门口的那几块砖铺平。",
                  note="小字：入门篇 → 深讲；本集标注「01」"),
             dict(say="第一集，只谈一件事：类型与箭头。类型是对象，函数是态射；复合与恒等，是范畴的两条规矩。先把话说清楚，再落到几行 Haskell。",
                  note="三行提纲：对象/箭头 · 复合 · 恒等"),
             dict(say="框架仍是 Milewski 的两本书：《程序员的范畴论》第一章，和《函数式编程之道》的「白板」与「复合」两章。哲学是钩子，数学要站得住。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《程序员的范畴论》第一章，和《函数式编程之道》的「白板」与「复合」两章。哲学是钩子，数学要站得住。片中表述都是释义，不是照录。",
                  note="CTFP 1.1/1.2 · DaoFP ch.1/ch.2；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道可道", quote="道可道，非常道；名可名，非常名。", chapter="《道德经》第一章",
         refs=["DaoFP ch.1 Clean Slate（Types and Functions）",
               "CTFP 1.1 Category: The Essence of Composition"],
         beats=[
             dict(say="道可道，非常道；名可名，非常名。", note="竖排书法原文，右起"),
             dict(say="Milewski 在《函数式编程之道》开篇，借老子的话说：能被描述干净的类型，就不是那个永恒的类型。类型是原始观念——你没法再往下定义它，也无须往硬件里追问它「究竟是什么」。",
                  tts="米列夫斯基在《函数式编程之道》开篇，借老子的话说：能被描述干净的类型，就不是那个永恒的类型。类型是原始观念——你没法再往下定义它，也无须往硬件里追问它「究竟是什么」。",
                  note="书法小字：The type that can be described…；旁注「原始观念」"),
             dict(say="换个名字也一样：在范畴论里叫对象，在逻辑里叫命题。名字不同，位置相同——它们都是「点」，不是故事本身。故事写在点与点之间。",
                  note="三栏：类型 / 对象 / 命题"),
             dict(say="真正能说清楚的，是点与点之间怎么连。箭头有起点，有终点；可以说从哪到哪，叫什么名字。可道者，是箭头。不可道者，是那个被箭头指着的点。",
                  note="两点一箭头；标注「可道者箭头也」"),
             dict(say="所以第一句可以这样读：能说清楚的，是关系怎样走；说不清楚的，是对象本身——它只活在箭头的端点上。忘掉「里面有什么」，先学会看连线。",
                  note="对象淡化、箭头加粗；书法「可道者箭头也」"),
         ]),

    dict(id="S2Map", title="二 · 地图", quote="", chapter="",
         refs=["DaoFP ch.1 Types and Functions", "CTFP 1.1"],
         beats=[
             dict(say="先忘掉抽象。想象一张地图：城市是点，公路是箭头。范畴论就是这样看世界的——不先问城市有多富，先问路怎么走。",
                  note="两点一公路；左「对象=点」右「箭头=路」"),
             dict(say="城市本身是什么？砖头、人口、气候——地图不关心。地图只关心：有没有路，从哪到哪，叫什么名字。名字不同，就是不同的路。",
                  note="城市圆点内部留白；箭头旁标注路名 f"),
             dict(say="对象也一样：不谈它「里面有什么」，只谈它怎样被箭头碰到。结构，写在连线上。这是范畴论跟集合论的一个分水岭：我们先看箭头，再谈元素。",
                  note="对象圆点空心；说明「结构在箭头上」"),
             dict(say="同一对城市之间，可以有不止一条路。一条叫通勤，一条叫绕行——两条都是合法的箭头，名字不同，就不算同一条。范畴允许平行的箭头。",
                  note="A→B 两条平行箭头 f、g"),
             dict(say="也可以绕回自己：环城路。后面会看到，每个对象都至少有一条特别的环路——恒等。现在先记住：环路也是箭头，合法，而且很重要。",
                  note="自环预告 id；小字「后文」"),
         ]),

    dict(id="S3Types", title="三 · 类型是对象", quote="", chapter="",
         refs=["DaoFP ch.1 Types and Functions", "CTFP 1.2 Types and Functions"],
         beats=[
             dict(say="落到程序里：类型就是对象。整数、字符串、布尔——各是一个点。先别管它们在内存里占几个字节，把它们当成地图上的城市。",
                  note="Int、String、Bool 三个圆点"),
             dict(say="函数就是箭头：把一种类型变成另一种。toString 从整数指向字符串；length 从字符串指回整数。方向写清楚，故事就清楚。",
                  note="箭头 toString、length；双向"),
             dict(say="Haskell 用双冒号写类型签名。读作：左边是名字，右边是「从哪到哪」。f 双冒号 a 箭头 b，就是一条从 a 到 b 的箭头。签名本身，就是在声明一条路。",
                  note="代码：f :: a -> b；标注「类型签名 = 箭头声明」"),
             dict(say="注意：箭头两端写的是类型，不是某个具体的值。值是走在路上的旅客；类型是城市本身。旅客可以换，城市的名字不变。",
                  note="旅客小点沿箭头移动；城市标签不变"),
             dict(say="同一对类型之间，也可以有很多函数。not 和 id 都能从布尔到布尔——两条不同的路，共用起终点。一条翻转，一条原样送回。",
                  note="Bool 自环：not 与 id 并排"),
             dict(say="Milewski 提醒：别急着想硬件怎么实现。类型与函数，先是一种说话方式——一种把计算画成图的方式。图画对了，实现可以后补。",
                  tts="米列夫斯基提醒：别急着想硬件怎么实现。类型与函数，先是一种说话方式——一种把计算画成图的方式。图画对了，实现可以后补。",
                  note="小字：physical substrate is irrelevant"),
         ]),

    dict(id="S4Compose", title="四 · 复合", quote="", chapter="",
         refs=["DaoFP ch.2 Composition", "CTFP 1.1 The Essence of Composition"],
         beats=[
             dict(say="两段路可以接起来。先走 f，从 a 到 b；再走 g，从 b 到 c。中间的城市对上了，就能合起来，得到从 a 直达 c 的箭头。接不上，就接不了——这是硬条件。",
                  note="三点 A→B→C；弧线 g ∘ f"),
             dict(say="数学里写作 g 圆点 f，读作「g 接在 f 之后」。Haskell 里，圆点写成一个句点：g 句点 f。同一个想法，两套记号。",
                  note="标注 g ∘ f 与 g . f 对照"),
             dict(say="顺序容易晕：先写的 g，其实后走。像水管：水从右边进，左边出——从右往左读。养成习惯：看见句点，就从右边的函数开始想。",
                  note="管道示意：右→左；「先 f 后 g」"),
             dict(say="复合有一条铁律：三段路，先接左再接右，和先接右再接左，结果必须一样。这叫结合律。没有结合律，括号会把你淹没。",
                  note="(h∘g)∘f = h∘(g∘f)"),
             dict(say="有了结合律，你就不必记括号。一长串函数接起来，只是一条更长的路——程序，说到底，就是在做分解与再复合。大问题拆小，小箭头接回大箭头。",
                  note="h = j ∘ k ∘ f 去括号；小字「programming is composition」"),
             dict(say="Milewski 在《程序员的范畴论》第一章说：范畴的本质，就是复合。没有复合，对象和箭头只是一堆散件；有了复合，才成系统。",
                  tts="米列夫斯基在《程序员的范畴论》第一章说：范畴的本质，就是复合。没有复合，对象和箭头只是一堆散件；有了复合，才成系统。",
                  note="引文 Composition is the essence of category"),
         ]),

    dict(id="S5Identity", title="五 · 恒等", quote="", chapter="",
         refs=["DaoFP ch.2 Identity（wu wei）", "CTFP 1.2"],
         beats=[
             dict(say="每个城市还有一条什么也不做的环路：从自己回到自己。这叫恒等箭头。它看起来无聊，却是整个范畴的支点。",
                  note="自环 id；标注「无为」"),
             dict(say="无为，不是没有这条路，而是走了等于没走。跟任何箭头相接，左接右接，都不改变对方。少了它，复合的单位就不存在。",
                  note="id_B ∘ f = f = f ∘ id_A"),
             dict(say="Haskell 里，所有类型共用一个名字：id。定义就是：id x 等于 x。什么也不做，原样送回。类型是 a 箭头 a——起点终点同一座城。",
                  note="代码：id :: a -> a；id x = x"),
             dict(say="恒等是复合的单位，就像数字里的一，是乘法的单位。乘一不改变；接上 id，也不改变。单位元一出现，代数结构才站稳。",
                  note="单位元示意；小字「unit of composition」"),
             dict(say="所以范畴有两条规矩，记住就够：一，箭头能接就得能接，并且结合；二，每个对象都有恒等，而且真的什么都不做。其它故事，都站在这两条上面。",
                  note="两条定律并排卡片"),
         ]),

    dict(id="S6Haskell", title="六 · 落到代码", quote="", chapter="",
         refs=["DaoFP ch.2 Composition", "CTFP 1.2"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。先是恒等，再是复合。屏幕上的代码，都能直接编译；我们一行一行对上刚才的图。",
                  note="代码块出现：identity / compose"),
             dict(say="identity 的类型是 a 箭头 a；实现就是把参数原样返回。compose 吃两条箭头，吐出一条更长的：先走 f，再走 g。类型写在前，实现跟在后。",
                  note="高亮 identity 与 compose 签名"),
             dict(say="再举个例子：toString 把整数变成字符串；strlen 量字符串长度。两者接起来，得到从整数到整数的箭头。中间的字符串城市，对上了。",
                  note="代码 toString / strlen / shout"),
             dict(say="输入四十二，toString 得到字符串四十二，strlen 数出两个字符——所以 shout 四十二等于二。一条复合出来的路，真的可以走。",
                  note="演算：42 ↦ \"42\" ↦ 2"),
             dict(say="你也可以直接写库里的句点：strlen 句点 toString，和自己写的 compose，是同一条路。自己写一遍，是为了看见复合；用句点，是为了日常省事。",
                  note="shout' = strlen . toString；对照"),
             dict(say="类型签名会替你守门：接错了方向，编译器直接拒绝。箭头对不上，路就修不通——这正是范畴观点落到工程里的好处：错路在编译期就被拦住。",
                  note="错误示例淡红闪过；正确签名稳住"),
         ]),

    dict(id="S7Next", title="结 · 看箭头", quote="", chapter="",
         refs=["DaoFP ch.1 Yin and Yang", "CTFP 1.2 / 下一集 Void 与 ()"],
         beats=[
             dict(say="今天只停在门口：对象不可道，箭头可道；类型是对象，函数是态射；复合与恒等，撑起整座范畴。门口的砖，铺平了。",
                  note="三句回顾小字环绕圆相"),
             dict(say="下一集，我们走进有与无：完全空的类型 Void，和只有一个值的单元类型。有无相生，箭头方向一翻，故事就对称了。始对象与终对象，会从这对本源里长出来。",
                  note="预告：Void ⟷ ()；小字「深讲 02」"),
             dict(say="借 Milewski 的提醒：看箭头。道可道，非常道。我们下集见。",
                  tts="借米列夫斯基的提醒：看箭头。道可道，非常道。我们下集见。",
                  note="「看箭头」书法；印章；谢谢观看"),
         ]),
]
