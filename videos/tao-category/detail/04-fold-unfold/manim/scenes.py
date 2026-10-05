# -*- coding: utf-8 -*-
"""Manim scenes for 深讲 04 · 构造与折叠."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=17).move_to([0, 0.55, 0]))
        title = callig("构造与折叠", size=82).move_to([0, 0.62, 0])
        sub = body("道可道 · 深讲 04 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("代数 · cata · ana", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("深讲 03", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("深讲 04", size=32, color=INK),
            body("本集 · 构造 / 折叠", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.3).move_to([2.2, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.58).move_to([-4.1, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  构造代数", size=32),
            body("②  折叠 cata / foldr", size=32),
            body("③  展开 ana（浅提）", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.11–12  ·  CTFP 3.8", size=24, color=INK3),
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
        note = VGroup(
            body("入门篇扫过 · 本集单独拉开", size=30, color=INK2),
            body("生出来之后，还要能归回去", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.4, 0])
        icons = VGroup(
            callig("生", size=48, color=INK),
            body("→", size=36, color=INK3),
            callig("归", size=48, color=SEAL),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, -1.4, 0])
        with self.beat(1):
            self.play(FadeIn(note), FadeIn(icons), run_time=1.5)
        q = body("递归类型，有哪些构造方式？", size=32, color=INK).move_to([-0.3, 0.8, 0])
        intro = body("引入规则 · 消解沿构造往回走", size=28, color=INK2).move_to([-0.3, -0.3, 0])
        with self.beat(2):
            self.play(FadeOut(note), FadeOut(icons), run_time=0.4)
            self.play(FadeIn(q), run_time=1.0)
            self.at(2, 0.45)
            self.play(FadeIn(intro), run_time=0.8)
        card1 = VGroup(
            mixed("Nil", size=34, color=INK3),
            body("→ 起点 init", size=28, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([-3.0, 0.3, 0])
        card2 = VGroup(
            mixed("Cons", size=34, color=TYPE_C),
            body("→ step(头, 已折尾)", size=28, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([2.2, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(q), FadeOut(intro), run_time=0.35)
            self.play(LaggedStart(FadeIn(card1, shift=UP * 0.1), FadeIn(card2, shift=UP * 0.1), lag_ratio=0.35),
                      run_time=1.5)
        motto = callig("只说清一步", size=64).move_to([-0.3, 0.4, 0])
        sub = body("递归替你走完全程", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(4):
            self.play(FadeOut(card1), FadeOut(card2), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S2Algebra(TaoScene):
    SID = "S2Algebra"
    QUOTE = ""
    TITLE = "二 · 构造代数"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0
        lab = body("代数 = 构造方式的集合", size=32, color=INK).move_to([-0.3, 1.2, 0])
        parts = VGroup(
            mixed("Nil", size=34, color=INK3),
            body("或", size=28, color=INK3),
            mixed("Cons a as", size=34, color=TYPE_C),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, 0.1, 0])
        tip = body("零件拼出成品", size=28, color=INK2).move_to([-0.3, -1.4, 0])
        with self.beat(0):
            self.play(FadeIn(lab), FadeIn(parts), FadeIn(tip), run_time=1.6)
        # beat 1
        sigs = VGroup(
            mixed("Nil  :: 1 → List a", size=32),
            mixed("Cons :: A × List a → List a", size=32),
        ).arrange(DOWN, buff=0.45).move_to([-0.3, 0.4, 0])
        with self.beat(1):
            self.play(FadeOut(lab), FadeOut(parts), FadeOut(tip), run_time=0.4)
            self.play(FadeIn(sigs), run_time=1.3)
        # beat 2
        fill = VGroup(
            callig("填洞", size=56),
            body("形状里的洞 → 目标类型里的值", size=28, color=INK2),
            body("—— DaoFP ch.11 · 释义", size=24, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(sigs), run_time=0.35)
            self.play(FadeIn(fill), run_time=1.4)
        # beat 3: same shape different algebras
        rows = VGroup(
            mixed("求和    Nil→0    Cons→(+)", size=30),
            mixed("求积    Nil→1    Cons→(*)", size=30),
            mixed("求长    Nil→0    Cons→(+1)", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-0.3, 0.3, 0])
        note = body("同一 List 形状 · 不同代数", size=28, color=SEAL).move_to([-0.3, -1.8, 0])
        with self.beat(3):
            self.play(FadeOut(fill), run_time=0.35)
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.08), run_time=0.5)
            self.play(FadeIn(note), run_time=0.5)
        # beat 4
        fold_def = VGroup(
            body("折叠 = 拿着代数", size=32),
            body("沿构造逆方向消费结构", size=32),
            body("收成代数指定的那个值", size=30, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(rows), FadeOut(note), run_time=0.35)
            self.play(FadeIn(fold_def), run_time=1.4)
        # beat 5: recipe metaphor
        recipe = VGroup(
            callig("菜谱", size=56),
            body("构造给出摆法 · 折叠按菜谱做完", size=28, color=INK2),
            body("桌上只剩一道菜 —— 结果值", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(fold_def), run_time=0.35)
            self.play(FadeIn(recipe), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S3Cata(TaoScene):
    SID = "S3Cata"
    QUOTE = ""
    TITLE = "三 · 折叠 cata"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0
        cata = VGroup(
            mixed("catamorphism", size=36, color=TYPE_C),
            body("简称 cata  ≈  fold", size=32, color=INK),
            body("沿着代数往回折的唯一箭头", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(cata), run_time=1.5)
        # beat 1 foldr
        foldr = VGroup(
            mixed("foldr step init", size=38, color=SEAL),
            body("空 → init", size=30, color=INK3),
            body("Cons x xs → step x (foldr … xs)", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(cata), run_time=0.35)
            self.play(FadeIn(foldr), run_time=1.4)
        # beat 2 sum animation
        chain = VGroup(
            mixed("1 : 2 : 3 : []", size=34),
            body("↓ foldr (+) 0", size=28, color=INK2),
            mixed("1 + (2 + (3 + 0))", size=32, color=TYPE_C),
            body("↓", size=28, color=INK3),
            mixed("6", size=48, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.2, 0])
        with self.beat(2):
            self.play(FadeOut(foldr), run_time=0.35)
            for c in chain:
                self.play(FadeIn(c, shift=UP * 0.06), run_time=0.45)
        # beat 3 product
        prod = VGroup(
            mixed("product = foldr (*) 1", size=36),
            body("空是一 · 非空是乘法", size=28, color=INK2),
            body("同一条列表 · 换代数 · 结果变", size=28, color=INK3),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(chain), run_time=0.35)
            self.play(FadeIn(prod), run_time=1.4)
        # beat 4 unique
        uniq = VGroup(
            body("由构造唯一决定", size=34, color=INK),
            body("每个构造子对应一步", size=28, color=INK2),
            body("路径被钉死 —— 没有别的合法折法", size=28, color=INK3),
            body("（直觉层 · 非 Lambek 证明）", size=24, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(prod), run_time=0.35)
            self.play(FadeIn(uniq), run_time=1.4)
        # beat 5 motto
        motto = callig("各复归其根", size=64).move_to([-0.3, 0.5, 0])
        sub = body("构造往外长 · cata 往回收", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(5):
            self.play(FadeOut(uniq), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S4Ana(TaoScene):
    SID = "S4Ana"
    QUOTE = ""
    TITLE = "四 · 展开 ana（浅提）"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0 duality
        left = VGroup(
            callig("折", size=56),
            mixed("cata / fold", size=28, color=INK2),
            body("消费结构", size=26, color=INK3),
        ).arrange(DOWN, buff=0.2).move_to([-3.2, 0.3, 0])
        right = VGroup(
            callig("展", size=56, color=SEAL),
            mixed("ana / unfold", size=28, color=INK2),
            body("生成结构", size=26, color=INK3),
        ).arrange(DOWN, buff=0.2).move_to([2.6, 0.3, 0])
        dual = body("⟷  对偶", size=32, color=SEAL).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(left), FadeIn(right), FadeIn(dual), run_time=1.5)
        # beat 1 metaphors
        m1 = VGroup(
            body("拆快递", size=32, color=INK),
            body("打开一层 · 处理 · 再拆剩下", size=26, color=INK3),
        ).arrange(DOWN, buff=0.2).move_to([-3.0, 0.3, 0])
        m2 = VGroup(
            body("种树", size=32, color=SEAL),
            body("种子 → 果 + 更小种子", size=26, color=INK3),
        ).arrange(DOWN, buff=0.2).move_to([2.4, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(left), FadeOut(right), FadeOut(dual), run_time=0.35)
            self.play(FadeIn(m1), FadeIn(m2), run_time=1.4)
        # beat 2 countdown
        steps = VGroup(
            mixed("5", size=36, color=SEAL),
            body("→", size=28, color=INK3),
            mixed("5 : 4 : 3 : 2 : 1 : []", size=32, color=TYPE_C),
        ).arrange(RIGHT, buff=0.3).move_to([-0.3, 0.6, 0])
        rule = body("n=0 停 · 否则结出 n，留下 n−1", size=28, color=INK2).move_to([-0.3, -1.2, 0])
        with self.beat(2):
            self.play(FadeOut(m1), FadeOut(m2), run_time=0.35)
            self.play(FadeIn(steps), FadeIn(rule), run_time=1.4)
        # beat 3 hylo
        hylo = VGroup(
            mixed("种子", size=30),
            body("─ana→", size=26, color=INK2),
            mixed("列表", size=30, color=TYPE_C),
            body("─cata→", size=26, color=INK2),
            mixed("结果", size=30, color=SEAL),
        ).arrange(RIGHT, buff=0.22).move_to([-0.3, 0.6, 0])
        hylo_n = body("hylo · 合态射 · 先生后归（浅提）", size=28, color=INK2).move_to([-0.3, -1.2, 0])
        with self.beat(3):
            self.play(FadeOut(steps), FadeOut(rule), run_time=0.35)
            self.play(FadeIn(hylo), FadeIn(hylo_n), run_time=1.4)
        # beat 4 反者道之动
        motto = callig("反者道之动", size=64).move_to([-0.3, 0.5, 0])
        sub = body("fold ⟷ unfold · 每学一个方向，白得相反的那个", size=26, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(4):
            self.play(FadeOut(hylo), FadeOut(hylo_n), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.4)
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
        code_c = make_code("s_cata", size=22, line_h=0.36).place(-6.2, 2.5)
        with self.beat(0):
            self.play(code_c.write(), run_time=2.0)
        with self.beat(1):
            self.play(code_c.focus(5, 7), run_time=0.7)
            self.at(1, 0.45)
            self.play(code_c.focus(9, 11), run_time=0.8)
            note = body("同一形状 · 两套代数", size=28, color=SEAL).move_to([3.4, -2.0, 0])
            self.play(FadeIn(note), run_time=0.5)
            self._note = note
            self._code_c = code_c
        code_f = make_code("s_foldr", size=26, line_h=0.42).place(-6.0, 1.8)
        with self.beat(2):
            self.play(FadeOut(self._code_c), FadeOut(self._note), run_time=0.4)
            self.play(code_f.write(), run_time=1.6)
            tip = body("手写递归 ⟷ foldr · 同一 cata", size=28, color=INK2).move_to([2.8, -1.6, 0])
            self.play(FadeIn(tip), run_time=0.6)
            self._tip = tip
            self._code_f = code_f
        code_a = make_code("s_ana", size=22, line_h=0.36).place(-6.2, 2.5)
        with self.beat(3):
            self.play(FadeOut(self._code_f), FadeOut(self._tip), run_time=0.4)
            self.play(code_a.write(), run_time=1.8)
            self.play(code_a.focus(3, 7), run_time=0.7)
            out = body("countdown 5  →  [5,4,3,2,1]", size=28, color=SEAL).move_to([3.0, -2.0, 0])
            self.play(FadeIn(out), run_time=0.5)
            self._out = out
            self._code_a = code_a
        fact = VGroup(
            mixed("fact n = foldProduct (countdown n)", size=28),
            body("先生后归 · 10! = 3628800", size=28, color=SEAL),
            mixed("factHylo：中间不落地", size=26, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(self._code_a), FadeOut(self._out), run_time=0.4)
            self.play(FadeIn(fact), run_time=1.3)
            self._fact = fact
        tip2 = body("图对齐了，代码只是把图念出来", size=32, color=INK).move_to([-0.2, 0.5, 0])
        tip3 = body("更深的 Fix / Lambek —— 留给以后", size=28, color=INK2).move_to([-0.2, -0.5, 0])
        with self.beat(5):
            self.play(FadeOut(self._fact), run_time=0.35)
            self.play(FadeIn(tip2), FadeIn(tip3), run_time=1.1)
        self.end_scene()


# =====================================================================================
class S6Next(TaoScene):
    SID = "S6Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=17).move_to([0, 0.8, 0]))
        points = VGroup(
            body("构造子合起来 → 代数", size=30),
            body("沿代数往回折 → cata / fold", size=30),
            body("方向一翻 → ana / unfold", size=30),
        ).arrange(DOWN, buff=0.28).move_to([0, -1.5, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.55)
        next_title = callig("函子 Functor", size=56).move_to([0, 0.6, 0])
        next_sub = body("下一集：在结构上描画箭头", size=30, color=INK2).move_to([0, -0.3, 0])
        next_tag = body("深讲 05", size=26, color=SEAL).move_to([0, -1.0, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(next_sub), FadeIn(next_tag), run_time=1.3)
        motto = callig("各复归其根", size=64).move_to([0, 0.7, 0])
        bye = body("先看构造，再看折叠。我们下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(next_sub), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
