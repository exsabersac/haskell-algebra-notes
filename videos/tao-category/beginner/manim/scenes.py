# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from content import SCENES

META = {s["id"]: s for s in SCENES}


def meta_cls(sid):
    m = META[sid]
    return dict(SID=sid, QUOTE=m["quote"], TITLE=m["title"], CHAPTER=m["chapter"])


def box(label, w=1.6, h=1.0, color=INK):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                         stroke_color=color, stroke_width=3, fill_opacity=0)
    t = mixed(label, size=28, color=color).move_to(r)
    return VGroup(r, t)


# =====================================================================================
class S0Title(TaoScene):
    SID = "S0Title"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value()).move_to([0, 0.55, 0]))
        title = callig("道可道", size=118).move_to([0, 0.62, 0])
        sub = body("范畴入门 · Haskell · 《道德经》", size=32, color=INK2).move_to([0, -2.15, 0])
        tag = body("入门篇", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.6, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.8)
        ring.clear_updaters()
        left = VGroup(ring, title)
        chapters = [
            ("一", "道可道", "对象、箭头与复合"),
            ("二", "有无相生", "Void 与单元类型"),
            ("三", "道生一", "Maybe、列表与折叠"),
            ("四", "反者道之动", "展开与折叠"),
            ("五", "知其雄，守其雌", "函子与 Applicative"),
            ("六", "无为而无不为", "单子与 do 记法"),
        ]
        rows = VGroup()
        for n, q, t in chapters:
            r = VGroup(callig(n, size=40), callig(q, size=40), body(t, size=26, color=INK2))
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].next_to(r[1], RIGHT, buff=0.4).align_to(r[1], DOWN).shift(UP * 0.04)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.5, 0.55, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.72).move_to([-4.1, 0.55, 0]), FadeOut(sub), FadeOut(tag), run_time=1.2)
            for i, r in enumerate(rows):
                self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.55)
                self.at(1, 0.12 + 0.13 * (i + 1))
        rhythm = VGroup(
            body("节奏", size=24, color=INK3),
            body("原文  →  日常比喻  →  几行代码", size=30, color=INK),
        ).arrange(DOWN, buff=0.2).move_to([0, -2.4, 0])
        with self.beat(2):
            self.play(FadeIn(rhythm, shift=UP * 0.1), run_time=1.0)
        refs = VGroup(
            body("参考：Bartosz Milewski　·　进阶篇另见", size=24, color=INK3),
            serif("Category Theory for Programmers  ·  The Dao of Functional Programming", size=26, color=INK2),
        ).arrange(DOWN, buff=0.12).move_to([0, -2.35, 0])
        s = seal(0.8).next_to(left, DOWN, buff=0.15).shift(RIGHT * 1.3)
        with self.beat(3):
            self.play(FadeOut(rhythm), run_time=0.4)
            self.play(FadeIn(refs, shift=UP * 0.1), run_time=1.0)
            self.at(3, 0.55)
            self.play(FadeIn(s, scale=1.6), run_time=0.5)
        self.end_scene()


