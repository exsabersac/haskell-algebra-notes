# -*- coding: utf-8 -*-
"""Single source of truth for narration — 进阶深讲第 8 集：有无相生.

Audience: finished beginner 01–06 and advanced 07; ready for formal duality.
Deeper than beginner ep02 (Void/()): opposite category, products/coproducts, probes, negation.
CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("Yoneda", "米田"),
    ("DaoFP", "道 F P"),
    ("CTFP", "C T F P"),
    ("Void", "Void"),
    ("Either", "Either"),
    ("Hom", "Hom"),
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
    dict(id="S0Title", title="有无相生", quote="", chapter="", refs=[],
         beats=[
             dict(say="有无相生。欢迎来到「道可道」进阶深讲——第八集。",
                  note="宣纸背景，圆相一笔画出；标题「有无相生」浮现"),
             dict(say="上一集钉牢了认识论：对象不可道，箭头可道。今天换一把尺子：始对象与终对象——无与有。入门深讲第二集已经见过 Void 与单元；本集不再重复扫盲，而是把对偶写正式，并把积与余积一并收进同一面镜子。",
                  note="小字：进阶 07 → 08；提纲 对偶 / 积·余积"),
             dict(say="本集四根钉子：始与终的 Hom 定义；对偶范畴里箭头整体翻转；积与余积互为镜像；全局元素与否定。钉子钉稳，Haskell 只作短印证。",
                  note="四行提纲"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第一章的阴阳与元素，以及《程序员的范畴论》积与余积那一章。片中表述都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第一章的阴阳与元素，以及《程序员的范畴论》积与余积那一章。片中表述都是释义，不是照录。",
                  note="DaoFP ch.1 · CTFP 1.5/1.6；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道德经钩子", quote="有无相生，难易相成，长短相形，高下相倾。", chapter="《道德经》第二章",
         refs=["DaoFP ch.1 Clean Slate（Yin and Yang / Elements）",
               "CTFP 1.5 Products and Coproducts"],
         beats=[
             dict(say="有无相生，难易相成，长短相形，高下相倾。", note="竖排书法原文，右起"),
             dict(say="老子说，有和无互相生成。《函数式编程之道》把这一节就叫作阴与阳。进阶篇里，我们把这句话读成一条硬规则：几乎每一个构造，都有一个把箭头全部掉个头的孪生兄弟。",
                  note="阴与阳；对偶预告"),
             dict(say="入门第二集已经告诉你：Void 是始对象，单元类型是终对象。今天要问的不是「它们是什么」，而是「为什么它们是一对」——以及这对镜子怎样照出积与余积。",
                  note="不重复扫盲 · 问为什么是一对"),
             dict(say="哲学仍是钩子。门后站着的是普遍性质：用 Hom 集合里「恰好一条箭头」来定义极端对象；再用对偶，把定义翻成另一侧。",
                  note="普遍性质 · Hom 唯一性"),
             dict(say="节奏照旧：先范畴论，后短 Haskell；证明语气要准，代码只负责把图念出来。",
                  note="本集路线图"),
         ]),

    dict(id="S2InitialTerminal", title="二 · 始与终", quote="", chapter="",
         refs=["DaoFP ch.1 Elements；CTFP 1.5 Initial / Terminal"],
         beats=[
             dict(say="先把定义钉死。始对象——记作零——对每个对象 a，从零到 a 的箭头存在且唯一。写成 Hom 的话：Hom 零 a 是单点集。存在，保证有路；唯一，保证没有两条可区分的路。",
                  note="始对象：∃! 0 → a；Hom(0,a)≅1"),
             dict(say="终对象——记作一——对每个对象 a，从 a 到一的箭头存在且唯一。Hom a 一 也是单点集。同一句话，只把箭头的脚和头对调。",
                  note="终对象：∃! a → 1；Hom(a,1)≅1"),
             dict(say="在 Hask 里——依惯例忽略底——零就是 Void，一就是单元类型。absurd 见证始对象的出射；const 单元见证终对象的入射。唯一性藏在类型里：没有输入可以区分两条 absurd；终点只有一个值，也区分不了两条 const。",
                  note="Hask：Void=0，()=1"),
             dict(say="注意：定义里从不打开对象。不问 Void「里面有没有元素」，只问从它出发有几支箭头。这与上一集「对象不可道、箭头可道」完全同调——极端对象，是用箭头计数标出来的。",
                  note="用箭头计数 · 不打开内部"),
             dict(say="所以始与终不是两个故事，是同一句模板的两个朝向。下一节，把「朝向」写成对偶范畴。",
                  note="过渡到对偶范畴"),
         ]),

    dict(id="S3Opposite", title="三 · 对偶范畴", quote="", chapter="",
         refs=["DaoFP ch.1 Yin and Yang；CTFP 1.5 dual / opposite category"],
         beats=[
             dict(say="对偶范畴 C 的 op：对象原样不动，每一支箭头掉头——原来从 a 到 b，现在从 b 到 a；复合的顺序跟着反。整张图翻个面，公理一个字都不用改。",
                  note="Cᵒᵖ：对象同，箭头反向"),
             dict(say="于是一句定理几乎免费：C 里的始对象，恰好是 C op 里的终对象；C 里的终对象，恰好是 C op 里的始对象。无，是倒过来看的有。",
                  note="0_C = 1_{Cᵒᵖ}"),
             dict(say="这不是修辞。你每证明一条关于始对象的命题，只要把所有箭头掉个头，就白得一条关于终对象的命题。对偶是生产力，不是装饰。",
                  note="定理 ⟷ 对偶定理"),
             dict(say="Milewski 用阴阳来喊这一对。进阶篇后面会一次次回到这个动作：代数对余代数、单子对余单子、左伴随对右伴随——全是同一面镜子。",
                  tts="米列夫斯基用阴阳来喊这一对。进阶篇后面会一次次回到这个动作：代数对余代数、单子对余单子、左伴随对右伴随——全是同一面镜子。",
                  note="阴阳贯穿后集"),
             dict(say="老子另有一句话描述这个动作：反者道之动。第四段的预告先别展开；今天先把镜子握在手里。",
                  note="预告：反者道之动"),
         ]),

    dict(id="S4ProdCoprod", title="四 · 积与余积", quote="", chapter="",
         refs=["CTFP 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types",
               "DaoFP ch.1"],
         beats=[
             dict(say="镜子一照，运算也成对出现。积：给定 a 与 b，找一个对象 a 乘 b，带着两支投影，使得任何一对箭头都唯一地媒介出来。余积——和——把投影换成注入，箭头方向全部反过来。",
                  note="积 ↔ 余积：投影 ↔ 注入"),
             dict(say="在 Hask 里，积是配对，余积是 Either。一对值同时持有两边；Either 是「左边或者右边」。同一套普遍性质，只差箭头朝向。",
                  note="(a,b) ↔ Either a b"),
             dict(say="始对象与终对象，正是这两种运算的单位。Void 是和的单位：Either Void a 同构于 a——空的那一支永远用不上。单元类型是积的单位：跟谁配对，都不增加信息。",
                  note="Either Void a ≅ a；((), a) ≅ a"),
             dict(say="所以有无相生，不只是两个极端对象的绰号。零与一，立在类型代数的两端；加与乘——余积与积——从这根标尺长出来。入门第二集点到单位律；本集把它嵌回对偶与普遍性质。",
                  note="0/1 为类型代数标尺"),
             dict(say="再进一步：积是终对象式的想法——用「入射的配对」来刻画；余积是始对象式的想法——用「出射的分支」来刻画。学会这一对，后面极限与余极限只是把「一对」换成「一大家族」。",
                  note="极限/余极限预告"),
         ]),

    dict(id="S5ProbeNegation", title="五 · 探针与否定", quote="", chapter="",
         refs=["DaoFP ch.1 Elements；CTFP 1.5 / 1.6"],
         beats=[
             dict(say="有，还是探针。从单元类型射向 a 的每一支箭头，都挑出 a 的一个全局元素。写成类型：单元箭头 a。元素这个词，上一集说不在范畴词典里——它借终对象重新进场，而且只作为箭头出现。",
                  note="() → a 即全局元素"),
             dict(say="没有任何箭头从有射向无——Hom 一 零 是空集——所以 Void 没有全局元素。这与「Void 零个值」是同一句话的箭头说法。",
                  note="Hom(1,0)=∅"),
             dict(say="反过来，一个以 Void 为终点的函数，等于宣告它的定义域「不可能有元素」。构造逻辑里，这正是否定：Not a，等于 a 箭头 Void。",
                  note="type Not a = a → Void"),
             dict(say="于是阴阳又咬合一次：有用来指认「有什么」；无用来陈述「不可能」。探针与否定，是终对象与始对象在逻辑侧的投影。",
                  note="有=指认 · 无=不可能"),
             dict(say="把箭头整体翻转，几乎每个构造都会得到孪生兄弟。今天握紧这面镜子；后面「反者道之动」会把翻转写成生产力。",
                  note="收束到翻转"),
         ]),

    dict(id="S6Haskell", title="六 · 短 Haskell", quote="", chapter="",
         refs=["DaoFP ch.1；CTFP 1.6；本集 haskell/src/YouWu.hs"],
         beats=[
             dict(say="把刚才的话写成几行 Haskell。wu 是 Void 到 a，实现 absurd；you 是 a 到单元，实现 const 单元。两支箭头，一出一入——始与终的见证。",
                  note="代码 s_wu / s_you"),
             dict(say="单位律：sumUnit 吃掉 Either Void a，左支交给 absurd，右支原样通过——空的「或者」消失。prodUnit 取配对的第二个分量——单元不增加信息。",
                  note="代码 s_units"),
             dict(say="探针：element 把一个值收成「从单元指向它」的箭头。否定：类型同义词 Not a，等于 a 到 Void。逻辑侧的有无，写在类型里。",
                  note="代码 s_probe"),
             dict(say="跑一下：element 四十二再应用到单元，得到四十二。sumUnit 放行 Right 七。demoNot 取成 Void 上的恒等——唯一「成立」的否定，是否定无本身。",
                  note="demo"),
             dict(say="图怎么说，代码就怎么应。唯一性不必手写证明：类型系统不许你写出第二条可区分的 absurd。进阶篇的 Haskell，始终是短印证，不是语法课。",
                  note="图 ⟷ 代码"),
         ]),

    dict(id="S7Next", title="结 · 下集道生一", quote="", chapter="",
         refs=["下集预告：道生一 · 初始代数"],
         beats=[
             dict(say="今天钉牢四件事：始与终用 Hom 唯一性定义；对偶范畴把无翻成有；积与余积互为镜像，零一是它们的单位；全局元素与否定，是有无在逻辑侧的投影。",
                  note="四句回顾环绕圆相"),
             dict(say="下一集《道生一》：从无出发，反复作用一个函子，取余极限——初始代数。Maybe 作用在 Void 上，一生二，二生三；万物从无中长出。有无相生的下一章，是生长。",
                  note="预告：初始代数 · Adámek"),
             dict(say="借 Milewski 的提醒：先看箭头，再谈翻转。有无相生。进阶篇，我们下集见。",
                  tts="借米列夫斯基的提醒：先看箭头，再谈翻转。有无相生。进阶篇，我们下集见。",
                  note="「有无相生」书法；印章；谢谢观看"),
         ]),
]
