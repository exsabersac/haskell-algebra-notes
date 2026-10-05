# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from content import SCENES

META = {s["id"]: s for s in SCENES}


def meta_cls(sid):
    m = META[sid]
    return dict(SID=sid, QUOTE=m["quote"], TITLE=m["title"], CHAPTER=m["chapter"])


def ref_note(s, size=20):
    return body(s, size=size, color=INK3)


# =====================================================================================
class S0Title(TaoScene):
    SID = "S0Title"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value()).move_to([0, 0.55, 0]))
        title = callig("道可道", size=118).move_to([0, 0.62, 0])
        sub = body("范畴论 · Haskell · 《道德经》", size=32, color=INK2).move_to([0, -2.15, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.6, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        ring.clear_updaters()
        left = VGroup(ring, title)
        chapters = [
            ("一", "道可道", "对象与箭头"),
            ("二", "有无相生", "始对象与终对象"),
            ("三", "道生一", "初始代数与不动点"),
            ("四", "反者道之动", "代数与余代数"),
            ("五", "知其雄，守其雌", "伴随：State 与 Store"),
            ("六", "无为而无不为", "米田引理"),
        ]
        rows = VGroup()
        for n, q, t in chapters:
            r = VGroup(callig(n, size=40), callig(q, size=40), body(t, size=28, color=INK2))
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].next_to(r[1], RIGHT, buff=0.4).align_to(r[1], DOWN).shift(UP * 0.04)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.55, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.78).move_to([-4.0, 0.55, 0]), FadeOut(sub), run_time=1.2)
            for i, r in enumerate(rows):
                self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.6)
                self.at(1, 0.12 + 0.13 * (i + 1))
        refs = VGroup(
            body("参考：Bartosz Milewski", size=24, color=INK3),
            serif("Category Theory for Programmers  ·  The Dao of Functional Programming", size=28, color=INK2),
        ).arrange(DOWN, buff=0.12).move_to([0, -2.35, 0])
        s = seal(0.8).next_to(left, DOWN, buff=0.15).shift(RIGHT * 1.3)
        with self.beat(2):
            self.play(FadeIn(refs, shift=UP * 0.1), run_time=1.0)
            self.at(2, 0.55)
            self.play(FadeIn(s, scale=1.6), run_time=0.5)
        self.end_scene()


# =====================================================================================
def radiating(center, r_in=2.2, r_out=2.4, n_in=4, n_out=4, seed=1):
    """Arrows into and out of a blob (Mobject) — the 'speakable' part."""
    c = center.get_center()
    ins, outs = VGroup(), VGroup()
    for i in range(n_in):
        ang = PI * (0.62 + 0.76 * i / max(1, n_in - 1))
        p = c + r_in * np.array([np.cos(ang), np.sin(ang), 0])
        ins.add(arrow(p, c + 0.95 * np.array([np.cos(ang), np.sin(ang), 0]), buff=0))
    for i in range(n_out):
        ang = PI * (-0.38 + 0.76 * i / max(1, n_out - 1))
        q = c + r_out * np.array([np.cos(ang), np.sin(ang), 0])
        outs.add(arrow(c + 0.95 * np.array([np.cos(ang), np.sin(ang), 0]), q, buff=0))
    return ins, outs


class S1Dao(TaoScene):
    locals().update(meta_cls("S1Dao"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        thesis = VGroup(body("论点", size=26, color=INK3),
                        body("对象不可言说；只有箭头可以言说。", size=40)).arrange(RIGHT, buff=0.35)
        thesis.move_to([-0.4, 2.55, 0])
        with self.beat(1):
            self.play(FadeIn(thesis, shift=DOWN * 0.1), run_time=1.0)
        q1 = serif("“The type that can be described is not the eternal type.”", size=40, color=INK)
        q2 = body("能被描述的类型，不是恒常的类型。", size=34, color=INK2)
        q3 = body("—— Bartosz Milewski，《函数式编程之道》第 1 章", size=24, color=INK3)
        quote = VGroup(q1, q2, q3).arrange(DOWN, buff=0.32).move_to([-0.3, 0.3, 0])
        q3.align_to(q1, RIGHT)
        with self.beat(2):
            self.play(FadeIn(q1, shift=UP * 0.1), run_time=1.2)
            self.play(FadeIn(q2), FadeIn(q3), run_time=1.0)
            self.at(2, 0.7)
            self.play(Indicate(q2, color=INK, scale_factor=1.04), run_time=1.0)
        blob = ink_blob(0.62, seed=11).move_to([-0.4, 0.15, 0])
        notes = VGroup(body("没有部分", size=30, color=INK2), body("没有元素", size=30, color=INK2)).arrange(DOWN, buff=0.25)
        notes.next_to(blob, RIGHT, buff=2.6)
        with self.beat(3):
            self.play(FadeOut(quote), FadeOut(thesis), run_time=0.6)
            self.play(FadeIn(blob, scale=0.6), run_time=1.6)
            self.at(3, 0.35)
            self.play(FadeIn(notes[0]), run_time=0.6)
            self.at(3, 0.75)
            self.play(FadeIn(notes[1]), run_time=0.6)
        ins, outs = radiating(blob, r_in=2.05, r_out=2.05)
        xs = VGroup(*[mixed(t, size=26, color=INK2) for t in ["x", "x'", "x''", "x'''"]])
        for t, a in zip(xs, ins):
            t.next_to(a.get_start(), normalize(a.get_start() - blob.get_center()), buff=0.08)
        ys = VGroup(*[mixed(t, size=26, color=INK2) for t in ["y", "y'", "y''", "y'''"]])
        for t, a in zip(ys, outs):
            t.next_to(a.get_end(), normalize(a.get_end() - blob.get_center()), buff=0.08)
        comp = arrow(ins[1].get_start(), outs[1].get_end(), dashed=True, color=INK2)
        comp = ArcBetweenPoints(ins[0].get_start() + DOWN * 0.1, outs[3].get_end() + UP * 0.1, angle=-PI * 0.6,
                                color=INK2, stroke_width=2.5)
        comp = DashedVMobject(comp, num_dashes=40)
        comp_l = mixed("g ∘ f", size=26, color=INK2).next_to(comp, UP, buff=0.08)
        cap = body("对象的结构，由箭头探测出来", size=28, color=INK2).move_to([-0.4, -2.55, 0])
        with self.beat(4):
            self.play(FadeOut(notes), run_time=0.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.25), FadeIn(xs), run_time=1.8)
            self.at(4, 0.22)
            self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.25), FadeIn(ys), run_time=1.8)
            self.at(4, 0.42)
            self.play(Create(comp), FadeIn(comp_l), run_time=1.6)
            self.at(4, 0.7)
            self.play(FadeIn(cap), run_time=0.8)
        diagram = VGroup(blob, ins, outs, xs, ys, comp, comp_l)
        code = make_code("s1", size=23, line_h=0.44).place(-6.2, 1.85)
        with self.beat(5):
            self.play(FadeOut(diagram), FadeOut(cap), run_time=0.8)
            self.play(code.write(), run_time=2.0)
            self.play(code.focus(0, 1), run_time=0.6)
            self.at(5, 0.5)
            self.play(code.focus(3, 4), run_time=0.6)
            self.at(5, 0.72)
            self.play(code.focus(6, 7), run_time=0.6)
        motto = callig("可道者箭头也　不可道者对象也", size=44, color=INK).move_to([-0.3, 2.55, 0])
        with self.beat(6):
            self.play(FadeIn(motto, shift=DOWN * 0.1), run_time=1.0)
            self.at(6, 0.45)
            self.play(code.focus(9, 10), run_time=0.7)
        a = ink_blob(0.42, seed=5).move_to([-2.4, 0.4, 0])
        b = ink_blob(0.42, seed=9).move_to([1.6, 0.4, 0])
        iso = mixed("≅ ?", size=60).move_to([-0.4, 0.4, 0])
        la = mixed("a", size=30, color=INK2).next_to(a, DOWN, buff=0.45)
        lb = mixed("b", size=30, color=INK2).next_to(b, DOWN, buff=0.45)
        later = body("待第六段 · 米田引理来赎回", size=30, color=INK2).move_to([-0.4, -1.75, 0])
        with self.beat(7):
            self.play(FadeOut(code), FadeOut(code.hl) if code.hl else Wait(0.01), FadeOut(motto), run_time=0.8)
            self.play(FadeIn(a, scale=0.7), FadeIn(b, scale=0.7), FadeIn(la), FadeIn(lb), run_time=1.0)
            self.play(Write(iso), run_time=0.8)
            self.at(7, 0.62)
            self.play(FadeIn(later, shift=UP * 0.1), run_time=0.8)
        self.end_scene()


