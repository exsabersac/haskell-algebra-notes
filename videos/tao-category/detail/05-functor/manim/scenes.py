# -*- coding: utf-8 -*-
"""Manim scenes for 深讲 05 · Functor 直觉."""
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
        title = callig("Functor 直觉", size=78).move_to([0, 0.62, 0])
        sub = body("道可道 · 深讲 05 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("保形 · fmap · 定律", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("深讲 04", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("深讲 05", size=32, color=INK),
            body("本集 · Functor", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.3).move_to([2.2, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.58).move_to([-4.1, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  函子保形", size=32),
            body("②  fmap / 交换图", size=32),
            body("③  单位 · 复合定律", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.8  ·  CTFP 1.7–1.8", size=24, color=INK3),
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
            body("映射而不撕裂", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.4, 0])
        icons = VGroup(
            callig("映", size=48, color=INK),
            body("→", size=36, color=INK3),
            callig("形", size=48, color=SEAL),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, -1.4, 0])
        with self.beat(1):
            self.play(FadeIn(note), FadeIn(icons), run_time=1.5)
        q = body("能否把里头的箭头抬到外壳上？", size=30, color=INK).move_to([-0.3, 0.8, 0])
        tip = body("能 → 函子　·　外壳形状不变", size=28, color=INK2).move_to([-0.3, -0.3, 0])
        with self.beat(2):
            self.play(FadeOut(note), FadeOut(icons), run_time=0.4)
            self.play(FadeIn(q), run_time=1.0)
            self.at(2, 0.45)
            self.play(FadeIn(tip), run_time=0.8)
        net = VGroup(
            body("范畴像一张织好的网", size=32, color=INK),
            body("可以压扁 · 可以粘合", size=28, color=INK2),
            body("但不许撕破 —— no-tearing", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(q), FadeOut(tip), run_time=0.35)
            self.play(FadeIn(net), run_time=1.5)
        motto = callig("保形", size=72).move_to([-0.3, 0.4, 0])
        sub = body("fmap 都站在它上面", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(4):
            self.play(FadeOut(net), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S2Shape(TaoScene):
    SID = "S2Shape"
    QUOTE = ""
    TITLE = "二 · 函子保形"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0
        two = VGroup(
            body("① 对象 → 对象", size=32),
            body("② 箭头 → 箭头", size=32),
            mixed("a  ↦  F a", size=34, color=TYPE_C),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(two), run_time=1.6)
        # beat 1
        ctors = VGroup(
            mixed("Maybe a", size=36, color=TYPE_C),
            body("也许有一个 a", size=28, color=INK2),
            mixed("List a", size=36, color=TYPE_C),
            body("一串 a", size=28, color=INK2),
            body("类型构造子 ≠ 类型", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([-0.3, 0.2, 0])
        with self.beat(1):
            self.play(FadeOut(two), run_time=0.4)
            self.play(FadeIn(ctors), run_time=1.4)
        # beat 2
        lift = VGroup(
            mixed("f  :  a → b", size=34),
            body("↓ 函子抬升", size=28, color=INK2),
            mixed("F f  :  F a → F b", size=34, color=SEAL),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(ctors), run_time=0.35)
            self.play(FadeIn(lift), run_time=1.4)
        # beat 3
        remember = VGroup(
            callig("记得构造", size=52),
            body("只改内容那一层记忆", size=28, color=INK2),
            body("Just 仍是 Just · [] 仍是 []", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(lift), run_time=0.35)
            self.play(FadeIn(remember), run_time=1.4)
        # beat 4 coat metaphor
        coat = VGroup(
            callig("外套", size=56),
            body("换衬衫 = fmap", size=28, color=INK2),
            body("剪裁 = 类型构造子", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(remember), run_time=0.35)
            self.play(FadeIn(coat), run_time=1.4)
        # beat 5
        shape = VGroup(
            body("函子 ≠ 随便一个 map", size=32, color=INK),
            body("在同一张网的形状上，把箭头抬过去", size=28, color=INK2),
            body("形状先于操作", size=30, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(coat), run_time=0.35)
            self.play(FadeIn(shape), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S3Fmap(TaoScene):
    SID = "S3Fmap"
    QUOTE = ""
    TITLE = "三 · fmap 与交换图"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0
        sig = VGroup(
            mixed("fmap", size=42, color=SEAL),
            mixed(":: (a → b) → (F a → F b)", size=32, color=TYPE_C),
            body("把箭头抬到结构上", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(sig), run_time=1.5)
        # beat 1 commuting square
        a = node("a", size=34).move_to([-3.2, 1.2, 0])
        b = node("b", size=34).move_to([-3.2, -1.2, 0])
        fa = node("F a", size=34, color=TYPE_C).move_to([2.4, 1.2, 0])
        fb = node("F b", size=34, color=TYPE_C).move_to([2.4, -1.2, 0])
        af = arrow(a, b, color=INK)
        ff = arrow(fa, fb, color=SEAL)
        top = DashedLine(a.get_right(), fa.get_left(), color=INK3, stroke_width=2.5, dash_length=0.12)
        bot = DashedLine(b.get_right(), fb.get_left(), color=INK3, stroke_width=2.5, dash_length=0.12)
        lf = label(af, "f", side=LEFT, size=26)
        rf = label(ff, "F f", side=RIGHT, size=26, color=SEAL)
        sq = VGroup(a, b, fa, fb, af, ff, top, bot, lf, rf)
        with self.beat(1):
            self.play(FadeOut(sig), run_time=0.35)
            self.play(FadeIn(sq), run_time=1.6)
        # beat 2 Maybe
        maybe = VGroup(
            mixed("fmap f Nothing  = Nothing", size=30, color=INK3),
            mixed("fmap f (Just x) = Just (f x)", size=30, color=TYPE_C),
            body("外壳两支：一支不动，一支只动内容", size=26, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(sq), run_time=0.35)
            self.play(FadeIn(maybe), run_time=1.4)
        # beat 3 list anim
        chain = VGroup(
            mixed("[1, 2, 3]", size=36),
            body("↓ fmap (*2)", size=28, color=INK2),
            mixed("[2, 4, 6]", size=36, color=SEAL),
            body("长度 · 顺序不变", size=26, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.2, 0])
        with self.beat(3):
            self.play(FadeOut(maybe), run_time=0.35)
            for c in chain:
                self.play(FadeIn(c, shift=UP * 0.06), run_time=0.45)
        # beat 4 lifting
        lift = VGroup(
            mixed("lifting", size=40, color=TYPE_C),
            body("值上的计算 → 抬到结构里", size=28, color=INK2),
            body("函子替你保管形状", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(chain), run_time=0.35)
            self.play(FadeIn(lift), run_time=1.4)
        # beat 5
        path = VGroup(
            body("先映射再装箱  ⟷  先装箱再映射", size=30, color=INK),
            body("路径一致，才叫函子", size=28, color=SEAL),
            body("不一致，只是碰巧同名的函数", size=26, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(lift), run_time=0.35)
            self.play(FadeIn(path), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S4Laws(TaoScene):
    SID = "S4Laws"
    QUOTE = ""
    TITLE = "四 · 函子定律"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0
        two = VGroup(
            body("两条定律", size=36, color=INK),
            mixed("①  单位 id", size=32, color=TYPE_C),
            mixed("②  复合 ∘", size=32, color=SEAL),
            body("类型写不出 · 责任写得进", size=26, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(two), run_time=1.5)
        # beat 1 identity
        ident = VGroup(
            mixed("fmap id  =  id", size=40, color=SEAL),
            body("什么都不做 → 结构原样回来", size=28, color=INK2),
            mixed("Just 3 → Just 3", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(two), run_time=0.35)
            self.play(FadeIn(ident), run_time=1.4)
        # beat 2 composition
        comp = VGroup(
            mixed("fmap (g ∘ f)", size=34, color=TYPE_C),
            body("=", size=28, color=INK3),
            mixed("fmap g ∘ fmap f", size=34, color=SEAL),
            body("抬两次 = 抬一次复合后的箭头", size=26, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(ident), run_time=0.35)
            self.play(FadeIn(comp), run_time=1.4)
        # beat 3 why
        why = VGroup(
            body("没有定律，fmap 只是同名函数", size=30, color=INK),
            body("可以撕破 · 乱序 · 吞掉元素", size=28, color=INK2),
            body("有了定律，保形才被钉死", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(comp), run_time=0.35)
            self.play(FadeIn(why), run_time=1.4)
        # beat 4 typeclass vs laws
        warn = VGroup(
            body("编译器认类型类实例", size=30, color=INK),
            body("合法与否 · 要人来核对", size=28, color=INK2),
            body("坏的 map 也能过类型检查", size=28, color=SEAL),
            body("定律 = 契约", size=26, color=INK3),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(why), run_time=0.35)
            self.play(FadeIn(warn), run_time=1.4)
        # beat 5 motto
        motto = callig("大制不割", size=64).move_to([-0.3, 0.5, 0])
        sub = body("单位保真 · 复合保序", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(5):
            self.play(FadeOut(warn), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S5Haskell(TaoScene):
    SID = "S5Haskell"
    QUOTE = ""
    TITLE = "五 · Maybe 与 List"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        code_c = make_code("s_class", size=26, line_h=0.42).place(-6.0, 1.6)
        with self.beat(0):
            self.play(code_c.write(), run_time=2.0)
            tip = body("把值上的箭头抬到结构上", size=26, color=INK2).move_to([3.0, -1.8, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._tip = tip
            self._code_c = code_c
        code_m = make_code("s_maybe", size=24, line_h=0.38).place(-6.2, 2.2)
        with self.beat(1):
            self.play(FadeOut(self._code_c), FadeOut(self._tip), run_time=0.4)
            self.play(code_m.write(), run_time=1.8)
            self.play(code_m.focus(4, 6), run_time=0.7)
            note = body("空不生有 · 有则改内容", size=28, color=SEAL).move_to([3.2, -2.0, 0])
            self.play(FadeIn(note), run_time=0.5)
            self._note = note
            self._code_m = code_m
        code_l = make_code("s_list", size=24, line_h=0.38).place(-6.2, 2.0)
        with self.beat(2):
            self.play(FadeOut(self._code_m), FadeOut(self._note), run_time=0.4)
            self.play(code_l.write(), run_time=1.8)
            tip2 = body("你每天写的 map，就是它", size=28, color=INK2).move_to([3.0, -1.8, 0])
            self.play(FadeIn(tip2), run_time=0.5)
            self._tip2 = tip2
            self._code_l = code_l
        demo = VGroup(
            mixed("fmap (+1) (Just 41)  →  Just 42", size=30, color=TYPE_C),
            mixed("fmap (*2) [1,2,3]   →  [2,4,6]", size=30, color=SEAL),
            body("外壳没动 · 数字动了", size=28, color=INK2),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(self._code_l), FadeOut(self._tip2), run_time=0.4)
            self.play(FadeIn(demo), run_time=1.3)
            self._demo = demo
        laws = VGroup(
            mixed("fmap id (Just 3) == Just 3", size=28),
            mixed("fmap (g∘f) xs == (fmap g ∘ fmap f) xs", size=26, color=TYPE_C),
            body("屏幕代码都能编译", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(self._demo), run_time=0.35)
            self.play(FadeIn(laws), run_time=1.3)
            self._laws = laws
        tip3 = body("图对齐了，代码只是把图念出来", size=32, color=INK).move_to([-0.2, 0.5, 0])
        tip4 = body("Bifunctor / Contravariant —— 留给以后", size=28, color=INK2).move_to([-0.2, -0.5, 0])
        with self.beat(5):
            self.play(FadeOut(self._laws), run_time=0.35)
            self.play(FadeIn(tip3), FadeIn(tip4), run_time=1.1)
        self.end_scene()


# =====================================================================================
class S6Next(TaoScene):
    SID = "S6Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=19).move_to([0, 0.8, 0]))
        points = VGroup(
            body("函子保形 · 不撕裂结构", size=30),
            body("fmap 把箭头抬到外壳上", size=30),
            body("单位与复合 · 写成契约", size=30),
        ).arrange(DOWN, buff=0.28).move_to([0, -1.5, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.55)
        next_title = callig("Monad / do", size=56).move_to([0, 0.6, 0])
        next_sub = body("下一集：在函子之上接上效应", size=30, color=INK2).move_to([0, -0.3, 0])
        next_tag = body("深讲 06", size=26, color=SEAL).move_to([0, -1.0, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(next_sub), FadeIn(next_tag), run_time=1.3)
        motto = callig("大制不割", size=64).move_to([0, 0.7, 0])
        bye = body("先看形状，再看映射。我们下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(next_sub), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