# =====================================================================================
class S1Compose(TaoScene):
    locals().update(meta_cls("S1Compose"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: map metaphor
        city_a = Dot(radius=0.12, color=INK).move_to([-2.2, 0.4, 0])
        city_b = Dot(radius=0.12, color=INK).move_to([1.8, 0.4, 0])
        la = body("城市 A", size=26, color=INK2).next_to(city_a, DOWN, buff=0.25)
        lb = body("城市 B", size=26, color=INK2).next_to(city_b, DOWN, buff=0.25)
        road = arrow(city_a, city_b)
        road_l = mixed("公路 f", size=26, color=INK2).next_to(road, UP, buff=0.15)
        meta = VGroup(
            body("对象 = 点", size=32),
            body("箭头 = 路", size=32),
        ).arrange(DOWN, buff=0.3).move_to([4.0, 1.8, 0])
        with self.beat(1):
            self.play(FadeIn(city_a), FadeIn(city_b), FadeIn(la), FadeIn(lb), run_time=0.8)
            self.play(GrowArrow(road), FadeIn(road_l), run_time=1.0)
            self.at(1, 0.45)
            self.play(FadeIn(meta, shift=LEFT * 0.1), run_time=0.8)
        # beat 2: types as objects
        nodes = VGroup(
            mixed("Int", size=34),
            mixed("String", size=34),
            mixed("Bool", size=34),
        )
        nodes[0].move_to([-3.2, 0.8, 0])
        nodes[1].move_to([0.2, 0.8, 0])
        nodes[2].move_to([3.2, 0.8, 0])
        a1 = arrow(nodes[0], nodes[1])
        a2 = arrow(nodes[1], nodes[0], color=INK2)
        l1 = mixed("toString", size=24, color=INK2).next_to(a1, UP, buff=0.1)
        l2 = mixed("length", size=24, color=INK2).next_to(a2, DOWN, buff=0.1)
        cap = body("类型是对象；函数是箭头", size=30, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(2):
            self.play(FadeOut(VGroup(city_a, city_b, la, lb, road, road_l, meta)), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.2), run_time=1.2)
            self.at(2, 0.35)
            self.play(GrowArrow(a1), FadeIn(l1), run_time=0.8)
            self.at(2, 0.65)
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(cap), run_time=1.0)
        # beat 3: composition
        A = mixed("A", size=36).move_to([-3.5, 0.3, 0])
        B = mixed("B", size=36).move_to([-0.3, 0.3, 0])
        C = mixed("C", size=36).move_to([2.9, 0.3, 0])
        f = arrow(A, B)
        g = arrow(B, C)
        fl = mixed("f", size=26, color=INK2).next_to(f, UP, buff=0.1)
        gl = mixed("g", size=26, color=INK2).next_to(g, UP, buff=0.1)
        comp = ArcBetweenPoints(A.get_center() + DOWN * 0.35, C.get_center() + DOWN * 0.35,
                                angle=PI * 0.45, color=INK, stroke_width=3)
        comp = DashedVMobject(comp, num_dashes=28)
        cl = mixed("g ∘ f", size=30).next_to(comp, DOWN, buff=0.15)
        pipe = body("像管道：从右往左读", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(3):
            self.play(FadeOut(VGroup(nodes, a1, a2, l1, l2, cap)), run_time=0.5)
            self.play(FadeIn(A), FadeIn(B), FadeIn(C), GrowArrow(f), GrowArrow(g), FadeIn(fl), FadeIn(gl), run_time=1.4)
            self.at(3, 0.4)
            self.play(Create(comp), FadeIn(cl), run_time=1.0)
            self.at(3, 0.7)
            self.play(FadeIn(pipe), run_time=0.6)
        # beat 4: associativity
        law = mixed("(h ∘ g) ∘ f  =  h ∘ (g ∘ f)", size=36)
        law.move_to([-0.3, 1.6, 0])
        law2 = body("结合律：怎么加括号，结果一样", size=30, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(4):
            self.play(FadeOut(pipe), run_time=0.3)
            self.play(FadeIn(law, shift=DOWN * 0.1), run_time=1.0)
            self.at(4, 0.5)
            self.play(FadeIn(law2), run_time=0.7)
        # beat 5: identity
        id_ring = Circle(radius=0.55, color=INK, stroke_width=3).move_to([-0.3, 0.3, 0])
        id_lab = mixed("id", size=32).next_to(id_ring, RIGHT, buff=0.3)
        id_note = body("恒等：什么也不做的环路", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        code = make_code("s1", size=22, line_h=0.40).place(-6.2, 2.0)
        with self.beat(5):
            self.play(FadeOut(VGroup(A, B, C, f, g, fl, gl, comp, cl, law, law2)), run_time=0.5)
            self.play(Create(id_ring), FadeIn(id_lab), run_time=1.0)
            self.at(5, 0.35)
            self.play(code.write(), run_time=1.8)
            self.play(code.focus(0, 2), FadeIn(id_note), run_time=0.7)
        # beat 6: shout example
        ex = VGroup(
            mixed("shout 42  =  strlen (toString 42)", size=30),
            mixed("           =  strlen \"42\"", size=30),
            mixed("           =  2", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([1.5, 0.4, 0])
        with self.beat(6):
            self.play(FadeOut(id_ring), FadeOut(id_lab), FadeOut(id_note), run_time=0.4)
            self.play(code.focus(8, 16), run_time=0.6)
            self.at(6, 0.3)
            self.play(LaggedStart(*[FadeIn(l) for l in ex], lag_ratio=0.3), run_time=1.8)
        # beat 7: Milewski quote
        q1 = serif("“Composition is the essence of category.”", size=36, color=INK)
        q2 = body("范畴的本质，就是复合。", size=32, color=INK2)
        q3 = body("—— Milewski，《程序员的范畴论》第 1 章", size=22, color=INK3)
        quote = VGroup(q1, q2, q3).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(7):
            self.play(FadeOut(code), FadeOut(ex), run_time=0.5)
            self.play(FadeIn(q1), run_time=1.0)
            self.play(FadeIn(q2), FadeIn(q3), run_time=0.9)
        # beat 8: motto
        motto = callig("可道者箭头也", size=52, color=INK).move_to([-0.3, 0.5, 0])
        subm = body("对象只存在于箭头的关系里", size=30, color=INK2).move_to([-0.3, -0.6, 0])
        with self.beat(8):
            self.play(FadeOut(quote), run_time=0.5)
            self.play(FadeIn(motto, scale=0.95), run_time=1.2)
            self.at(8, 0.45)
            self.play(FadeIn(subm), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S2YouWu(TaoScene):
    locals().update(meta_cls("S2YouWu"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: yin yang intro
        wu_lab = VGroup(callig("无", size=64), mixed("Void", size=30, color=INK2)).arrange(DOWN, buff=0.2)
        you_lab = VGroup(callig("有", size=64), mixed("()", size=30, color=INK2)).arrange(DOWN, buff=0.2)
        wu_lab.move_to([-3.0, 0.6, 0])
        you_lab.move_to([2.4, 0.6, 0])
        mirror = DashedLine([0.1, 2.4, 0], [0.1, -1.8, 0], color=INK3, dash_length=0.12)
        mid = body("阴  ·  阳", size=28, color=INK3).move_to([-0.3, -2.3, 0])
        with self.beat(1):
            self.play(FadeIn(wu_lab), FadeIn(you_lab), Create(mirror), run_time=1.4)
            self.at(1, 0.55)
            self.play(FadeIn(mid), run_time=0.6)
        # beat 2: empty room
        empty = RoundedRectangle(corner_radius=0.15, width=3.2, height=2.2,
                                 stroke_color=INK, stroke_width=2.5).move_to([-0.3, 0.4, 0])
        empty_t = body("空屋 · 零个值", size=30, color=INK2).next_to(empty, DOWN, buff=0.3)
        vlab = mixed("Void", size=36).move_to(empty)
        with self.beat(2):
            self.play(FadeOut(wu_lab), FadeOut(you_lab), FadeOut(mirror), FadeOut(mid), run_time=0.5)
            self.play(Create(empty), FadeIn(vlab), FadeIn(empty_t), run_time=1.2)
        # beat 3: absurd
        V = mixed("Void", size=34).move_to([-3.5, 0.5, 0])
        targets = VGroup(*[mixed(t, size=30) for t in ["A", "B", "C"]])
        targets.arrange(DOWN, buff=0.7).move_to([2.5, 0.5, 0])
        arrs = VGroup(*[arrow(V, t) for t in targets])
        alabs = VGroup(*[mixed("absurd", size=20, color=INK2).next_to(a, UP if i == 0 else (DOWN if i == 2 else ORIGIN), buff=0.05)
                         for i, a in enumerate(arrs)])
        note = body("没有输入，无需说话", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(3):
            self.play(FadeOut(empty), FadeOut(vlab), FadeOut(empty_t), run_time=0.4)
            self.play(FadeIn(V), FadeIn(targets), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.25), FadeIn(alabs), run_time=1.6)
            self.at(3, 0.65)
            self.play(FadeIn(note), run_time=0.6)
        # beat 4: const ()
        srcs = VGroup(*[mixed(t, size=30) for t in ["A", "B", "C"]])
        srcs.arrange(DOWN, buff=0.7).move_to([-3.5, 0.5, 0])
        U = mixed("()", size=34).move_to([2.5, 0.5, 0])
        arrs2 = VGroup(*[arrow(s, U) for s in srcs])
        al2 = VGroup(*[mixed("const ()", size=20, color=INK2).next_to(a, UP if i == 0 else (DOWN if i == 2 else ORIGIN), buff=0.05)
                       for i, a in enumerate(arrs2)])
        note2 = body("万物归于同一个点", size=28, color=INK2).move_to([-0.3, -2.3, 0])
        with self.beat(4):
            self.play(FadeOut(V), FadeOut(targets), FadeOut(arrs), FadeOut(alabs), FadeOut(note), run_time=0.5)
            self.play(FadeIn(srcs), FadeIn(U), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs2], lag_ratio=0.25), FadeIn(al2), run_time=1.6)
            self.at(4, 0.6)
            self.play(FadeIn(note2), run_time=0.6)
        # beat 5: mirror flip
        left_g = VGroup(
            mixed("Void → a", size=32),
            body("从无通往万物", size=26, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([-3.0, 0.5, 0])
        right_g = VGroup(
            mixed("a → ()", size=32),
            body("从万物归于一点", size=26, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([2.4, 0.5, 0])
        flip = body("箭头一翻，无变成有", size=30, color=INK).move_to([-0.3, -2.3, 0])
        mir = DashedLine([-0.3, 2.2, 0], [-0.3, -1.6, 0], color=INK3, dash_length=0.12)
        with self.beat(5):
            self.play(FadeOut(srcs), FadeOut(U), FadeOut(arrs2), FadeOut(al2), FadeOut(note2), run_time=0.5)
            self.play(FadeIn(left_g), Create(mir), run_time=1.0)
            self.at(5, 0.4)
            self.play(FadeIn(right_g), run_time=0.9)
            self.at(5, 0.7)
            self.play(FadeIn(flip), run_time=0.6)
        # beat 6: metaphors + code wu/you
        env = VGroup(body("空信封", size=28), mixed("Void", size=24, color=INK3)).arrange(DOWN, buff=0.15)
        boxm = VGroup(body("公用邮筒", size=28), mixed("()", size=24, color=INK3)).arrange(DOWN, buff=0.15)
        env.move_to([-3.2, 1.5, 0]); boxm.move_to([2.2, 1.5, 0])
        cw = make_code("s2wu", size=26, line_h=0.48).place(-6.0, 0.3)
        cy = make_code("s2you", size=26, line_h=0.48).place(-0.5, 0.3)
        with self.beat(6):
            self.play(FadeOut(left_g), FadeOut(right_g), FadeOut(mir), FadeOut(flip), run_time=0.5)
            self.play(FadeIn(env), FadeIn(boxm), run_time=0.8)
            self.at(6, 0.4)
            self.play(cw.write(), cy.write(), run_time=1.4)
        # beat 7: units
        cb = make_code("s2b", size=24, line_h=0.46).place(-6.2, 1.6)
        with self.beat(7):
            self.play(FadeOut(env), FadeOut(boxm), FadeOut(cw), FadeOut(cy), run_time=0.5)
            self.play(cb.write(), run_time=1.6)
            self.play(cb.focus(0, 2), run_time=0.6)
            self.at(7, 0.5)
            self.play(cb.focus(4, 6), run_time=0.6)
        # beat 8: bridge
        bridge = VGroup(
            callig("有无相生", size=48),
            body("下一句：从「无」里生出东西 →", size=28, color=INK2),
        ).arrange(DOWN, buff=0.4).move_to([-0.3, 0.3, 0])
        with self.beat(8):
            self.play(FadeOut(cb), run_time=0.5)
            self.play(FadeIn(bridge[0], scale=0.95), run_time=1.0)
            self.at(8, 0.5)
            self.play(FadeIn(bridge[1]), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S3Maybe(TaoScene):
    locals().update(meta_cls("S3Maybe"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: intro
        ref = body("DaoFP 第 7 章 Recursion", size=24, color=INK3).move_to([-0.3, 2.4, 0])
        icons = VGroup(
            box("Maybe", w=2.0, h=1.1),
            box("List", w=2.0, h=1.1),
        ).arrange(RIGHT, buff=1.2).move_to([-0.3, 0.2, 0])
        with self.beat(1):
            self.play(FadeIn(ref), run_time=0.6)
            self.play(FadeIn(icons[0], shift=UP * 0.1), FadeIn(icons[1], shift=UP * 0.1), run_time=1.2)
        # beat 2: Maybe definition
        code_m = make_code("s3maybe", size=24, line_h=0.44).place(-6.2, 2.0)
        noth = box("Nothing", w=2.2, h=0.9).move_to([2.0, 1.2, 0])
        just = box("Just x", w=2.2, h=0.9).move_to([2.0, -0.3, 0])
        with self.beat(2):
            self.play(FadeOut(ref), FadeOut(icons), run_time=0.4)
            self.play(code_m.write(), run_time=1.6)
            self.play(code_m.focus(0, 1), run_time=0.5)
            self.at(2, 0.4)
            self.play(FadeIn(noth), FadeIn(just), run_time=0.9)
        # beat 3: chain 0,1,2,3
        stages = []
        labels_c = ["无", "一", "二", "三"]
        counts = [0, 1, 2, 3]
        names = ["Void", "Maybe Void", "Maybe² Void", "Maybe³ Void"]
        row = VGroup()
        for i, (lab, cnt, nm) in enumerate(zip(labels_c, counts, names)):
            d = dots(cnt, gap=0.22).scale(1.1)
            t = callig(lab, size=36)
            n = mixed(nm, size=18, color=INK3)
            g = VGroup(t, d, n).arrange(DOWN, buff=0.2)
            row.add(g)
        row.arrange(RIGHT, buff=0.7).move_to([-0.4, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(code_m), FadeOut(noth), FadeOut(just), run_time=0.5)
            for i, g in enumerate(row):
                self.play(FadeIn(g, shift=RIGHT * 0.1), run_time=0.7)
                self.at(3, 0.15 + 0.2 * (i + 1))
        # beat 4: more layers
        grow = body("每多一层，就多一个「在此停住」的选择", size=30, color=INK2).move_to([-0.3, -2.3, 0])
        dots_more = VGroup(*[Dot(radius=0.06, color=INK2) for _ in range(8)]).arrange(RIGHT, buff=0.15)
        dots_more.move_to([-0.3, -1.4, 0])
        more_l = body("……万物", size=26, color=INK3).next_to(dots_more, RIGHT, buff=0.3)
        with self.beat(4):
            self.play(FadeIn(grow), run_time=0.8)
            self.at(4, 0.45)
            self.play(FadeIn(dots_more), FadeIn(more_l), run_time=1.0)
        # beat 5: list growth
        lists = VGroup(
            mixed("[]", size=34),
            mixed("1 : []", size=34),
            mixed("1 : 2 : []", size=34),
            mixed("1 : 2 : 3 : []", size=34),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-1.5, 0.5, 0])
        side = VGroup(
            body("空 = 无", size=28, color=INK2),
            body("接一个 = 一", size=28, color=INK2),
            body("再接 = 二", size=28, color=INK2),
            body("任意长 = 万物", size=28, color=INK),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([2.5, 0.5, 0])
        with self.beat(5):
            self.play(FadeOut(row), FadeOut(grow), FadeOut(dots_more), FadeOut(more_l), run_time=0.5)
            for i in range(4):
                self.play(FadeIn(lists[i]), FadeIn(side[i]), run_time=0.7)
                self.at(5, 0.15 + 0.18 * (i + 1))
        # beat 6: fold metaphor
        paper = RoundedRectangle(corner_radius=0.08, width=5.5, height=1.4,
                                 stroke_color=INK, stroke_width=2).move_to([-0.3, 0.8, 0])
        cells = VGroup(*[mixed(str(n), size=32) for n in [1, 2, 3]]).arrange(RIGHT, buff=0.8)
        cells.move_to(paper)
        fold_note = body("折叠 = 沿着构造的逆方向走", size=30, color=INK2).move_to([-0.3, -1.5, 0])
        with self.beat(6):
            self.play(FadeOut(lists), FadeOut(side), run_time=0.5)
            self.play(Create(paper), FadeIn(cells), run_time=1.0)
            self.at(6, 0.4)
            self.play(FadeIn(fold_note), run_time=0.7)
            self.at(6, 0.7)
            self.play(paper.animate.stretch_to_fit_width(2.2), cells.animate.arrange(RIGHT, buff=0.25).move_to([-0.3, 0.8, 0]), run_time=1.2)
        # beat 7: sumList code
        code_l = make_code("s3list", size=26, line_h=0.50).place(-6.2, 1.8)
        result = VGroup(
            mixed("sumList [1,2,3]", size=30),
            mixed("= 1 + (2 + (3 + 0))", size=30),
            mixed("= 6", size=36, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.0, 0.3, 0])
        with self.beat(7):
            self.play(FadeOut(paper), FadeOut(cells), FadeOut(fold_note), run_time=0.5)
            self.play(code_l.write(), run_time=1.4)
            self.play(code_l.focus(3, 5), run_time=0.5)
            self.at(7, 0.4)
            self.play(LaggedStart(*[FadeIn(r) for r in result], lag_ratio=0.35), run_time=1.8)
        # beat 8: close
        close = VGroup(
            callig("夫物芸芸，各复归其根", size=44),
            body("下一句：把生与归反过来看 →", size=28, color=INK2),
        ).arrange(DOWN, buff=0.4).move_to([-0.3, 0.3, 0])
        with self.beat(8):
            self.play(FadeOut(code_l), FadeOut(result), run_time=0.5)
            self.play(FadeIn(close[0]), run_time=1.1)
            self.at(8, 0.55)
            self.play(FadeIn(close[1]), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S4FoldUnfold(TaoScene):
    locals().update(meta_cls("S4FoldUnfold"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: reverse direction
        left = VGroup(body("折叠", size=36), mixed("list → number", size=26, color=INK2)).arrange(DOWN, buff=0.2)
        right = VGroup(body("展开", size=36), mixed("seed → list", size=26, color=INK2)).arrange(DOWN, buff=0.2)
        left.move_to([-3.0, 0.5, 0]); right.move_to([2.4, 0.5, 0])
        arr_l = arrow([ -0.8, 0.5, 0], [-1.8, 0.5, 0])
        arr_r = arrow([0.2, 0.5, 0], [1.2, 0.5, 0])
        with self.beat(1):
            self.play(FadeIn(left), GrowArrow(arr_l), run_time=1.0)
            self.at(1, 0.45)
            self.play(FadeIn(right), GrowArrow(arr_r), run_time=1.0)
        # beat 2: fold = unpack
        pack = box("1 : 2 : 3 : []", w=3.8, h=1.0).move_to([-0.3, 1.0, 0])
        steps = VGroup(
            body("打开一层 → 处理头 → 对尾重复", size=28, color=INK2),
        ).move_to([-0.3, -0.5, 0])
        cf = make_code("s4fold", size=26, line_h=0.50).place(-6.0, -1.5)
        with self.beat(2):
            self.play(FadeOut(left), FadeOut(right), FadeOut(arr_l), FadeOut(arr_r), run_time=0.4)
            self.play(FadeIn(pack), run_time=0.8)
            self.at(2, 0.35)
            self.play(FadeIn(steps), run_time=0.7)
            self.at(2, 0.6)
            self.play(cf.write(), run_time=1.0)
        # beat 3: unfold = plant
        seed = Dot(radius=0.15, color=INK).move_to([-3.5, 0.5, 0])
        seed_l = body("种子", size=24, color=INK2).next_to(seed, DOWN, buff=0.2)
        fruit = mixed("n", size=32).move_to([-0.5, 1.2, 0])
        seed2 = Dot(radius=0.12, color=INK2).move_to([-0.5, -0.3, 0])
        seed2_l = body("更小的种子", size=22, color=INK3).next_to(seed2, DOWN, buff=0.15)
        a1 = arrow(seed, fruit)
        a2 = arrow(seed, seed2, color=INK2)
        cu = make_code("s4unfold", size=24, line_h=0.44).place(-6.2, -2.0)
        with self.beat(3):
            self.play(FadeOut(pack), FadeOut(steps), FadeOut(cf), run_time=0.4)
            self.play(FadeIn(seed), FadeIn(seed_l), run_time=0.6)
            self.at(3, 0.3)
            self.play(GrowArrow(a1), FadeIn(fruit), GrowArrow(a2), FadeIn(seed2), FadeIn(seed2_l), run_time=1.4)
            self.at(3, 0.65)
            self.play(cu.write(), run_time=1.2)
        # beat 4: countdown animation
        nums = VGroup(*[mixed(str(n), size=40) for n in [5, 4, 3, 2, 1]]).arrange(RIGHT, buff=0.55)
        nums.move_to([-0.3, 0.6, 0])
        nil = mixed("[]", size=36, color=INK3).next_to(nums, RIGHT, buff=0.5)
        with self.beat(4):
            self.play(FadeOut(VGroup(seed, seed_l, fruit, seed2, seed2_l, a1, a2, cu)), run_time=0.5)
            for i, n in enumerate(nums):
                self.play(FadeIn(n, scale=0.9), run_time=0.55)
                self.at(4, 0.12 + 0.14 * (i + 1))
            self.play(FadeIn(nil), run_time=0.5)
        # beat 5: connect
        flow = VGroup(
            mixed("seed", size=30),
            mixed("─ unfold →", size=28, color=INK2),
            mixed("list", size=30),
            mixed("─ fold →", size=28, color=INK2),
            mixed("result", size=30),
        ).arrange(RIGHT, buff=0.25).move_to([-0.3, 0.5, 0])
        motto = body("先生，而后归", size=32, color=INK).move_to([-0.3, -1.5, 0])
        with self.beat(5):
            self.play(FadeOut(nums), FadeOut(nil), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(f) for f in flow], lag_ratio=0.2), run_time=1.6)
            self.at(5, 0.6)
            self.play(FadeIn(motto), run_time=0.7)
        # beat 6: fact
        ch = make_code("s4hylo", size=24, line_h=0.46).place(-6.2, 1.9)
        res = VGroup(
            mixed("fact 10", size=32),
            mixed("= 3,628,800", size=40),
        ).arrange(DOWN, buff=0.3).move_to([2.2, 0.2, 0])
        with self.beat(6):
            self.play(FadeOut(flow), FadeOut(motto), run_time=0.4)
            self.play(ch.write(), run_time=1.4)
            self.play(ch.focus(0, 2), run_time=0.5)
            self.at(6, 0.45)
            self.play(FadeIn(res), run_time=0.9)
        # beat 7: hylo light
        hy = callig("生而不有", size=52).move_to([-0.3, 0.8, 0])
        hy2 = body("hylo：中间列表从不完整落地", size=28, color=INK2).move_to([-0.3, -0.5, 0])
        with self.beat(7):
            self.play(FadeOut(res), run_time=0.3)
            self.play(ch.focus(4, 8), run_time=0.6)
            self.at(7, 0.4)
            self.play(FadeIn(hy), FadeIn(hy2), run_time=1.2)
        # beat 8: duality
        dual = VGroup(
            mixed("fold  ⟷  unfold", size=40),
            body("每学会一个方向，就白得相反的那个", size=28, color=INK2),
        ).arrange(DOWN, buff=0.4).move_to([-0.3, 0.3, 0])
        with self.beat(8):
            self.play(FadeOut(ch), FadeOut(hy), FadeOut(hy2), run_time=0.5)
            self.play(FadeIn(dual[0]), run_time=1.0)
            self.at(8, 0.45)
            self.play(FadeIn(dual[1]), run_time=0.8)
        self.end_scene()


# =====================================================================================
class S5Functor(TaoScene):
    locals().update(meta_cls("S5Functor"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: boxes
        b1 = box("Maybe a", w=2.4, h=1.2).move_to([-2.8, 0.4, 0])
        b2 = box("[a]", w=2.4, h=1.2).move_to([2.0, 0.4, 0])
        cap = body("形状不同，都是「装着值的盒子」", size=28, color=INK2).move_to([-0.3, -2.0, 0])
        with self.beat(1):
            self.play(FadeIn(b1), FadeIn(b2), run_time=1.2)
            self.at(1, 0.5)
            self.play(FadeIn(cap), run_time=0.7)
        # beat 2: fmap idea
        outer = RoundedRectangle(corner_radius=0.15, width=4.5, height=2.4,
                                 stroke_color=INK, stroke_width=3).move_to([-0.3, 0.5, 0])
        inner_a = mixed("a", size=40).move_to([-0.3, 0.5, 0])
        inner_b = mixed("b", size=40).move_to([-0.3, 0.5, 0])
        f_lab = mixed("fmap f", size=28, color=INK2).next_to(outer, UP, buff=0.25)
        shape = body("形状不变，内容可换", size=30, color=INK2).move_to([-0.3, -2.2, 0])
        cf = make_code("s5fmap", size=24, line_h=0.46).place(-6.2, -0.5)
        with self.beat(2):
            self.play(FadeOut(b1), FadeOut(b2), FadeOut(cap), run_time=0.4)
            self.play(Create(outer), FadeIn(inner_a), FadeIn(f_lab), run_time=1.2)
            self.at(2, 0.4)
            self.play(Transform(inner_a, inner_b), run_time=1.0)
            self.play(FadeIn(shape), run_time=0.5)
            self.at(2, 0.7)
            self.play(cf.write(), run_time=1.2)
        # beat 3: Maybe map
        n1 = box("Nothing", w=2.0, h=0.85).move_to([-3.0, 1.0, 0])
        n2 = box("Nothing", w=2.0, h=0.85).move_to([2.0, 1.0, 0])
        j1 = box("Just 3", w=2.0, h=0.85).move_to([-3.0, -0.5, 0])
        j2 = box("Just 4", w=2.0, h=0.85).move_to([2.0, -0.5, 0])
        ar1 = arrow(n1, n2); ar2 = arrow(j1, j2)
        with self.beat(3):
            self.play(FadeOut(outer), FadeOut(inner_a), FadeOut(f_lab), FadeOut(shape), FadeOut(cf), run_time=0.5)
            self.play(FadeIn(n1), GrowArrow(ar1), FadeIn(n2), run_time=1.0)
            self.at(3, 0.4)
            self.play(FadeIn(j1), GrowArrow(ar2), FadeIn(j2), run_time=1.2)
        # beat 4: list map
        before = mixed("[1, 2, 3]", size=36).move_to([-3.0, 0.5, 0])
        after = mixed("[2, 4, 6]", size=36).move_to([2.2, 0.5, 0])
        mid = mixed("map (*2)", size=28, color=INK2).move_to([-0.4, 0.5, 0])
        shape2 = body("长短、顺序都不动 —— 形不变", size=28, color=INK2).move_to([-0.3, -1.8, 0])
        with self.beat(4):
            self.play(FadeOut(VGroup(n1, n2, j1, j2, ar1, ar2)), run_time=0.4)
            self.play(FadeIn(before), FadeIn(mid), run_time=0.8)
            self.at(4, 0.4)
            self.play(FadeIn(after), FadeIn(shape2), run_time=1.0)
        # beat 5: male/female
        male = VGroup(callig("雄", size=56), body("函数 f", size=28, color=INK2)).arrange(DOWN, buff=0.25)
        female = VGroup(callig("雌", size=56), body("形状 / 盒子", size=28, color=INK2)).arrange(DOWN, buff=0.25)
        male.move_to([-3.0, 0.5, 0]); female.move_to([2.2, 0.5, 0])
        note = body("函数再猛，也不能把列表变成 Maybe", size=28, color=INK2).move_to([-0.3, -2.0, 0])
        with self.beat(5):
            self.play(FadeOut(before), FadeOut(after), FadeOut(mid), FadeOut(shape2), run_time=0.4)
            self.play(FadeIn(male), FadeIn(female), run_time=1.2)
            self.at(5, 0.5)
            self.play(FadeIn(note), run_time=0.7)
        # beat 6: laws
        laws = VGroup(
            mixed("fmap id  =  id", size=34),
            mixed("fmap (g ∘ f)  =  fmap g ∘ fmap f", size=30),
        ).arrange(DOWN, buff=0.45).move_to([-0.3, 0.6, 0])
        law_n = body("诚信条款：不守规矩，就不是函子", size=28, color=INK2).move_to([-0.3, -1.8, 0])
        cl = make_code("s5law", size=22, line_h=0.42).place(-6.2, -0.8)
        with self.beat(6):
            self.play(FadeOut(male), FadeOut(female), FadeOut(note), run_time=0.4)
            self.play(FadeIn(laws[0]), run_time=0.8)
            self.at(6, 0.3)
            self.play(FadeIn(laws[1]), run_time=0.8)
            self.at(6, 0.55)
            self.play(FadeIn(law_n), cl.write(), run_time=1.2)
        # beat 7: Applicative
        ca = make_code("s5app", size=24, line_h=0.46).place(-6.2, 1.8)
        app_ex = VGroup(
            mixed("Just (+1) <*> Just 3", size=30),
            mixed("= Just 4", size=36),
        ).arrange(DOWN, buff=0.3).move_to([2.0, 0.3, 0])
        with self.beat(7):
            self.play(FadeOut(laws), FadeOut(law_n), FadeOut(cl), run_time=0.4)
            self.play(ca.write(), run_time=1.4)
            self.at(7, 0.45)
            self.play(FadeIn(app_ex), run_time=1.0)
        # beat 8: creek
        creek = Line([-4.5, -0.8, 0], [3.8, -0.8, 0], color=INK, stroke_width=4)
        c_lab = callig("溪", size=40).next_to(creek, DOWN, buff=0.2)
        left2 = body("雄 · 函数", size=28).move_to([-3.0, 0.8, 0])
        right2 = body("雌 · 形状", size=28).move_to([2.2, 0.8, 0])
        with self.beat(8):
            self.play(FadeOut(ca), FadeOut(app_ex), run_time=0.4)
            self.play(FadeIn(left2), FadeIn(right2), run_time=0.8)
            self.at(8, 0.35)
            self.play(Create(creek), FadeIn(c_lab), run_time=1.2)
        self.end_scene()


# =====================================================================================
class S6Monad(TaoScene):
    locals().update(meta_cls("S6Monad"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: nested boxes
        outer = RoundedRectangle(corner_radius=0.12, width=4.0, height=2.6,
                                 stroke_color=INK, stroke_width=3).move_to([-0.3, 0.4, 0])
        inner = RoundedRectangle(corner_radius=0.1, width=2.2, height=1.3,
                                 stroke_color=INK2, stroke_width=2.5).move_to([-0.3, 0.4, 0])
        val = mixed("b", size=32).move_to(inner)
        lab = mixed("Maybe (Maybe b)", size=28, color=INK2).move_to([-0.3, -2.0, 0])
        with self.beat(1):
            self.play(Create(outer), run_time=0.8)
            self.play(Create(inner), FadeIn(val), run_time=0.9)
            self.at(1, 0.55)
            self.play(FadeIn(lab), run_time=0.6)
        # beat 2: flatten
        flat = RoundedRectangle(corner_radius=0.12, width=2.8, height=1.5,
                                stroke_color=INK, stroke_width=3).move_to([-0.3, 0.4, 0])
        val2 = mixed("b", size=36).move_to(flat)
        lab2 = mixed("Maybe b   ←  bind / join", size=28, color=INK2).move_to([-0.3, -2.0, 0])
        with self.beat(2):
            self.play(Transform(outer, flat), FadeOut(inner), Transform(val, val2), run_time=1.4)
            self.play(Transform(lab, lab2), run_time=0.6)
        # beat 3: assistant metaphor
        asst = VGroup(
            body("助手", size=32),
            body("不会交来「另一个助手手里的字条」", size=26, color=INK2),
            body("而是直接把字条给你", size=26, color=INK2),
            body("—— bind 就是那位会拆套的助手", size=28),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(outer), FadeOut(val), FadeOut(lab), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(a) for a in asst], lag_ratio=0.25), run_time=2.2)
        # beat 4: half example
        cb = make_code("s6bind", size=24, line_h=0.46).place(-6.2, 2.0)
        ex = VGroup(
            mixed("8 >>= half >>= half  =  Just 2", size=28),
            mixed("7 >>= half           =  Nothing", size=28),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([1.8, -0.8, 0])
        with self.beat(4):
            self.play(FadeOut(asst), run_time=0.4)
            self.play(cb.write(), run_time=1.5)
            self.at(4, 0.45)
            self.play(FadeIn(ex), run_time=1.0)
        # beat 5: pipeline
        steps = VGroup(
            box("读配置", w=1.8, h=0.85),
            mixed("→", size=30, color=INK2),
            box("开文件", w=1.8, h=0.85),
            mixed("→", size=30, color=INK2),
            box("解析", w=1.8, h=0.85),
        ).arrange(RIGHT, buff=0.2).move_to([-0.3, 0.8, 0])
        note = body("一步 Nothing，后面自动跳过 —— 不用满屏 if", size=28, color=INK2).move_to([-0.3, -1.5, 0])
        with self.beat(5):
            self.play(FadeOut(cb), FadeOut(ex), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.2), run_time=1.6)
            self.at(5, 0.55)
            self.play(FadeIn(note), run_time=0.7)
        # beat 6: do notation
        cd = make_code("s6do", size=22, line_h=0.40).place(-6.2, 2.1)
        with self.beat(6):
            self.play(FadeOut(steps), FadeOut(note), run_time=0.4)
            self.play(cd.write(), run_time=1.8)
            self.play(cd.focus(7, 11), run_time=0.6)
            self.at(6, 0.55)
            self.play(cd.focus(0, 5), run_time=0.6)
        # beat 7: wu wei
        motto = callig("无为而无不为", size=52).move_to([-0.3, 0.8, 0])
        expl = VGroup(
            body("无为：不强行把效果从盒子里掏出来", size=28, color=INK2),
            body("无不为：排好顺序，该做的都能做完", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, -0.8, 0])
        with self.beat(7):
            self.play(FadeOut(cd), run_time=0.4)
            self.play(FadeIn(motto, scale=0.95), run_time=1.1)
            self.at(7, 0.4)
            self.play(FadeIn(expl), run_time=1.0)
        # beat 8: point ahead
        ahead = VGroup(
            body("进阶篇预告", size=26, color=SEAL),
            body("Fix · 不动点 · 伴随 · 米田引理", size=32),
            body("先把这五块摸熟：箭头 · 有无 · 折叠 · 函子 · 单子", size=26, color=INK2),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(8):
            self.play(FadeOut(motto), FadeOut(expl), run_time=0.5)
            self.play(FadeIn(ahead[0]), run_time=0.6)
            self.at(8, 0.25)
            self.play(FadeIn(ahead[1]), run_time=0.9)
            self.at(8, 0.6)
            self.play(FadeIn(ahead[2]), run_time=0.9)
        self.end_scene()


# =====================================================================================
class S7Ending(TaoScene):
    SID = "S7Ending"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=9).move_to([0, 0.5, 0]))
        six = ["道可道", "有无相生", "道生一", "反者道之动", "知其雄", "无为"]
        ang = [90, 30, -30, -90, -150, 150]
        labels = VGroup(*[callig(t, size=36, color=INK2).move_to(
            [0, 0.5, 0] + 3.05 * np.array([np.cos(a * DEGREES) * 1.45, np.sin(a * DEGREES) * 0.98, 0]))
            for t, a in zip(six, ang)])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.25), run_time=2.4)
        ring.clear_updaters()
        kan = callig("看箭头", size=72).move_to([0, 0.55, 0])
        bye = body("谢谢观看　·　进阶篇见", size=32, color=INK2).move_to([0, -2.0, 0])
        s = seal(0.75).move_to([2.25, -1.1, 0])
        cred = body("参考：Bartosz Milewski《程序员的范畴论》《函数式编程之道》", size=20, color=INK3).move_to([0, -2.6, 0])
        with self.beat(1, tail=1.6):
            self.play(FadeOut(labels), FadeIn(kan, scale=0.92), run_time=1.2)
            self.at(1, 0.55)
            self.play(FadeIn(s, scale=1.6), run_time=0.5)
            self.play(FadeIn(bye), FadeIn(cred), run_time=0.8)
        self.end_scene(rt=1.4)
