# -*- coding: utf-8 -*-
"""Single source of truth for narration — 进阶深讲第 12 集（系列终章）：无为而无不为.

Audience: finished beginner 01–06 and advanced 07–11.
Pays off ep07's 道可道 Yoneda tease: objects ineffable, arrows speakable;
Yoneda lemma = object determined by Hom(a,−); Yoneda embedding fully faithful;
Yoneda ≅ Ran Identity; Mac Lane: all concepts are Kan extensions.
CT first, then short Haskell.
"""

TTS_FIX = [
    ("Milewski", "米列夫斯基"),
    ("Haskell", "哈斯凯尔"),
    ("DaoFP", "道 F P"),
    ("CTFP", "C T F P"),
    ("Yoneda", "米田"),
    ("Mac Lane", "麦克莱恩"),
    ("Kan", "康"),
    ("Ran", "右康扩张"),
    ("Lan", "左康扩张"),
    ("fmap", "f map"),
    ("forall", "for all"),
    ("Identity", "恒等"),
    ("Speak", "Speak"),
    ("CPS", "续体传递"),
    ("η", "伊塔"),
    ("ε", "艾普西隆"),
]


def tts_text(beat):
    if "tts" in beat:
        return beat["tts"]
    s = beat["say"]
    for a, b in TTS_FIX:
        s = s.replace(a, b)
    return s


