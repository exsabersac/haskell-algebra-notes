# -*- coding: utf-8 -*-
"""Single source of truth for narration — 深讲第 3 集：Maybe 与 List。

Audience: knows some programming; Haskell optional.
Expand beginner point 3 (道生一) into ~8–12 min. CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Void", "Void"),
    ("Maybe", "Maybe"),
    ("Nothing", "Nothing"),
    ("Just", "Just"),
    ("Either", "Either"),
    ("Nil", "Nil"),
    ("Cons", "Cons"),
    ("List", "List"),
    ("fold", "fold"),
    ("unfold", "unfold"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="Maybe 与 List", quote="", chapter="", refs=[],
         beats=[
             dict(say="道生一。欢迎来到「道可道」深讲第三集。",
                  note="宣纸背景，圆相一笔画出；标题「Maybe 与 List」浮现"),
             dict(say="上一集钉牢了零与一：Void 是始对象，单元类型是终对象。这一集，我们从这对标尺里，生出两样最熟的东西——Maybe，和列表。",
                  note="小字：深讲 02 → 03；提纲 Maybe / List"),
             dict(say="范畴论里，它们是代数数据类型：用求和与递归，把构造子写清楚。先把话说明白，再落到几行 Haskell。",
                  note="三行：Maybe = 1+A · List 递归 · 构造直觉"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》讲递归的那一章，以及《程序员的范畴论》里简单代数数据类型那一节。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》讲递归的那一章，以及《程序员的范畴论》里简单代数数据类型那一节。片中表述都是释义，不是照录。",
                  note="DaoFP ch.7 · CTFP 1.6；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道生一", quote="道生一，一生二，二生三，三生万物。", chapter="《道德经》第四十二章",
         refs=["DaoFP ch.7 Recursion（以此句开篇）",
               "CTFP 1.6 Simple Algebraic Data Types"],
         beats=[
             dict(say="道生一，一生二，二生三，三生万物。", note="竖排书法原文，右起"),
             dict(say="《函数式编程之道》讲递归的那一章，正是以这句话开篇的。入门篇扫过一遍；这一集，我们把 Maybe 和列表单独拉开。",
                  note="小字：DaoFP ch.7；入门篇 → 深讲 03"),
             dict(say="先问范畴论的问题：一个类型，有哪些构造方式？每种方式对应一条引入规则。构造子一旦写清，值怎么数、箭头怎么画，都跟着定了。",
                  note="引入规则 / 构造子示意"),
             dict(say="Maybe 说的是：要么什么都没有，要么装着一个东西。列表说的是：要么空，要么头，再加上另一份列表。一个是有限的选择；一个是自己指回自己。",
                  note="Maybe 盒子 / List 链 并排"),
             dict(say="从「无」开始想，一层层包下去，选择越来越多——道生一的感觉，就在这里。慢一点，只把构造看明白。",
                  note="书法小字：从无生长"),
         ]),

    dict(id="S2Maybe", title="二 · Maybe = 1 + A", quote="", chapter="",
         refs=["DaoFP ch.7；CTFP 1.6（Maybe ≅ Either () a）"],
         beats=[
             dict(say="先看 Maybe。Maybe a 表示「也许有一个 a，也许没有」。两个构造子：Nothing，什么都没有；Just x，装着一个 x。像一个可能空的盒子。",
                  note="data Maybe；Nothing / Just 图示"),
             dict(say="用类型代数的语言：Maybe a 就是一加 a。一是单元类型——那个唯一的点；加号是 Either，二选一。要么选左边的点，要么选右边的 a。",
                  note="Maybe a ≅ Either () a ≅ 1 + A"),
             dict(say="选左边：只剩那一个点，没有额外信息——这就是 Nothing。选右边：带着一个 a——这就是 Just。盒子的两种打开方式，正好对应求和的两支。",
                  note="Left () ↔ Nothing；Right x ↔ Just x"),
             dict(say="所以 Maybe 不是凭空发明的关键字。它是终对象与余积拼出来的：把「有」和「一个 a」并排放在一起，就得到「也许有 a」。",
                  note="() + A → Maybe A；小字：terminal + coproduct"),
             dict(say="为什么程序员在乎？因为失败、缺失、尚未加载，都可以用同一形状表达——不必用魔法空值，也不必假装总有答案。",
                  note="小字：缺失 / 失败 / 尚未加载 → Maybe"),
             dict(say="日常比喻：Maybe 像一封可能空的信——要么信封是空的，要么里面有一张纸条。你拆开之前，两种可能都合法。",
                  note="信封：空 / 有纸条"),
         ]),

    dict(id="S3List", title="三 · List：递归", quote="", chapter="",
         refs=["DaoFP ch.7 Lists；CTFP 1.6（recursive ADT）"],
         beats=[
             dict(say="再看列表。列表的定义自己指回自己：要么是空列表，要么是「一个元素，再加上另一份列表」。空是终点；接上去的那一步，才是生长。",
                  note="Nil / Cons 图示；箭头指回 List"),
             dict(say="两个构造子：Nil，什么都没有，对应单元那一侧。Cons，吃一个头和一个尾，拼出更长的列表。尾的类型，还是列表本身——这就是递归。",
                  note="Nil :: List a；Cons :: a → List a → List a"),
             dict(say="空是无；接一个元素是一；再接一个是二。万物，就是任意长的列表。长度不封顶，因为 Cons 可以永远再套一层。",
                  note="[] / (1:[]) / (1:2:[]) 展开"),
             dict(say="跟 Maybe 对比：Maybe 的选择是有限的——有或没有，两支就够。列表的选择是开放的——每接一次，就多一个元素的位置。有限求和，对上无限递归。",
                  note="Maybe：有限 · List：递归"),
             dict(say="消解规则，是构造的反面：遇到 Nil，给一个起点；遇到 Cons，把头和已处理的尾合成一步。今天只点到这里——完整的折叠，留给下一集。",
                  note="init / step 示意；预告 fold"),
             dict(say="Milewski 提醒：递归构造子，是引入规则里自己用到自己的那一支。自然数用后继；列表用 Cons。形状不同，手法一样。",
                  tts="米列夫斯基提醒：递归构造子，是引入规则里自己用到自己的那一支。自然数用后继；列表用 Cons。形状不同，手法一样。",
                  note="小字：introduction rules · successor / Cons"),
         ]),

    dict(id="S4Grow", title="四 · 从无生长", quote="", chapter="",
         refs=["DaoFP ch.7；入门篇「道生一」计数直觉；CTFP 1.6"],
         beats=[
             dict(say="回到道生一。从「无」开始：Void 一个值都没有——这是零。Maybe 作用于 Void，只能是 Nothing——这是一。",
                  note="Void → Maybe Void；点数 0 → 1；书法「无 · 一」"),
             dict(say="再包一层：Maybe 的 Maybe 作用于 Void。两个可能：Nothing，或 Just Nothing——这是二。再一层，三个可能——这是三。",
                  note="Maybe² Void / Maybe³ Void；点数 2、3"),
             dict(say="每包一层，就多一个「在这一层停住」的选择。一层层包下去，选择越来越多——三生万物的感觉，就在精确的计数里。",
                  note="层数与值的个数对齐；「无一二三」"),
             dict(say="列表也是这样长出来的：Nil 是种子；Cons 一次，多一个格子。你不是在循环里「追加」，你是在用构造子声明形状——值跟着形状出现。",
                  note="Nil ─Cons→ Cons x Nil ─Cons→ …"),
             dict(say="自然数也是同一手法：零，或一个数的后继。列表把「后继」换成「再接一个元素」。形状不同，从无生长的节奏一样。",
                  note="Z / S ⟷ Nil / Cons"),
             dict(say="构造，是往外长；折叠，是往回收。今天只把「生」看清楚。收回去的那半边——fold 与 unfold——留给下一集。",
                  note="生 → ；归 ← ；预告折叠"),
         ]),

    dict(id="S5Haskell", title="五 · 落到代码", quote="", chapter="",
         refs=["DaoFP ch.7；CTFP 1.6"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。手写一份 Maybe，好看见构造子；再写出它跟 Either 单元的互转。",
                  note="代码块：s_maybe"),
             dict(say="fromEitherUnit：左边的单元变成 Nothing，右边的值变成 Just。toEitherUnit 反过来。类型写在前，同构藏在两支匹配里。",
                  note="高亮 fromEitherUnit / toEitherUnit"),
             dict(say="再看计数。One、Two、Three 是类型同义词：Maybe 套 Void，套两层，套三层。one、two、three 列出所有值——个数正好是一、二、三。",
                  note="代码 s_count；点数对齐"),
             dict(say="列表这边，手写 Nil 与 Cons。sumList 遇到空回零；遇到 Cons，头加上尾的总和。你只说清一步，递归替你走完全程——折叠的预告。",
                  note="代码 s_list；1:2:3 → 6"),
             dict(say="屏幕上的代码都能直接编译。自己写一遍构造子，是为了看见形状；用标准库的 Maybe 与列表，是为了日常省事。图对齐了，代码只是把图念出来。",
                  note="对照：图 ⟷ 代码"),
         ]),

    dict(id="S6Next", title="结 · 道生一", quote="", chapter="",
         refs=["DaoFP ch.11 / ch.12；CTFP 3.8；下一集构造与折叠"],
         beats=[
             dict(say="今天只钉牢两件事：Maybe 是一加 a，有限的选择；列表是递归的 Cons，无限的生长。从无包上去，一二三，万物跟着来。",
                  note="三句回顾环绕圆相"),
             dict(say="下一集，我们把方向反过来：构造往外长，折叠往回收；展开从种子生出列表，折叠再把列表收成一个值。先生，而后归。",
                  note="预告：构造与折叠 · fold / unfold；小字「深讲 04」"),
             dict(say="借 Milewski 的提醒：看构造子。道生一。我们下集见。",
                  tts="借米列夫斯基的提醒：看构造子。道生一。我们下集见。",
                  note="「看构造子」书法；印章；谢谢观看"),
         ]),
]
