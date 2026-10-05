# -*- coding: utf-8 -*-
"""Manim scenes for 深讲 03 · Maybe 与 List."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=13).move_to([0, 0.55, 0]))
        title = callig("Maybe 与 List", size=82).move_to([0, 0.62, 0])
        sub = body("道可道 · 深讲 03 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("1 + A · 递归 · 从无生长", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("深讲 02", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("深讲 03", size=32, color=INK),
            body("本集 · Maybe / List", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.3).move_to([2.2, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.58).move_to([-4.1, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  Maybe = 1 + A", size=32),
            body("②  List 递归", size=32),
            body("③  从无生长", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.7  ·  CTFP 1.6", size=24, color=INK3),
            serif("Bartosz Milewski", size=28, color=INK2),
        ).arrange(DOWN, buff=0.12).move_to([2.4, -2.2, 0])
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
        # beat 1: dao / series
        note = VGroup(
            body("DaoFP ch.7 Recursion", size=30, color=INK2),
            body("入门篇扫过 · 本集单独拉开", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.4, 0])
        icons = VGroup(
            mixed("Maybe", size=36, color=TYPE_C),
            body("·", size=36, color=INK3),
            mixed("List", size=36, color=TYPE_C),
        ).arrange(RIGHT, buff=0.25).move_to([-0.3, -1.4, 0])
        with self.beat(1):
            self.play(FadeIn(note), FadeIn(icons), run_time=1.5)
        # beat 2: constructors
        q = body("一个类型，有哪些构造方式？", size=32, color=INK).move_to([-0.3, 0.8, 0])
        intro = body("每种方式 —— 一条引入规则 · 一个构造子", size=28, color=INK2).move_to([-0.3, -0.3, 0])
        with self.beat(2):
            self.play(FadeOut(note), FadeOut(icons), run_time=0.4)
            self.play(FadeIn(q), run_time=1.0)
            self.at(2, 0.45)
            self.play(FadeIn(intro), run_time=0.8)
        # beat 3: Maybe vs List cards
        card1 = VGroup(
            body("Maybe", size=30, color=SEAL),
            body("要么没有", size=26, color=INK3),
            body("要么装着一个", size=26, color=INK3),
            mixed("有限选择", size=26, color=INK2),
        ).arrange(DOWN, buff=0.18)
        card2 = VGroup(
            body("List", size=30, color=SEAL),
            body("要么空", size=26, color=INK3),
            body("要么头 + 另一份列表", size=26, color=INK3),
            mixed("自己指回自己", size=26, color=INK2),
        ).arrange(DOWN, buff=0.18)
        cards = VGroup(card1, card2).arrange(RIGHT, buff=1.4).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(q), FadeOut(intro), run_time=0.35)
            self.play(LaggedStart(FadeIn(card1, shift=UP * 0.1), FadeIn(card2, shift=UP * 0.1), lag_ratio=0.35),
                      run_time=1.5)
        # beat 4: from void
        motto = callig("从无生长", size=64).move_to([-0.3, 0.4, 0])
        sub = body("慢一点，只把构造看明白", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(4):
            self.play(FadeOut(cards), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S2Maybe(TaoScene):
    SID = "S2Maybe"
    QUOTE = ""
    TITLE = "二 · Maybe = 1 + A"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: Maybe box
        box = RoundedRectangle(corner_radius=0.15, width=3.6, height=2.2,
                               stroke_color=INK, stroke_width=2.5).move_to([-0.3, 0.6, 0])
        noth = mixed("Nothing", size=30, color=INK3).move_to([-1.4, 0.6, 0])
        just = mixed("Just x", size=30, color=TYPE_C).move_to([0.9, 0.6, 0])
        div = DashedLine([-0.3, 1.5, 0], [-0.3, -0.3, 0], color=INK3, stroke_width=2, dash_length=0.1)
        lab = mixed("Maybe a", size=36).move_to([-0.3, -1.8, 0])
        with self.beat(0):
            self.play(Create(box), Create(div), FadeIn(noth), FadeIn(just), FadeIn(lab), run_time=1.6)
        # beat 1: 1 + A
        eq = VGroup(
            mixed("Maybe a", size=34),
            mixed("≅", size=34, color=INK3),
            mixed("Either () a", size=34),
            mixed("≅", size=34, color=INK3),
            mixed("1 + A", size=38, color=SEAL),
        ).arrange(RIGHT, buff=0.28).move_to([-0.3, 0.5, 0])
        note = body("一是单元 · 加号是 Either", size=28, color=INK2).move_to([-0.3, -1.6, 0])
        with self.beat(1):
            self.play(FadeOut(box), FadeOut(div), FadeOut(noth), FadeOut(just), FadeOut(lab), run_time=0.4)
            self.play(FadeIn(eq), FadeIn(note), run_time=1.4)
        # beat 2: correspondence
        left = VGroup(
            mixed("Left ()", size=30, color=INK3),
            body("↓", size=28, color=INK3),
            mixed("Nothing", size=32),
        ).arrange(DOWN, buff=0.2).move_to([-3.0, 0.4, 0])
        right = VGroup(
            mixed("Right x", size=30, color=TYPE_C),
            body("↓", size=28, color=INK3),
            mixed("Just x", size=32),
        ).arrange(DOWN, buff=0.2).move_to([2.4, 0.4, 0])
        with self.beat(2):
            self.play(FadeOut(eq), FadeOut(note), run_time=0.35)
            self.play(FadeIn(left), FadeIn(right), run_time=1.4)
        # beat 3: terminal + coproduct
        formula = VGroup(
            mixed("()  +  A", size=40),
            body("终对象与余积拼出「也许有 a」", size=28, color=INK2),
        ).arrange(DOWN, buff=0.4).move_to([-0.3, 0.4, 0])
        with self.beat(3):
            self.play(FadeOut(left), FadeOut(right), run_time=0.35)
            self.play(FadeIn(formula), run_time=1.3)
        # beat 4: why care
        why = VGroup(
            body("缺失 · 失败 · 尚未加载", size=32, color=INK),
            body("同一形状 · 不必假装总有答案", size=28, color=INK2),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.4, 0])
        with self.beat(4):
            self.play(FadeOut(formula), run_time=0.35)
            self.play(FadeIn(why), run_time=1.3)
        # beat 5: envelope
        env = RoundedRectangle(corner_radius=0.12, width=3.4, height=1.9,
                               stroke_color=INK, stroke_width=2.5).move_to([-0.3, 0.5, 0])
        flap = Line([-1.7, 0.85, 0], [-0.3, 0.15, 0], color=INK2, stroke_width=2)
        flap2 = Line([-0.3, 0.15, 0], [1.1, 0.85, 0], color=INK2, stroke_width=2)
        cap = body("空信封 · 或一张纸条", size=28, color=INK2).move_to([-0.3, -1.8, 0])
        with self.beat(5):
            self.play(FadeOut(why), run_time=0.35)
            self.play(Create(env), Create(flap), Create(flap2), FadeIn(cap), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S3List(TaoScene):
    SID = "S3List"
    QUOTE = ""
    TITLE = "三 · List：递归"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: recursive def
        nil_n = mixed("Nil", size=34).move_to([-3.6, 0.8, 0])
        cons_n = mixed("Cons", size=34).move_to([-3.6, -0.6, 0])
        list_n = mixed("List a", size=40, color=TYPE_C).move_to([2.0, 0.2, 0])
        ar1 = arrow(nil_n, list_n)
        # Cons needs a and List a
        a_n = mixed("a", size=30).move_to([-0.8, -1.6, 0])
        ar2 = arrow(cons_n, list_n)
        ar3 = arrow(a_n, cons_n)
        loop = CurvedArrow(list_n.get_bottom() + DOWN * 0.1, cons_n.get_right() + RIGHT * 0.1,
                           angle=-1.2, color=SEAL, stroke_width=3, tip_length=0.18)
        loop_l = body("指回自己", size=24, color=SEAL).next_to(loop, DOWN, buff=0.1)
        with self.beat(0):
            self.play(FadeIn(nil_n), FadeIn(cons_n), FadeIn(list_n), FadeIn(a_n), run_time=1.0)
            self.play(GrowArrow(ar1), GrowArrow(ar2), GrowArrow(ar3), Create(loop), FadeIn(loop_l), run_time=1.4)
        # beat 1: types of constructors
        sigs = VGroup(
            mixed("Nil  :: List a", size=32),
            mixed("Cons :: a → List a → List a", size=32),
        ).arrange(DOWN, buff=0.45).move_to([-0.3, 0.4, 0])
        note = body("尾的类型，还是列表本身", size=28, color=INK2).move_to([-0.3, -1.6, 0])
        with self.beat(1):
            self.play(FadeOut(VGroup(nil_n, cons_n, list_n, a_n, ar1, ar2, ar3, loop, loop_l)), run_time=0.4)
            self.play(FadeIn(sigs), FadeIn(note), run_time=1.3)
        # beat 2: growth animation
        cells = VGroup(
            mixed("[]", size=32, color=INK3),
            mixed("1 : []", size=32),
            mixed("1 : 2 : []", size=32),
            mixed("1 : 2 : 3 : []", size=32, color=TYPE_C),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(sigs), FadeOut(note), run_time=0.35)
            for c in cells:
                self.play(FadeIn(c, shift=RIGHT * 0.1), run_time=0.5)
        # beat 3: finite vs recursive
        cmp1 = VGroup(
            body("Maybe", size=30, color=SEAL),
            body("有限选择", size=28),
            mixed("有 / 没有", size=26, color=INK3),
        ).arrange(DOWN, buff=0.2).move_to([-3.0, 0.3, 0])
        cmp2 = VGroup(
            body("List", size=30, color=SEAL),
            body("开放递归", size=28),
            mixed("任意长度", size=26, color=INK3),
        ).arrange(DOWN, buff=0.2).move_to([2.4, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(cells), run_time=0.35)
            self.play(FadeIn(cmp1), FadeIn(cmp2), run_time=1.3)
        # beat 4: elimination tease
        elim = VGroup(
            mixed("Nil  →  init", size=32),
            mixed("Cons →  step(head, folded tail)", size=30),
        ).arrange(DOWN, buff=0.4).move_to([-0.3, 0.5, 0])
        elim_n = body("消解 = 构造的反面 · 下集展开", size=28, color=SEAL).move_to([-0.3, -1.6, 0])
        with self.beat(4):
            self.play(FadeOut(cmp1), FadeOut(cmp2), run_time=0.35)
            self.play(FadeIn(elim), FadeIn(elim_n), run_time=1.3)
        # beat 5: introduction rules
        tip = callig("引入规则", size=56).move_to([-0.3, 0.6, 0])
        tip2 = body("自然数用后继 · 列表用 Cons", size=28, color=INK2).move_to([-0.3, -0.6, 0])
        tip3 = body("—— DaoFP ch.7 · 释义", size=24, color=INK3).move_to([-0.3, -1.4, 0])
        with self.beat(5):
            self.play(FadeOut(elim), FadeOut(elim_n), run_time=0.35)
            self.play(FadeIn(tip, scale=0.95), FadeIn(tip2), FadeIn(tip3), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S4Grow(TaoScene):
    SID = "S4Grow"
    QUOTE = ""
    TITLE = "四 · 从无生长"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: Void → Maybe Void
        void_d = dots(0).move_to([-3.5, 0.6, 0])
        void_l = mixed("Void", size=28).next_to(void_d, DOWN, buff=0.25)
        one_d = dots(1).move_to([1.5, 0.6, 0])
        one_l = mixed("Maybe Void", size=28).next_to(one_d, DOWN, buff=0.25)
        ar = arrow([-2.6, 0.6, 0], [0.6, 0.6, 0])
        nums = VGroup(
            callig("无", size=48),
            body("→", size=36, color=INK3),
            callig("一", size=48, color=SEAL),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, -1.8, 0])
        with self.beat(0):
            self.play(FadeIn(void_d), FadeIn(void_l), run_time=0.8)
            self.play(GrowArrow(ar), FadeIn(one_d), FadeIn(one_l), FadeIn(nums), run_time=1.3)
        # beat 1: two and three
        two_d = dots(2).move_to([-3.0, 0.8, 0])
        two_l = mixed("Maybe² Void", size=26).next_to(two_d, DOWN, buff=0.2)
        three_d = dots(3).move_to([1.8, 0.8, 0])
        three_l = mixed("Maybe³ Void", size=26).next_to(three_d, DOWN, buff=0.2)
        nums2 = VGroup(
            callig("二", size=48, color=SEAL),
            body("·", size=36, color=INK3),
            callig("三", size=48, color=SEAL),
        ).arrange(RIGHT, buff=0.4).move_to([-0.3, -1.8, 0])
        with self.beat(1):
            self.play(FadeOut(VGroup(void_d, void_l, one_d, one_l, ar, nums)), run_time=0.4)
            self.play(FadeIn(two_d), FadeIn(two_l), FadeIn(three_d), FadeIn(three_l), FadeIn(nums2), run_time=1.4)
        # beat 2: alignment
        rows = VGroup(
            mixed("层 0  Void          →  0  个值", size=28),
            mixed("层 1  Maybe Void    →  1  个值", size=28),
            mixed("层 2  Maybe² Void   →  2  个值", size=28),
            mixed("层 3  Maybe³ Void   →  3  个值", size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(VGroup(two_d, two_l, three_d, three_l, nums2)), run_time=0.35)
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.08), run_time=0.45)
        # beat 3: list growth
        chain = VGroup(
            mixed("Nil", size=30, color=INK3),
            body("─Cons→", size=26, color=INK2),
            mixed("Cons x Nil", size=30),
            body("─Cons→", size=26, color=INK2),
            mixed("…", size=30, color=TYPE_C),
        ).arrange(RIGHT, buff=0.2).move_to([-0.3, 0.5, 0])
        tip = body("用构造子声明形状 —— 值跟着形状出现", size=28, color=INK2).move_to([-0.3, -1.6, 0])
        with self.beat(3):
            self.play(FadeOut(rows), run_time=0.35)
            self.play(FadeIn(chain), FadeIn(tip), run_time=1.4)
        # beat 4: Nat analogy
        nat = VGroup(
            mixed("Nat：  Z  |  S n", size=34),
            mixed("List： Nil | Cons a as", size=34),
        ).arrange(DOWN, buff=0.4).move_to([-0.3, 0.5, 0])
        nat_n = body("形状不同 · 从无生长的节奏一样", size=28, color=INK2).move_to([-0.3, -1.6, 0])
        with self.beat(4):
            self.play(FadeOut(chain), FadeOut(tip), run_time=0.35)
            self.play(FadeIn(nat), FadeIn(nat_n), run_time=1.3)
        # beat 5: grow vs fold tease
        grow = VGroup(
            callig("生", size=64),
            body("构造 · 往外长", size=28, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([-3.0, 0.3, 0])
        fold = VGroup(
            callig("归", size=64, color=INK3),
            body("折叠 · 往回收", size=28, color=INK3),
        ).arrange(DOWN, buff=0.25).move_to([2.4, 0.3, 0])
        tease = body("收回去的那半边 —— 留给下一集", size=28, color=SEAL).move_to([-0.3, -2.0, 0])
        with self.beat(5):
            self.play(FadeOut(nat), FadeOut(nat_n), run_time=0.35)
            self.play(FadeIn(grow), FadeIn(fold), FadeIn(tease), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S5Haskell(TaoScene):
    SID = "S5Haskell"
    QUOTE = ""
    TITLE = "五 · 落到代码"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        code_m = make_code("s_maybe", size=24, line_h=0.42).place(-6.2, 2.2)
        with self.beat(0):
            self.play(code_m.write(), run_time=2.0)
        with self.beat(1):
            self.play(code_m.focus(5, 7), run_time=0.7)
            self.at(1, 0.5)
            self.play(code_m.focus(9, 11), run_time=0.8)
        code_c = make_code("s_count", size=24, line_h=0.40).place(-6.2, 2.3)
        with self.beat(2):
            self.play(FadeOut(code_m), run_time=0.4)
            self.play(code_c.write(), run_time=1.8)
            self.play(code_c.focus(0, 3), run_time=0.6)
            cnt = body("个数正好是一、二、三", size=28, color=INK2).move_to([3.2, -1.8, 0])
            self.play(FadeIn(cnt), run_time=0.5)
            self._cnt = cnt
            self._code_c = code_c
        code_l = make_code("s_list", size=24, line_h=0.40).place(-6.2, 2.2)
        with self.beat(3):
            self.play(FadeOut(self._code_c), FadeOut(self._cnt), run_time=0.4)
            self.play(code_l.write(), run_time=1.8)
            self.play(code_l.focus(5, 7), run_time=0.7)
            sum_n = body("1 : 2 : 3  →  6", size=30, color=SEAL).move_to([3.0, -1.5, 0])
            self.play(FadeIn(sum_n), run_time=0.5)
            self._sum = sum_n
            self._code_l = code_l
        tip = body("图对齐了，代码只是把图念出来", size=32, color=INK).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(self._code_l), FadeOut(self._sum), run_time=0.4)
            self.play(FadeIn(tip), run_time=1.0)
        self.end_scene()


# =====================================================================================
class S6Next(TaoScene):
    SID = "S6Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=13).move_to([0, 0.8, 0]))
        points = VGroup(
            body("Maybe：1 + A · 有限选择", size=30),
            body("List：Cons 递归 · 无限生长", size=30),
            body("从无包上去：一二三 · 万物", size=30),
        ).arrange(DOWN, buff=0.28).move_to([0, -1.5, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.55)
        next_title = callig("构造与折叠", size=56).move_to([0, 0.6, 0])
        next_sub = body("下一集：fold · unfold · 先生后归", size=30, color=INK2).move_to([0, -0.3, 0])
        next_tag = body("深讲 04", size=26, color=SEAL).move_to([0, -1.0, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(next_sub), FadeIn(next_tag), run_time=1.3)
        motto = callig("看构造子", size=72).move_to([0, 0.7, 0])
        bye = body("道生一。我们下集见。", size=30, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(next_sub), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