# =====================================================================================
class S2YouWu(TaoScene):
    locals().update(meta_cls("S2YouWu"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        mirror = DashedLine([-0.35, 2.75, 0], [-0.35, -2.2, 0], color=INK3, stroke_width=2, dash_length=0.1)
        void = mixed("Void", size=34).move_to([-5.4, 0.7, 0])
        unit = mixed("()", size=36).move_to([4.6, 0.7, 0])
        cap_l = VGroup(callig("无", size=54), body("始对象", size=26, color=INK2)).arrange(RIGHT, buff=0.2).move_to([-5.2, 2.55, 0])
        cap_r = VGroup(callig("有", size=54), body("终对象", size=26, color=INK2)).arrange(RIGHT, buff=0.2).move_to([4.5, 2.55, 0])
        yy = body("阴 与 阳 —— DaoFP 第 1 章", size=22, color=INK3).move_to([-0.35, 3.05, 0])
        with self.beat(1):
            self.play(FadeIn(void), FadeIn(cap_l), run_time=0.8)
            self.play(FadeIn(unit), FadeIn(cap_r), run_time=0.8)
            self.play(Create(mirror), FadeIn(yy), run_time=1.0)
        tl = [mixed(t, size=30) for t in ["A", "B", "C"]]
        for t, y in zip(tl, [2.0, 0.7, -0.6]):
            t.move_to([-2.0, y, 0])
        tl = VGroup(*tl)
        al = VGroup(*[arrow(void, t) for t in tl])
        lab_l = mixed("absurd", size=24, color=INK2).move_to([-3.55, 1.72, 0]).rotate(0.42)
        code_wu = make_code("s2wu", size=24).place(-6.1, -1.55)
        with self.beat(2):
            self.play(FadeIn(tl), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(a) for a in al], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(lab_l), run_time=0.5)
            self.at(2, 0.4)
            self.play(code_wu.write(), run_time=1.0)
        sl = [mixed(t, size=30) for t in ["A", "B", "C"]]
        for t, y in zip(sl, [2.0, 0.7, -0.6]):
            t.move_to([1.3, y, 0])
        sl = VGroup(*sl)
        ar = VGroup(*[arrow(t, unit) for t in sl])
        lab_r = mixed("const ()", size=24, color=INK2).move_to([2.85, 1.72, 0]).rotate(-0.42)
        code_you = make_code("s2you", size=24).place(1.0, -1.55)
        with self.beat(3):
            self.play(FadeIn(sl), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(lab_r), code_you.write(), run_time=1.0)
        # mirror: copy the left diagram, flip across the mirror line, reverse arrows → right diagram
        ghost = VGroup(void.copy(), tl.copy(), al.copy())
        ghost.set_color(INK2)
        mx = mirror.get_x()
        target_void = unit.copy()
        flipped_arrows = VGroup(*[arrow(t, unit, color=INK2) for t in sl])
        op_txt = VGroup(mixed("C 里的始对象", size=28), mixed("=", size=28),
                        mixed("Cᵒᵖ 里的终对象", size=28)).arrange(RIGHT, buff=0.25).move_to([-0.35, -2.55, 0])
        with self.beat(4):
            self.play(FadeOut(code_wu), FadeOut(code_you), run_time=0.5)
            self.add(ghost)
            self.play(ghost.animate.flip(UP, about_point=[mx, 0, 0]), run_time=1.6)
            self.play(Transform(ghost[2], flipped_arrows), Transform(ghost[0], target_void.set_color(INK2)),
                      run_time=1.4)
            self.play(FadeOut(ghost), run_time=0.6)
            self.play(FadeIn(op_txt), run_time=0.8)
            self.at(4, 0.78)
            self.play(Transform(op_txt, body("无，是倒过来看的有。", size=32).move_to(op_txt)), run_time=0.8)
        diag = VGroup(mirror, void, unit, cap_l, cap_r, yy, tl, al, lab_l, sl, ar, lab_r, op_txt)
        cb = make_code("s2b", size=24).place(-6.3, 2.2)
        with self.beat(5):
            self.play(FadeOut(diag), run_time=0.7)
            self.play(cb.write(), run_time=1.6)
            self.play(cb.focus(0, 2), run_time=0.6)
            self.at(5, 0.45)
            self.play(cb.focus(4, 6), run_time=0.6)
        cc = make_code("s2c", size=24).place(0.1, 2.2)
        ell = Ellipse(width=1.3, height=1.15, color=INK2, stroke_width=2).move_to([4.3, -1.45, 0])
        pts = VGroup(*[Dot(radius=0.06, color=INK) for _ in range(3)]).arrange(DOWN, buff=0.2).move_to(ell)
        unit_n = mixed("()", size=30).move_to([1.6, -1.45, 0])
        a_n = mixed("a", size=28, color=INK2).next_to(ell, RIGHT, buff=0.15)
        pt = VGroup(unit_n, ell, a_n)
        pa = VGroup(*[arrow(unit_n.get_right() + RIGHT * 0.12, p.get_center() + LEFT * 0.1, buff=0, sw=2.4, tip=0.13) for p in pts])
        with self.beat(6):
            self.play(cb.unfocus(), run_time=0.4)
            self.play(cc.write(), run_time=1.2)
            self.play(cc.focus(0, 2), run_time=0.6)
            self.play(FadeIn(pt), FadeIn(pts), LaggedStart(*[GrowArrow(a) for a in pa], lag_ratio=0.3), run_time=1.4)
            self.at(6, 0.7)
            self.play(Indicate(cb.lines[1], color=INK, scale_factor=1.03), run_time=0.8)
        with self.beat(7):
            self.play(cc.focus(4, 5), FadeOut(VGroup(pt, pts, pa)), run_time=0.7)
        icon_a = VGroup(mixed("a", size=40), mixed("b", size=40)).arrange(RIGHT, buff=2.2).move_to([-0.4, 0.4, 0])
        ia = arrow(icon_a[0], icon_a[1], sw=4)
        ib = arrow(icon_a[1], icon_a[0], sw=4)
        nxt = VGroup(callig("反者道之动", size=56), body("→ 第四段", size=28, color=INK2)).arrange(RIGHT, buff=0.4).move_to([-0.4, -1.4, 0])
        with self.beat(8):
            self.play(FadeOut(cb), FadeOut(cc), run_time=0.7)
            self.play(FadeIn(icon_a), GrowArrow(ia), run_time=0.8)
            self.play(Transform(ia, ib), run_time=1.0)
            self.at(8, 0.55)
            self.play(FadeIn(nxt, shift=UP * 0.1), run_time=1.0)
        self.end_scene()


# =====================================================================================
class S3Fix(TaoScene):
    locals().update(meta_cls("S3Fix"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        tq = serif("“The Tao gives birth to One. One gives birth to Two …”", size=36, color=INK)
        tr = body("—— DaoFP 第 7 章《递归》以此句开篇", size=24, color=INK3)
        top = VGroup(tq, tr).arrange(DOWN, buff=0.2).move_to([-0.35, 2.3, 0])
        thm = body("其实，它是一个定理。", size=36).move_to([-0.35, 0.6, 0])
        with self.beat(1):
            self.play(FadeIn(top, shift=DOWN * 0.1), run_time=1.0)
            self.at(1, 0.6)
            self.play(FadeIn(thm), run_time=0.8)
        fm = VGroup(mixed("f = Maybe", size=34), mixed("Maybe a = Nothing | Just a", size=28, color=INK2),
                    body("生成的一步：旧的东西 ↦ 新的东西", size=28, color=INK2)).arrange(DOWN, buff=0.22)
        fm.move_to([-0.35, 0.4, 0])
        with self.beat(2):
            self.play(FadeOut(thm), top.animate.scale(0.8).move_to([-0.35, 2.85, 0]), run_time=0.7)
            self.play(FadeIn(fm[2]), run_time=0.8)
            self.at(2, 0.72)
            self.play(FadeIn(fm[0]), FadeIn(fm[1]), run_time=0.8)
        # the initial chain 0 → f0 → f²0 → f³0 → … → Nat
        xs = [-6.05, -3.55, -0.95, 1.65, 3.45, 5.2]
        names = ["Void", "f Void", "f² Void", "f³ Void", "⋯", "Nat"]
        nodes = VGroup(*[mixed(n, size=26) for n in names])
        for nd, x in zip(nodes, xs):
            nd.move_to([x, 1.15, 0])
        arrs = VGroup(*[arrow(nodes[i], nodes[i + 1], buff=0.15) for i in range(5)])
        alabs = VGroup(*[mixed(t, size=20, color=INK2).next_to(arrs[i], UP, buff=0.06)
                         for i, t in enumerate(["!", "f !", "f² !", "", ""])])
        counts = VGroup(dots(0), dots(1), dots(2), dots(3), mixed("", size=10), VGroup(*[Dot(radius=0.04, color=INK) for _ in range(12)]))
        counts[5].arrange_in_grid(rows=3, buff=0.09)
        for c, x in zip(counts, xs):
            c.move_to([x, 0.3, 0])
        nums = VGroup(*[callig(t, size=50) for t in ["无", "一", "二", "三", "", "万物"]])
        for n, x in zip(nums, xs):
            n.move_to([x, -0.65, 0])
        with self.beat(3):
            self.play(FadeOut(fm), run_time=0.6)
            self.play(FadeIn(nodes[0]), FadeIn(counts[0]), FadeIn(nums[0]), run_time=0.8)
            for i, fr in zip([1, 2, 3], [0.22, 0.6, 0.82]):
                self.at(3, fr)
                self.play(GrowArrow(arrs[i - 1]), FadeIn(alabs[i - 1]), FadeIn(nodes[i]), FadeIn(counts[i]),
                          FadeIn(nums[i]), run_time=0.9)
        cocone = SurroundingRectangle(VGroup(nodes[5], counts[5], nums[5]), buff=0.18, color=INK3, stroke_width=1.6, corner_radius=0.12)
        cocone = DashedVMobject(cocone, num_dashes=40)
        colim = body("余极限 = 初始代数（Adámek 定理）", size=28, color=INK2).move_to([-0.35, -2.05, 0])
        ch40 = callig("天下万物生于有　有生于无", size=40, color=INK).move_to([-0.35, -2.05, 0])
        with self.beat(4):
            self.play(GrowArrow(arrs[3]), FadeIn(nodes[4]), run_time=0.7)
            self.play(GrowArrow(arrs[4]), FadeIn(nodes[5]), FadeIn(counts[5]), FadeIn(nums[5]), run_time=0.9)
            self.at(4, 0.18)
            self.play(Create(cocone), run_time=1.6)
            self.play(FadeIn(colim), run_time=0.8)
            self.at(4, 0.82)
            self.play(FadeOut(colim), FadeIn(ch40), run_time=0.9)
        chain = VGroup(nodes, arrs, alabs, counts, nums, cocone, ch40, top)
        code = make_code("s3a", size=24, line_h=0.42).place(-6.3, 0.0)
        with self.beat(5):
            self.play(FadeOut(chain), run_time=0.7)
            self.play(code.write(), run_time=1.6)
            self.play(code.focus(0), run_time=0.6)
        # Lambek diagram: f (Fix f) ⇄ Fix f
        lf = mixed("f (Fix f)", size=32).move_to([-5.0, 1.9, 0])
        lx = mixed("Fix f", size=32).move_to([-1.4, 1.9, 0])
        top_a = arrow(lf.get_right() + UP * 0.12 + RIGHT * 0.15, lx.get_left() + UP * 0.12 + LEFT * 0.15, buff=0)
        bot_a = arrow(lx.get_left() + DOWN * 0.12 + LEFT * 0.15, lf.get_right() + DOWN * 0.12 + RIGHT * 0.15, buff=0)
        top_l = mixed("Fix", size=24, color=INK2).next_to(top_a, UP, buff=0.1)
        bot_l = mixed("unFix", size=24, color=INK2).next_to(bot_a, DOWN, buff=0.1)
        lam = VGroup(lf, lx, top_a, bot_a, top_l, bot_l)
        lam_t = body("兰贝克引理", size=26, color=INK3).next_to(lam, UP, buff=0.25)
        with self.beat(6):
            self.play(FadeIn(lam_t), FadeIn(lf), FadeIn(lx), run_time=0.7)
            self.play(GrowArrow(top_a), FadeIn(top_l), run_time=0.8)
            self.play(GrowArrow(bot_a), FadeIn(bot_l), run_time=0.8)
            self.play(code.focus(1), run_time=0.5)
        pf = VGroup(mixed("f (Fix f) 也是代数（fmap Fix）", size=22, color=INK2),
                    mixed("初始性 ⇒ 回程箭头；唯一性 ⇒ 复合 = id", size=22, color=INK2)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        pf.next_to(lam, RIGHT, buff=0.55).shift(DOWN * 0.05)
        with self.beat(7):
            self.play(FadeIn(pf[0]), run_time=0.8)
            self.at(7, 0.45)
            self.play(FadeIn(pf[1]), run_time=0.8)
            self.play(Indicate(top_a, color=INK, scale_factor=1.0), Indicate(bot_a, color=INK, scale_factor=1.0), run_time=1.0)
        zr = VGroup(callig("道法自然", size=58), body("自然 = 自己如此", size=26, color=INK2)).arrange(DOWN, buff=0.2)
        zr.move_to([2.6, 1.8, 0])
        with self.beat(8):
            self.play(FadeOut(pf), run_time=0.5)
            self.play(FadeIn(zr[0], scale=1.05), run_time=1.2)
            self.play(FadeIn(zr[1]), run_time=0.7)
        # cata square (DaoFP ch.11 layout)
        TL, TR, BL, BR = [-4.4, 2.55, 0], [0.6, 2.55, 0], [-4.4, 0.8, 0], [0.6, 0.8, 0]
        n_tl, n_tr = mixed("f (Fix f)", size=28).move_to(TL), mixed("f a", size=28).move_to(TR)
        n_bl, n_br = mixed("Fix f", size=28).move_to(BL), mixed("a", size=28).move_to(BR)
        a_top = arrow(n_tl, n_tr)
        a_left = arrow(n_bl, n_tl)
        a_right = arrow(n_tr, n_br)
        a_bot = arrow(n_bl, n_br, dashed=True)
        l_top = mixed("fmap (cata alg)", size=22, color=INK2).next_to(a_top, UP, buff=0.08)
        l_left = mixed("unFix", size=22, color=INK2).next_to(a_left, LEFT, buff=0.1)
        l_right = mixed("alg", size=22, color=INK2).next_to(a_right, RIGHT, buff=0.1)
        l_bot = mixed("cata alg  ∃!", size=22, color=INK2).next_to(a_bot, DOWN, buff=0.08)
        sq = VGroup(n_tl, n_tr, n_bl, n_br, a_top, a_left, a_right, a_bot, l_top, l_left, l_right, l_bot)
        with self.beat(9):
            self.play(FadeOut(lam), FadeOut(lam_t), FadeOut(zr), run_time=0.6)
            self.play(FadeIn(VGroup(n_tl, n_tr, n_bl, n_br)), run_time=0.6)
            self.play(GrowArrow(a_left), FadeIn(l_left), run_time=0.6)
            self.play(GrowArrow(a_top), FadeIn(l_top), run_time=0.6)
            self.play(GrowArrow(a_right), FadeIn(l_right), run_time=0.6)
            self.at(9, 0.65)
            self.play(Create(a_bot), FadeIn(l_bot), run_time=1.0)
            self.play(code.focus(3, 6), run_time=0.6)
        gh = VGroup(callig("复归其根", size=54), body("唯一的归途", size=26, color=INK2)).arrange(DOWN, buff=0.2).move_to([3.6, 1.7, 0])
        path = VMobject().set_points_as_corners([n_bl.get_top() + UP * 0.2, n_tl.get_bottom() + DOWN * 0.2,
                                                 n_tl.get_right() + RIGHT * 0.15, n_tr.get_left() + LEFT * 0.15,
                                                 n_tr.get_bottom() + DOWN * 0.2, n_br.get_top() + UP * 0.2])
        bead = Dot(radius=0.08, color=INK)
        with self.beat(10):
            self.play(FadeIn(gh[0], scale=1.05), run_time=1.0)
            self.play(code.focus(5, 6), FadeIn(gh[1]), run_time=0.6)
            self.at(10, 0.45)
            self.play(MoveAlongPath(bead, path), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeOut(bead), run_time=0.4)
        cb = make_code("s3b", size=21, line_h=0.43).place(-6.4, 2.6)
        cc = make_code("s3c", size=21, line_h=0.43).place(0.35, 2.6)
        with self.beat(11):
            self.play(FadeOut(sq), FadeOut(gh), FadeOut(code), run_time=0.6)
            self.play(cb.write(), run_time=1.2)
            self.play(cb.focus(0), run_time=0.5)
            self.at(11, 0.3)
            self.play(cc.write(), run_time=1.2)
            self.play(cc.focus(1, 4), run_time=0.5)
            self.at(11, 0.62)
            self.play(cb.focus(9, 11), cc.unfocus(), run_time=0.6)
        self.end_scene()


# =====================================================================================
def square(TL, TR, BL, BR, names, arrows_spec, labels, size=26, lsize=21):
    """arrows_spec: list of (from_idx, to_idx, dashed); nodes 0..3 = TL TR BL BR."""
    ns = VGroup(*[mixed(n, size=size).move_to(p) for n, p in zip(names, [TL, TR, BL, BR])])
    ars, lbs = VGroup(), VGroup()
    for (i, j, dsh), (txt, side) in zip(arrows_spec, labels):
        a = arrow(ns[i], ns[j], dashed=dsh)
        ars.add(a)
        lbs.add(mixed(txt, size=lsize, color=INK2).next_to(a, side, buff=0.08))
    return ns, ars, lbs


class S4Hylo(TaoScene):
    locals().update(meta_cls("S4Hylo"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        L = (-5.7, -1.9)
        R = (1.3, 5.1)
        cata_n, cata_a, cata_l = square([L[0], 2.45, 0], [L[1], 2.45, 0], [L[0], 0.75, 0], [L[1], 0.75, 0],
                                        ["f (Fix f)", "f a", "Fix f", "a"],
                                        [(0, 1, False), (2, 0, False), (1, 3, False), (2, 3, True)],
                                        [("fmap (cata alg)", UP), ("unFix", LEFT), ("alg", RIGHT), ("cata alg", DOWN)])
        cata_t = body("代数 · 折叠", size=24, color=INK3).move_to([(L[0] + L[1]) / 2, -0.05, 0])
        with self.beat(1):
            self.play(FadeIn(cata_n), FadeIn(cata_a), FadeIn(cata_l), FadeIn(cata_t), run_time=1.2)
        alg = VGroup(mixed("Algebra f a   = f a -> a", size=28), body("收拢一层结构", size=24, color=INK2))
        coa = VGroup(mixed("Coalgebra f a = a -> f a", size=28), body("从种子长出一层结构", size=24, color=INK2))
        for g in (alg, coa):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rv = VGroup(alg, coa).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.0, 1.55, 0])
        chop = body("cata 砍树，ana 种树 —— DaoFP 第 12 章", size=24, color=INK3).move_to([-0.35, -0.7, 0])
        with self.beat(2):
            self.play(FadeIn(alg), run_time=0.8)
            self.at(2, 0.3)
            self.play(FadeIn(coa), run_time=0.8)
            self.at(2, 0.66)
            self.play(FadeIn(chop), run_time=0.8)
        ana_n, ana_a, ana_l = square([R[0], 2.45, 0], [R[1], 2.45, 0], [R[0], 0.75, 0], [R[1], 0.75, 0],
                                     ["f (Fix f)", "f a", "Fix f", "a"],
                                     [(1, 0, False), (0, 2, False), (3, 1, False), (3, 2, True)],
                                     [("fmap (ana coa)", UP), ("Fix", LEFT), ("coa", RIGHT), ("ana coa", DOWN)])
        ana_t = body("余代数 · 展开", size=24, color=INK3).move_to([(R[0] + R[1]) / 2, -0.05, 0])
        with self.beat(3):
            self.play(FadeOut(rv), FadeOut(chop), run_time=0.6)
            ghost = VGroup(cata_n.copy(), cata_a.copy()).set_color(INK2)
            self.add(ghost)
            self.play(ghost.animate.shift(RIGHT * (R[0] - L[0])), run_time=1.2)
            self.play(*[Transform(g, t) for g, t in zip(ghost[1], ana_a)], run_time=1.4)
            self.play(FadeOut(ghost), FadeIn(ana_n), FadeIn(ana_a), FadeIn(ana_l), FadeIn(ana_t), run_time=0.8)
        code = make_code("s4a", size=25, line_h=0.45).place(-6.0, -0.65)
        with self.beat(4):
            self.play(*[Indicate(a, color=INK, scale_factor=1.0) for a in list(cata_a) + list(ana_a)], run_time=1.2)
            self.at(4, 0.42)
            self.play(FadeOut(cata_t), FadeOut(ana_t), run_time=0.4)
            self.play(code.write(), run_time=1.2)
            self.play(code.focus(2), run_time=0.5)
            self.at(4, 0.72)
            self.play(code.focus(3, 4), run_time=0.6)
        top = VGroup(cata_n, cata_a, cata_l, cata_t, ana_n, ana_a, ana_l, ana_t, code)
        c1 = VGroup(*[mixed(t, size=28) for t in ["0", "F 0", "F² 0", "⋯", "μF"]]).arrange(RIGHT, buff=1.0)
        c2 = VGroup(*[mixed(t, size=28) for t in ["1", "F 1", "F² 1", "⋯", "νF"]]).arrange(RIGHT, buff=1.0)
        c1.move_to([-1.3, 1.9, 0]); c2.move_to([-1.3, 0.1, 0])
        c2.align_to(c1, LEFT)
        a1 = VGroup(*[arrow(c1[i], c1[i + 1], buff=0.12) for i in range(4)])
        a2 = VGroup(*[arrow(c2[i + 1], c2[i], buff=0.12) for i in range(4)])
        t1 = body("从始对象（无）生长", size=24, color=INK2).next_to(c1, RIGHT, buff=0.5)
        t2 = body("从终对象（有）逼近", size=24, color=INK2).next_to(c2, RIGHT, buff=0.5)
        yw = callig("有无相生", size=50).move_to([-0.35, -1.4, 0])
        with self.beat(5):
            self.play(FadeOut(top), run_time=0.7)
            self.play(FadeIn(c1), LaggedStart(*[GrowArrow(a) for a in a1], lag_ratio=0.2), run_time=1.4)
            self.play(FadeIn(t1), run_time=0.5)
            self.at(5, 0.42)
            self.play(FadeIn(c2), LaggedStart(*[GrowArrow(a) for a in a2], lag_ratio=0.2), run_time=1.4)
            self.play(FadeIn(t2), run_time=0.5)
            self.at(5, 0.75)
            self.play(FadeIn(yw, scale=1.05), run_time=1.0)
        st = VGroup(mixed("Set：  μF ⊊ νF", size=28),
                    mixed("Haskell（惰性）：一个 Fix f 兼任二者", size=28),
                    mixed("nats = ana (\\n -> StreamF n (n + 1)) 0", size=24, color=INK2)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        st.move_to([-0.6, -1.25, 0])
        with self.beat(6):
            self.play(FadeOut(yw), run_time=0.4)
            self.play(FadeIn(st[0]), run_time=0.7)
            self.at(6, 0.3)
            self.play(FadeIn(st[1]), run_time=0.7)
            self.at(6, 0.62)
            self.play(FadeIn(st[2]), run_time=0.7)
        ha = mixed("a", size=32).move_to([-4.6, 2.35, 0])
        hf = mixed("Fix f", size=32).move_to([-0.8, 2.35, 0])
        hb = mixed("b", size=32).move_to([3.0, 2.35, 0])
        h1 = arrow(ha, hf); h2 = arrow(hf, hb)
        l1 = mixed("ana coa", size=22, color=INK2).next_to(h1, UP, buff=0.08)
        l2 = mixed("cata alg", size=22, color=INK2).next_to(h2, UP, buff=0.08)
        s1 = callig("先生", size=36).next_to(h1, DOWN, buff=0.15)
        s2 = callig("后归", size=36).next_to(h2, DOWN, buff=0.15)
        hd = ArcBetweenPoints(ha.get_bottom() + DOWN * 0.12, hb.get_bottom() + DOWN * 0.12, angle=PI * 0.28,
                              color=INK, stroke_width=3)
        hd = DashedVMobject(hd, num_dashes=46)
        hl = mixed("hylo alg coa", size=22, color=INK2).next_to(hd, DOWN, buff=0.06)
        hylo = VGroup(ha, hf, hb, h1, h2, l1, l2, s1, s2, hd, hl)
        with self.beat(7):
            self.play(FadeOut(VGroup(c1, c2, a1, a2, t1, t2, st)), run_time=0.7)
            self.play(FadeIn(ha), GrowArrow(h1), FadeIn(l1), FadeIn(hf), run_time=1.0)
            self.play(FadeIn(s1), run_time=0.5)
            self.at(7, 0.35)
            self.play(GrowArrow(h2), FadeIn(l2), FadeIn(hb), FadeIn(s2), run_time=1.0)
            self.at(7, 0.62)
            self.play(Create(hd), FadeIn(hl), run_time=1.2)
        code = make_code("s4b", size=23, line_h=0.44).place(-6.0, 1.55)
        with self.beat(8):
            self.play(hylo.animate.scale(0.62).move_to([3.3, 2.5, 0]), run_time=0.8)
            self.play(code.write(), run_time=1.4)
            self.play(code.focus(3, 9), run_time=0.6)
        bu = VGroup(callig("生而不有", size=56), body("中间结构从未完整存在", size=24, color=INK2)).arrange(DOWN, buff=0.2)
        bu.move_to([3.5, -0.9, 0])
        with self.beat(9):
            self.play(code.focus(0, 1), run_time=0.6)
            self.at(9, 0.3)
            self.play(hf.animate.set_opacity(0.18), h1.animate.set_opacity(0.3), h2.animate.set_opacity(0.3), run_time=1.6)
            self.at(9, 0.62)
            self.play(FadeIn(bu, scale=1.05), run_time=1.0)
        warn = VGroup(body("代价：展开不终止，hylo 便不终止", size=28, color=INK2),
                      body("（DaoFP 第 12 章 · impedance mismatch）", size=22, color=INK3)).arrange(DOWN, buff=0.12)
        warn.move_to([-0.35, 1.1, 0])
        th = VGroup(body("定理", size=40), mixed("⟷", size=44), body("对偶定理", size=40)).arrange(RIGHT, buff=0.4).move_to([-0.35, -0.9, 0])
        with self.beat(10):
            self.play(FadeOut(hylo), FadeOut(code), FadeOut(bu), run_time=0.7)
            self.play(FadeIn(warn), run_time=0.8)
            self.at(10, 0.45)
            self.play(FadeIn(th[0]), run_time=0.5)
            self.play(GrowFromCenter(th[1]), FadeIn(th[2]), run_time=0.8)
        self.end_scene()


# =====================================================================================
class S5Adjunction(TaoScene):
    locals().update(meta_cls("S5Adjunction"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        cC = Ellipse(width=2.1, height=2.4, color=INK2, stroke_width=2.5).move_to([-2.3, 1.55, 0])
        cD = Ellipse(width=2.1, height=2.4, color=INK2, stroke_width=2.5).move_to([1.6, 1.55, 0])
        lC = mixed("C", size=32, color=INK2).next_to(cC, LEFT, buff=0.2)
        lD = mixed("D", size=32, color=INK2).next_to(cD, RIGHT, buff=0.2)
        aL = CurvedArrow(cD.get_top() + DOWN * 0.45 + LEFT * 0.3, cC.get_top() + DOWN * 0.45 + RIGHT * 0.3, angle=PI * 0.35,
                         color=INK, stroke_width=3, tip_length=0.17)
        aR = CurvedArrow(cC.get_bottom() + UP * 0.45 + RIGHT * 0.3, cD.get_bottom() + UP * 0.45 + LEFT * 0.3, angle=PI * 0.35,
                         color=INK, stroke_width=3, tip_length=0.17)
        tL = mixed("L", size=30).next_to(aL, UP, buff=0.08)
        tR = mixed("R", size=30).next_to(aR, DOWN, buff=0.08)
        adj = mixed("⊣", size=40).move_to([-0.35, 1.55, 0]).rotate(-PI / 2)
        cats = VGroup(cC, cD, lC, lD, aL, aR, tL, tR, adj)
        hom = mixed("C(L a, b)  ≅  D(a, R b)", size=34).move_to([-0.35, -0.9, 0])
        homt = mixed("L ⊣ R", size=30, color=INK2).next_to(hom, DOWN, buff=0.35)
        with self.beat(1):
            self.play(Create(cC), Create(cD), FadeIn(lC), FadeIn(lD), run_time=1.0)
            self.play(Create(aL), FadeIn(tL), Create(aR), FadeIn(tR), run_time=1.0)
            self.play(FadeIn(adj), run_time=0.5)
            self.at(1, 0.5)
            self.play(FadeIn(hom), FadeIn(homt), run_time=1.0)
        cur = mixed("((a, s) -> b)  ≅  (a -> s -> b)", size=32).move_to([-0.35, -0.55, 0])
        ca = VGroup(mixed("curry  →", size=24, color=INK2), mixed("←  uncurry", size=24, color=INK2)).arrange(RIGHT, buff=1.2).next_to(cur, DOWN, buff=0.3)
        cn = VGroup(mixed("(,) s  ⊣  (->) s", size=30), body("柯里化伴随 —— DaoFP 第 10 章", size=22, color=INK3)).arrange(RIGHT, buff=0.5)
        cn.next_to(ca, DOWN, buff=0.35)
        with self.beat(2):
            self.play(FadeOut(hom), FadeOut(homt), run_time=0.5)
            self.play(Transform(tL, mixed("(,) s", size=26).move_to(tL)), Transform(tR, mixed("(->) s", size=26).move_to(tR)), run_time=0.8)
            self.at(2, 0.4)
            self.play(FadeIn(cur), run_time=0.8)
            self.play(FadeIn(ca), run_time=0.6)
            self.at(2, 0.7)
            self.play(FadeIn(cn), run_time=0.8)
        code = make_code("s5a", size=24, line_h=0.44).place(-6.2, 2.45)
        with self.beat(3):
            self.play(FadeOut(VGroup(cats, cur, ca, cn)), run_time=0.6)
            self.play(code.write(), run_time=1.4)
            self.play(code.focus(7, 8), run_time=0.5)
            self.at(3, 0.5)
            self.play(code.focus(10, 11), run_time=0.5)
        f1 = mixed("R ∘ L :  a ↦ s -> (a, s)", size=28)
        f2 = mixed("L ∘ R :  c ↦ (s -> c, s)", size=28)
        cs = make_code([l for l in load_snip("s5b")[1:] if l.strip()], size=23, line_h=0.44)
        cst = make_code([l for l in load_snip("s5c")[1:] if l.strip()], size=23, line_h=0.44)
        f1.move_to([0, 2.7, 0]).align_to([-6.2, 0, 0], LEFT)
        cs.place(-6.2, 2.1)
        f2.move_to([0, 0.55, 0]).align_to([-6.2, 0, 0], LEFT)
        cst.place(-6.2, -0.05)
        tag1 = body("State 单子", size=28, color=INK2).next_to(f1, RIGHT, buff=0.6)
        tag2 = body("Store 余单子", size=28, color=INK2).next_to(f2, RIGHT, buff=0.6)
        with self.beat(4):
            self.play(FadeOut(code), run_time=0.5)
            self.play(FadeIn(f1), run_time=0.6)
            self.play(cs.write(), FadeIn(tag1), run_time=1.0)
            self.play(cs.focus(0), run_time=0.5)
        with self.beat(5):
            self.play(FadeIn(f2), run_time=0.6)
            self.play(cst.write(), FadeIn(tag2), run_time=1.0)
            self.play(cst.focus(0), run_time=0.5)
            self.at(5, 0.55)
            self.play(cst.focus(1, 2), run_time=0.5)
        with self.beat(6):
            self.play(cs.focus(1, 2), run_time=0.6)
            self.at(6, 0.45)
            self.play(cst.focus(3, 4), run_time=0.6)
        xm = VGroup(callig("雄", size=110), mixed("State", size=34), body("效果 · 主动 · 向外", size=28, color=INK2)).arrange(DOWN, buff=0.25)
        cf = VGroup(callig("雌", size=110), mixed("Store", size=34), body("语境 · 接纳 · 向内", size=28, color=INK2)).arrange(DOWN, buff=0.25)
        xm.move_to([-3.8, 0.5, 0]); cf.move_to([3.0, 0.5, 0])
        sp = np.array([[-0.35 + 0.16 * np.sin(t * 2.4), 2.8 - t, 0] for t in np.linspace(0, 4.6, 60)])
        stream = VMobject(color=INK, stroke_width=4).set_points_smoothly(sp)
        sl = mixed("L ⊣ R", size=28, color=INK2).next_to(stream, RIGHT, buff=0.25).shift(UP * 1.6)
        with self.beat(7):
            self.play(FadeOut(VGroup(f1, f2, cs, cst, tag1, tag2)), run_time=0.6)
            self.play(FadeIn(xm, shift=RIGHT * 0.1), run_time=1.0)
            self.at(7, 0.48)
            self.play(FadeIn(cf, shift=LEFT * 0.1), run_time=1.0)
        xi = callig("为天下溪", size=44).move_to([-0.35, -2.45, 0])
        with self.beat(8):
            self.play(Create(stream), run_time=1.8)
            self.play(FadeIn(sl), FadeIn(xi), run_time=0.8)
        lens = make_code("s5d", size=26).place(-4.6, 1.2)
        ln = body("合法 lens = Store 余单子的余代数 —— DaoFP 第 17 章", size=24, color=INK3).move_to([-0.35, -2.2, 0])
        with self.beat(9):
            self.play(FadeOut(VGroup(xm, cf, stream, sl, xi)), run_time=0.6)
            self.play(lens.write(), run_time=1.0)
            self.play(lens.focus(1), FadeIn(ln), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S6Yoneda(TaoScene):
    locals().update(meta_cls("S6Yoneda"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        lhs = mixed("(forall x. (a -> x) -> f x)", size=40)
        iso = mixed("≅", size=44)
        rhs = mixed("f a", size=40)
        yo = VGroup(lhs, iso, rhs).arrange(RIGHT, buff=0.4).move_to([-0.35, 1.7, 0])
        yt = body("米田引理", size=26, color=INK3).next_to(yo, UP, buff=0.35)
        with self.beat(1):
            self.play(FadeIn(yt), FadeIn(lhs, shift=RIGHT * 0.1), run_time=1.2)
            self.at(1, 0.62)
            self.play(FadeIn(iso), FadeIn(rhs), run_time=0.8)
        # mask the x's
        x_idx = [i for i, ch in enumerate([c for c in "(forallx.(a->x)->fx)"]) if ch == "x"]
        glyphs = lhs  # glyph order = non-space chars of the string
        masks = VGroup(*[SurroundingRectangle(glyphs[i], buff=0.05, stroke_width=0, fill_color=WASH2, fill_opacity=0.9)
                         for i in x_idx])
        ww = VGroup(callig("无为", size=64), body("对 x 一无所知 —— 只能原样使用箭头", size=28, color=INK2)).arrange(RIGHT, buff=0.5)
        ww.move_to([-0.35, -0.2, 0])
        with self.beat(2):
            self.at(2, 0.2)
            self.play(LaggedStart(*[FadeIn(m) for m in masks], lag_ratio=0.25), run_time=1.2)
            self.at(2, 0.75)
            self.play(FadeIn(ww), run_time=0.9)
        # identity loop + propagation
        pa = ink_blob(0.3, seed=21).move_to([-4.6, -1.3, 0])
        loop = Arc(radius=0.36, start_angle=PI * 0.15, angle=PI * 1.55, color=INK, stroke_width=3).move_to(pa.get_center() + UP * 0.62)
        loop.add_tip(tip_length=0.14)
        idl = mixed("id", size=26).next_to(loop, UP, buff=0.05)
        targets = [np.array([x, y, 0]) for x, y in [(-2.0, -0.35), (-1.4, -1.25), (-2.0, -2.25), (0.4, -0.6), (0.8, -1.9), (2.6, -1.2)]]
        tdots = VGroup(*[Dot(t, radius=0.07, color=INK2) for t in targets])
        prop = VGroup(*[arrow(pa, Dot(t), buff=0.12, color=INK2, sw=2.4, tip=0.13) for t in targets[:3]])
        prop2 = VGroup(arrow(targets[0], targets[3], buff=0.12, color=INK2, sw=2.2, tip=0.12),
                       arrow(targets[2], targets[4], buff=0.12, color=INK2, sw=2.2, tip=0.12),
                       arrow(targets[3], targets[5], buff=0.12, color=INK2, sw=2.2, tip=0.12))
        n1 = body("恒等箭头 = 无为（DaoFP 第 2 章）", size=24, color=INK2).move_to([3.4, -0.1, 0])
        n2 = body("自然性把 id 传遍整个范畴（第 9 章）", size=24, color=INK2).move_to([3.4, -2.35, 0])
        with self.beat(3):
            self.play(FadeOut(ww), run_time=0.5)
            self.play(FadeIn(pa), Create(loop), FadeIn(idl), run_time=1.2)
            self.play(FadeIn(n1), run_time=0.6)
            self.at(3, 0.55)
            self.play(LaggedStart(*[GrowArrow(a) for a in prop], lag_ratio=0.3), FadeIn(tdots[:3]), run_time=1.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in prop2], lag_ratio=0.3), FadeIn(tdots[3:]), run_time=1.4)
            self.play(FadeIn(n2), run_time=0.6)
        net = VGroup(pa, loop, idl, tdots, prop, prop2, n1, n2)
        code = make_code("s6a", size=24, line_h=0.45).place(-6.2, 0.6)
        wbw = callig("无不为", size=56).move_to([5.15, 1.1, 0])
        with self.beat(4):
            self.play(FadeOut(net), FadeOut(masks), run_time=0.6)
            self.play(code.write(), run_time=1.2)
            self.play(code.focus(5, 6), run_time=0.5)
            self.at(4, 0.5)
            self.play(code.focus(2, 3), FadeIn(wbw), run_time=0.6)
        fu = VGroup(mixed("fmap h (Yoneda g) = Yoneda (\\k -> g (k . h))", size=24),
                    mixed("fmap h . fmap g   ⇒   一次 fmap (h . g)", size=26, color=INK2)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fu.move_to([-0.6, -0.4, 0])
        with self.beat(5):
            self.play(FadeOut(wbw), FadeOut(code), run_time=0.6)
            self.play(FadeIn(fu[0]), run_time=0.8)
            self.at(5, 0.5)
            self.play(FadeIn(fu[1]), run_time=0.8)
        recall = mixed("第一段：type Speak a = forall x. (a -> x) -> x", size=24, color=INK3).move_to([-0.35, 2.75, 0])
        cb = make_code("s6b", size=25, line_h=0.5).place(-6.2, 1.85)
        cps = body("恒等函子情形 = 续体传递风格（CPS）", size=24, color=INK2).move_to([2.6, -2.45, 0])
        with self.beat(6):
            self.play(FadeOut(fu), FadeOut(yo), FadeOut(yt), run_time=0.6)
            self.play(FadeIn(recall), run_time=0.6)
            self.play(cb.write(), run_time=1.2)
            self.play(cb.focus(0, 4), run_time=0.5)
            self.at(6, 0.7)
            self.play(FadeIn(cps), run_time=0.6)
        # the redemption: the blob of segment 1 comes back
        blob = ink_blob(0.62, seed=11).move_to([-1.6, 0.25, 0])
        ins, outs = radiating(blob, r_in=2.0, r_out=2.0)
        one = outs[1]
        f1 = body("单独一支箭头：说不出", size=26, color=INK2).move_to([3.6, 1.6, 0])
        f2 = body("全部箭头 + 自然性：就是 a", size=26, color=INK).move_to([3.6, -0.5, 0])
        f3 = body("（在同构的意义下）", size=22, color=INK3).next_to(f2, DOWN, buff=0.15)
        aname = mixed("a", size=40, color=WHITE).move_to(blob)
        with self.beat(7):
            self.play(FadeOut(cb), FadeOut(recall), FadeOut(cps), run_time=0.6)
            self.play(FadeIn(blob, scale=0.7), run_time=1.0)
            self.play(GrowArrow(one), FadeIn(f1), run_time=0.9)
            self.at(7, 0.3)
            self.play(LaggedStart(*[GrowArrow(a) for a in list(ins) + [outs[0], outs[2], outs[3]]], lag_ratio=0.15), run_time=2.0)
            self.at(7, 0.55)
            self.play(FadeIn(f2), FadeIn(f3), FadeIn(aname, scale=0.8), run_time=1.0)
        emb = VGroup(mixed("a ≅ b   ⟺   C(a, −) ≅ C(b, −)", size=34),
                     body("米田嵌入：满忠实", size=26, color=INK2)).arrange(DOWN, buff=0.25).move_to([-0.35, -1.95, 0])
        with self.beat(8):
            self.play(VGroup(blob, ins, outs, aname).animate.scale(0.75).shift(UP * 0.45), FadeOut(f1),
                      VGroup(f2, f3).animate.shift(UP * 1.1), run_time=0.8)
            self.play(FadeIn(emb), run_time=0.9)
        ran = make_code(["newtype Ran g h a = Ran (forall b. (a -> g b) -> h b)",
                         "-- Yoneda f ≅ Ran Identity f"], size=25).place(-6.0, 1.7)
        mq = VGroup(serif("“All concepts are Kan extensions.”", size=40, color=INK),
                    body("—— Saunders Mac Lane（DaoFP 第 20 章、CTFP 3.11 均引此句）", size=22, color=INK3)).arrange(DOWN, buff=0.2)
        mq.move_to([-0.35, -0.35, 0])
        ks = body("极限 · 伴随 · 米田", size=30, color=INK2).move_to([-0.35, -1.85, 0])
        with self.beat(9):
            self.play(FadeOut(VGroup(blob, ins, outs, aname, f2, f3, emb)), run_time=0.6)
            self.play(ran.write(), run_time=1.0)
            self.at(9, 0.42)
            self.play(FadeIn(mq), run_time=1.0)
            self.at(9, 0.72)
            self.play(FadeIn(ks), run_time=0.8)
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
        labels = VGroup(*[callig(t, size=36, color=INK2).move_to([0, 0.5, 0] + 3.05 * np.array([np.cos(a * DEGREES) * 1.45, np.sin(a * DEGREES) * 0.98, 0]))
                          for t, a in zip(six, ang)])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.25), run_time=2.4)
        ring.clear_updaters()
        kan = callig("看箭头", size=72).move_to([0, 0.55, 0])
        bye = body("谢谢观看", size=34, color=INK2).move_to([0, -2.0, 0])
        s = seal(0.75).move_to([2.25, -1.1, 0])
        cred = body("参考：Bartosz Milewski《程序员的范畴论》《函数式编程之道》", size=20, color=INK3).move_to([0, -2.6, 0])
        with self.beat(1, tail=1.6):
            self.play(FadeOut(labels), FadeIn(kan, scale=0.92), run_time=1.2)
            self.at(1, 0.55)
            self.play(FadeIn(s, scale=1.6), run_time=0.5)
            self.play(FadeIn(bye), FadeIn(cred), run_time=0.8)
        self.end_scene(rt=1.4)
