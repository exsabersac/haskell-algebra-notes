# -*- coding: utf-8 -*-
"""Manim scenes for 进阶深讲 08 · 有无相生."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from content import SCENES

META = {s["id"]: s for s in SCENES}


def meta_cls(sid):
    m = META[sid]
    return dict(SID=sid, QUOTE=m["quote"], TITLE=m["title"], CHAPTER=m["chapter"])


# =====================================================================================
class S0Title(TaoScene):
    SID = "S0Title"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=19).move_to([0, 0.55, 0]))
        title = callig("有无相生", size=84).move_to([0, 0.62, 0])
        sub = body("道可道 · 进阶深讲 08 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("始 / 终 · 对偶 · 积与余积", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("进阶 07 道可道", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("进阶 08", size=32, color=INK),
            body("对偶正式上场", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.28).move_to([2.0, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.52).move_to([-4.35, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  始与终 · Hom 唯一性", size=30),
            body("②  对偶范畴 Cᵒᵖ", size=30),
            body("③  积 ↔ 余积", size=30),
            body("④  探针与否定", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.3, 0.05, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.48)
        refs = VGroup(
            body("参考：DaoFP ch.1  ·  CTFP 1.5–1.6", size=24, color=INK3),
            serif("Bartosz Milewski", size=28, color=INK2),
        ).arrange(DOWN, buff=0.12).move_to([2.3, -2.25, 0])
        s = seal(0.75).next_to(left, DOWN, buff=0.15).shift(RIGHT * 1.2)
        with self.beat(3):
            self.play(FadeIn(refs, shift=UP * 0.1), run_time=1.0)
            self.at(3, 0.55)
            self.play(FadeIn(s, scale=1.5), run_time=0.5)
        self.end_scene()


# =====================================================================================
class S1Hook(TaoScene):
    locals().update(meta_cls("S1Hook"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        yin = VGroup(
            body("阴 · 无 · Void · 始", size=30, color=INK2),
            body("阳 · 有 · () · 终", size=30, color=INK2),
            body("几乎每个构造都有孪生兄弟", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.35, 0])
        with self.beat(1):
            self.play(FadeIn(yin), run_time=1.5)
        deeper = VGroup(
            body("入门 02 已见 Void / ()", size=28, color=INK3),
            body("本集问：为什么它们是一对？", size=32, color=INK),
            body("镜子怎样照出积与余积？", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(yin), run_time=0.35)
            self.play(FadeIn(deeper), run_time=1.5)
        univ = VGroup(
            body("普遍性质", size=28, color=INK3),
            body("Hom 里「恰好一条箭头」", size=34, color=INK),
            body("对偶 = 把定义翻到另一侧", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(deeper), run_time=0.35)
            self.play(FadeIn(univ), run_time=1.5)
        road = VGroup(
            body("① 始终 → ② 对偶 → ③ 积余积 → ④ 探针 → Haskell", size=26, color=INK2),
            callig("翻转", size=56, color=INK),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(univ), run_time=0.35)
            self.play(FadeIn(road), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S2InitialTerminal(TaoScene):
    SID = "S2InitialTerminal"
    QUOTE = ""
    TITLE = "二 · 始与终"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: initial
        zero = ink_blob(0.45, seed=3).move_to([-3.6, 0.5, 0])
        lz = mixed("0", size=32, color=INK2).next_to(zero, DOWN, buff=0.3)
        targets = VGroup(*[ink_blob(0.32, seed=5 + i).move_to([0.2 + i * 1.7, 1.4 - (i % 2) * 1.6, 0]) for i in range(3)])
        labs = VGroup(*[mixed(n, size=24, color=INK2).next_to(t, DOWN, buff=0.2) for t, n in zip(targets, ["a", "b", "c"])])
        arrs = VGroup(*[arrow(zero, t, color=INK) for t in targets])
        cap0 = VGroup(
            mixed("∃!  0 → a", size=32, color=SEAL),
            mixed("Hom(0, a) ≅ 1", size=28, color=TYPE_C),
        ).arrange(DOWN, buff=0.2).move_to([2.8, -2.2, 0])
        with self.beat(0):
            self.play(FadeIn(zero, scale=0.7), FadeIn(lz), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in targets], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.15), run_time=1.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), run_time=1.2)
            self.play(FadeIn(cap0), run_time=0.6)
            self._init = VGroup(zero, lz, targets, labs, arrs, cap0)
        # beat 1: terminal
        one = ink_blob(0.45, seed=8).move_to([3.6, 0.5, 0])
        lo = mixed("1", size=32, color=INK2).next_to(one, DOWN, buff=0.3)
        srcs = VGroup(*[ink_blob(0.32, seed=11 + i).move_to([-3.4 + i * 1.7, 1.4 - (i % 2) * 1.6, 0]) for i in range(3)])
        labs2 = VGroup(*[mixed(n, size=24, color=INK2).next_to(t, DOWN, buff=0.2) for t, n in zip(srcs, ["a", "b", "c"])])
        arrs2 = VGroup(*[arrow(t, one, color=INK) for t in srcs])
        cap1 = VGroup(
            mixed("∃!  a → 1", size=32, color=SEAL),
            mixed("Hom(a, 1) ≅ 1", size=28, color=TYPE_C),
        ).arrange(DOWN, buff=0.2).move_to([-2.6, -2.2, 0])
        with self.beat(1):
            self.play(FadeOut(self._init), run_time=0.4)
            self.play(FadeIn(one, scale=0.7), FadeIn(lo), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in srcs], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(l) for l in labs2], lag_ratio=0.15), run_time=1.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs2], lag_ratio=0.2), run_time=1.2)
            self.play(FadeIn(cap1), run_time=0.6)
            self._term = VGroup(one, lo, srcs, labs2, arrs2, cap1)
        # beat 2: Hask
        hask = VGroup(
            mixed("Hask（忽略 ⊥）", size=28, color=INK3),
            mixed("0 = Void    1 = ()", size=36, color=INK),
            mixed("wu = absurd    you = const ()", size=30, color=TYPE_C),
            body("唯一性藏在类型里", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(2):
            self.play(FadeOut(self._term), run_time=0.4)
            self.play(FadeIn(hask), run_time=1.5)
        # beat 3: arrows not insides
        note = VGroup(
            callig("不打开", size=56),
            body("不问里面有没有元素", size=30, color=INK2),
            body("只问：从它出发有几支箭头", size=28, color=SEAL),
            body("与「对象不可道」同调", size=28, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(3):
            self.play(FadeOut(hask), run_time=0.35)
            self.play(FadeIn(note), run_time=1.5)
        hand = VGroup(
            body("同一句模板 · 两个朝向", size=32, color=INK),
            body("下一节：对偶范畴", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.35).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(note), run_time=0.35)
            self.play(FadeIn(hand), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S3Opposite(TaoScene):
    SID = "S3Opposite"
    QUOTE = ""
    TITLE = "三 · 对偶范畴"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: C^op definition
        a = ink_blob(0.4, seed=5).move_to([-2.8, 0.6, 0])
        b = ink_blob(0.4, seed=9).move_to([1.6, 0.6, 0])
        la = mixed("a", size=28, color=INK2).next_to(a, DOWN, buff=0.35)
        lb = mixed("b", size=28, color=INK2).next_to(b, DOWN, buff=0.35)
        ar = arrow(a, b, color=INK)
        lab = mixed("f : a → b", size=26, color=TYPE_C).next_to(ar, UP, buff=0.2)
        flip = mixed("Cᵒᵖ：fᵒᵖ : b → a", size=30, color=SEAL).move_to([-0.6, -1.8, 0])
        with self.beat(0):
            self.play(FadeIn(a, scale=0.7), FadeIn(b, scale=0.7), FadeIn(la), FadeIn(lb), run_time=1.0)
            self.play(GrowArrow(ar), FadeIn(lab), run_time=0.9)
            self.at(0, 0.45)
            ar2 = arrow(b, a, color=SEAL)
            lab2 = mixed("掉头", size=26, color=SEAL).next_to(ar2, DOWN, buff=0.15)
            self.play(FadeOut(ar), FadeOut(lab), GrowArrow(ar2), FadeIn(lab2), FadeIn(flip), run_time=1.2)
            self._opp = VGroup(a, b, la, lb, ar2, lab2, flip)
        # beat 1: theorem
        thm = VGroup(
            body("几乎免费的定理", size=28, color=INK3),
            mixed("0_C  =  1_{Cᵒᵖ}", size=40, color=TYPE_C),
            mixed("1_C  =  0_{Cᵒᵖ}", size=40, color=TYPE_C),
            body("无，是倒过来看的有", size=30, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(1):
            self.play(FadeOut(self._opp), run_time=0.4)
            self.play(FadeIn(thm), run_time=1.5)
        # beat 2: productivity
        prod = VGroup(
            callig("对偶是生产力", size=48),
            body("证明一条关于始的命题", size=30, color=INK2),
            body("箭头掉头 → 白得终的命题", size=30, color=SEAL),
            mixed("定理  ⟺  对偶定理", size=32, color=TYPE_C),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(2):
            self.play(FadeOut(thm), run_time=0.35)
            self.play(FadeIn(prod), run_time=1.5)
        # beat 3: yin yang future
        future = VGroup(
            body("阴阳贯穿后集", size=28, color=INK3),
            body("代数 ↔ 余代数", size=32, color=INK),
            body("单子 ↔ 余单子", size=32, color=INK),
            body("左伴随 ↔ 右伴随", size=32, color=INK),
            body("同一面镜子", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([-0.2, 0.2, 0])
        with self.beat(3):
            self.play(FadeOut(prod), run_time=0.35)
            self.play(FadeIn(future), run_time=1.5)
        # beat 4: preview 反者道之动
        preview = VGroup(
            callig("反者道之动", size=56),
            body("翻转写成生产力 · 后集展开", size=28, color=INK2),
            body("今天先把镜子握紧", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(future), run_time=0.35)
            self.play(FadeIn(preview), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S4ProdCoprod(TaoScene):
    SID = "S4ProdCoprod"
    QUOTE = ""
    TITLE = "四 · 积与余积"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: product vs coproduct
        left = VGroup(
            body("积", size=36, color=INK),
            mixed("a × b", size=32, color=TYPE_C),
            body("两支投影", size=26, color=INK2),
            body("入射式媒介", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([-3.2, 0.4, 0])
        right = VGroup(
            body("余积（和）", size=36, color=INK),
            mixed("a + b", size=32, color=TYPE_C),
            body("两支注入", size=26, color=INK2),
            body("出射式媒介", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([2.6, 0.4, 0])
        mirror = DashedLine([ -0.4, 2.2, 0], [-0.4, -1.8, 0], color=INK3, dash_length=0.12)
        mid = body("箭头掉头", size=26, color=SEAL).move_to([-0.4, -2.3, 0])
        with self.beat(0):
            self.play(FadeIn(left), FadeIn(right), FadeIn(mirror), FadeIn(mid), run_time=1.6)
            self._pair = VGroup(left, right, mirror, mid)
        # beat 1: Hask
        hask = VGroup(
            mixed("(a, b)     ↔     Either a b", size=34, color=TYPE_C),
            body("配对：同时持有两边", size=28, color=INK2),
            body("Either：左边或者右边", size=28, color=INK2),
            body("同一套普遍性质 · 只差朝向", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(1):
            self.play(FadeOut(self._pair), run_time=0.4)
            self.play(FadeIn(hask), run_time=1.5)
        # beat 2: units
        units = VGroup(
            body("运算的单位", size=28, color=INK3),
            mixed("Either Void a  ≅  a", size=34, color=TYPE_C),
            mixed("((), a)        ≅  a", size=34, color=TYPE_C),
            body("无 = 和的单位 · 有 = 积的单位", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(2):
            self.play(FadeOut(hask), run_time=0.35)
            self.play(FadeIn(units), run_time=1.5)
        # beat 3: algebra of types
        alg = VGroup(
            callig("零与一", size=56),
            body("立在类型代数的两端", size=30, color=INK2),
            body("加与乘——余积与积——从标尺长出", size=28, color=INK3),
            body("单位律嵌回对偶与普遍性质", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(3):
            self.play(FadeOut(units), run_time=0.35)
            self.play(FadeIn(alg), run_time=1.5)
        # beat 4: limits tease
        lim = VGroup(
            body("积 ≈ 终对象式想法", size=30, color=INK),
            body("余积 ≈ 始对象式想法", size=30, color=INK),
            body("极限 / 余极限 = 把「一对」换成「一大家族」", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(alg), run_time=0.35)
            self.play(FadeIn(lim), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S5ProbeNegation(TaoScene):
    SID = "S5ProbeNegation"
    QUOTE = ""
    TITLE = "五 · 探针与否定"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: global element
        unit = ink_blob(0.35, seed=2).move_to([-3.2, 0.5, 0])
        lu = mixed("1", size=28, color=INK2).next_to(unit, DOWN, buff=0.3)
        aa = ink_blob(0.55, seed=12).move_to([1.5, 0.5, 0])
        la = mixed("a", size=28, color=INK2).next_to(aa, DOWN, buff=0.35)
        ar = arrow(unit, aa, color=SEAL)
        lab = mixed("() → a", size=30, color=TYPE_C).next_to(ar, UP, buff=0.2)
        tip = body("全局元素 · 借终对象进场的「元素」", size=28, color=SEAL).move_to([-0.4, -2.0, 0])
        with self.beat(0):
            self.play(FadeIn(unit, scale=0.7), FadeIn(lu), FadeIn(aa, scale=0.7), FadeIn(la), run_time=1.0)
            self.play(GrowArrow(ar), FadeIn(lab), run_time=0.9)
            self.play(FadeIn(tip), run_time=0.6)
            self._probe = VGroup(unit, lu, aa, la, ar, lab, tip)
        # beat 1: no arrow 1→0
        empty = VGroup(
            mixed("Hom(1, 0)  =  ∅", size=40, color=TYPE_C),
            body("没有任何箭头从有射向无", size=30, color=INK2),
            body("Void 没有全局元素", size=30, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(self._probe), run_time=0.4)
            self.play(FadeIn(empty), run_time=1.5)
        # beat 2: negation
        neg = VGroup(
            mixed("Not a  =  a → Void", size=38, color=TYPE_C),
            body("以无为终点 = 定义域不可能有元素", size=28, color=INK2),
            body("构造逻辑里的否定", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(empty), run_time=0.35)
            self.play(FadeIn(neg), run_time=1.5)
        # beat 3: bite again
        bite = VGroup(
            body("有 = 指认「有什么」", size=32, color=INK),
            body("无 = 陈述「不可能」", size=32, color=INK),
            body("探针与否定 · 逻辑侧的投影", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(neg), run_time=0.35)
            self.play(FadeIn(bite), run_time=1.4)
        # beat 4: close
        close = VGroup(
            callig("翻转", size=64),
            body("几乎每个构造都有孪生兄弟", size=28, color=INK2),
            body("镜子握紧 · 后集写成生产力", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(bite), run_time=0.35)
            self.play(FadeIn(close), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S6Haskell(TaoScene):
    SID = "S6Haskell"
    QUOTE = ""
    TITLE = "六 · 短 Haskell"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        code_w = make_code("s_wu", size=26, line_h=0.42).place(-6.2, 1.8)
        code_y = make_code("s_you", size=26, line_h=0.42).place(-6.2, -0.4)
        with self.beat(0):
            self.play(code_w.write(), run_time=1.2)
            self.play(code_y.write(), run_time=1.2)
            tip = body("一出一入 · 始与终的见证", size=26, color=SEAL).move_to([3.4, -2.2, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._cw, self._cy, self._tip = code_w, code_y, tip
        code_u = make_code("s_units", size=24, line_h=0.40).place(-6.2, 2.0)
        with self.beat(1):
            self.play(FadeOut(self._cw), FadeOut(self._cy), FadeOut(self._tip), run_time=0.4)
            self.play(code_u.write(), run_time=1.6)
            tip2 = body("和的单位 · 积的单位", size=26, color=TYPE_C).move_to([3.5, -2.3, 0])
            self.play(FadeIn(tip2), run_time=0.5)
            self._cu, self._tip2 = code_u, tip2
        code_p = make_code("s_probe", size=26, line_h=0.42).place(-6.2, 1.6)
        with self.beat(2):
            self.play(FadeOut(self._cu), FadeOut(self._tip2), run_time=0.4)
            self.play(code_p.write(), run_time=1.5)
            tip3 = body("探针 · 否定", size=26, color=SEAL).move_to([3.5, -2.0, 0])
            self.play(FadeIn(tip3), run_time=0.5)
            self._cp, self._tip3 = code_p, tip3
        demo = VGroup(
            mixed("element 42 ()     →  42", size=30, color=TYPE_C),
            mixed("sumUnit (Right 7) →  7", size=30, color=TYPE_C),
            mixed("demoNot = id :: Void → Void", size=28, color=SEAL),
            body("唯一成立的否定：否定无本身", size=26, color=INK2),
        ).arrange(DOWN, buff=0.28).move_to([-0.2, 0.25, 0])
        with self.beat(3):
            self.play(FadeOut(self._cp), FadeOut(self._tip3), run_time=0.35)
            self.play(FadeIn(demo), run_time=1.5)
        close = VGroup(
            body("图 ⟷ 代码", size=36, color=INK),
            body("唯一性由类型系统保证", size=28, color=INK2),
            body("进阶篇 Haskell = 短印证", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(demo), run_time=0.35)
            self.play(FadeIn(close), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S7Next(TaoScene):
    SID = "S7Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=19).move_to([0, 0.95, 0]))
        points = VGroup(
            body("Hom 唯一性定义始与终", size=28),
            body("对偶范畴：无是倒过来的有", size=28),
            body("积 ↔ 余积 · 零一为单位", size=28),
            body("探针与否定", size=28),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.55, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.42)
        next_title = callig("道生一", size=56).move_to([0, 1.15, 0])
        topics = VGroup(
            body("从无出发 · 反复作用函子", size=30, color=INK2),
            body("余极限 = 初始代数", size=30, color=INK2),
            body("一生二 · 二生三 · 万物生长", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([0, -0.45, 0])
        next_tag = body("下集预告", size=26, color=INK3).move_to([0, -2.15, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(topics), FadeIn(next_tag), run_time=1.4)
        motto = callig("有无相生", size=72).move_to([0, 0.7, 0])
        bye = body("先看箭头，再谈翻转。下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(topics), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
