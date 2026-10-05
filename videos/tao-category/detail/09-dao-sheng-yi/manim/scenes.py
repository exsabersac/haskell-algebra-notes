# -*- coding: utf-8 -*-
"""Manim scenes for 进阶深讲 09 · 道生一 (initial algebras, Lambek, Fix, cata, Adámek)."""
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
    """Commutative square. Top arrow tl→tr, right arrow tr→br, bottom bl→br,
    left arrow tl→bl (or bl→tl when up_left). Returns dict of parts + VGroup 'all'."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=19).move_to([0, 0.55, 0]))
        title = callig("道生一", size=84).move_to([-0.1, 0.6, 0])
        sub = body("道可道 · 进阶深讲 09 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("初始代数 · Fix · 兰贝克 · cata", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.0)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("进阶 08 始对象", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("进阶 09", size=32, color=INK),
            body("代数范畴里的始对象", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.28).move_to([2.0, 1.6, 0])
        eq = mixed("一  =  Alg(F) 的始对象  =  初始代数", size=30, color=TYPE_C).move_to([2.0, 0.3, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.52).move_to([-4.35, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
            self.at(1, 0.6)
            self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  代数与同态 · Alg(F)", size=30),
            body("②  初始代数 · cata", size=30),
            body("③  兰贝克引理 · 不动点 μF", size=30),
            body("④  从无出发 · 余极限", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.3, 0.05, 0])
        with self.beat(2):
            self.play(FadeOut(series), FadeOut(eq), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.48)
        refs = VGroup(
            body("参考：DaoFP ch.7 · ch.11  ·  CTFP 3.8", size=24, color=INK3),
            serif("Bartosz Milewski", size=28, color=INK2),
        ).arrange(DOWN, buff=0.12).move_to([2.3, -2.25, 0])
        s = seal(0.75).next_to(left, DOWN, buff=0.15).shift(RIGHT * 1.2)
        with self.beat(3):
            self.play(FadeIn(refs, shift=UP * 0.1), run_time=1.0)
            self.at(3, 0.55)
            self.play(FadeIn(s, scale=1.5), run_time=0.5)
        self.end_scene()


# =====================================================================================
class S1Hook(Base):
    locals().update(meta_cls("S1Hook"))

    def construct(self):
        self.hold(0.3)
        self.quote_card(0)
        # beat 1: counting = phenomenon
        labels = ["Void", "Maybe Void", "Maybe² Void", "Maybe³ Void"]
        xs = [-5.3, -2.3, 0.9, 4.1]
        nodes = VGroup(*[mixed(l, size=22, color=TYPE_C).move_to([x, 0.9, 0]) for l, x in zip(labels, xs)])
        arrs = VGroup(*[arrow(nodes[i], nodes[i + 1], sw=2.6) for i in range(3)])
        cnt = VGroup(*[dots(n).next_to(nodes[i], DOWN, buff=0.45) for i, n in enumerate([0, 1, 2, 3])])
        nums = VGroup(*[callig(c, size=44, color=INK2).next_to(cnt[i], DOWN, buff=0.3)
                        for i, c in enumerate(["无", "一", "二", "三"])])
        tagp = body("入门 03：计数 —— 这是现象", size=28, color=SEAL).move_to([-0.6, -2.2, 0])
        with self.beat(1):
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(c) for c in cnt], lag_ratio=0.2), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.15), run_time=1.0)
            self.at(1, 0.75)
            self.play(FadeIn(tagp), run_time=0.6)
        chain = VGroup(nodes, arrs, cnt, nums, tagp)
        qs = panel(
            body("进阶篇的两个问题", size=28, color=INK3),
            body("① 为什么一层层套下去，会停在一个确定的类型上？", size=30, color=INK),
            body("② 为什么从它出发，折叠恰好只有一种？", size=30, color=INK),
        )
        with self.beat(2):
            self.swap(chain, qs)
        ans = panel(
            body("答案：普遍性质", size=28, color=INK3),
            mixed("递归类型  =  Alg(F) 的始对象", size=36, color=TYPE_C),
            body("刻画一旦成立 → 递归 · 折叠 · 同构 全都跟来", size=28, color=SEAL),
        )
        with self.beat(3):
            self.swap(qs, ans)
        box_l = VGroup(body("递归的机关", size=32), mixed("Fix · cata", size=28, color=TYPE_C),
                       body("只写一次", size=24, color=INK3)).arrange(DOWN, buff=0.2)
        box_r = VGroup(body("可插拔的零件", size=32), mixed("函子 F · 代数 α", size=28, color=TYPE_C),
                       body("不递归 · 随你插", size=24, color=INK3)).arrange(DOWN, buff=0.2)
        VGroup(box_l, box_r).arrange(RIGHT, buff=1.6).move_to([-0.4, 0.5, 0])
        fr_l = SurroundingRectangle(box_l, color=INK3, buff=0.3, stroke_width=1.6, corner_radius=0.1)
        fr_r = SurroundingRectangle(box_r, color=INK3, buff=0.3, stroke_width=1.6, corner_radius=0.1)
        cap = body("Milewski：把递归拆成两半", size=26, color=SEAL).move_to([-0.4, -1.9, 0])
        with self.beat(4):
            self.play(FadeOut(ans), run_time=0.35)
            self.play(FadeIn(box_l), Create(fr_l), run_time=0.9)
            self.play(FadeIn(box_r), Create(fr_r), run_time=0.9)
            self.play(FadeIn(cap), run_time=0.5)
        self.end_scene()


# =====================================================================================
class S2Algebras(Base):
    SID = "S2Algebras"
    TITLE = "二 · 代数与同态"

    def construct(self):
        self.head_only()
        # beat 0: shape functor ExprF with holes
        decl = mixed("data ExprF x = ValF Int | PlusF x x", size=30, color=TYPE_C).move_to([0, 2.2, 0])
        plus_n = Circle(radius=0.36, color=INK, stroke_width=3).move_to([1.6, 0.6, 0])
        plus_t = mixed("+", size=34).move_to(plus_n)
        holes = VGroup(*[DashedVMobject(Circle(radius=0.3, color=INK3, stroke_width=2.4), num_dashes=14)
                         .move_to([1.6 + dx, -1.0, 0]) for dx in (-1.0, 1.0)])
        hx = VGroup(*[mixed("x", size=26, color=INK3).move_to(h) for h in holes])
        edges = VGroup(*[Line(plus_n.get_center() + (h.get_center() - plus_n.get_center()) * 0.28,
                              h.get_center() + (plus_n.get_center() - h.get_center()) * 0.22,
                              color=INK, stroke_width=2.6) for h in holes])
        leaf = RoundedRectangle(width=1.1, height=0.62, corner_radius=0.1, color=INK, stroke_width=3).move_to([-2.4, 0.6, 0])
        leaf_t = mixed("Int", size=26, color=TYPE_C).move_to(leaf)
        or_t = body("或", size=30, color=INK3).move_to([-0.4, 0.6, 0])
        cap0 = body("一层形状 · 洞标出子结构", size=28, color=SEAL).move_to([-0.3, -2.3, 0])
        with self.beat(0):
            self.play(FadeIn(decl, shift=DOWN * 0.1), run_time=0.9)
            self.play(Create(leaf), FadeIn(leaf_t), run_time=0.8)
            self.play(FadeIn(or_t), Create(plus_n), FadeIn(plus_t), run_time=0.7)
            self.play(Create(edges), Create(holes), FadeIn(hx), run_time=1.0)
            self.play(FadeIn(cap0), run_time=0.5)
        g0 = VGroup(decl, plus_n, plus_t, holes, hx, edges, leaf, leaf_t, or_t, cap0)
        # beat 1: algebra (a, alpha)
        fa = node("F a", size=40).move_to([-1.8, 1.3, 0])
        a_ = node("a", size=40).move_to([-1.8, -1.1, 0])
        al = arrow(fa, a_, color=SEAL, sw=3.6)
        al_l = label(al, "α", LEFT, size=32, color=SEAL)
        defn = VGroup(
            body("F-代数", size=34, color=INK),
            mixed("(a,  α : F a → a)", size=32, color=TYPE_C),
            body("载体 a · 结构映射 α", size=26, color=INK2),
            body("洞里已是结果 → 这一步怎么收尾", size=26, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, 0.1, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            self.play(FadeIn(fa), FadeIn(a_), run_time=0.6)
            self.play(GrowArrow(al), FadeIn(al_l), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in defn], lag_ratio=0.25), run_time=1.4)
        g1 = VGroup(fa, a_, al, al_l, defn)
        # beat 2: eval vs pretty
        ev = VGroup(body("求值", size=32), mixed("eval : ExprF Int → Int", size=26, color=TYPE_C),
                    mixed("PlusF m n ↦ m + n", size=24, color=INK2)).arrange(DOWN, buff=0.22)
        pr = VGroup(body("打印", size=32), mixed("pretty : ExprF String → String", size=26, color=TYPE_C),
                    mixed('PlusF s t ↦ s ++ " + " ++ t', size=24, color=INK2)).arrange(DOWN, buff=0.22)
        VGroup(ev, pr).arrange(RIGHT, buff=1.2).move_to([-0.3, 0.6, 0])
        same = body("同一形状 · 许多代数 · 不评判", size=28, color=SEAL).move_to([-0.3, -1.6, 0])
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.4)
            self.play(FadeIn(ev, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(pr, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(same), run_time=0.6)
        g2 = VGroup(ev, pr, same)
        # beat 3: algebra morphism square
        d = square("F a", "F b", "a", "b", "F f", "α", "β", "f", center=[-1.2, 0.35, 0],
                   w=4.6, h=2.6, dash_bottom=False, size=36, lsize=28)
        eqn = mixed("f ∘ α  =  β ∘ F f", size=34, color=SEAL).move_to([-1.2, -2.35, 0])
        with self.beat(3):
            self.play(FadeOut(g2), run_time=0.4)
            draw_square(self, d, rt=2.4)
            self.at(3, 0.45)
            p1 = VGroup(d["top"], d["right"]).copy().set_color(SEAL)
            self.play(ShowPassingFlash(p1[0].copy().set_stroke(width=8), time_width=0.6),
                      d["top"].animate.set_color(SEAL), d["right"].animate.set_color(SEAL), run_time=1.0)
            self.at(3, 0.7)
            self.play(d["left"].animate.set_color(TYPE_C), d["bot"].animate.set_color(TYPE_C), run_time=0.8)
            self.play(FadeIn(eqn), run_time=0.6)
        self._sq = VGroup(d["all"], eqn)
        cat = panel(
            mixed("Alg(F)", size=44, color=TYPE_C),
            body("对象：代数　箭头：同态", size=30, color=INK),
            body("恒等 · 复合：函子保持，方块可拼接", size=26, color=INK2),
            mixed("show : Int → String   ✗  不是同态", size=28, color=SEAL),
        )
        with self.beat(4):
            self.swap(self._sq, cat)
        self.end_scene()


# =====================================================================================
class S3Initial(Base):
    SID = "S3Initial"
    TITLE = "三 · 初始代数与 cata"

    def construct(self):
        self.head_only()
        d = square("F i", "F a", "i", "a", "F ⦇α⦈", "ι", "α", "∃!", center=[-1.6, 0.4, 0],
                   w=4.8, h=2.6, size=38, lsize=28)
        side = VGroup(
            body("初始代数 (i, ι)", size=30, color=INK),
            body("对任意代数 (a, α)", size=26, color=INK2),
            body("同态存在且唯一", size=26, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.9, 0.6, 0])
        with self.beat(0):
            draw_square(self, d, rt=3.0)
            self.play(FadeIn(side, shift=LEFT * 0.1), run_time=0.8)
        name = VGroup(
            mixed("⦇α⦈  =  cata α", size=34, color=TYPE_C),
            body("始对象的唯一出射", size=28, color=SEAL),
            body("入门 04：cata 就是 fold", size=24, color=INK3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.9, 0.4, 0])
        with self.beat(1):
            self.play(FadeOut(side), run_time=0.35)
            self.play(Indicate(d["bot"], color=SEAL, scale_factor=1.05), Indicate(d["l_bot"], color=SEAL), run_time=1.0)
            nl = mixed("cata α", size=28, color=SEAL).move_to(d["l_bot"])
            self.play(Transform(d["l_bot"], nl), FadeIn(name, shift=LEFT * 0.1), run_time=1.0)
        two = VGroup(
            VGroup(body("存在", size=34), body("= 算法", size=28, color=TYPE_C),
                   body("任选代数 → 一条折法", size=24, color=INK2)).arrange(DOWN, buff=0.2),
            VGroup(body("唯一", size=34), body("= 证明原则", size=28, color=TYPE_C),
                   body("同一方块 → 函数相等", size=24, color=INK2)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=1.8).move_to([-0.3, 0.5, 0])
        no = body("不用归纳 · 不逐项比较", size=26, color=SEAL).move_to([-0.3, -1.6, 0])
        with self.beat(2):
            self.play(FadeOut(d["all"]), FadeOut(name), run_time=0.4)
            self.play(FadeIn(two[0], shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(two[1], shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(no), run_time=0.5)
        mb = panel(
            body("F = Maybe", size=30, color=INK3),
            mixed("Maybe a → a   ≅   (a ,  a → a)", size=34, color=TYPE_C),
            body("Nothing ↦ 起点　·　Just ↦ 一步", size=28, color=INK2),
            body("cata = 自然数的递归子", size=28, color=SEAL),
        )
        with self.beat(3):
            self.swap(VGroup(two, no), mb)
        ls = panel(
            body("F = ListF e", size=30, color=INK3),
            mixed("ListF e a → a   ≅   (a ,  (e, a) → a)", size=32, color=TYPE_C),
            body("NilF ↦ 起点　·　ConsF ↦ 头与已折尾", size=28, color=INK2),
            mixed("cata  =  foldr", size=34, color=SEAL),
            body("一切递归类型的折叠 · 同一定理的特例", size=26, color=INK3),
        )
        with self.beat(4):
            self.swap(mb, ls)
        self.end_scene()


# =====================================================================================
class S4Lambek(Base):
    SID = "S4Lambek"
    TITLE = "四 · 兰贝克引理"

    def construct(self):
        self.head_only()
        # beat 0: statement
        fi = node("F i", size=44).move_to([-2.2, 0.6, 0])
        ii = node("i", size=44).move_to([2.2, 0.6, 0])
        a1 = arrow(fi.get_right() + [0.3, 0.18, 0], ii.get_left() + [-0.3, 0.18, 0], buff=0)
        a2 = arrow(ii.get_left() + [-0.3, -0.18, 0], fi.get_right() + [0.3, -0.18, 0], buff=0, color=SEAL)
        l1 = mixed("ι", size=30).next_to(a1, UP, buff=0.12)
        l2 = mixed("ι⁻¹", size=30, color=SEAL).next_to(a2, DOWN, buff=0.12)
        st = mixed("兰贝克引理：ι 是同构　F i ≅ i", size=32, color=TYPE_C).move_to([0, -1.7, 0])
        with self.beat(0):
            self.play(FadeIn(fi), FadeIn(ii), run_time=0.6)
            self.play(GrowArrow(a1), FadeIn(l1), run_time=0.7)
            self.play(FadeIn(st), run_time=0.7)
            self.play(GrowArrow(a2), FadeIn(l2), run_time=0.8)
        g0 = VGroup(fi, ii, a1, a2, l1, l2, st)
        # beat 1: lifted algebra and h
        cx, cy, w, h = -3.4, 0.55, 3.6, 2.5
        d = square("F i", "F (F i)", "i", "F i", "F h", "ι", "F ι", "h", center=[cx, cy, 0],
                   w=w, h=h, size=34, lsize=26)
        note1 = VGroup(
            body("代数自相似", size=28, color=INK3),
            mixed("(F i,  F ι)  也是代数", size=28, color=TYPE_C),
            body("初始性 ⇒ 唯一同态 h", size=26, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -2.0, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            draw_square(self, d, rt=2.6)
            self.play(FadeIn(note1), run_time=0.7)
        # beat 2: paste trivially commuting square
        x2 = cx + w / 2 + w
        n_tr2 = node("F i", size=34).move_to([x2, cy + h / 2, 0])
        n_br2 = node("i", size=34).move_to([x2, cy - h / 2, 0])
        t2 = arrow(d["tr"], n_tr2)
        b2 = arrow(d["br"], n_br2)
        r2 = arrow(n_tr2, n_br2)
        lt2 = label(t2, "F ι", UP, size=26)
        lb2 = label(b2, "ι", DOWN, size=26)
        lr2 = label(r2, "ι", RIGHT, size=26)
        brace = BraceBetweenPoints(d["bl"].get_bottom() + [0, -0.55, 0], n_br2.get_bottom() + [0, -0.55, 0],
                                   direction=DOWN, color=SEAL)
        btxt = mixed("ι ∘ h  =  id   （唯一性）", size=28, color=SEAL).next_to(brace, DOWN, buff=0.12)
        with self.beat(2):
            self.play(FadeOut(note1), run_time=0.35)
            self.play(FadeIn(n_tr2), FadeIn(n_br2), run_time=0.5)
            self.play(Create(t2), FadeIn(lt2), Create(r2), FadeIn(lr2), Create(b2), FadeIn(lb2), run_time=1.4)
            self.at(2, 0.45)
            self.play(GrowFromCenter(brace), run_time=0.6)
            self.at(2, 0.78)
            self.play(FadeIn(btxt), run_time=0.7)
        big = VGroup(d["all"], n_tr2, n_br2, t2, b2, r2, lt2, lb2, lr2, brace, btxt)
        # beat 3: equations
        eqs = VGroup(
            mixed("h ∘ ι", size=36, color=INK),
            mixed("=  F ι ∘ F h", size=36, color=INK),
            mixed("=  F (ι ∘ h)", size=36, color=INK),
            mixed("=  F id  =  id", size=36, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-1.0, 0.45, 0])
        conc = mixed("⇒  h = ι⁻¹", size=36, color=TYPE_C).move_to([3.6, 0.45, 0])
        with self.beat(3):
            self.play(FadeOut(big), run_time=0.4)
            for k, e in enumerate(eqs):
                self.play(FadeIn(e, shift=RIGHT * 0.1), run_time=0.6)
                self.at(3, 0.18 + 0.18 * (k + 1))
            self.play(FadeIn(conc, scale=1.1), run_time=0.7)
        g3 = VGroup(eqs, conc)
        fx = panel(
            mixed("i  =  μF", size=48, color=TYPE_C),
            body("不动点：再作用一次 F，它不变", size=30, color=INK),
            body("最小：任何不动点也是代数 → i 到它总有箭头", size=26, color=INK2),
            body("最小不动点", size=28, color=SEAL),
        )
        with self.beat(4):
            self.swap(g3, fx)
        zr = VGroup(
            callig("道法自然", size=80),
            body("自然 = 自己如此", size=32, color=INK2),
            body("展开一层，还是它自己", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.4).move_to([-0.2, 0.35, 0])
        with self.beat(5):
            self.play(FadeOut(fx), run_time=0.35)
            self.play(FadeIn(zr[0], scale=0.95), run_time=1.2)
            self.play(FadeIn(zr[1]), FadeIn(zr[2]), run_time=0.9)
        self.end_scene()


# =====================================================================================
class S5Fix(Base):
    SID = "S5Fix"
    TITLE = "五 · Fix 与 cata 的来历"

    def construct(self):
        self.head_only()
        decl = mixed("newtype Fix f = Fix { unFix :: f (Fix f) }", size=30, color=TYPE_C).move_to([0, 2.3, 0])
        fi = node("f (Fix f)", size=36).move_to([-3.0, 0.3, 0])
        ii = node("Fix f", size=36).move_to([3.0, 0.3, 0])
        a1 = arrow(fi.get_right() + [0.3, 0.2, 0], ii.get_left() + [-0.3, 0.2, 0], buff=0)
        a2 = arrow(ii.get_left() + [-0.3, -0.2, 0], fi.get_right() + [0.3, -0.2, 0], buff=0, color=SEAL)
        l1 = mixed("Fix  = ι", size=28).next_to(a1, UP, buff=0.12)
        l2 = mixed("unFix = ι⁻¹", size=28, color=SEAL).next_to(a2, DOWN, buff=0.12)
        with self.beat(0):
            self.play(FadeIn(decl, shift=DOWN * 0.1), run_time=0.9)
            self.play(FadeIn(fi), FadeIn(ii), run_time=0.6)
            self.play(GrowArrow(a1), FadeIn(l1), run_time=0.8)
            self.at(0, 0.6)
            self.play(GrowArrow(a2), FadeIn(l2), run_time=0.8)
        g0 = VGroup(decl, fi, ii, a1, a2, l1, l2)
        # beat 1: cata square in Haskell notation
        d = square("f (Fix f)", "f a", "Fix f", "a", "fmap (cata alg)", "unFix", "alg", "cata alg",
                   center=[0, 0.55, 0], w=6.4, h=2.6, up_left=True, size=32, lsize=26)
        defn = mixed("cata alg = alg . fmap (cata alg) . unFix", size=30, color=SEAL).move_to([0, -2.35, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            draw_square(self, d, rt=2.6)
            self.at(1, 0.45)
            for key in ["left", "top", "right"]:
                self.play(d[key].animate.set_color(SEAL).set_stroke(width=5), run_time=0.55)
            self.play(FadeIn(defn, shift=UP * 0.1), run_time=0.8)
        g1 = VGroup(d["all"], defn)
        box_l = VGroup(body("机关", size=34), mixed("Fix · cata", size=28, color=TYPE_C),
                       body("递归只写一次", size=24, color=INK3)).arrange(DOWN, buff=0.2)
        box_r = VGroup(body("零件", size=34), mixed("F · α", size=28, color=TYPE_C),
                       body("不递归 · 由你提供", size=24, color=INK3)).arrange(DOWN, buff=0.2)
        VGroup(box_l, box_r).arrange(RIGHT, buff=1.8).move_to([-0.3, 0.5, 0])
        fr = VGroup(*[SurroundingRectangle(b, color=INK3, buff=0.3, stroke_width=1.6, corner_radius=0.1)
                      for b in (box_l, box_r)])
        cap = body("复杂问题 → 简单零件", size=28, color=SEAL).move_to([-0.3, -1.7, 0])
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.4)
            self.play(FadeIn(box_l), Create(fr[0]), run_time=0.8)
            self.play(FadeIn(box_r), Create(fr[1]), run_time=0.8)
            self.play(FadeIn(cap), run_time=0.5)
        g2 = VGroup(box_l, box_r, fr, cap)
        hon = panel(
            body("诚实的附注", size=28, color=INK3),
            mixed("Set：Fix f  ≅  μF（最小不动点）", size=32, color=TYPE_C),
            body("Hask：惰性 → Fix 也装得下无穷的值", size=28, color=INK2),
            body("最小与最大不动点重合 · 最大不动点 νF 见下集", size=26, color=SEAL),
        )
        with self.beat(3):
            self.swap(g2, hon)
        leaf = panel(
            body("要从无生出东西，形状里须有「叶子」", size=30, color=INK),
            mixed("Nothing  ·  NilF  ·  ValF n", size=32, color=TYPE_C),
            mixed("反例 F x = (Int, x)：在 Set 里 μF = 0", size=28, color=INK2),
            body("没有叶子，就没有起点", size=28, color=SEAL),
        )
        with self.beat(4):
            self.swap(hon, leaf)
        self.end_scene()


# =====================================================================================
class S6Colimit(Base):
    SID = "S6Colimit"
    TITLE = "六 · 从无出发：余极限"

    def construct(self):
        self.head_only()
        names = ["0", "F 0", "F² 0", "F³ 0"]
        xs = [-5.0, -2.5, 0.0, 2.5]
        sizes = [0.18, 0.3, 0.42, 0.54]
        blobs = VGroup(*[ink_blob(r, seed=20 + i).move_to([x, 0.9, 0]) for i, (x, r) in enumerate(zip(xs, sizes))])
        blobs[0] = Circle(radius=0.2, color=INK3, stroke_width=2.4).move_to([xs[0], 0.9, 0])
        labs = VGroup(*[mixed(n, size=28, color=INK2).move_to([x, -0.25, 0]) for n, x in zip(names, xs)])
        arrs = VGroup(*[arrow(blobs[i], blobs[i + 1], sw=2.8) for i in range(3)])
        more = mixed("⋯", size=40, color=INK2).move_to([4.3, 0.9, 0])
        a_more = arrow(blobs[3], more, sw=2.8)
        cap0 = body("F 0 里只剩叶子 · 每作用一次，树高一层", size=28, color=SEAL).move_to([-0.3, -1.4, 0])
        with self.beat(0):
            self.play(FadeIn(blobs[0]), FadeIn(labs[0]), run_time=0.6)
            for i in range(3):
                self.play(GrowArrow(arrs[i]), FadeIn(blobs[i + 1], scale=0.6), FadeIn(labs[i + 1]), run_time=0.8)
            self.play(GrowArrow(a_more), FadeIn(more), run_time=0.6)
            self.play(FadeIn(cap0), run_time=0.6)
        al = VGroup(*[label(arrs[i], t, UP, size=24, buff=0.2) for i, t in enumerate(["!", "F !", "F² !"])])
        colim = DashedVMobject(RoundedRectangle(width=1.7, height=1.3, corner_radius=0.3, color=SEAL, stroke_width=2.6),
                               num_dashes=26).move_to([6.0, 0.9, 0])
        ctxt = mixed("colim", size=24, color=SEAL).move_to(colim)
        a_col = arrow(more, colim, sw=2.8, color=SEAL)
        cap1 = body("ω-链 · 余极限把所有有限阶段粘在一起", size=28, color=SEAL).move_to([-0.3, -1.4, 0])
        with self.beat(1):
            self.play(LaggedStart(*[FadeIn(l) for l in al], lag_ratio=0.25), run_time=1.0)
            self.play(GrowArrow(a_col), Create(colim), FadeIn(ctxt), run_time=1.0)
            self.play(Transform(cap0, cap1), run_time=0.6)
        chain = VGroup(blobs, labs, arrs, more, a_more, al, colim, ctxt, a_col)
        thm = VGroup(
            body("Adámek 定理", size=32, color=INK),
            mixed("F 保持 ω-余极限  ⇒  colim Fⁿ0  =  μF", size=30, color=TYPE_C),
            body("Set 中多项式函子皆满足 · Maybe、ListF 在内", size=26, color=INK2),
            body("无穷加一，还是无穷", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, -1.85, 0])
        with self.beat(2):
            self.play(FadeOut(cap0), chain.animate.scale(0.8).shift(UP * 0.85), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in thm], lag_ratio=0.3), run_time=1.8)
        ex = panel(
            body("F = Maybe", size=28, color=INK3),
            mixed("0 → 1 → 2 → 3 → ⋯   colim = ℕ", size=34, color=TYPE_C),
            body("F x = 1 + a × x", size=28, color=INK3),
            mixed("L  =  1 + a + a² + a³ + ⋯", size=34, color=TYPE_C),
            body("「几何级数」在此有了严格意义", size=26, color=SEAL),
        )
        with self.beat(3):
            self.swap(VGroup(chain, thm), ex)
        mu = panel(
            body("从普遍性看初始代数（Church 编码）", size=28, color=INK3),
            mixed("Mu f  =  ∀ a.  (f a → a) → a", size=38, color=TYPE_C),
            body("一个值 = 它对所有代数的折法", size=28, color=INK2),
            body("「一」，是全部归途的总和", size=30, color=SEAL),
        )
        with self.beat(4):
            self.swap(ex, mu)
        self.end_scene()


# =====================================================================================
class S7Haskell(Base):
    SID = "S7Haskell"
    TITLE = "七 · 短 Haskell"

    def construct(self):
        self.head_only()
        code_f = make_code("s_fix", size=26, line_h=0.44).place(-6.2, 2.2)
        with self.beat(0):
            self.play(code_f.write(), run_time=2.0)
            self.at(0, 0.62)
            self.play(code_f.focus(7, 8), run_time=0.7)
            tip = body("三行机关 · 沿方块读出", size=26, color=SEAL).move_to([3.6, -2.6, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._g = VGroup(code_f, tip)
        code_e = make_code("s_expr", size=25, line_h=0.44).place(-6.2, 2.2)
        code_a = make_code("s_algs", size=25, line_h=0.42).place(-6.2, 2.3)
        with self.beat(1):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_e.write(), run_time=1.2)
            self.at(1, 0.33)
            self.play(FadeOut(code_e), run_time=0.4)
            self.play(code_a.write(), run_time=1.4)
            res = VGroup(mixed("cata eval   e9  →  9", size=26, color=TYPE_C),
                         mixed('cata pretty e9  →  "2 + 3 + 4"', size=26, color=TYPE_C)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, -2.75, 0])
            self.at(1, 0.68)
            self.play(FadeIn(res), run_time=0.7)
            self._g = VGroup(code_a, res)
        code_l = make_code("s_lambek", size=27, line_h=0.48).place(-6.2, 1.6)
        with self.beat(2):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_l.write(), run_time=1.4)
            self.at(2, 0.3)
            self.play(code_l.focus(2, 3), run_time=0.7)
            tip = VGroup(mixed("fmap Fix  =  F ι", size=28, color=TYPE_C),
                         mixed("cata (fmap Fix)  =  h  =  unFix", size=28, color=SEAL)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([1.6, -1.6, 0])
            self.at(2, 0.55)
            self.play(FadeIn(tip), run_time=0.7)
            self._g = VGroup(code_l, tip)
        code_n = make_code("s_nat", size=25, line_h=0.42).place(-6.2, 2.3)
        code_m = make_code("s_mu", size=25, line_h=0.42).place(-6.2, 2.3)
        with self.beat(3):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_n.write(), run_time=1.3)
            self.at(3, 0.42)
            self.play(FadeOut(code_n), run_time=0.4)
            self.play(code_m.write(), run_time=1.4)
            self.play(code_m.focus(9, 10), run_time=0.6)
            self._g = VGroup(code_m)
        demo = VGroup(
            mixed("$ cabal run tao-category-dao-sheng-yi", size=24, color=INK3),
            mixed("cata eval   e9                  = 9", size=28, color=TYPE_C),
            mixed("cata pretty e9                  = 2 + 3 + 4", size=28, color=TYPE_C),
            mixed("lambekOut agrees with unFix     : True", size=28, color=TYPE_C),
            mixed("toInt (suc (suc (suc zero)))    = 3", size=28, color=TYPE_C),
            mixed("cataMu sumAlg (fromList [1..10]) = 55", size=28, color=TYPE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-0.4, 0.55, 0])
        motto = body("图怎么说，代码就怎么应", size=30, color=SEAL).move_to([-0.4, -2.4, 0])
        with self.beat(4):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in demo], lag_ratio=0.3), run_time=2.6)
            self.at(4, 0.75)
            self.play(FadeIn(motto), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S8Next(TaoScene):
    SID = "S8Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.55, frac=tr.get_value(), seed=19).move_to([0, 1.45, 0]))
        one = callig("一", size=96).move_to([0, 1.45, 0])
        points = VGroup(
            body("代数与同态组成范畴 Alg(F)", size=28),
            body("初始代数的唯一出射 = cata", size=28),
            body("兰贝克：ι 同构 → 最小不动点 μF", size=28),
            body("Adámek：从无出发那条链的余极限", size=28),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.95, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            self.play(FadeIn(one, scale=0.9), run_time=0.7)
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.42)
        next_title = callig("反者道之动", size=56).move_to([0, 1.15, 0])
        topics = VGroup(
            body("箭头全部掉头", size=30, color=INK2),
            body("代数 → 余代数 · 始 → 终 · cata → ana", size=30, color=INK2),
            body("从种子展开无穷 · 最大不动点 νF", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([0, -0.45, 0])
        next_tag = body("下集预告", size=26, color=INK3).move_to([0, -2.15, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), FadeOut(one), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(topics), FadeIn(next_tag), run_time=1.4)
        motto = callig("道生一", size=80).move_to([0, 0.7, 0])
        bye = body("机关只写一次，零件随你插。下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(topics), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
