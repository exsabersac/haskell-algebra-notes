# -*- coding: utf-8 -*-
"""Single source of truth for narration — 进阶深讲第 7 集：道可道.

Audience: finished beginner deep-dives 01–06; ready for advanced CT.
First advanced episode. CT first, then short Haskell. Yoneda teased only.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Yoneda", "米田"),
    ("DaoFP", "道 F P"),
    ("CTFP", "C T F P"),
    ("Speak", "Speak"),
    ("Dao", "道"),
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
    dict(id="S0Title", title="道可道", quote="", chapter="", refs=[],
         beats=[
             dict(say="道可道，非常道。欢迎来到「道可道」进阶深讲——第七集，也是进阶篇的开篇。",
                  note="宣纸背景，圆相一笔画出；标题「道可道」浮现"),
             dict(say="入门深讲六集，从类型、箭头、Void 与单元，走到函子与 Monad。底已经铺好。从这一集起，我们换一副口气：少讲语法糖，多讲范畴里真正难说清的事——对象与箭头的认识论。",
                  note="小字：入门 01–06 → 进阶 07；提纲"),
             dict(say="本集只钉一件事：对象不可道，箭头可道；并在末尾轻轻点一句米田——把「凭什么说两个对象相同」的问题先挂起来。钉子钉稳，证明留给后集。",
                  note="三行：对象 · 箭头 · 米田一句"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第一章与第三章，以及《程序员的范畴论》开篇那几节。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第一章与第三章，以及《程序员的范畴论》开篇那几节。片中表述都是释义，不是照录。",
                  note="DaoFP ch.1 / ch.3 · CTFP 1.1–1.2；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道德经钩子", quote="道可道，非常道；名可名，非常名。", chapter="《道德经》第一章",
         refs=["DaoFP ch.1 Clean Slate（Types and Functions / Elements）",
               "CTFP 1.1, 1.2"],
         beats=[
             dict(say="道可道，非常道；名可名，非常名。", note="竖排书法原文，右起"),
             dict(say="进阶篇的第一集，仍用老子作钩子。但钩子只负责开门：门后站着的，是范畴论的一条硬论点——对象本身说不出口。哲学是引子，数学是正文。",
                  note="小字：进阶开篇 · 论点预告"),
             dict(say="Milewski 在《函数式编程之道》第一章，几乎原样改写了这句：能被描述的类型，不是恒常的类型。类型是原始概念，无法定义。",
                  tts="米列夫斯基在《函数式编程之道》第一章，几乎原样改写了这句：能被描述的类型，不是恒常的类型。类型是原始概念，无法定义。",
                  note="引文：The type that can be described… —— DaoFP ch.1"),
             dict(say="注意：这不是神秘主义。它是在说——范畴的公理里，根本没有「打开对象看内部」这一条。能写进公理的，只有对象、箭头、复合与恒等。内部若真要谈，也只能借箭头间接谈。",
                  note="公理四件：对象 · 箭头 · 复合 · 恒等"),
             dict(say="所以本集的节奏很慢：先把「不可道」钉死，再把「可道」交给箭头；Haskell 只作短印证；米田一句，留给后面赎回。",
                  note="本集路线图"),
         ]),

    dict(id="S2Object", title="二 · 对象不可道", quote="", chapter="",
         refs=["DaoFP ch.1 Types and Functions；CTFP 1.1"],
         beats=[
             dict(say="先立论点：在范畴里，对象是不可言说的。你不能指着一个对象说：看，这是我的元素。元素这个词，不在范畴的词典里。词典里只有关系。",
                  note="论点大字；墨团对象 a"),
             dict(say="对象没有部分。它不是集合论里的袋子，不能翻开、不能枚举、不能指着里面一粒一粒报数。它只是一个点——一个名字。集合论问「里面有什么」；范畴论问「通向哪里、从哪里来」。",
                  note="淡墨晕染对象 a，无内部标签"),
             dict(say="这听起来很空。正是这份空，逼我们换一种认识方式：不靠打开，而靠探测。探测的工具，就是箭头。空不是虚无，是把内部让出来，好把关系写清楚。",
                  note="书法小字：不靠打开 · 靠探测"),
             dict(say="Haskell 程序员其实早有直觉：一个不导出构造子的抽象类型，模块外看不见内部。你对它的全部了解，只能来自那些以它为参数、或以它为结果的函数。",
                  note="抽象类型 · 不导出构造子"),
             dict(say="对象不可道——不是说对象不存在，而是说：我们对它的全部可说之词，都不在它「里面」，而在它与别的对象之间的关系上。",
                  note="可说之词在关系上"),
             dict(say="记住这句话。下一节，我们把话筒交给箭头。",
                  note="过渡到箭头"),
         ]),

    dict(id="S3Arrow", title="三 · 箭头可道", quote="", chapter="",
         refs=["DaoFP ch.3 Isomorphism（Reasoning with Arrows）；CTFP 1.2"],
         beats=[
             dict(say="能说出口的，只有箭头：射入它的箭头，从它射出的箭头，以及这些箭头怎样复合。对象的结构，是用箭头一下一下探测出来的。探测，就是言说。",
                  note="箭头从四周射入、射出；复合"),
             dict(say="DaoFP 第三章有一句几乎成了口号：Master Yoneda says: At the arrows look!——先别盯着对象，盯着箭头看。",
                  tts="道 F P 第三章有一句几乎成了口号：Master Yoneda says: At the arrows look!——先别盯着对象，盯着箭头看。",
                  note="书法/小字：At the arrows look!"),
             dict(say="一支从 a 射向 x 的箭头，是对 a 的一种说法：它告诉你，在 x 的语境里，a 被怎样使用。换一个 x，就多一种说法。说法可以复合：先说 f，再说 g，等于一口气说 g 圆点 f。",
                  note="a → x 作为一种说法；复合"),
             dict(say="把所有可能的说法收在一起——对每一个 x，给一支 a 到 x 的箭头——你就得到「从 a 出发的全部可道」。Haskell 里，这正是续体风格的类型：Speak a。名字叫 Speak，正是「可道」二字的英文影子。",
                  note="forall x. (a → x) → x"),
             dict(say="所以可以写成一句对仗：可道者，箭头也；不可道者，对象也。对象沉默；箭头替它说话。",
                  note="书法对仗：可道者箭头也"),
             dict(say="但立刻有一个漏洞：若对象本身不可言说，我们凭什么断定两个对象相同？a 同构于 b，这句话的根据在哪里？",
                  note="问号 a ≅ b ?"),
         ]),

    dict(id="S4Yoneda", title="四 · 自然性铺垫 / 米田一句", quote="", chapter="",
         refs=["DaoFP ch.3 / ch.9 Yoneda tease；CTFP 2.5–2.6（仅预告）"],
         beats=[
             dict(say="漏洞不能假装没看见。范畴论的回答是：两个对象相同，不靠打开它们，而靠它们发出的箭头「一样」。相同，是外在的对齐，不是内在的剖视。",
                  note="同构 = 箭头层面的对应"),
             dict(say="更精确一点：若从 a 出发的每一种说法，都唯一对应从 b 出发的同一种说法，并且这种对应还要在箭头合成时保持一致——这叫自然性。自然性，是「说法对齐」的纪律：你不能只对齐几个点，还要对齐路上的每一步。",
                  note="自然性 = 说法对齐的纪律"),
             dict(say="米田引理会说：一个对象，被它出发的所有箭头完全刻画。对象不可道；但「它的全部说法」可道——而且恰好够用。DaoFP 里那句 Master Yoneda says，指的就是这件事。",
                  tts="米田引理会说：一个对象，被它出发的所有箭头完全刻画。对象不可道；但「它的全部说法」可道——而且恰好够用。道 F P 里那句 Master Yoneda says，指的就是这件事。",
                  note="Yoneda 一句：对象被 Hom(a, −) 刻画"),
             dict(say="今天只点到这里。不写证明，不展开嵌入。先把钉子钉上：可道在箭头；同构在说法的对齐；米田，是后面赎回这句话的钥匙。",
                  note="待进阶后集赎回"),
             dict(say="入门篇里，你已经见过函子保形、自然变换方块。那些方块，正是自然性的图示。进阶篇会一次次回到它们。",
                  note="自然变换方块回响"),
         ]),

    dict(id="S5Haskell", title="五 · 短 Haskell", quote="", chapter="",
         refs=["DaoFP ch.1；本集 haskell/src/DaoSayable.hs"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。先做一个不导出构造子的类型 Dao：外界看不见内部，只能通过射入的 birth、射出的 speak 来认识它。",
                  note="代码 s_dao；构造子不导出"),
             dict(say="birth 把整数送进 Dao；speak 从 Dao 读出字符串。两支箭头，一进一出——这就是模块边界上全部可说的话。",
                  note="高亮 birth / speak"),
             dict(say="再写类型同义词 Speak a：对任意 x，吃一支 a 到 x 的箭头，交出一个 x。它收集「从 a 出发的一切说法」。这不是玄学，是类型里写出来的探测器。",
                  note="代码 s_speak"),
             dict(say="hear 把一个具体的 a，变成它的说法：给你一支箭头 k，就把 a 喂给 k。这是续体传递的最小种子——后面米田会认出它。今天只要记住：值可以变成说法。",
                  note="hear :: a → Speak a"),
             dict(say="跑一下：birth 四十二，再 speak，得到「道四十二」。hear 把四十二收成说法，再交给加一，得到四十三。图怎么说，代码就怎么应——不可道在类型边界，可道在函数签名。",
                  note="demo；边界 vs 签名"),
         ]),

    dict(id="S6Next", title="结 · 下集有无相生", quote="", chapter="",
         refs=["下集预告：有无相生 · 始对象与终对象"],
         beats=[
             dict(say="今天钉牢三件事：对象不可道；箭头可道；米田一句——对象被它发出的箭头所认识。漏洞挂在墙上，钥匙留给后集。进阶篇的第一颗钉子，就钉在这里。",
                  note="三句回顾环绕圆相"),
             dict(say="下一集《有无相生》：始对象与终对象——无与有，Void 与单元。它们是彼此的镜像；对偶，第一次正式上场。有和无互相生成——范畴里，这句话有精确的图。",
                  note="预告：始 · 终 · 对偶"),
             dict(say="借 Milewski 的提醒：先别打开对象，先看箭头。道可道，非常道。进阶篇，我们下集见。",
                  tts="借米列夫斯基的提醒：先别打开对象，先看箭头。道可道，非常道。进阶篇，我们下集见。",
                  note="「道可道」书法；印章；谢谢观看"),
         ]),
]
