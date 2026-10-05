# -*- coding: utf-8 -*-
"""Manim scenes for 进阶深讲 12 · 无为而无不为 (Yoneda lemma, Kan extensions) — series finale."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from content import SCENES

META = {s["id"]: s for s in SCENES}


def meta_cls(sid):
    m = META[sid]
    return dict(SID=sid, QUOTE=m["quote"], TITLE=m["title"], CHAPTER=m["chapter"])


def panel(*rows, y=0.3, buff=0.28):
    return VGroup(*rows).arrange(DOWN, buff=buff).move_to([-0.2, y, 0])


def hom_fan(center=ORIGIN, n=5, r=2.2, label_a="a", color=INK):
    """Object a with outgoing Hom-arrows to x0..xn."""
    c = np.array(center, dtype=float)
    blob = ink_blob(radius=0.55, seed=11).move_to(c)
    la = mixed(label_a, size=36, color=color).move_to(c)
    outs = VGroup()
    labs = VGroup()
    for i in range(n):
        ang = PI * (-0.35 + 0.7 * i / max(1, n - 1))
        q = c + r * np.array([np.cos(ang), np.sin(ang), 0])
        tgt = Dot(q, radius=0.06, color=INK2)
        ar = arrow(c + 0.7 * np.array([np.cos(ang), np.sin(ang), 0]), q, buff=0.05, color=INK)
        outs.add(VGroup(ar, tgt))
        labs.add(mixed(f"x{i}", size=22, color=INK3).next_to(tgt, RIGHT if abs(ang) < 0.5 else UP, buff=0.08))
    return VGroup(blob, la, outs, labs)


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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=41).move_to([0, 0.55, 0]))
        title = callig("无为而无不为", size=60).move_to([-0.05, 0.6, 0])
        sub = body("道可道 · 进阶深讲 12 · 系列终章", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("米田引理 · Kan 扩张 · 看箭头", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.0)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("进阶 07 道可道", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("进阶 12 · 赎回", size=32, color=INK),
            body("对象不可道 · 箭头可道", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.22).move_to([1.6, 1.6, 0])
        tease = mixed("待赎回 → 今日赎回", size=28, color=TYPE_C).move_to([1.6, 0.3, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.48).move_to([-4.5, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
            self.at(1, 0.65)
            self.play(FadeIn(tease, shift=UP * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  可表函子 Hom(a, −)", size=30),
            body("②  米田引理 · 对象由箭头决定", size=30),
            body("③  Haskell · Yoneda · forall", size=30),
            body("④  Kan 扩张 Ran / Lan → 回到道可道", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([1.5, -1.3, 0])
        with self.beat(2):
            for i, row in enumerate(outline):
                self.at(2, [0.05, 0.28, 0.52, 0.75][i])
                self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.45)
        books = VGroup(
            body("DaoFP ch.9 / 20", size=28, color=INK2),
            body("CTFP 2.5 / 2.6 / 3.11", size=28, color=INK2),
            body("释义，不是照录", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([1.5, -1.5, 0])
        s = seal(0.75).move_to([5.2, -2.4, 0])
        with self.beat(3):
            self.play(FadeOut(outline), FadeOut(series), FadeOut(tease), run_time=0.4)
            self.play(FadeIn(books), FadeIn(s, scale=1.3), run_time=1.0)
        self.end_scene()


# =====================================================================================
class S1Hook(TaoScene):
    SID = "S1Hook"
    QUOTE = "道常无为而无不为。"
    TITLE = "一 · 道德经钩子"
    CHAPTER = "《道德经》第三十七章"

    def construct(self):
        self.quote_card(0)
        # beat 1: id = wu wei
        id_loop = Circle(radius=0.9, color=INK, stroke_width=4).move_to([-2.5, 0.4, 0])
        tip = Triangle(color=INK, fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.12)
        tip.rotate(-0.3).move_to(id_loop.point_from_proportion(0.12))
        id_lab = mixed("id_a", size=36, color=SEAL).move_to([-2.5, 0.4, 0])
        wu = callig("无为", size=64).move_to([2.0, 1.0, 0])
        cap1 = VGroup(
            body("恒等箭头 = wu wei", size=30, color=INK2),
            body("什么也不改变，也不花时间", size=28, color=INK3),
            serif("DaoFP ch.2", size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.0, -0.8, 0])
        with self.beat(1):
            self.play(Create(id_loop), FadeIn(tip), FadeIn(id_lab), run_time=1.2)
            self.at(1, 0.35)
            self.play(FadeIn(wu, scale=0.95), run_time=0.8)
            self.at(1, 0.6)
            self.play(FadeIn(cap1), run_time=0.8)
        g1 = VGroup(id_loop, tip, id_lab, wu, cap1)
        # beat 2: 无不为
        eq = panel(
            mixed("fromYoneda  g  =  g id", size=34, color=TYPE_C),
            mixed("toYoneda  fa  =  Yoneda (fmap (−) fa)", size=30, color=INK),
            body("无为：只给 id　·　无不为：应对一切箭头", size=28, color=SEAL),
        )
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.35)
            self.play(FadeIn(eq[0]), run_time=0.8)
            self.at(2, 0.4)
            self.play(FadeIn(eq[1]), run_time=0.7)
            self.at(2, 0.7)
            self.play(FadeIn(eq[2]), run_time=0.6)
        # beat 3: ep07 hole
        hole = panel(
            body("第七集留下的漏洞", size=28, color=INK3),
            mixed("对象不可道  ⇒  凭什么 a ≅ b ？", size=32, color=INK),
            mixed("米田：C(a,−) ≅ C(b,−)  ⟺  a ≅ b", size=32, color=SEAL),
            body("同构 = 范畴论里「相同」的全部含义", size=28, color=INK2),
        )
        with self.beat(3):
            self.play(FadeOut(eq), run_time=0.35)
            for i, row in enumerate(hole):
                self.at(3, [0.0, 0.2, 0.5, 0.75][i])
                self.play(FadeIn(row, shift=UP * 0.08), run_time=0.5)
        # beat 4: roadmap
        road = VGroup(
            body("① 可表函子", size=32),
            body("② 米田引理", size=32),
            body("③ Haskell forall", size=32),
            body("④ Kan 扩张", size=32),
            body("⑤ 赎回道可道", size=32, color=SEAL),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(hole), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in road], lag_ratio=0.2), run_time=2.0)
        self.end_scene()


# =====================================================================================
class S2Representable(Base):
    SID = "S2Representable"
    TITLE = "二 · 可表函子"

    def construct(self):
        self.head_only()
        # beat 0: Hom(a,−)
        a = ink_blob(radius=0.5, seed=7).move_to([-3.5, 0.2, 0])
        la = mixed("a", size=40).move_to(a)
        xs = VGroup()
        ars = VGroup()
        for i, name in enumerate(["x", "y", "z"]):
            pos = [1.5 + i * 0.15, 1.6 - i * 1.5, 0]
            n = mixed(name, size=34).move_to(pos)
            xs.add(n)
            ars.add(arrow(a, n, color=INK, sw=3))
        formula = mixed("Hom(a, −) : C → Set", size=34, color=TYPE_C).move_to([-0.5, -2.3, 0])
        with self.beat(0):
            self.play(FadeIn(a), FadeIn(la), run_time=0.7)
            self.play(LaggedStart(*[AnimationGroup(Create(ar), FadeIn(x)) for ar, x in zip(ars, xs)], lag_ratio=0.25),
                      run_time=1.6)
            self.at(0, 0.7)
            self.play(FadeIn(formula), run_time=0.6)
        g0 = VGroup(a, la, xs, ars, formula)
        # beat 1: representable / contravariant
        cov = VGroup(
            mixed("Hom(a, −)", size=36, color=TYPE_C),
            body("正变 · 看出去", size=28, color=INK2),
        ).arrange(DOWN, buff=0.2).move_to([-3.2, 0.5, 0])
        cont = VGroup(
            mixed("Hom(−, a)", size=36, color=TYPE_C),
            body("反变 · 看进来", size=28, color=INK2),
        ).arrange(DOWN, buff=0.2).move_to([2.5, 0.5, 0])
        mid = body("可表函子 · 表示元 a", size=30, color=SEAL).move_to([-0.3, -1.8, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.35)
            self.play(FadeIn(cov), FadeIn(cont), run_time=1.0)
            self.at(1, 0.55)
            self.play(FadeIn(mid), run_time=0.7)
        g1 = VGroup(cov, cont, mid)
        # beat 2: F ≅ Hom(a,−)
        rep = panel(
            mixed("F  ≅  Hom(a, −)", size=40, color=TYPE_C),
            body("F 被 a 表示 · a 是表示元", size=30, color=SEAL),
            body("「万能箭头」瞄准的对象", size=28, color=INK2),
        )
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.35)
            self.play(FadeIn(rep[0]), run_time=0.9)
            self.at(2, 0.4)
            self.play(FadeIn(rep[1]), run_time=0.7)
            self.at(2, 0.7)
            self.play(FadeIn(rep[2]), run_time=0.6)
        # beat 3: Haskell
        hs = panel(
            mixed("a → −    可表", size=36, color=TYPE_C),
            mixed("Speak a  =  forall x. (a → x) → x", size=30, color=INK),
            body("第七集的探测器 · 今天赎回", size=28, color=SEAL),
        )
        with self.beat(3):
            self.play(FadeOut(rep), run_time=0.35)
            self.play(FadeIn(hs[0]), run_time=0.8)
            self.at(3, 0.4)
            self.play(FadeIn(hs[1]), run_time=0.8)
            self.at(3, 0.75)
            self.play(FadeIn(hs[2]), run_time=0.6)
        # beat 4: tease lemma
        tease = panel(
            mixed("Nat( Hom(a, −) ,  F )  ≅  F a", size=38, color=SEAL),
            body("自然变换 ←→ F 在 a 上的一个元素", size=30, color=INK2),
        )
        with self.beat(4):
            self.play(FadeOut(hs), run_time=0.35)
            self.play(FadeIn(tease[0], scale=0.95), run_time=1.1)
            self.at(4, 0.55)
            self.play(FadeIn(tease[1]), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S3Yoneda(Base):
    SID = "S3Yoneda"
    TITLE = "三 · 米田引理"

    def construct(self):
        self.head_only()
        # beat 0: statement
        stmt = panel(
            mixed("Nat( C(a, −) ,  F )  ≅  F(a)", size=40, color=TYPE_C),
            body("米田引理 · Yoneda lemma", size=30, color=SEAL),
            serif("DaoFP ch.9 · CTFP 2.5", size=26),
        )
        with self.beat(0):
            self.play(FadeIn(stmt[0], scale=0.95), run_time=1.2)
            self.at(0, 0.45)
            self.play(FadeIn(stmt[1]), FadeIn(stmt[2]), run_time=0.9)
        # beat 1: α_a(id)
        idn = Circle(radius=0.7, color=SEAL, stroke_width=3.5).move_to([-3.2, 0.5, 0])
        idl = mixed("id_a", size=32, color=SEAL).move_to(idn)
        arr = arrow([-2.2, 0.5, 0], [0.5, 0.5, 0], color=INK, sw=3.5)
        fa = mixed("α_a(id_a)  ∈  F a", size=34, color=TYPE_C).move_to([2.8, 0.5, 0])
        wu = callig("无为", size=48).move_to([-0.5, -1.8, 0])
        with self.beat(1):
            self.play(FadeOut(stmt), run_time=0.35)
            self.play(Create(idn), FadeIn(idl), run_time=0.9)
            self.play(Create(arr), FadeIn(fa), run_time=1.0)
            self.at(1, 0.7)
            self.play(FadeIn(wu, scale=0.95), run_time=0.7)
        g1 = VGroup(idn, idl, arr, fa, wu)
        # beat 2: reverse
        rev = panel(
            mixed("ξ ∈ F a", size=36, color=TYPE_C),
            mixed("α_x(h)  =  F(h)(ξ)", size=36, color=INK),
            body("自然性保证：唯一可能的那一个", size=28, color=SEAL),
            callig("无不为", size=48),
        )
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.35)
            self.play(FadeIn(rev[0]), run_time=0.7)
            self.at(2, 0.3)
            self.play(FadeIn(rev[1]), run_time=0.8)
            self.at(2, 0.6)
            self.play(FadeIn(rev[2]), run_time=0.6)
            self.at(2, 0.8)
            self.play(FadeIn(rev[3], scale=0.95), run_time=0.6)
        # beat 3: 无为而无不为
        both = panel(
            body("无为：不能检查 x，不能凭空造 x", size=30),
            body("只能把你给的箭头原样用上", size=30),
            body("无不为：整族变换被一个元素钉死", size=30, color=SEAL),
            mixed("参数性 = 自然性 = 无为而无不为", size=28, color=TYPE_C),
        )
        with self.beat(3):
            self.play(FadeOut(rev), run_time=0.35)
            for i, row in enumerate(both):
                self.at(3, [0.05, 0.25, 0.5, 0.75][i])
                self.play(FadeIn(row, shift=RIGHT * 0.08), run_time=0.5)
        # beat 4: embedding
        emb = panel(
            mixed("C(a, b)  ≅  Nat( Hom(a,−) , Hom(b,−) )", size=32, color=TYPE_C),
            body("米田嵌入 · 满忠实", size=32, color=SEAL),
            body("fully faithful Yoneda embedding", size=26, color=INK3),
        )
        with self.beat(4):
            self.play(FadeOut(both), run_time=0.35)
            self.play(FadeIn(emb[0]), run_time=1.0)
            self.at(4, 0.45)
            self.play(FadeIn(emb[1]), FadeIn(emb[2]), run_time=0.9)
        # beat 5: redeem ep07
        red = panel(
            mixed("a ≅ b   ⟺   C(a,−) ≅ C(b,−)", size=36, color=SEAL),
            body("对象不可道；全部说法可道——恰好够用", size=28, color=INK),
            body("第七集挂起的话，今日落地", size=28, color=INK2),
        )
        blob = ink_blob(radius=0.7, seed=3).move_to([-4.5, 0.3, 0])
        name = mixed("a", size=36).move_to(blob)
        ins, outs = radiating(blob, r_in=1.6, r_out=1.8, n_in=3, n_out=4)
        with self.beat(5):
            self.play(FadeOut(emb), run_time=0.35)
            self.play(FadeIn(blob), FadeIn(name), FadeIn(ins), FadeIn(outs), run_time=1.0)
            self.at(5, 0.35)
            self.play(FadeIn(red[0].move_to([1.5, 1.0, 0])), run_time=0.8)
            self.at(5, 0.6)
            self.play(FadeIn(red[1].move_to([1.5, -0.2, 0])), run_time=0.6)
            self.at(5, 0.8)
            self.play(FadeIn(red[2].move_to([1.5, -1.2, 0])), run_time=0.5)
        self.end_scene()


# =====================================================================================
class S4Haskell(Base):
    SID = "S4Haskell"
    TITLE = "四 · Haskell：Yoneda 与 forall"

    def construct(self):
        self.head_only()
        code_y = make_code("s_yoneda", size=24, line_h=0.40).place(-6.2, 2.35)
        with self.beat(0):
            self.play(code_y.write(), run_time=2.0)
            tip = mixed("(forall x. (a → x) → f x)  ≅  f a", size=28, color=SEAL).move_to([3.2, -2.5, 0])
            self.at(0, 0.55)
            self.play(FadeIn(tip), run_time=0.6)
            self._g = VGroup(code_y, tip)
        with self.beat(1):
            self.play(code_y.focus(5, 6), run_time=0.6)
            self.at(1, 0.35)
            self.play(code_y.focus(8, 9), run_time=0.6)
            lab = VGroup(
                body("toYoneda · 无不为", size=26, color=TYPE_C),
                body("fromYoneda · 无为", size=26, color=SEAL),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, 0.5, 0])
            self.play(FadeIn(lab), run_time=0.7)
            self._g = VGroup(code_y, tip, lab)
        # beat 2: fmap fusion
        fusion = panel(
            mixed("fmap h (Yoneda g) = Yoneda (\\k → g (k ∘ h))", size=28, color=TYPE_C),
            mixed("fmap h ∘ fmap g  ⇒  一次复合", size=32, color=SEAL),
            body("无为，也是一种优化", size=28, color=INK2),
        )
        with self.beat(2):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(FadeIn(fusion[0]), run_time=1.0)
            self.at(2, 0.4)
            self.play(FadeIn(fusion[1]), run_time=0.8)
            self.at(2, 0.75)
            self.play(FadeIn(fusion[2]), run_time=0.5)
        # beat 3: Speak / redeem
        code_r = make_code("s_redeem", size=25, line_h=0.42).place(-6.2, 2.2)
        with self.beat(3):
            self.play(FadeOut(fusion), run_time=0.35)
            self.play(code_r.write(), run_time=1.8)
            self.at(3, 0.35)
            self.play(code_r.focus(2, 3), run_time=0.5)
            self.at(3, 0.55)
            self.play(code_r.focus(5, 6), run_time=0.5)
            self.at(3, 0.75)
            self.play(code_r.focus(8, 9), run_time=0.5)
            tip3 = body("第七集 Speak · 今日赎回", size=28, color=SEAL).move_to([3.8, -2.4, 0])
            self.play(FadeIn(tip3), run_time=0.5)
            self._g = VGroup(code_r, tip3)
        # beat 4: demo
        demo = VGroup(
            mixed("$ cabal run tao-category-wu-wei", size=24, color=INK3),
            mixed("fromYoneda (toYoneda [1,2,3])            = [1,2,3]", size=24, color=TYPE_C),
            mixed("fromYoneda (fmap (+1) (fmap (*2) y))     = [3,5,7]", size=24, color=TYPE_C),
            mixed("fmap ((+1).(*2)) [1,2,3]                 = [3,5,7]", size=24, color=TYPE_C),
            mixed("redeem (hear 42)                         = 42", size=24, color=TYPE_C),
            mixed("fromYoneda (ranToYoneda (yonedaToRan y)) = [1,2,3]", size=24, color=TYPE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-0.2, 0.55, 0])
        motto = body("代码怎么写，米田就怎么说", size=30, color=SEAL).move_to([-0.2, -2.45, 0])
        with self.beat(4):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in demo], lag_ratio=0.25), run_time=2.8)
            self.at(4, 0.8)
            self.play(FadeIn(motto), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S5Kan(Base):
    SID = "S5Kan"
    TITLE = "五 · Kan 扩张：Ran 与 Lan"

    def construct(self):
        self.head_only()
        # beat 0: setup
        A = Ellipse(width=1.8, height=1.3, stroke_color=INK2, stroke_width=2,
                    fill_color=WASH, fill_opacity=0.85).move_to([-3.5, 0.3, 0])
        B = Ellipse(width=1.8, height=1.3, stroke_color=INK2, stroke_width=2,
                    fill_color=WASH, fill_opacity=0.85).move_to([0.5, 0.3, 0])
        C = Ellipse(width=1.8, height=1.3, stroke_color=INK2, stroke_width=2,
                    fill_color=WASH, fill_opacity=0.85).move_to([-1.5, -2.0, 0])
        tA = mixed("A", size=34).move_to(A)
        tB = mixed("B", size=34).move_to(B)
        tC = mixed("C", size=34).move_to(C)
        p = CurvedArrow(A.get_right() + LEFT * 0.1, B.get_left() + RIGHT * 0.1,
                        angle=-0.3, color=SEAL, stroke_width=3.2, tip_length=0.18)
        f = CurvedArrow(A.get_bottom() + UP * 0.1, C.get_top() + DOWN * 0.05 + LEFT * 0.3,
                        angle=0.4, color=TYPE_C, stroke_width=3.2, tip_length=0.18)
        lp = mixed("p", size=28, color=SEAL).next_to(p, UP, buff=0.08)
        lf = mixed("f", size=28, color=TYPE_C).next_to(f, LEFT, buff=0.08)
        q = body("怎样沿 p 把 f 扩张到 B？", size=30, color=INK).move_to([3.5, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(A), FadeIn(tA), FadeIn(B), FadeIn(tB), FadeIn(C), FadeIn(tC), run_time=1.0)
            self.play(Create(p), FadeIn(lp), Create(f), FadeIn(lf), run_time=1.2)
            self.at(0, 0.7)
            self.play(FadeIn(q), run_time=0.6)
        g0 = VGroup(A, B, C, tA, tB, tC, p, f, lp, lf, q)
        # beat 1: Ran / Lan
        ran = panel(
            mixed("Ran_p f  a  =  ∀b. (a → p b) → f b", size=32, color=TYPE_C),
            body("右 Kan · 最保守的扩张", size=28, color=SEAL),
            mixed("Lan_p f", size=32, color=TYPE_C),
            body("左 Kan · 最慷慨的一侧（对偶）", size=28, color=INK2),
        )
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.35)
            self.play(FadeIn(ran[0]), FadeIn(ran[1]), run_time=1.1)
            self.at(1, 0.55)
            self.play(FadeIn(ran[2]), FadeIn(ran[3]), run_time=0.9)
        # beat 2: universality
        univ = panel(
            body("普遍性：任何其他扩张，唯一地经过它", size=30),
            body("极限 · 伴随 · 米田 ⊆ Kan 扩张", size=30, color=SEAL),
            body("Ran = 右伴随意义下的最佳逼近", size=28, color=INK2),
        )
        with self.beat(2):
            self.play(FadeOut(ran), run_time=0.35)
            for i, row in enumerate(univ):
                self.at(2, [0.1, 0.4, 0.7][i])
                self.play(FadeIn(row, shift=UP * 0.08), run_time=0.6)
        # beat 3: Yoneda ≅ Ran Id
        code_ran = make_code("s_ran", size=23, line_h=0.38).place(-6.2, 2.4)
        tip = mixed("Yoneda f  ≅  Ran Identity f", size=30, color=SEAL).move_to([3.0, -2.4, 0])
        with self.beat(3):
            self.play(FadeOut(univ), run_time=0.35)
            self.play(code_ran.write(), run_time=2.0)
            self.at(3, 0.45)
            self.play(code_ran.focus(0, 2), run_time=0.5)
            self.at(3, 0.7)
            self.play(FadeIn(tip), run_time=0.6)
            self._g = VGroup(code_ran, tip)
        # beat 4: Mac Lane
        mac = panel(
            serif("All concepts are Kan extensions.", size=36, color=INK),
            body("—— Mac Lane", size=28, color=INK3),
            callig("无为而无不为", size=52),
            body("沿恒等扩张：什么也没加，却什么都能说", size=28, color=SEAL),
        )
        with self.beat(4):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(FadeIn(mac[0]), FadeIn(mac[1]), run_time=1.2)
            self.at(4, 0.45)
            self.play(FadeIn(mac[2], scale=0.95), run_time=0.9)
            self.at(4, 0.75)
            self.play(FadeIn(mac[3]), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S6Close(TaoScene):
    SID = "S6Close"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.55, frac=tr.get_value(), seed=41).move_to([0, 1.55, 0]))
        glyph = callig("为", size=96).move_to([0, 1.55, 0])
        points = VGroup(
            body("可表函子 = Hom", size=28),
            body("米田：自然变换被一个元素钉死", size=28),
            body("Yoneda / Speak = 字面翻译", size=28),
            body("Kan 扩张收纳米田", size=28),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.85, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            self.play(FadeIn(glyph, scale=0.9), run_time=0.7)
            for i, p in enumerate(points):
                self.at(0, [0.2, 0.4, 0.6, 0.78][i])
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.42)
        # beat 1: series map
        six = VGroup(
            body("道可道", size=26, color=INK2),
            body("有无相生", size=26, color=INK2),
            body("道生一", size=26, color=INK2),
            body("反者道之动", size=26, color=INK2),
            body("知其雄守其雌", size=26, color=INK2),
            body("无为而无不为", size=26, color=SEAL),
        ).arrange(DOWN, buff=0.18).move_to([-3.5, 0.2, 0])
        one = callig("结构在箭头里", size=48).move_to([2.0, 0.4, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), FadeOut(glyph), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(r) for r in six], lag_ratio=0.12), run_time=1.5)
            self.at(1, 0.55)
            self.play(FadeIn(one, scale=0.95), run_time=1.0)
        # beat 2: redeem
        ans = panel(
            mixed("全部说法自然同构  =  同构", size=34, color=TYPE_C),
            body("不可道的对象，被可道的箭头之全体赎回", size=28, color=SEAL),
            callig("道可道，非常道", size=44),
        )
        with self.beat(2):
            self.play(FadeOut(six), FadeOut(one), run_time=0.4)
            self.play(FadeIn(ans[0]), run_time=0.9)
            self.at(2, 0.4)
            self.play(FadeIn(ans[1]), run_time=0.7)
            self.at(2, 0.7)
            self.play(FadeIn(ans[2], scale=0.95), run_time=0.8)
        # beat 3: finale
        motto = callig("看箭头", size=80).move_to([0, 1.2, 0])
        lines = VGroup(
            body("道可道，非常道。", size=32, color=INK2),
            body("无为而无不为。", size=32, color=INK2),
            body("「道可道」系列，到此完结。", size=30, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([0, -0.6, 0])
        s = seal(0.9).move_to([0, -2.5, 0])
        thanks = body("谢谢观看", size=28, color=INK3).next_to(s, DOWN, buff=0.25)
        with self.beat(3):
            self.play(FadeOut(ans), run_time=0.4)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.at(3, 0.3)
            self.play(FadeIn(lines[0]), run_time=0.5)
            self.at(3, 0.45)
            self.play(FadeIn(lines[1]), run_time=0.5)
            self.at(3, 0.65)
            self.play(FadeIn(lines[2]), FadeIn(s, scale=1.4), FadeIn(thanks), run_time=1.0)
        self.end_scene()
