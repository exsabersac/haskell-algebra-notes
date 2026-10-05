# -*- coding: utf-8 -*-
"""Manim scenes for 深讲 02 · Void 与 ()."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=11).move_to([0, 0.55, 0]))
        title = callig("Void 与 ()", size=90).move_to([0, 0.62, 0])
        sub = body("道可道 · 深讲 02 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("始对象 · 终对象 · 对偶", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("深讲 01", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("深讲 02", size=32, color=INK),
            body("本集 · Void / ()", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.3).move_to([2.2, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.62).move_to([-4.1, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  始对象 Void", size=32),
            body("②  终对象 ()", size=32),
            body("③  对偶", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.1  ·  CTFP 1.5–1.6", size=24, color=INK3),
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
        # beat 1: yin yang labels
        left = VGroup(
            callig("无", size=72),
            mixed("Void", size=36, color=INK2),
            body("零个值", size=26, color=INK3),
        ).arrange(DOWN, buff=0.25).move_to([-3.2, 0.4, 0])
        right = VGroup(
            callig("有", size=72),
            mixed("()", size=36, color=INK2),
            body("一个值", size=26, color=INK3),
        ).arrange(DOWN, buff=0.25).move_to([2.6, 0.4, 0])
        mirror = DashedLine([ -0.3, 2.2, 0], [-0.3, -1.6, 0], color=INK3, stroke_width=2, dash_length=0.12)
        mid = body("阴 · 阳", size=28, color=SEAL).move_to([-0.3, -2.2, 0])
        with self.beat(1):
            self.play(FadeIn(left), FadeIn(right), Create(mirror), FadeIn(mid), run_time=1.6)
        # beat 2: count arrows
        q = body("从它出发有几条？通向它有几条？", size=30, color=INK).move_to([-0.3, 0.6, 0])
        uniq = body("答案一旦唯一 —— 这个对象就特别", size=28, color=INK2).move_to([-0.3, -0.4, 0])
        with self.beat(2):
            self.play(FadeOut(left), FadeOut(right), FadeOut(mirror), FadeOut(mid), run_time=0.4)
            self.play(FadeIn(q), run_time=1.0)
            self.at(2, 0.5)
            self.play(FadeIn(uniq), run_time=0.8)
        # beat 3: definitions
        card1 = VGroup(
            body("始对象", size=28, color=SEAL),
            body("对每个 a", size=24, color=INK3),
            mixed("∃!  箭头  0 → a", size=28),
        ).arrange(DOWN, buff=0.18)
        card2 = VGroup(
            body("终对象", size=28, color=SEAL),
            body("对每个 a", size=24, color=INK3),
            mixed("∃!  箭头  a → 1", size=28),
        ).arrange(DOWN, buff=0.18)
        cards = VGroup(card1, card2).arrange(RIGHT, buff=1.6).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(q), FadeOut(uniq), run_time=0.35)
            self.play(LaggedStart(FadeIn(card1, shift=UP * 0.1), FadeIn(card2, shift=UP * 0.1), lag_ratio=0.35),
                      run_time=1.5)
        # beat 4: Hask names
        hask = VGroup(
            mixed("Hask：Void = 0", size=34),
            mixed("Hask：() = 1", size=34),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        note = body("（依惯例忽略 ⊥）", size=24, color=INK3).move_to([-0.3, -1.6, 0])
        with self.beat(4):
            self.play(FadeOut(cards), run_time=0.35)
            self.play(FadeIn(hask), FadeIn(note), run_time=1.2)
        self.end_scene()


# =====================================================================================
class S2Void(TaoScene):
    SID = "S2Void"
    QUOTE = ""
    TITLE = "二 · Void：无出射"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: empty house
        empty = Circle(radius=1.1, color=INK3, stroke_width=2.5).move_to([-0.3, 0.5, 0])
        lab = mixed("Void", size=40).next_to(empty, DOWN, buff=0.35)
        zero = body("零个值", size=30, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(0):
            self.play(Create(empty), FadeIn(lab), FadeIn(zero), run_time=1.5)
        # beat 1: arrows out
        void_n = mixed("Void", size=36).move_to([-3.6, 0.5, 0])
        targets = VGroup(mixed("A", size=32), mixed("B", size=32), mixed("C", size=32))
        targets[0].move_to([2.0, 1.6, 0])
        targets[1].move_to([2.8, 0.5, 0])
        targets[2].move_to([2.0, -0.6, 0])
        ars = VGroup(*[arrow(void_n, t) for t in targets])
        als = VGroup(*[mixed("absurd", size=20, color=INK2).next_to(ar, UP if i == 0 else (DOWN if i == 2 else RIGHT), buff=0.08)
                       for i, ar in enumerate(ars)])
        with self.beat(1):
            self.play(FadeOut(empty), FadeOut(lab), FadeOut(zero), run_time=0.35)
            self.play(FadeIn(void_n), LaggedStart(*[FadeIn(t) for t in targets], lag_ratio=0.2), run_time=1.0)
            self.play(*[GrowArrow(ar) for ar in ars], *[FadeIn(l) for l in als], run_time=1.3)
        # beat 2: never called
        never = body("合法，却永远不会被真正调用", size=30, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(2):
            self.play(FadeIn(never), run_time=0.9)
        # beat 3: uniqueness
        uniq = mixed("Hom(Void, a)  恰有  1  元", size=34).move_to([-0.3, -2.2, 0])
        with self.beat(3):
            self.play(FadeOut(never), run_time=0.3)
            self.play(FadeIn(uniq), run_time=1.0)
        # beat 4: initial
        motto = callig("始对象", size=64).move_to([-0.3, 0.5, 0])
        en = serif("initial object", size=32, color=INK2).move_to([-0.3, -0.6, 0])
        with self.beat(4):
            self.play(FadeOut(void_n), FadeOut(targets), FadeOut(ars), FadeOut(als), FadeOut(uniq), run_time=0.45)
            self.play(FadeIn(motto, scale=0.95), FadeIn(en), run_time=1.3)
        # beat 5: envelope
        env = RoundedRectangle(corner_radius=0.12, width=3.2, height=1.8,
                               stroke_color=INK, stroke_width=2.5, fill_opacity=0).move_to([-0.3, 0.4, 0])
        flap = Line([-1.6, 0.7, 0], [-0.3, 0.1, 0], color=INK2, stroke_width=2)
        flap2 = Line([-0.3, 0.1, 0], [1.0, 0.7, 0], color=INK2, stroke_width=2)
        empty_l = body("空信封 · 寄不出去", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(5):
            self.play(FadeOut(motto), FadeOut(en), run_time=0.35)
            self.play(Create(env), Create(flap), Create(flap2), FadeIn(empty_l), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S3Unit(TaoScene):
    SID = "S3Unit"
    QUOTE = ""
    TITLE = "三 · ()：唯一入"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: one point
        unit = Dot(radius=0.16, color=INK).move_to([-0.3, 0.6, 0])
        lab = mixed("()", size=42).next_to(unit, DOWN, buff=0.4)
        one = body("恰好一个值", size=30, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(0):
            self.play(FadeIn(unit, scale=0.5), FadeIn(lab), FadeIn(one), run_time=1.4)
        # beat 1: arrows in
        unit_n = mixed("()", size=36).move_to([2.8, 0.5, 0])
        srcs = VGroup(mixed("A", size=32), mixed("B", size=32), mixed("C", size=32))
        srcs[0].move_to([-3.4, 1.6, 0])
        srcs[1].move_to([-3.8, 0.5, 0])
        srcs[2].move_to([-3.4, -0.6, 0])
        ars = VGroup(*[arrow(s, unit_n) for s in srcs])
        als = VGroup(*[mixed("const ()", size=20, color=INK2).next_to(ar, UP if i == 0 else (DOWN if i == 2 else LEFT), buff=0.08)
                       for i, ar in enumerate(ars)])
        with self.beat(1):
            self.play(FadeOut(unit), FadeOut(lab), FadeOut(one), run_time=0.35)
            self.play(FadeIn(unit_n), LaggedStart(*[FadeIn(s) for s in srcs], lag_ratio=0.2), run_time=1.0)
            self.play(*[GrowArrow(ar) for ar in ars], *[FadeIn(l) for l in als], run_time=1.3)
        # beat 2: uniqueness
        uniq = mixed("Hom(a, ())  恰有  1  元", size=34).move_to([-0.3, -2.2, 0])
        with self.beat(2):
            self.play(FadeIn(uniq), run_time=1.0)
        # beat 3: terminal
        motto = callig("终对象", size=64).move_to([-0.3, 0.5, 0])
        en = serif("terminal object", size=32, color=INK2).move_to([-0.3, -0.6, 0])
        with self.beat(3):
            self.play(FadeOut(unit_n), FadeOut(srcs), FadeOut(ars), FadeOut(als), FadeOut(uniq), run_time=0.45)
            self.play(FadeIn(motto, scale=0.95), FadeIn(en), run_time=1.3)
        # beat 4: mailbox
        box = RoundedRectangle(corner_radius=0.1, width=2.4, height=2.0,
                               stroke_color=INK, stroke_width=2.5).move_to([-0.3, 0.5, 0])
        slot = Line([-0.9, 1.0, 0], [0.3, 1.0, 0], color=INK2, stroke_width=3)
        mail = body("公用邮筒 · 已投递", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(4):
            self.play(FadeOut(motto), FadeOut(en), run_time=0.35)
            self.play(Create(box), Create(slot), FadeIn(mail), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S4Dual(TaoScene):
    SID = "S4Dual"
    QUOTE = ""
    TITLE = "四 · 对偶"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: side by side
        void_n = mixed("Void", size=32).move_to([-4.0, 0.8, 0])
        outs = VGroup(mixed("A", size=26), mixed("B", size=26), mixed("C", size=26))
        outs.arrange(DOWN, buff=0.55).move_to([-1.2, 0.8, 0])
        ar_out = VGroup(*[arrow(void_n, o) for o in outs])
        unit_n = mixed("()", size=32).move_to([4.0, 0.8, 0])
        ins = VGroup(mixed("A", size=26), mixed("B", size=26), mixed("C", size=26))
        ins.arrange(DOWN, buff=0.55).move_to([1.2, 0.8, 0])
        ar_in = VGroup(*[arrow(i, unit_n) for i in ins])
        cap = body("出射唯一  ·  入射唯一", size=28, color=INK2).move_to([-0.2, -2.2, 0])
        with self.beat(0):
            self.play(FadeIn(void_n), FadeIn(outs), *[GrowArrow(a) for a in ar_out], run_time=1.2)
            self.play(FadeIn(unit_n), FadeIn(ins), *[GrowArrow(a) for a in ar_in], FadeIn(cap), run_time=1.2)
        # beat 1: flip
        dual = callig("对偶", size=64).move_to([-0.2, 0.3, 0])
        dual_en = serif("duality: reverse every arrow", size=28, color=INK2).move_to([-0.2, -0.8, 0])
        with self.beat(1):
            self.play(FadeOut(VGroup(void_n, outs, ar_out, unit_n, ins, ar_in, cap)), run_time=0.4)
            self.play(FadeIn(dual, scale=0.95), FadeIn(dual_en), run_time=1.3)
        # beat 2: unit laws
        law1 = mixed("Either Void a  ≅  a", size=34)
        law2 = mixed("((), a)  ≅  a", size=34)
        laws = VGroup(law1, law2).arrange(DOWN, buff=0.45).move_to([-0.2, 0.5, 0])
        note = body("「或者」的单位 · 「并且」的单位", size=28, color=INK2).move_to([-0.2, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(dual), FadeOut(dual_en), run_time=0.35)
            self.play(FadeIn(laws), FadeIn(note), run_time=1.3)
        # beat 3: coin
        coin = callig("有无相生", size=56).move_to([-0.2, 0.6, 0])
        sub = body("零与一 · 始与终 · 同一枚硬币", size=28, color=INK2).move_to([-0.2, -0.5, 0])
        with self.beat(3):
            self.play(FadeOut(laws), FadeOut(note), run_time=0.35)
            self.play(FadeIn(coin, scale=0.95), FadeIn(sub), run_time=1.3)
        # beat 4: milewski
        tip = body("先把这一对极端钉牢：类型代数的 0 与 1", size=30, color=INK).move_to([-0.2, 0.3, 0])
        tip2 = body("—— DaoFP / CTFP · 释义", size=24, color=INK3).move_to([-0.2, -0.5, 0])
        with self.beat(4):
            self.play(FadeOut(coin), FadeOut(sub), run_time=0.35)
            self.play(FadeIn(tip), FadeIn(tip2), run_time=1.2)
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
        code_wu = make_code("s_wu", size=26, line_h=0.48).place(-6.0, 1.8)
        code_you = make_code("s_you", size=26, line_h=0.48).place(-6.0, -0.2)
        with self.beat(0):
            self.play(code_wu.write(), run_time=1.2)
            self.play(code_you.write(), run_time=1.2)
        with self.beat(1):
            self.play(code_wu.focus(0, 2), run_time=0.7)
            self.at(1, 0.45)
            self.play(code_wu.unfocus(), code_you.focus(0, 2), run_time=0.9)
        code_sum = make_code("s_sum", size=26, line_h=0.48).place(-6.0, 1.6)
        with self.beat(2):
            self.play(FadeOut(code_wu), FadeOut(code_you), run_time=0.4)
            self.play(code_sum.write(), run_time=1.4)
            self.play(code_sum.focus(0, 2), run_time=0.6)
            note = body("左支不可能 · 只剩 a", size=28, color=INK2).move_to([2.5, -0.5, 0])
            self.play(FadeIn(note), run_time=0.6)
            self._sum_note = note
        code_prod = make_code("s_prod", size=26, line_h=0.48).place(-6.0, 1.6)
        with self.beat(3):
            self.play(FadeOut(code_sum), FadeOut(self._sum_note), run_time=0.4)
            self.play(code_prod.write(), run_time=1.3)
            self.play(code_prod.focus(0, 2), run_time=0.6)
            note2 = body("单元不增加信息", size=28, color=INK2).move_to([2.5, -0.5, 0])
            self.play(FadeIn(note2), run_time=0.6)
            self._prod_note = note2
            self._prod_code = code_prod
        tip = body("唯一性，是类型在替你说话", size=32, color=INK).move_to([-0.2, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(self._prod_code), FadeOut(self._prod_note), run_time=0.4)
            self.play(FadeIn(tip), run_time=1.0)
        align = body("图对齐了，代码只是把图念出来", size=30, color=INK2).move_to([-0.2, -0.6, 0])
        with self.beat(5):
            self.play(FadeIn(align), run_time=0.9)
        self.end_scene()


# =====================================================================================
class S6Next(TaoScene):
    SID = "S6Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=11).move_to([0, 0.8, 0]))
        points = VGroup(
            body("Void：出射唯一 · 始对象", size=30),
            body("()：入射唯一 · 终对象", size=30),
            body("箭头一翻，有无相生", size=30),
        ).arrange(DOWN, buff=0.28).move_to([0, -1.5, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.55)
        next_title = callig("道生一", size=56).move_to([0, 0.6, 0])
        next_sub = body("下一集：Maybe 与列表", size=30, color=INK2).move_to([0, -0.3, 0])
        next_tag = body("深讲 03", size=26, color=SEAL).move_to([0, -1.0, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(next_sub), FadeIn(next_tag), run_time=1.3)
        motto = callig("看箭头", size=72).move_to([0, 0.7, 0])
        bye = body("有无相生。我们下集见。", size=30, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(next_sub), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