SCENES = [
    dict(id="S0Title", title="无为而无不为", quote="", chapter="", refs=[],
         beats=[
             dict(say="道常无为而无不为。欢迎来到「道可道」进阶深讲——第十二集，也是本系列的终章。",
                  note="宣纸背景，圆相一笔画出；标题「无为而无不为」浮现"),
             dict(say="第七集钉过一句话：对象不可道，箭头可道；并把米田轻轻挂上，说后集赎回。今天，就是赎回的日子。",
                  note="回扣进阶 07：对象不可道 · 待赎回"),
             dict(say="本集四根钉子：可表函子；米田引理——对象由箭头决定；Haskell 里的 Yoneda 与 forall；Kan 扩张——Ran 与 Lan 的直觉。最后，整条系列回到道可道。",
                  note="四行提纲"),
             dict(say="框架仍是 Milewski 的两本书：《函数式编程之道》第九章、第二十章，与《程序员的范畴论》里米田与 Kan 各章。片中都是释义，不是照录。",
                  tts="框架仍是米列夫斯基的两本书：《函数式编程之道》第九章、第二十章，与《程序员的范畴论》里米田与康各章。片中都是释义，不是照录。",
                  note="DaoFP ch.9 / 20 · CTFP 2.5 / 2.6 / 3.11；印章「知白守黑」"),
         ]),

    dict(id="S1Hook", title="一 · 道德经钩子", quote="道常无为而无不为。", chapter="《道德经》第三十七章",
         refs=["DaoFP ch.2 Composition（Identity = wu wei）", "DaoFP ch.9 The Yoneda Lemma", "CTFP 2.5"],
         beats=[
             dict(say="道常无为而无不为。", note="竖排书法原文，右起"),
             dict(say="无为，不是什么都不做；是不做多余的事。DaoFP 第二章把恒等箭头称为无为：什么也不改变，也不花时间。米田的证明，正是从一支恒等出发。",
                  tts="无为，不是什么都不做；是不做多余的事。道 F P 第二章把恒等箭头称为无为：什么也不改变，也不花时间。米田的证明，正是从一支恒等出发。",
                  note="id = wu wei；一支自环"),
             dict(say="无不为，是说：正因为不掺私货，它被完全确定，因而能应对一切。喂给它 id，就得到一个值；有了值，用 fmap 就能应对任何箭头。",
                  note="fromYoneda = g id；toYoneda = fmap"),
             dict(say="第七集留下的漏洞是：若对象不可言说，凭什么断定两个对象相同？米田说：看它们出发的全部箭头是否自然同构。同构，在范畴论里就是相同的全部含义。",
                  note="回扣 a ≅ b ? → Hom(a,−) ≅ Hom(b,−)"),
             dict(say="今天的路线：先认识可表函子，再陈述米田引理，落到 Haskell 的 forall，再瞥一眼 Kan 扩张，最后用米田嵌入把道可道整句赎回。",
                  note="本集路线图"),
         ]),

    dict(id="S2Representable", title="二 · 可表函子", quote="", chapter="",
         refs=["DaoFP ch.9 Representable Functors", "CTFP 2.5 The Yoneda Lemma（前置）"],
         beats=[
             dict(say="从一个对象 a 出发，对每个对象 x，收集从 a 到 x 的全部箭头，得到一个集合 Hom(a, x)。这对 x 是函子：箭头 f 从 x 到 y，就把 g 后复合变成 f 复合 g。",
                  note="Hom(a, −) : C → Set；后复合"),
             dict(say="这个函子叫可表函子，a 是它的表示元。反过来，从 a 射入的箭头，给出反变可表函子 Hom(−, a)。正变看出去，反变看进来。",
                  note="可表 · 表示元 a；Hom(−, a) 反变"),
             dict(say="可表的意思是：这个函子长得像某个 Hom。若 F 与 Hom(a, −) 自然同构，就说 F 被 a 表示。a 是什么？是那支被挑出来的「万能箭头」所瞄准的对象。",
                  note="F ≅ Hom(a, −) ⇒ F 被 a 表示"),
             dict(say="Haskell 程序员天天见可表：从 a 出发的函数类型，a 到 x，就是 Hom(a, x)。continuation 类型 Speak a，是把 Hom(a, −) 喂进一个「取元素」的函子——后面赎回会用到。",
                  note="(a → −) 可表；Speak a = forall x. (a → x) → x"),
             dict(say="米田引理要回答的，正是：自然变换从 Hom(a, −) 到任意函子 F，长什么样？答案短得惊人——它们一一对应于 F 在 a 上的一个元素。",
                  note="Nat(Hom(a,−), F) ≅ F a"),
         ]),

    dict(id="S3Yoneda", title="三 · 米田引理", quote="", chapter="",
         refs=["DaoFP ch.9 The Yoneda Lemma；Yoneda lemma in programming", "CTFP 2.5 The Yoneda Lemma"],
         beats=[
             dict(say="陈述。设 F 是从 C 到集合范畴的函子。从可表函子 Hom(a, −) 到 F 的自然变换，与 F 在 a 处的元素，一一对应。",
                  note="Nat(C(a,−), F) ≅ F(a)"),
             dict(say="为什么？一个自然变换 α，对每个 x，给出从 Hom(a, x) 到 F x 的函数。它必须对后复合自然。取 x 等于 a，左边有一支现成的箭头：恒等。α 在恒等上的值，就是 F a 里的那个元素。",
                  note="α_a(id_a) ∈ F a；无为：只看 id"),
             dict(say="反过来，有了 F a 里的一个元素，怎么造出整族 α？对任意箭头 h 从 a 到 x，用 F 作用在 h 上，推到 F x。自然性保证：这样做出来的，恰好是唯一可能的那一个。",
                  note="α_x(h) = F(h)(ξ)；无不为"),
             dict(say="所以：无为——它不能检查 x，不能凭空造 x，只能把你给的箭头原样用上；无不为——正因为如此，整族变换被一个元素完全钉死。",
                  note="参数性 / 自然性 = 无为而无不为"),
             dict(say="取 F 为另一个可表函子 Hom(b, −)，就得到米田嵌入：从 a 到 b 的箭头，一一对应 Hom(a, −) 到 Hom(b, −) 的自然变换。嵌入是满忠实的。",
                  note="C(a,b) ≅ Nat(Hom(a,−), Hom(b,−))；满忠实"),
             dict(say="于是：两个对象同构，当且仅当它们的可表函子自然同构。对象不可道；「它的全部说法」可道——而且恰好够用。第七集挂起的那句话，在这里落地。",
                  note="a ≅ b ⟺ C(a,−) ≅ C(b,−)；赎回"),
         ]),

    dict(id="S4Haskell", title="四 · Haskell：Yoneda 与 forall", quote="", chapter="",
         refs=["DaoFP ch.9 Yoneda lemma in programming", "CTFP 2.5；本集 haskell/src/WuWei.hs"],
         beats=[
             dict(say="落到 Haskell。Yoneda f a，就是对一切 x，给定从 a 到 x 的箭头，产出一个 f x。米田说：它与 f a 同构。",
                  note="代码 s_yoneda：newtype Yoneda"),
             dict(say="toYoneda 有了 f a，用 fmap 应对任何箭头——无不为。fromYoneda 只喂给它 id——无为。来回一圈，回到原处。",
                  note="toYoneda / fromYoneda 高亮"),
             dict(say="Functor 实例更妙：fmap 在 Yoneda 里不做真正的映射，只把函数复合攒起来。一连串 fmap，什么也不做，直到 fromYoneda 的那一刻一次完成。无为，也是一种优化。",
                  note="fmap h . fmap g ⇒ 一次复合"),
             dict(say="取 f 为恒等函子：Speak a，对一切 x 能把 a 到 x 变成 x 的东西，同构于 a 本身。redeem 只给它 id。这正是续体传递风格的最小种子——第七集写下的 Speak，今天赎回。",
                  note="代码 s_redeem；回看 ep07 Speak"),
             dict(say="跑一下：列表包进 Yoneda，连 fmap 三次，最后取出，等于一次 fmap 复合；Speak 的 hear 与 redeem 互逆。代码怎么写，米田就怎么说。",
                  note="demo 输出"),
         ]),

    dict(id="S5Kan", title="五 · Kan 扩张：Ran 与 Lan", quote="", chapter="",
         refs=["DaoFP ch.20 Kan Extensions；Right Kan extension in Haskell", "CTFP 3.11 Kan Extensions", "Mac Lane: All concepts are Kan extensions"],
         beats=[
             dict(say="最后抬眼看一层。你有函子 f，从 A 到 C；还有一支「道路」函子 p，从 A 到 B。问：怎样把 f 沿着 p「扩张」到整个 B 上？",
                  note="f : A → C；p : A → B；扩张到 B → C"),
             dict(say="右 Kan 扩张 Ran_p f，是最「保守」的扩张：在 B 的每个点，收集所有从该点到 p 像的箭头，再喂给 f——Haskell 里写成 forall。左 Kan 扩张 Lan 是对偶的「最慷慨」一侧。",
                  note="Ran p f a = forall b. (a → p b) → f b；Lan 对偶"),
             dict(say="普遍性：任何其他扩张，都唯一地经过它。Ran 是右伴随意义下的最佳逼近；Lan 是左伴随意义下的。极限、伴随、米田——都可以写成某次 Kan 扩张。",
                  note="普遍性；lim / ⊣ / Yoneda ⊆ Kan"),
             dict(say="特例：p 取恒等函子。右 Kan 扩张还原 f 自身——而 Yoneda f，恰好就是 Ran Identity f。米田不是旁边的小岛，是 Kan 扩张的海岸线。",
                  note="Yoneda f ≅ Ran Identity f"),
             dict(say="Mac Lane 有一句几乎成了口号：所有概念都是 Kan 扩张。极限是，伴随是，米田也是。今天只取其直觉：无为而无不为——沿恒等扩张，什么也没加，却什么都能说。",
                  tts="麦克莱恩有一句几乎成了口号：所有概念都是康扩张。极限是，伴随是，米田也是。今天只取其直觉：无为而无不为——沿恒等扩张，什么也没加，却什么都能说。",
                  note="All concepts are Kan extensions"),
         ]),

    dict(id="S6Close", title="结 · 回到道可道", quote="", chapter="",
         refs=["系列收束：道可道 · 看箭头"],
         beats=[
             dict(say="回顾本集：可表函子是 Hom；米田引理说自然变换被一个元素钉死；Haskell 的 Yoneda 与 Speak 是它的字面翻译；Kan 扩张把米田收进更大的版图。",
                  note="四句回顾环绕圆相"),
             dict(say="再回看整条系列。从无与有，到生与归；从雄与雌，到无为。六句《道德经》，六次换挡，其实只说了一件事：结构在箭头里。",
                  note="六句小字环绕；系列地图"),
             dict(say="第七集问：对象不可道，凭什么说相同？今天答：全部说法自然同构，就是同构。不可道的对象，被可道的箭头之全体赎回了。",
                  note="道可道，非常道；米田嵌入满忠实"),
             dict(say="借 Milewski 书里米田大师的一句话：看箭头。道可道，非常道。无为而无不为。谢谢观看——「道可道」系列，到此完结。",
                  tts="借米列夫斯基书里米田大师的一句话：看箭头。道可道，非常道。无为而无不为。谢谢观看——「道可道」系列，到此完结。",
                  note="「看箭头」书法；印章；系列完结"),
         ]),
]
