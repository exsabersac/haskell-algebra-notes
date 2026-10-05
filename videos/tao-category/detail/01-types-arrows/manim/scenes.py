# -*- coding: utf-8 -*-
"""Manim scenes for 深讲 01 · 类型与箭头."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value()).move_to([0, 0.55, 0]))
        title = callig("类型与箭头", size=96).move_to([0, 0.62, 0])
        sub = body("道可道 · 深讲 01 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("对象 · 态射 · 复合 · 恒等", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("入门篇", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("深讲系列", size=32, color=INK),
            body("本集 · 01", size=28, color=SEAL),
        ).arrange(RIGHT, buff=0.35).move_to([2.4, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.68).move_to([-4.0, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  对象与箭头", size=32),
            body("②  复合", size=32),
            body("③  恒等", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.1–2  ·  CTFP 1.1–1.2", size=24, color=INK3),
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
        # beat 1: DaoFP paraphrase
        line = serif("“The type that can be described\nis not the eternal type.”", size=34, color=INK)
        line2 = body("能被说净的类型，不是永恒的类型。", size=30, color=INK2)
        line3 = body("—— DaoFP ch.1 · 释义", size=22, color=INK3)
        quote = VGroup(line, line2, line3).arrange(DOWN, buff=0.28).move_to([-0.3, 0.4, 0])
        with self.beat(1):
            self.play(FadeIn(line), run_time=1.1)
            self.at(1, 0.4)
            self.play(FadeIn(line2), FadeIn(line3), run_time=1.0)
        # beat 2: three names
        cols = VGroup(
            VGroup(body("编程", size=24, color=INK3), mixed("type", size=36)).arrange(DOWN, buff=0.2),
            VGroup(body("范畴", size=24, color=INK3), body("对象", size=36)).arrange(DOWN, buff=0.2),
            VGroup(body("逻辑", size=24, color=INK3), body("命题", size=36)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=1.4).move_to([-0.3, 0.5, 0])
        note = body("名字不同，位置相同——都是「点」", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(quote), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, scale=0.92) for c in cols], lag_ratio=0.25), run_time=1.4)
            self.at(2, 0.55)
            self.play(FadeIn(note), run_time=0.7)
        # beat 3: arrows are speakable
        a = Dot(radius=0.14, color=INK).move_to([-2.8, 0.4, 0])
        b = Dot(radius=0.14, color=INK).move_to([2.2, 0.4, 0])
        ar = arrow(a, b)
        lab = mixed("f", size=30, color=INK2).next_to(ar, UP, buff=0.15)
        motto = callig("可道者箭头也", size=44).move_to([-0.3, -1.8, 0])
        with self.beat(3):
            self.play(FadeOut(cols), FadeOut(note), run_time=0.4)
            self.play(FadeIn(a), FadeIn(b), GrowArrow(ar), FadeIn(lab), run_time=1.2)
            self.at(3, 0.5)
            self.play(FadeIn(motto, scale=0.95), run_time=1.0)
        # beat 4: objects live at endpoints
        dim_a = a.copy().set_opacity(0.25)
        dim_b = b.copy().set_opacity(0.25)
        strong = body("对象只活在箭头的端点上", size=30, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(4):
            self.play(a.animate.set_opacity(0.3), b.animate.set_opacity(0.3),
                      ar.animate.set_stroke(width=5), run_time=0.8)
            self.at(4, 0.4)
            self.play(FadeIn(strong), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S2Map(TaoScene):
    SID = "S2Map"
    QUOTE = ""
    TITLE = "二 · 地图"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0: map metaphor
        city_a = Dot(radius=0.13, color=INK).move_to([-2.4, 0.5, 0])
        city_b = Dot(radius=0.13, color=INK).move_to([1.8, 0.5, 0])
        la = body("城市 A", size=26, color=INK2).next_to(city_a, DOWN, buff=0.25)
        lb = body("城市 B", size=26, color=INK2).next_to(city_b, DOWN, buff=0.25)
        road = arrow(city_a, city_b)
        road_l = mixed("公路 f", size=26, color=INK2).next_to(road, UP, buff=0.15)
        meta = VGroup(body("对象 = 点", size=32), body("箭头 = 路", size=32)).arrange(DOWN, buff=0.28).move_to([4.1, 1.7, 0])
        with self.beat(0):
            self.play(FadeIn(city_a), FadeIn(city_b), FadeIn(la), FadeIn(lb), run_time=0.9)
            self.play(GrowArrow(road), FadeIn(road_l), run_time=1.0)
            self.at(0, 0.5)
            self.play(FadeIn(meta, shift=LEFT * 0.1), run_time=0.8)
        # beat 1: map doesn't care interior
        hollow = Circle(radius=0.55, color=INK3, stroke_width=2).move_to([-2.4, 0.5, 0])
        note1 = body("地图不关心城市里面有什么", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(1):
            self.play(FadeOut(meta), run_time=0.3)
            self.play(Create(hollow), FadeIn(note1), run_time=1.1)
        # beat 2: structure on arrows
        note2 = body("结构，写在连线上", size=32, color=INK).move_to([-0.3, -2.3, 0])
        with self.beat(2):
            self.play(FadeOut(hollow), FadeOut(note1), run_time=0.4)
            self.play(road.animate.set_stroke(width=5.5), FadeIn(note2), run_time=1.0)
        # beat 3: multiple arrows
        road2 = arrow(city_a, city_b, color=INK2)
        road2.shift(DOWN * 0.55)
        l2 = mixed("绕行 g", size=24, color=INK2).next_to(road2, DOWN, buff=0.1)
        note3 = body("同一对点，可以有多条箭头", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(3):
            self.play(FadeOut(note2), run_time=0.3)
            self.play(GrowArrow(road2), FadeIn(l2), FadeIn(note3), run_time=1.2)
        # beat 4: self-loop preview
        loop = Circle(radius=0.7, color=INK, stroke_width=3).move_to([4.0, 0.5, 0])
        idlab = mixed("id ?", size=28, color=INK2).next_to(loop, DOWN, buff=0.2)
        preview = body("环路预告：恒等", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(4):
            self.play(FadeOut(note3), run_time=0.3)
            self.play(Create(loop), FadeIn(idlab), FadeIn(preview), run_time=1.2)
        self.end_scene()


# =====================================================================================
class S3Types(TaoScene):
    SID = "S3Types"
    QUOTE = ""
    TITLE = "三 · 类型是对象"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        nodes = VGroup(mixed("Int", size=36), mixed("String", size=36), mixed("Bool", size=36))
        nodes[0].move_to([-3.4, 0.9, 0])
        nodes[1].move_to([0.0, 0.9, 0])
        nodes[2].move_to([3.4, 0.9, 0])
        with self.beat(0):
            self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.22), run_time=1.4)
        a1 = arrow(nodes[0], nodes[1])
        a2 = arrow(nodes[1], nodes[0], color=INK2)
        l1 = mixed("toString", size=24, color=INK2).next_to(a1, UP, buff=0.1)
        l2 = mixed("length", size=24, color=INK2).next_to(a2, DOWN, buff=0.1)
        cap = body("类型是对象；函数是箭头", size=30, color=INK2).move_to([-0.2, -2.3, 0])
        with self.beat(1):
            self.play(GrowArrow(a1), FadeIn(l1), run_time=0.9)
            self.at(1, 0.45)
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(cap), run_time=1.0)
        code = make_code("s_sig", size=26, line_h=0.48).place(-5.8, 1.6)
        sig_note = body("类型签名 = 箭头声明", size=28, color=INK2).move_to([2.5, -0.6, 0])
        with self.beat(2):
            self.play(FadeOut(VGroup(nodes, a1, a2, l1, l2, cap)), run_time=0.45)
            self.play(code.write(), run_time=1.5)
            self.at(2, 0.45)
            self.play(code.focus(0, 1), FadeIn(sig_note), run_time=0.8)
        traveler = Dot(radius=0.1, color=SEAL).move_to([-3.5, 0.2, 0])
        cities = VGroup(mixed("Int", size=30), mixed("String", size=30))
        cities[0].move_to([-3.5, 1.0, 0])
        cities[1].move_to([2.5, 1.0, 0])
        path = arrow(cities[0], cities[1])
        path_l = mixed("toString", size=24, color=INK2).next_to(path, UP, buff=0.1)
        note_v = body("值是旅客；类型是城市", size=28, color=INK2).move_to([-0.2, -2.3, 0])
        with self.beat(3):
            self.play(FadeOut(code), FadeOut(sig_note), run_time=0.4)
            self.play(FadeIn(cities), GrowArrow(path), FadeIn(path_l), FadeIn(traveler), run_time=1.1)
            self.play(traveler.animate.move_to([2.5, 0.2, 0]), run_time=1.4)
            self.play(FadeIn(note_v), run_time=0.6)
        bool_n = mixed("Bool", size=36).move_to([-0.2, 0.6, 0])
        loop1 = Arc(start_angle=PI * 0.15, angle=PI * 1.5, radius=0.85, color=INK, stroke_width=3).move_to([-0.2, 0.6, 0])
        loop2 = Arc(start_angle=PI * 0.15, angle=-PI * 1.5, radius=1.15, color=INK2, stroke_width=2.5).move_to([-0.2, 0.6, 0])
        ln1 = mixed("not", size=24, color=INK2).move_to([1.3, 1.5, 0])
        ln2 = mixed("id", size=24, color=INK2).move_to([-1.7, -0.3, 0])
        note_m = body("同一对类型，多条箭头", size=28, color=INK2).move_to([-0.2, -2.3, 0])
        with self.beat(4):
            self.play(FadeOut(VGroup(cities, path, path_l, traveler, note_v)), run_time=0.4)
            self.play(FadeIn(bool_n), Create(loop1), Create(loop2), FadeIn(ln1), FadeIn(ln2), FadeIn(note_m), run_time=1.6)
        tip = body("先把计算画成图，再谈实现", size=30, color=INK2).move_to([-0.2, -2.3, 0])
        with self.beat(5):
            self.play(FadeOut(note_m), run_time=0.3)
            self.play(FadeIn(tip), run_time=0.8)
        self.end_scene()


# =====================================================================================
class S4Compose(TaoScene):
    SID = "S4Compose"
    QUOTE = ""
    TITLE = "四 · 复合"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        A = mixed("a", size=36).move_to([-3.6, 0.4, 0])
        B = mixed("b", size=36).move_to([-0.3, 0.4, 0])
        C = mixed("c", size=36).move_to([3.0, 0.4, 0])
        f = arrow(A, B)
        g = arrow(B, C)
        fl = mixed("f", size=26, color=INK2).next_to(f, UP, buff=0.1)
        gl = mixed("g", size=26, color=INK2).next_to(g, UP, buff=0.1)
        with self.beat(0):
            self.play(FadeIn(A), FadeIn(B), FadeIn(C), GrowArrow(f), GrowArrow(g),
                      FadeIn(fl), FadeIn(gl), run_time=1.5)
            comp = ArcBetweenPoints(A.get_center() + DOWN * 0.4, C.get_center() + DOWN * 0.4,
                                    angle=PI * 0.45, color=INK, stroke_width=3)
            comp = DashedVMobject(comp, num_dashes=28)
            cl = mixed("g ∘ f", size=30).next_to(comp, DOWN, buff=0.15)
            self.play(Create(comp), FadeIn(cl), run_time=1.0)
            self.comp, self.cl = comp, cl
        hs = VGroup(
            mixed("g ∘ f", size=34),
            body("⟷", size=30, color=INK3),
            mixed("g . f", size=34),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, -2.2, 0])
        with self.beat(1):
            self.play(FadeIn(hs), run_time=1.0)
        pipe = body("像水管：从右往左读 · 先 f 后 g", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(hs), run_time=0.3)
            self.play(FadeIn(pipe), run_time=0.8)
        law = mixed("(h ∘ g) ∘ f  =  h ∘ (g ∘ f)", size=34).move_to([-0.3, 1.8, 0])
        law2 = body("结合律：括号怎么加，结果一样", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(3):
            self.play(FadeOut(pipe), run_time=0.3)
            self.play(FadeIn(law, shift=DOWN * 0.1), run_time=1.0)
            self.at(3, 0.45)
            self.play(FadeIn(law2), run_time=0.7)
        longc = mixed("h  =  j ∘ k ∘ f", size=36).move_to([-0.3, -1.0, 0])
        prog = body("程序 = 分解，再复合", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(4):
            self.play(FadeOut(law2), run_time=0.3)
            self.play(FadeIn(longc), FadeIn(prog), run_time=1.1)
        q1 = serif("“Composition is the essence of category.”", size=34, color=INK)
        q2 = body("范畴的本质，就是复合。", size=30, color=INK2)
        q3 = body("—— Milewski，《程序员的范畴论》第 1 章", size=22, color=INK3)
        quote = VGroup(q1, q2, q3).arrange(DOWN, buff=0.25).move_to([-0.3, 0.2, 0])
        with self.beat(5):
            self.play(FadeOut(VGroup(A, B, C, f, g, fl, gl, self.comp, self.cl, law, longc, prog)), run_time=0.5)
            self.play(FadeIn(q1), run_time=1.0)
            self.play(FadeIn(q2), FadeIn(q3), run_time=0.9)
        self.end_scene()


# =====================================================================================
class S5Identity(TaoScene):
    SID = "S5Identity"
    QUOTE = ""
    TITLE = "五 · 恒等"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        ring = Circle(radius=0.7, color=INK, stroke_width=3.5).move_to([-0.3, 0.5, 0])
        lab = mixed("id", size=36).next_to(ring, RIGHT, buff=0.35)
        note = body("恒等：什么也不做的环路", size=28, color=INK2).move_to([-0.3, -2.2, 0])
        with self.beat(0):
            self.play(Create(ring), FadeIn(lab), run_time=1.2)
            self.at(0, 0.45)
            self.play(FadeIn(note), run_time=0.7)
        law = mixed("id_b ∘ f  =  f  =  f ∘ id_a", size=34).move_to([-0.3, 1.7, 0])
        wu = callig("无为", size=48, color=INK).move_to([-0.3, -0.9, 0])
        with self.beat(1):
            self.play(FadeOut(note), run_time=0.3)
            self.play(FadeIn(law), FadeIn(wu, scale=0.95), run_time=1.3)
        code = make_code("s_id", size=28, line_h=0.5).place(-5.5, 1.4)
        with self.beat(2):
            self.play(FadeOut(ring), FadeOut(lab), FadeOut(law), FadeOut(wu), run_time=0.45)
            self.play(code.write(), run_time=1.4)
            self.play(code.focus(0, 2), run_time=0.6)
        unit = VGroup(
            body("恒等是复合的单位", size=32),
            body("像乘法里的 1", size=28, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([2.2, 0.3, 0])
        with self.beat(3):
            self.play(FadeIn(unit, shift=LEFT * 0.1), run_time=1.0)
        cards = VGroup(
            VGroup(
                body("规矩一", size=24, color=SEAL),
                body("可接则接，且结合", size=28),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                body("规矩二", size=24, color=SEAL),
                body("每对象有恒等，且无为", size=28),
            ).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.2).move_to([-0.2, -1.5, 0])
        with self.beat(4):
            self.play(FadeOut(code), FadeOut(unit), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.3), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S6Haskell(TaoScene):
    SID = "S6Haskell"
    QUOTE = ""
    TITLE = "六 · 落到代码"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        code1 = make_code("s_id", size=24, line_h=0.42).place(-6.2, 2.0)
        code2 = make_code("s_compose", size=24, line_h=0.42).place(-6.2, 0.2)
        with self.beat(0):
            self.play(code1.write(), run_time=1.2)
            self.play(code2.write(), run_time=1.2)
        with self.beat(1):
            self.play(code1.focus(0, 1), run_time=0.7)
            self.at(1, 0.4)
            self.play(code1.unfocus(), code2.focus(0, 2), run_time=0.9)
        code3 = make_code("s_shout", size=22, line_h=0.40).place(-6.2, 2.1)
        with self.beat(2):
            self.play(FadeOut(code1), FadeOut(code2), run_time=0.4)
            self.play(code3.write(), run_time=1.6)
            self.play(code3.focus(0, 3), run_time=0.6)
        ex = VGroup(
            mixed("shout 42", size=30),
            mixed("= strlen (toString 42)", size=30),
            mixed("= strlen \"42\"", size=30),
            mixed("= 2", size=34, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.0, 0.3, 0])
        with self.beat(3):
            self.play(code3.focus(4, 6), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(l) for l in ex], lag_ratio=0.28), run_time=2.0)
        dot = mixed("shoutDot = strlen . toString", size=28).move_to([-0.2, -2.2, 0])
        with self.beat(4):
            self.play(code3.focus(8, 10), FadeIn(dot), run_time=1.0)
        gate = body("类型对不上，路就修不通", size=30, color=INK2).move_to([-0.2, -2.2, 0])
        with self.beat(5):
            self.play(FadeOut(dot), run_time=0.3)
            self.play(FadeIn(gate), run_time=0.8)
        self.end_scene()


# =====================================================================================
class S7Next(TaoScene):
    SID = "S7Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value()).move_to([0, 0.8, 0]))
        points = VGroup(
            body("对象不可道，箭头可道", size=30),
            body("类型是对象，函数是态射", size=30),
            body("复合与恒等，撑起范畴", size=30),
        ).arrange(DOWN, buff=0.28).move_to([0, -1.5, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.55)
        next_title = callig("有无相生", size=56).move_to([0, 0.6, 0])
        next_sub = body("下一集：Void 与单元类型 ()", size=30, color=INK2).move_to([0, -0.3, 0])
        next_tag = body("深讲 02", size=26, color=SEAL).move_to([0, -1.0, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(next_sub), FadeIn(next_tag), run_time=1.3)
        motto = callig("看箭头", size=72).move_to([0, 0.7, 0])
        bye = body("道可道，非常道。我们下集见。", size=30, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(next_sub), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
