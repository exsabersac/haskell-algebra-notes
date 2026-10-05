# -*- coding: utf-8 -*-
"""Manim scenes for 进阶深讲 11 · 知其雄，守其雌 (adjunctions → State monad / Store comonad, lens)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from content import SCENES

META = {s["id"]: s for s in SCENES}


def meta_cls(sid):
    m = META[sid]
    return dict(SID=sid, QUOTE=m["quote"], TITLE=m["title"], CHAPTER=m["chapter"])


def square(tl, tr, bl, br, top, left, right, bottom, center=ORIGIN, w=4.4, h=2.4,
           up_left=False, dash_bottom=True, size=30, lsize=24, bottom_color=SEAL):
    c = np.array(center, dtype=float)
    n_tl = node(tl, size=size).move_to(c + [-w / 2, h / 2, 0])
    n_tr = node(tr, size=size).move_to(c + [w / 2, h / 2, 0])
    n_bl = node(bl, size=size).move_to(c + [-w / 2, -h / 2, 0])
    n_br = node(br, size=size).move_to(c + [w / 2, -h / 2, 0])
    a_top = arrow(n_tl, n_tr)
    a_left = arrow(n_bl, n_tl) if up_left else arrow(n_tl, n_bl)
    a_right = arrow(n_tr, n_br)
    a_bot = arrow(n_bl, n_br, dashed=dash_bottom, color=bottom_color if dash_bottom else INK)
    l_top = label(a_top, top, UP, size=lsize)
    l_left = label(a_left, left, LEFT, size=lsize)
    l_right = label(a_right, right, RIGHT, size=lsize)
    l_bot = label(a_bot, bottom, DOWN, size=lsize, color=bottom_color if dash_bottom else INK2)
    d = dict(tl=n_tl, tr=n_tr, bl=n_bl, br=n_br, top=a_top, left=a_left, right=a_right, bot=a_bot,
             l_top=l_top, l_left=l_left, l_right=l_right, l_bot=l_bot)
    d["nodes"] = VGroup(n_tl, n_tr, n_bl, n_br)
    d["arrows"] = VGroup(a_top, a_left, a_right, a_bot)
    d["labels"] = VGroup(l_top, l_left, l_right, l_bot)
    d["all"] = VGroup(d["nodes"], d["arrows"], d["labels"])
    return d


def draw_square(scene, d, rt=2.4, bottom_last=True):
    scene.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in d["nodes"]], lag_ratio=0.12), run_time=rt * 0.3)
    arrs = [(d["top"], d["l_top"]), (d["left"], d["l_left"]), (d["right"], d["l_right"])]
    scene.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(l)) for a, l in arrs], lag_ratio=0.25),
               run_time=rt * 0.45)
    if bottom_last:
        scene.play(Create(d["bot"]), FadeIn(d["l_bot"]), run_time=rt * 0.25)


def panel(*rows, y=0.3, buff=0.28):
    return VGroup(*rows).arrange(DOWN, buff=buff).move_to([-0.2, y, 0])


def brook(x=0.0, top=2.4, bottom=-2.4, amp=0.16, width=0.16, seed=5, color=INK):
    """A sinuous, tapered ink stroke running top→bottom: the 溪 between the two banks."""
    rng = np.random.default_rng(seed)
    n = 160
    s = np.linspace(0, 1, n)
    y = top + (bottom - top) * s
    ph = rng.uniform(0, 2 * np.pi)
    xc = x + amp * np.sin(2.6 * np.pi * s + ph) + 0.05 * np.sin(9 * s + 1.1)
    taper = np.clip(np.minimum(s / 0.12, (1 - s) / 0.18), 0.12, 1) ** 0.7
    w = width * taper * (1 + 0.12 * np.sin(21 * s + 0.3))
    left = np.stack([xc - w / 2, y, 0 * s], 1)
    right = np.stack([xc + w / 2, y, 0 * s], 1)
    return Polygon(*np.concatenate([left, right[::-1]], 0), stroke_width=0, fill_color=color, fill_opacity=0.85)


def adj_picture(center=ORIGIN, w=6.4, size=34):
    """D (left) and C (right) as washes; L: D→C over the top, R: C→D underneath."""
    c = np.array(center, dtype=float)
    eD = Ellipse(width=2.2, height=1.6, stroke_color=INK2, stroke_width=2, fill_color=WASH, fill_opacity=0.9)
    eC = eD.copy()
    eD.move_to(c + [-w / 2, 0, 0]); eC.move_to(c + [w / 2, 0, 0])
    tD = mixed("D", size=size + 6, color=INK).move_to(eD)
    tC = mixed("C", size=size + 6, color=INK).move_to(eC)
    aL = CurvedArrow(eD.get_top() + RIGHT * 0.5 + DOWN * 0.08, eC.get_top() + LEFT * 0.5 + DOWN * 0.08,
                     angle=-PI / 3.2, color=SEAL, stroke_width=3.4, tip_length=0.2)
    aR = CurvedArrow(eC.get_bottom() + LEFT * 0.5 + UP * 0.08, eD.get_bottom() + RIGHT * 0.5 + UP * 0.08,
                     angle=-PI / 3.2, color=TYPE_C, stroke_width=3.4, tip_length=0.2)
    lL = mixed("L", size=size, color=SEAL).next_to(aL.point_from_proportion(0.5), UP, buff=0.12)
    lR = mixed("R", size=size, color=TYPE_C).next_to(aR.point_from_proportion(0.5), DOWN, buff=0.12)
    g = VGroup(eD, eC, tD, tC, aL, aR, lL, lR)
    g.parts = dict(eD=eD, eC=eC, tD=tD, tC=tC, aL=aL, aR=aR, lL=lL, lR=lR)
    return g


def tri(a, b, c, top, right, diag, center=ORIGIN, w=2.9, h=2.2, size=30, lsize=24):
    """Triangle identity: a --top--> b --right--> c, diagonal a --diag--> c."""
    o = np.array(center, dtype=float)
    na = node(a, size=size).move_to(o + [-w / 2, h / 2, 0])
    nb = node(b, size=size).move_to(o + [w / 2, h / 2, 0])
    nc = node(c, size=size).move_to(o + [w / 2, -h / 2, 0])
    at = arrow(na, nb); ar = arrow(nb, nc); ad = arrow(na, nc, dashed=True, color=SEAL)
    lt = label(at, top, UP, size=lsize); lr = label(ar, right, RIGHT, size=lsize)
    ld = mixed(diag, size=lsize, color=SEAL).next_to(ad.get_center(), DL, buff=0.06)
    return VGroup(VGroup(na, nb, nc), VGroup(at, ar), VGroup(lt, lr), VGroup(ad, ld))


def string_mu(center=ORIGIN, sx=0.75, h=3.0):
    """String diagram for μ = R ε L : (R L)(R L) → R L, read bottom → top."""
    o = np.array(center, dtype=float)
    yb, yt = -h / 2, h / 2
    xs = [-1.5 * sx, -0.5 * sx, 0.5 * sx, 1.5 * sx]
    region = Rectangle(width=4 * sx + 1.6, height=h, stroke_width=0, fill_color=WASH, fill_opacity=0.7).move_to(o)
    def P(x, y):
        return o + np.array([x, y, 0])
    left = CubicBezier(P(xs[0], yb), P(xs[0], yb + h * 0.45), P(-0.5 * sx, yt - h * 0.45), P(-0.5 * sx, yt),
                       stroke_color=SEAL, stroke_width=4)
    right = CubicBezier(P(xs[3], yb), P(xs[3], yb + h * 0.45), P(0.5 * sx, yt - h * 0.45), P(0.5 * sx, yt),
                        stroke_color=TYPE_C, stroke_width=4)
    ycap = yb + h * 0.42
    cap = VGroup(
        CubicBezier(P(xs[1], yb), P(xs[1], ycap * 0.55 + yb * 0.45), P(xs[1] * 0.55, ycap), P(0, ycap),
                    stroke_color=TYPE_C, stroke_width=4),
        CubicBezier(P(0, ycap), P(xs[2] * 0.55, ycap), P(xs[2], ycap * 0.55 + yb * 0.45), P(xs[2], yb),
                    stroke_color=SEAL, stroke_width=4),
    )
    dot = Dot(P(0, ycap), radius=0.08, color=INK)
    eps = mixed("ε", size=28, color=INK).next_to(dot, UP, buff=0.1)
    bl = VGroup(*[mixed(t, size=26, color=SEAL if t == "L" else TYPE_C).move_to(P(x, yb - 0.3))
                  for t, x in zip("LRLR", xs)])
    tl = VGroup(mixed("L", size=26, color=SEAL).move_to(P(-0.5 * sx, yt + 0.3)),
                mixed("R", size=26, color=TYPE_C).move_to(P(0.5 * sx, yt + 0.3)))
    return VGroup(region, left, right, cap, dot, eps, bl, tl)


def tape(vals, focus=None, cell=1.0, y=0.0, x0=None, size=26, color=INK):
    n = len(vals)
    x0 = -(n - 1) * cell / 2 if x0 is None else x0
    cells = VGroup()
    for i, v in enumerate(vals):
        sq = Square(side_length=cell * 0.92, stroke_color=INK2, stroke_width=2,
                    fill_color=WASH, fill_opacity=0.55).move_to([x0 + i * cell, y, 0])
        t = mixed(v, size=size, color=color).move_to(sq)
        if t.width > cell * 0.84:
            t.scale_to_fit_width(cell * 0.84)
        cells.add(VGroup(sq, t))
    return cells


def mini_store(k, n=5, cell=0.92, focus_at=None):
    """Tiny tape icon of n boxes with a red focus box — 'a Store focused at k'."""
    w = cell * 0.82 / n
    row = VGroup(*[Square(side_length=w * 0.86, stroke_color=INK2, stroke_width=1.2,
                          fill_color=SEAL if i == focus_at else WASH,
                          fill_opacity=0.9 if i == focus_at else 0.5) for i in range(n)])
    row.arrange(RIGHT, buff=w * 0.14)
    return row


class Base(TaoScene):
    def head_only(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()

    def swap(self, old, new, rt=1.4, out=0.35):
        if old is not None:
            self.play(FadeOut(old), run_time=out)
        self.play(FadeIn(new), run_time=rt)
        return new


# =====================================================================================
class S0Title(TaoScene):
    SID = "S0Title"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=29).move_to([0, 0.55, 0]))
        title = callig("知其雄，守其雌", size=64).move_to([-0.05, 0.6, 0])
        sub = body("道可道 · 进阶深讲 11 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("伴随 · 单子 · 余单子 · State · Store", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.0)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("进阶 10 终余代数", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("进阶 11", size=32, color=INK),
            body("函子之间的普遍性", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.28).move_to([2.0, 1.6, 0])
        eq = mixed("伴随 L ⊣ R ：  C(L x, y)  ≅  D(x, R y)", size=28, color=TYPE_C).move_to([2.0, 0.3, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.48).move_to([-4.5, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
            self.at(1, 0.65)
            self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  伴随 · hom 集的自然同构", size=30),
            body("②  单位 η · 余单位 ε · 三角恒等式", size=30),
            body("③  R∘L ⇒ 单子 · State", size=30),
            body("④  L∘R ⇒ 余单子 · Store · lens", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.3, 0.05, 0])
        with self.beat(2):
            self.play(FadeOut(series), FadeOut(eq), run_time=0.4)
            for i, row in enumerate(outline):
                self.at(2, [0.02, 0.22, 0.48, 0.70][i])
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.48)
        refs = VGroup(
            body("参考：DaoFP ch.10 / 16 / 17  ·  CTFP 3.2 / 3.6 / 3.7", size=24, color=INK3),
            serif("Bartosz Milewski", size=28, color=INK2),
        ).arrange(DOWN, buff=0.12).move_to([2.3, -2.25, 0])
        s = seal(0.75).next_to(left, DOWN, buff=0.15).shift(RIGHT * 1.2)
        src = body("知其白，守其黑 ——第二十八章", size=22, color=SEAL).next_to(s, DOWN, buff=0.15)
        with self.beat(3):
            self.play(FadeIn(refs, shift=UP * 0.1), run_time=1.0)
            self.at(3, 0.7)
            self.play(FadeIn(s, scale=1.5), FadeIn(src), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S1Hook(Base):
    locals().update(meta_cls("S1Hook"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: two banks, one brook; L and R in opposite directions
        xiong = VGroup(callig("雄", size=84), body("一岸向外流", size=26, color=INK2)).arrange(DOWN, buff=0.2)
        ci = VGroup(callig("雌", size=84), body("一岸向内收", size=26, color=INK2)).arrange(DOWN, buff=0.2)
        xiong.move_to([-3.6, 0.6, 0]); ci.move_to([2.8, 0.6, 0])
        bk = brook(x=-0.4, top=2.3, bottom=-1.2, seed=11)
        aL = arrow([-2.4, 1.5, 0], [1.6, 1.5, 0], color=SEAL, sw=3.4)
        aR = arrow([1.6, -0.3, 0], [-2.4, -0.3, 0], color=TYPE_C, sw=3.4)
        lL = mixed("L", size=30, color=SEAL).next_to(aL, UP, buff=0.08).shift(RIGHT * 1.0)
        lR = mixed("R", size=30, color=TYPE_C).next_to(aR, DOWN, buff=0.08).shift(RIGHT * 1.0)
        cap = body("方向相反 · 互不为逆 · 彼此知晓", size=28, color=SEAL).move_to([-0.4, -2.2, 0])
        with self.beat(1):
            self.play(FadeIn(xiong, shift=RIGHT * 0.1), FadeIn(ci, shift=LEFT * 0.1), run_time=1.0)
            self.play(FadeIn(bk), run_time=0.9)
            self.at(1, 0.45)
            self.play(GrowArrow(aL), FadeIn(lL), run_time=0.8)
            self.play(GrowArrow(aR), FadeIn(lR), run_time=0.8)
            self.play(FadeIn(cap), run_time=0.5)
        g1 = VGroup(xiong, ci, bk, aL, aR, lL, lR, cap)
        # beat 2: iso / equivalence / adjunction
        rows = VGroup(
            VGroup(body("同构", size=30), mixed("R∘L = Id     L∘R = Id", size=30, color=INK3)),
            VGroup(body("等价", size=30), mixed("R∘L ≅ Id     L∘R ≅ Id", size=30, color=INK2)),
            VGroup(body("伴随", size=30, color=SEAL), mixed("η : Id → R∘L     ε : L∘R → Id", size=30, color=TYPE_C)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.7)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-0.4, 0.55, 0])
        half = body("Milewski：「半个等价」 half-equivalence", size=26, color=INK3).move_to([-0.4, -1.9, 0])
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.35)
            for i, r in enumerate(rows):
                self.at(2, [0.0, 0.22, 0.45][i])
                self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.7)
            self.at(2, 0.8)
            self.play(FadeIn(half), run_time=0.5)
        g2 = VGroup(rows, half)
        ev = panel(
            mixed("+  ⊣  Δ  ⊣  ×", size=40, color=TYPE_C),
            mixed("colim  ⊣  Δ  ⊣  lim", size=36, color=TYPE_C),
            mixed("Free  ⊣  U", size=36, color=TYPE_C),
            body("hom 集之间的同构 · 一旦认出，到处冒头", size=28, color=SEAL),
        )
        with self.beat(3):
            self.swap(g2, ev)
        pair = panel(
            body("最朴素的一对", size=28, color=INK3),
            mixed("(− , s)  ⊣  (s → −)", size=42, color=TYPE_C),
            body("天天在用 · 名字叫 curry", size=28, color=INK2),
            body("流出两条支流：State · Store", size=30, color=SEAL),
        )
        with self.beat(4):
            self.swap(ev, pair)
        self.end_scene()


# =====================================================================================
class S2Adjunction(Base):
    SID = "S2Adjunction"
    TITLE = "二 · 伴随：hom 集的同构"

    def construct(self):
        self.head_only()
        pic = adj_picture(center=[-0.4, 1.05, 0], w=6.0)
        P = pic.parts
        f1 = mixed("C(L x, y)   ≅   D(x, R y)", size=40, color=INK).move_to([-0.4, -1.45, 0])
        f2 = mixed("L ⊣ R", size=36, color=SEAL).move_to([-0.4, -2.35, 0])
        with self.beat(0):
            self.play(FadeIn(P["eD"]), FadeIn(P["eC"]), FadeIn(P["tD"]), FadeIn(P["tC"]), run_time=0.8)
            self.at(0, 0.2)
            self.play(Create(P["aL"]), FadeIn(P["lL"]), run_time=0.8)
            self.at(0, 0.32)
            self.play(Create(P["aR"]), FadeIn(P["lR"]), run_time=0.8)
            self.at(0, 0.55)
            self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(f2), run_time=0.5)
        g0 = VGroup(pic, f1, f2)
        d = square("C(L x, y)", "C(L x, y′)", "D(x, R y)", "D(x, R y′)", "f ∘ −", "φ", "φ", "R f ∘ −",
                   center=[-0.6, 0.55, 0], w=5.6, h=2.5, size=30, lsize=26, dash_bottom=False)
        eqn = mixed("φ(f ∘ g)  =  R f ∘ φ(g)", size=32, color=SEAL).move_to([-0.6, -1.85, 0])
        tp = body("对应的两支箭头：互称转置", size=26, color=INK2).move_to([-0.6, -2.55, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            draw_square(self, d, rt=2.6)
            self.at(1, 0.5)
            self.play(FadeIn(eqn), run_time=0.7)
            self.at(1, 0.78)
            self.play(FadeIn(tp), run_time=0.5)
        g1 = VGroup(d["all"], eqn, tp)
        lc = VGroup(body("映出", size=34, color=SEAL), mixed("L x  →  y", size=34, color=TYPE_C),
                    body("左伴随保持余极限", size=28, color=INK2)).arrange(DOWN, buff=0.26)
        rc = VGroup(body("映入", size=34, color=TYPE_C), mixed("x  →  R y", size=34, color=TYPE_C),
                    body("右伴随保持极限", size=28, color=INK2)).arrange(DOWN, buff=0.26)
        VGroup(lc, rc).arrange(RIGHT, buff=2.2).move_to([-0.4, 0.5, 0])
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.4)
            self.play(FadeIn(lc, shift=UP * 0.1), run_time=0.8)
            self.at(2, 0.3)
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.8)
            self.at(2, 0.62)
            self.play(Indicate(lc[2], color=SEAL), Indicate(rc[2], color=SEAL), run_time=1.0)
        g2 = VGroup(lc, rc)
        ccc = panel(
            body("指数：最经典的伴随", size=28, color=INK3),
            mixed("C(e × a, b)   ≅   C(e, bᵃ)", size=38, color=TYPE_C),
            mixed("(− × a)  ⊣  (−)ᵃ", size=36, color=SEAL),
            body("对所有 a 成立 ⇒ 笛卡尔闭范畴", size=28, color=INK2),
        )
        with self.beat(3):
            self.swap(g2, ccc)
        hs = panel(
            mixed("((a, s) → b)   ≅   (a → s → b)", size=36, color=TYPE_C),
            mixed("curry  →        ←  uncurry", size=30, color=INK2),
            mixed("L a = (a, s)        R b = s → b", size=30, color=INK),
            mixed("(,) s  ⊣  (->) s", size=38, color=SEAL),
            body("（(a, s) ≅ (s, a)，分量顺序无关）", size=22, color=INK3),
            buff=0.3,
        )
        with self.beat(4):
            self.play(FadeOut(ccc), run_time=0.35)
            self.play(FadeIn(hs[0]), run_time=0.8)
            self.at(4, 0.35)
            self.play(FadeIn(hs[1]), run_time=0.6)
            self.at(4, 0.6)
            self.play(FadeIn(hs[2]), run_time=0.6)
            self.play(FadeIn(hs[3]), FadeIn(hs[4]), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S3UnitCounit(Base):
    SID = "S3UnitCounit"
    TITLE = "三 · 单位、余单位与三角"

    def construct(self):
        self.head_only()
        u = panel(
            mixed("C(L x, L x)   ≅   D(x, R(L x))", size=36, color=INK),
            mixed("id   ↦   η", size=34, color=INK2),
            mixed("η : x → R(L x)", size=40, color=SEAL),
            body("拿恒等去换 · 米田式技巧", size=26, color=INK3),
        )
        with self.beat(0):
            self.play(FadeIn(u[0]), run_time=0.9)
            self.at(0, 0.4)
            self.play(FadeIn(u[1], shift=DOWN * 0.1), run_time=0.7)
            self.at(0, 0.62)
            self.play(FadeIn(u[2], scale=1.05), run_time=0.7)
            self.at(0, 0.8)
            self.play(FadeIn(u[3]), run_time=0.5)
        c = panel(
            mixed("C(L(R y), y)   ≅   D(R y, R y)", size=36, color=INK),
            mixed("ε   ↤   id", size=34, color=INK2),
            mixed("ε : L(R y) → y", size=40, color=SEAL),
            mixed("η : Id → R∘L        ε : L∘R → Id", size=32, color=TYPE_C),
        )
        with self.beat(1):
            self.play(FadeOut(u), run_time=0.35)
            self.play(FadeIn(c[0]), run_time=0.8)
            self.at(1, 0.25)
            self.play(FadeIn(c[1]), FadeIn(c[2]), run_time=0.8)
            self.at(1, 0.55)
            self.play(FadeIn(c[3], shift=UP * 0.1), run_time=0.8)
        t1 = tri("L", "L R L", "L", "L η", "ε L", "id", center=[-3.4, 0.55, 0])
        t2 = tri("R", "R L R", "R", "η R", "R ε", "id", center=[2.4, 0.55, 0])
        f1 = mixed("(εL)·(Lη) = id_L", size=28, color=TYPE_C).move_to([-3.4, -1.45, 0])
        f2 = mixed("(Rε)·(ηR) = id_R", size=28, color=TYPE_C).move_to([2.4, -1.45, 0])
        wu = body("插入再消去 —— 归于无为", size=30, color=SEAL).move_to([-0.5, -2.45, 0])
        with self.beat(2):
            self.play(FadeOut(c), run_time=0.35)
            self.play(FadeIn(t1[0]), Create(t1[1]), FadeIn(t1[2]), run_time=1.0)
            self.play(Create(t1[3]), FadeIn(f1), run_time=0.7)
            self.at(2, 0.55)
            self.play(FadeIn(t2[0]), Create(t2[1]), FadeIn(t2[2]), run_time=1.0)
            self.play(Create(t2[3]), FadeIn(f2), run_time=0.7)
            self.play(FadeIn(wu), run_time=0.5)
        g2 = VGroup(t1, t2, f1, f2, wu)
        back = panel(
            mixed("f : x → R y      ⟹      ε ∘ L f : L x → y", size=32, color=TYPE_C),
            mixed("g : L x → y      ⟹      R g ∘ η : x → R y", size=32, color=TYPE_C),
            mixed("(η, ε, 三角)   ⟺   hom 同构", size=36, color=SEAL),
            buff=0.5,
        )
        with self.beat(3):
            self.play(FadeOut(g2), run_time=0.35)
            self.play(FadeIn(back[0], shift=RIGHT * 0.1), run_time=0.8)
            self.at(3, 0.5)
            self.play(FadeIn(back[1], shift=RIGHT * 0.1), run_time=0.8)
            self.at(3, 0.8)
            self.play(FadeIn(back[2]), run_time=0.6)
        lc = VGroup(body("单位 η", size=32, color=SEAL), mixed("curry id", size=34, color=TYPE_C),
                    mixed("a ↦ \\s → (a, s)", size=28, color=INK), body("等一个 s，就配成一对", size=24, color=INK2)
                    ).arrange(DOWN, buff=0.25)
        rc = VGroup(body("余单位 ε", size=32, color=SEAL), mixed("uncurry id", size=34, color=TYPE_C),
                    mixed("(f, s) ↦ f s", size=28, color=INK), body("求值 eval", size=24, color=INK2)
                    ).arrange(DOWN, buff=0.25)
        VGroup(lc, rc).arrange(RIGHT, buff=2.0).move_to([-0.4, 0.4, 0])
        with self.beat(4):
            self.play(FadeOut(back), run_time=0.35)
            self.play(FadeIn(lc, shift=UP * 0.1), run_time=0.9)
            self.at(4, 0.5)
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.9)
        self.end_scene()


# =====================================================================================
class S4State(Base):
    SID = "S4State"
    TITLE = "四 · R∘L：State 单子"

    def construct(self):
        self.head_only()
        m = panel(
            mixed("T  =  R ∘ L", size=46, color=TYPE_C),
            mixed("η : Id → T", size=34, color=INK),
            mixed("μ  =  R ε L  :  T ∘ T → T", size=34, color=INK),
            body("任何伴随 ⇒ 一个单子", size=30, color=SEAL),
        )
        with self.beat(0):
            self.play(FadeIn(m[0], scale=0.95), run_time=0.9)
            self.at(0, 0.5)
            self.play(FadeIn(m[3]), run_time=0.6)
            self.at(0, 0.62)
            self.play(FadeIn(m[1]), run_time=0.6)
            self.at(0, 0.78)
            self.play(FadeIn(m[2]), run_time=0.7)
        sd = string_mu(center=[-3.2, 0.2, 0], sx=0.72, h=3.2)
        laws = VGroup(
            body("两条单位律  ⇐  两个三角恒等式", size=28, color=INK),
            body("结合律  ⇐  ε 的自然性", size=28, color=INK),
            mixed("μ = R ε L：中间一对 R L 被 ε 收口", size=26, color=SEAL),
            body("DaoFP ch.16 · 弦图", size=22, color=INK3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([2.6, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(m), run_time=0.35)
            self.play(FadeIn(laws[0], shift=LEFT * 0.1), run_time=0.7)
            self.at(1, 0.22)
            self.play(FadeIn(laws[1], shift=LEFT * 0.1), run_time=0.7)
            self.at(1, 0.45)
            self.play(FadeIn(sd[0]), FadeIn(sd[6]), FadeIn(sd[7]), run_time=0.6)
            self.play(Create(sd[1]), Create(sd[2]), run_time=0.9)
            self.play(Create(sd[3]), FadeIn(sd[4]), FadeIn(sd[5]), run_time=0.9)
            self.play(FadeIn(laws[2]), FadeIn(laws[3]), run_time=0.6)
        g1 = VGroup(sd, laws)
        st = panel(
            mixed("R(L a)   =   s → (a, s)", size=40, color=INK),
            mixed("=   State s a", size=40, color=TYPE_C),
            mixed("η a  =  \\s → (a, s)  =  return a", size=32, color=SEAL),
        )
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.35)
            self.play(FadeIn(st[0]), run_time=0.9)
            self.at(2, 0.4)
            self.play(FadeIn(st[1], shift=UP * 0.1), run_time=0.8)
            self.at(2, 0.62)
            self.play(FadeIn(st[2]), run_time=0.8)
        n_s = node("s", size=36).move_to([-4.6, 1.2, 0])
        n_m = node("(inner, s′)", size=32).move_to([-0.9, 1.2, 0])
        n_e = node("(a, s″)", size=32).move_to([2.8, 1.2, 0])
        a1 = arrow(n_s, n_m, color=TYPE_C, sw=3.2)
        a2 = arrow(n_m, n_e, color=SEAL, sw=3.2)
        l1 = mixed("外层", size=24, color=TYPE_C).next_to(a1, UP, buff=0.1)
        l2 = mixed("ε：内层作用于 s′", size=24, color=SEAL).next_to(a2, UP, buff=0.1)
        j1 = mixed("join = fmap counit        -- R ε L", size=30, color=TYPE_C).move_to([-0.6, -0.4, 0])
        j2 = mixed("join mma = State (fmap (uncurry runState) (runState mma))", size=24, color=INK).move_to([-0.6, -1.3, 0])
        j3 = mixed("uncurry runState  ≡  ε", size=28, color=SEAL).move_to([-0.6, -2.2, 0])
        with self.beat(3):
            self.play(FadeOut(st), run_time=0.35)
            self.play(FadeIn(j1), run_time=0.7)
            self.at(3, 0.25)
            self.play(FadeIn(n_s), FadeIn(n_m), GrowArrow(a1), FadeIn(l1), run_time=0.9)
            self.at(3, 0.55)
            self.play(FadeIn(n_e), GrowArrow(a2), FadeIn(l2), run_time=0.9)
            self.at(3, 0.75)
            self.play(FadeIn(j2), FadeIn(j3), run_time=0.8)
        g3 = VGroup(n_s, n_m, n_e, a1, a2, l1, l2, j1, j2, j3)
        rest = panel(
            mixed("List   ⇐   Free ⊣ U", size=32, color=INK2),
            body("（自由幺半群：离开 Hask）", size=24, color=INK3),
            mixed("State   ⇐   (−, s) ⊣ (s → −)", size=32, color=TYPE_C),
            body("（两边都留在 Hask）", size=24, color=INK3),
            body("每个单子 = 某个伴随：Kleisli · Eilenberg–Moore（不唯一）", size=26, color=SEAL),
            buff=0.22,
        )
        with self.beat(4):
            self.play(FadeOut(g3), run_time=0.35)
            self.play(FadeIn(rest[0]), FadeIn(rest[1]), run_time=0.8)
            self.at(4, 0.3)
            self.play(FadeIn(rest[2]), FadeIn(rest[3]), run_time=0.8)
            self.at(4, 0.6)
            self.play(FadeIn(rest[4]), run_time=0.8)
        self.end_scene()


# =====================================================================================
class S5Store(Base):
    SID = "S5Store"
    TITLE = "五 · L∘R：Store 余单子"

    def construct(self):
        self.head_only()
        w = panel(
            mixed("W  =  L ∘ R", size=46, color=TYPE_C),
            mixed("ε : W → Id", size=34, color=INK),
            mixed("δ  =  L η R  :  W → W ∘ W", size=34, color=INK),
            body("对偶：任何伴随 ⇒ 一个余单子", size=30, color=SEAL),
        )
        with self.beat(0):
            self.play(FadeIn(w[0], scale=0.95), run_time=0.9)
            self.at(0, 0.45)
            self.play(FadeIn(w[3]), run_time=0.6)
            self.at(0, 0.58)
            self.play(FadeIn(w[1]), run_time=0.6)
            self.at(0, 0.76)
            self.play(FadeIn(w[2]), run_time=0.7)
        st = panel(
            mixed("L(R c)   =   (s → c,  s)", size=40, color=INK),
            mixed("=   Store s c", size=40, color=TYPE_C),
            body("余状态余单子 · costate comonad", size=28, color=SEAL),
        )
        with self.beat(1):
            self.swap(w, st)
        # beat 2: tape + focus, extract
        idx = [-3, -2, -1, 0, 1, 2, 3]
        tp = tape([f"f({i})".replace("-", "−") for i in idx], cell=1.15, y=0.9, size=24)
        nums = VGroup(*[mixed(str(i).replace("-", "−"), size=20, color=INK3).next_to(c, DOWN, buff=0.12)
                        for i, c in zip(idx, tp)])
        ptr = Triangle(fill_color=SEAL, fill_opacity=1, stroke_width=0).scale(0.14).rotate(0)
        ptr.next_to(nums[3], DOWN, buff=0.08)
        pl = mixed("s", size=26, color=SEAL).next_to(ptr, DOWN, buff=0.06)
        cap = VGroup(mixed("函数 = 以 s 为下标的整张表", size=28, color=INK2),
                     mixed("extract = ε ：在焦点上查表", size=30, color=SEAL)).arrange(DOWN, buff=0.22).move_to([-0.3, -1.85, 0])
        with self.beat(2):
            self.play(FadeOut(st), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(c) for c in tp], lag_ratio=0.08), FadeIn(nums), run_time=1.2)
            self.play(FadeIn(ptr, shift=UP * 0.1), FadeIn(pl), FadeIn(cap[0]), run_time=0.6)
            self.at(2, 0.6)
            self.play(tp[3][0].animate.set_fill(SEAL, opacity=0.25), Indicate(tp[3][1], color=SEAL), FadeIn(cap[1]),
                      run_time=0.9)
        # beat 3: duplicate — every cell becomes a store focused there
        minis = VGroup()
        for k, c in enumerate(tp):
            ms = mini_store(k, n=7, cell=1.15 * 0.92, focus_at=k).move_to(c[0])
            minis.add(ms)
        code = mixed("duplicate (St f s)  =  St (St f) s", size=32, color=TYPE_C).move_to([-0.3, -1.55, 0])
        cap3 = body("每一格 = 以那一格为焦点的 Store · 视角之表", size=28, color=SEAL).move_to([-0.3, -2.35, 0])
        with self.beat(3):
            self.play(FadeOut(cap), run_time=0.35)
            self.play(FadeIn(code), run_time=0.7)
            self.at(3, 0.3)
            self.play(*[FadeOut(c[1]) for c in tp], run_time=0.4)
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in minis], lag_ratio=0.1), run_time=1.4)
            self.at(3, 0.7)
            self.play(FadeIn(cap3), run_time=0.5)
        g3 = VGroup(tp, nums, ptr, pl, minis, code, cap3)
        # beat 4: extend sum3 on the squares tape
        xs = [0, 1, 2, 3, 4]
        top = tape([str(i * i) for i in [-1] + xs + [5]], cell=1.0, y=1.25, size=26)
        topn = VGroup(*[mixed(str(i).replace("-", "−"), size=18, color=INK3).next_to(c, UP, buff=0.08)
                        for i, c in zip([-1] + xs + [5], top)])
        out = tape(["", "2", "5", "14", "29", "50", ""], cell=1.0, y=-0.35, size=26, color=SEAL)
        for c in (out[0], out[6]):
            c[0].set_opacity(0)
        brk = SurroundingRectangle(VGroup(top[0], top[2]), color=SEAL, stroke_width=3, buff=0.04)
        ar = arrow(brk.get_bottom(), out[1].get_top(), color=SEAL, sw=2.6, buff=0.06)
        ex = mixed("extend k = fmap k ∘ duplicate        k = sum3", size=28, color=TYPE_C).move_to([-0.3, -1.55, 0])
        cap4 = body("一维卷积 · rule 110 · 生命游戏 —— 惰性只算你看的格子", size=26, color=INK2).move_to([-0.3, -2.35, 0])
        with self.beat(4):
            self.play(FadeOut(g3), run_time=0.35)
            self.play(FadeIn(top), FadeIn(topn), FadeIn(ex), run_time=0.9)
            self.play(Create(brk), run_time=0.4)
            self.play(GrowArrow(ar), FadeIn(out[1]), run_time=0.5)
            for k in range(2, 6):
                nb = SurroundingRectangle(VGroup(top[k - 1], top[k + 1]), color=SEAL, stroke_width=3, buff=0.04)
                na = arrow(nb.get_bottom(), out[k].get_top(), color=SEAL, sw=2.6, buff=0.06)
                self.play(Transform(brk, nb), Transform(ar, na), FadeIn(out[k]), run_time=0.45)
            self.at(4, 0.6)
            self.play(FadeIn(cap4), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S6XiongCi(Base):
    SID = "S6XiongCi"
    TITLE = "六 · 知其雄，守其雌"

    def construct(self):
        self.head_only()
        L = VGroup(callig("雄", size=80), mixed("State s", size=34, color=TYPE_C),
                   mixed("a → State s b", size=28, color=INK), body("Kleisli · 效果 · 改写状态", size=24, color=INK2)
                   ).arrange(DOWN, buff=0.24)
        R = VGroup(callig("雌", size=80), mixed("Store s", size=34, color=TYPE_C),
                   mixed("Store s a → b", size=28, color=INK), body("余 Kleisli · 语境 · 守着焦点", size=24, color=INK2)
                   ).arrange(DOWN, buff=0.24)
        L.move_to([-3.7, 0.3, 0]); R.move_to([2.9, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(L, shift=RIGHT * 0.1), run_time=1.0)
            self.at(0, 0.5)
            self.play(FadeIn(R, shift=LEFT * 0.1), run_time=1.0)
        # beat 1: table
        hdr = [body("", size=28), body("State（单子）", size=28, color=TYPE_C), body("Store（余单子）", size=28, color=TYPE_C)]
        r1 = [mixed("η", size=34, color=SEAL), mixed("return", size=28), mixed("藏在 duplicate = L η R", size=26, color=INK2)]
        r2 = [mixed("ε", size=34, color=SEAL), mixed("藏在 join = R ε L", size=26, color=INK2), mixed("extract", size=28)]
        cols_x = [-4.6, -1.6, 2.6]
        rows_y = [1.4, 0.3, -0.8]
        cells = VGroup()
        for row, y in zip([hdr, r1, r2], rows_y):
            for m, x in zip(row, cols_x):
                m.move_to([x, y, 0]); cells.add(m)
        hl = Line([-5.3, 0.85, 0], [4.6, 0.85, 0], color=INK3, stroke_width=1.5)
        cap1 = body("一对 η 与 ε · 两种结构", size=30, color=SEAL).move_to([-0.4, -2.1, 0])
        with self.beat(1):
            self.play(FadeOut(L), FadeOut(R), run_time=0.4)
            self.play(FadeIn(VGroup(*cells[:3])), Create(hl), run_time=0.7)
            self.play(FadeIn(VGroup(*cells[3:6]), shift=RIGHT * 0.1), run_time=0.8)
            self.at(1, 0.55)
            self.play(FadeIn(VGroup(*cells[6:9]), shift=RIGHT * 0.1), run_time=0.8)
            self.at(1, 0.8)
            self.play(FadeIn(cap1), run_time=0.5)
        g1 = VGroup(cells, hl, cap1)
        # beat 2: two banks, one brook = the adjunction
        L2 = VGroup(callig("雄", size=72), mixed("State · 单子", size=30, color=TYPE_C)).arrange(DOWN, buff=0.2).move_to([-3.6, 0.7, 0])
        R2 = VGroup(callig("雌", size=72), mixed("Store · 余单子", size=30, color=TYPE_C)).arrange(DOWN, buff=0.2).move_to([2.8, 0.7, 0])
        bk = brook(x=-0.4, top=2.5, bottom=-1.3, seed=17, width=0.2)
        adj = mixed("L ⊣ R", size=32, color=SEAL).move_to([0.6, 1.9, 0])
        xi = callig("为天下溪", size=56).move_to([-0.4, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.35)
            self.play(FadeIn(L2), FadeIn(R2), run_time=0.8)
            self.play(FadeIn(bk, shift=DOWN * 0.15), run_time=1.1)
            self.play(FadeIn(adj), run_time=0.5)
            self.at(2, 0.6)
            self.play(FadeIn(xi, scale=0.95), run_time=0.9)
        g2 = VGroup(L2, R2, bk, adj, xi)
        lens = panel(
            mixed("φ : s → Store a s", size=40, color=TYPE_C),
            mixed("≅   (get : s → a ,  set : s → a → s)", size=32, color=INK),
            body("lens ：s 是整体 · a 是焦点", size=30, color=SEAL),
            body("Store 余单子的余代数", size=26, color=INK2),
        )
        with self.beat(3):
            self.play(FadeOut(g2), run_time=0.35)
            self.play(FadeIn(lens[0]), FadeIn(lens[3]), run_time=0.9)
            self.at(3, 0.45)
            self.play(FadeIn(lens[1], shift=UP * 0.1), run_time=0.8)
            self.at(3, 0.75)
            self.play(FadeIn(lens[2]), run_time=0.6)
        laws = panel(
            mixed("set s (get s)  =  s", size=32, color=TYPE_C),
            mixed("get (set s a)  =  a", size=32, color=TYPE_C),
            mixed("set (set s a) a′  =  set s a′", size=32, color=TYPE_C),
            body("余代数（第十集）又出现了 —— 这次带着定律", size=28, color=SEAL),
            buff=0.36,
        )
        with self.beat(4):
            self.play(FadeOut(lens), run_time=0.35)
            for i in range(3):
                self.at(4, [0.0, 0.2, 0.42][i])
                self.play(FadeIn(laws[i], shift=RIGHT * 0.1), run_time=0.6)
            self.at(4, 0.65)
            self.play(FadeIn(laws[3]), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S7Haskell(Base):
    SID = "S7Haskell"
    TITLE = "七 · 短 Haskell"

    def construct(self):
        self.head_only()
        code_a = make_code("s_adj", size=24, line_h=0.38).place(-6.2, 2.45)
        with self.beat(0):
            self.play(code_a.write(), run_time=2.0)
            self.at(0, 0.3)
            self.play(code_a.focus(2, 6), run_time=0.6)
            self.at(0, 0.6)
            self.play(code_a.focus(8, 12), run_time=0.6)
            tip = body("伴随的四个零件", size=26, color=SEAL).move_to([4.2, -2.7, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._g = VGroup(code_a, tip)
        code_s = make_code("s_state", size=24, line_h=0.42).place(-6.2, 2.1)
        with self.beat(1):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_s.write(), run_time=1.6)
            self.at(1, 0.35)
            self.play(code_s.focus(3, 5), run_time=0.7)
            tip = mixed("join = R ε L", size=30, color=SEAL).move_to([3.8, -2.4, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._g = VGroup(code_s, tip)
        code_t = make_code("s_store", size=24, line_h=0.38).place(-6.2, 2.45)
        with self.beat(2):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_t.write(), run_time=1.8)
            self.at(2, 0.18)
            self.play(code_t.focus(3, 4), run_time=0.5)
            self.at(2, 0.36)
            self.play(code_t.focus(6, 7), run_time=0.5)
            self.at(2, 0.6)
            self.play(code_t.focus(9, 10), run_time=0.5)
            self.at(2, 0.8)
            self.play(code_t.focus(12, 13), run_time=0.5)
            self._g = VGroup(code_t)
        code_l = make_code("s_lens", size=25, line_h=0.42).place(-6.2, 2.2)
        with self.beat(3):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_l.write(), run_time=1.5)
            self.at(3, 0.3)
            self.play(code_l.focus(9, 10), run_time=0.6)
            tip = mixed("lens = Store 的余代数", size=28, color=SEAL).move_to([3.6, -2.4, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self.at(3, 0.65)
            self.play(code_l.focus(3, 7), run_time=0.6)
            self._g = VGroup(code_l, tip)
        demo = VGroup(
            mixed("$ cabal run tao-category-xiong-ci", size=24, color=INK3),
            mixed("triangleL (7, 's')                 = (7,'s')", size=24, color=TYPE_C),
            mixed("triangleR (+1) 41                  = 42", size=24, color=TYPE_C),
            mixed("runState (replicateM 3 tick) 0     = ([0,1,2],3)", size=24, color=TYPE_C),
            mixed("map (`peek` extend sum3 sq) [0..4] = [2,5,14,29,50]", size=24, color=TYPE_C),
            mixed("set _1 (1, 'x') 9                  = (9,'x')", size=24, color=TYPE_C),
            mixed("lens laws on _1                    = [True,True,True]", size=24, color=TYPE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-0.3, 0.55, 0])
        motto = body("代码怎么写，伴随就怎么说", size=30, color=SEAL).move_to([-0.3, -2.45, 0])
        with self.beat(4):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in demo], lag_ratio=0.28), run_time=3.0)
            self.at(4, 0.8)
            self.play(FadeIn(motto), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S8Next(TaoScene):
    SID = "S8Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.55, frac=tr.get_value(), seed=29).move_to([0, 1.45, 0]))
        glyph = callig("溪", size=96).move_to([0, 1.45, 0])
        points = VGroup(
            body("伴随 = hom 集的自然同构", size=28),
            body("η · ε · 三角恒等式：第二张面孔", size=28),
            body("R∘L ⇒ 单子 State", size=28),
            body("L∘R ⇒ 余单子 Store · lens 是它的余代数", size=28),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.95, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            self.play(FadeIn(glyph, scale=0.9), run_time=0.7)
            for i, p in enumerate(points):
                self.at(0, [0.2, 0.38, 0.62, 0.78][i])
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.42)
        next_title = callig("无为而无不为", size=56).move_to([0, 1.15, 0])
        topics = VGroup(
            body("米田引理 · 只看箭头", size=30, color=INK2),
            body("Kan 扩张", size=30, color=INK2),
            body("不碰对象，就能知道一切", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([0, -0.45, 0])
        next_tag = body("下集预告 · 进阶深讲 12", size=26, color=INK3).move_to([0, -2.15, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), FadeOut(glyph), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(topics), FadeIn(next_tag), run_time=1.4)
        motto = callig("知其雄，守其雌", size=64).move_to([0, 0.7, 0])
        bye = body("伴随一旦被认出，就到处都是。下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(topics), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
