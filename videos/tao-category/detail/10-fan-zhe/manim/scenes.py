# -*- coding: utf-8 -*-
"""Manim scenes for 进阶深讲 10 · 反者道之动 (coalgebras, ana, hylo, μF/νF)."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=23).move_to([0, 0.55, 0]))
        title = callig("反者道之动", size=72).move_to([-0.1, 0.6, 0])
        sub = body("道可道 · 进阶深讲 10 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("余代数 · ana · hylo · νF", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.0)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("进阶 09 初始代数", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("进阶 10", size=32, color=INK),
            body("箭头全部掉头", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.28).move_to([2.0, 1.6, 0])
        eq = mixed("终余代数  =  CoAlg(F) 的终对象  =  ana", size=28, color=TYPE_C).move_to([2.0, 0.3, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.48).move_to([-4.5, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
            self.at(1, 0.6)
            self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  余代数与同态 · CoAlg(F)", size=30),
            body("②  终余代数 · ana", size=30),
            body("③  μF 与 νF · 阻抗失配", size=30),
            body("④  hylo · 先生而后归", size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.3, 0.05, 0])
        with self.beat(2):
            self.play(FadeOut(series), FadeOut(eq), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.48)
        refs = VGroup(
            body("参考：DaoFP ch.12  ·  CTFP 3.8 Coalgebras", size=24, color=INK3),
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
        # beat 1: flip = duality
        a = node("A", size=40).move_to([-2.4, 0.8, 0])
        b = node("B", size=40).move_to([2.4, 0.8, 0])
        fwd = arrow(a, b, color=INK, sw=3.6)
        fl = mixed("f", size=30).next_to(fwd, UP, buff=0.12)
        tag = body("「反」= 掉头，不是否定", size=28, color=SEAL).move_to([-0.4, -1.6, 0])
        dual = mixed("定理  ⟷  对偶定理", size=32, color=TYPE_C).move_to([-0.4, -2.3, 0])
        with self.beat(1):
            self.play(FadeIn(a), FadeIn(b), GrowArrow(fwd), FadeIn(fl), run_time=1.2)
            self.at(1, 0.35)
            rev = arrow(b, a, color=SEAL, sw=3.6)
            rl = mixed("fᵒᵖ", size=28, color=SEAL).next_to(rev, DOWN, buff=0.12)
            self.play(FadeOut(fwd), FadeOut(fl), GrowArrow(rev), FadeIn(rl), run_time=1.2)
            self.play(FadeIn(tag), FadeIn(dual), run_time=0.7)
            self._g = VGroup(a, b, rev, rl, tag, dual)
        # beat 2: algebra vs coalgebra
        left_col = VGroup(
            body("代数 · 砍树", size=30, color=INK),
            mixed("α : F a → a", size=34, color=TYPE_C),
            body("收拢一层结构", size=26, color=INK2),
            body("cata", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22)
        right_col = VGroup(
            body("余代数 · 种树", size=30, color=INK),
            mixed("γ : a → F a", size=34, color=TYPE_C),
            body("从种子长出一层", size=26, color=INK2),
            body("ana", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22)
        VGroup(left_col, right_col).arrange(RIGHT, buff=1.8).move_to([-0.4, 0.5, 0])
        mile = body("Milewski：cata 砍树，ana 种树", size=26, color=INK3).move_to([-0.4, -2.1, 0])
        with self.beat(2):
            self.play(FadeOut(self._g), run_time=0.35)
            self.play(FadeIn(left_col, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(right_col, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(mile), run_time=0.5)
            self._g = VGroup(left_col, right_col, mile)
        qs = panel(
            body("入门 04：展开是现象", size=28, color=INK3),
            body("① 为什么展开恰好只有一种？", size=30, color=INK),
            body("② 为什么无穷的流也能被同一个 Fix 装下？", size=30, color=INK),
        )
        with self.beat(3):
            self.swap(self._g, qs)
        ans = panel(
            body("答案：普遍性质（掉头）", size=28, color=INK3),
            mixed("终余代数  =  CoAlg(F) 的终对象", size=34, color=TYPE_C),
            body("刻画一旦掉头 → 展开 · 共归纳 · νF 全都跟来", size=26, color=SEAL),
        )
        with self.beat(4):
            self.swap(qs, ans)
        self.end_scene()


# =====================================================================================
class S2Coalgebras(Base):
    SID = "S2Coalgebras"
    TITLE = "二 · 余代数与同态"

    def construct(self):
        self.head_only()
        # beat 0: observe vs fold
        obs = VGroup(
            body("观察", size=34, color=SEAL),
            mixed("a  →  F a", size=36, color=TYPE_C),
            body("从载体里看出一层形状", size=26, color=INK2),
        ).arrange(DOWN, buff=0.25)
        fold = VGroup(
            body("收尾", size=34, color=INK3),
            mixed("F a  →  a", size=36, color=INK3),
            body("上一集：洞里已是结果", size=26, color=INK3),
        ).arrange(DOWN, buff=0.25)
        VGroup(obs, fold).arrange(RIGHT, buff=1.6).move_to([-0.3, 0.5, 0])
        cap0 = body("同一函子 F · 方向反了", size=28, color=SEAL).move_to([-0.3, -2.0, 0])
        with self.beat(0):
            self.play(FadeIn(obs, shift=UP * 0.1), run_time=1.0)
            self.play(FadeIn(fold, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(cap0), run_time=0.5)
        g0 = VGroup(obs, fold, cap0)
        # beat 1: coalgebra definition
        a_ = node("a", size=40).move_to([-1.8, 1.3, 0])
        fa = node("F a", size=40).move_to([-1.8, -1.1, 0])
        al = arrow(a_, fa, color=SEAL, sw=3.6)
        al_l = label(al, "γ", LEFT, size=32, color=SEAL)
        defn = VGroup(
            body("F-余代数", size=34, color=INK),
            mixed("(a,  γ : a → F a)", size=32, color=TYPE_C),
            body("载体 a · 结构映射 γ", size=26, color=INK2),
            body("种子 → 这一步长出什么", size=26, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, 0.1, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            self.play(FadeIn(a_), FadeIn(fa), run_time=0.6)
            self.play(GrowArrow(al), FadeIn(al_l), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in defn], lag_ratio=0.25), run_time=1.4)
        g1 = VGroup(a_, fa, al, al_l, defn)
        # beat 2: two coalgebras
        rg = VGroup(body("有限 · 阶乘的生", size=30),
                    mixed("0 ↦ NilF", size=26, color=TYPE_C),
                    mixed("n ↦ ConsF n (n-1)", size=26, color=TYPE_C)).arrange(DOWN, buff=0.2)
        nt = VGroup(body("无穷 · 自然数流", size=30),
                    mixed("n ↦ StreamF n (n+1)", size=26, color=TYPE_C),
                    body("每一层都有头和尾", size=24, color=INK2)).arrange(DOWN, buff=0.2)
        VGroup(rg, nt).arrange(RIGHT, buff=1.4).move_to([-0.3, 0.55, 0])
        same = body("同一形状 · 许多余代数 · 不评判", size=28, color=SEAL).move_to([-0.3, -1.8, 0])
        with self.beat(2):
            self.play(FadeOut(g1), run_time=0.4)
            self.play(FadeIn(rg, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(same), run_time=0.5)
        g2 = VGroup(rg, nt, same)
        # beat 3: coalgebra morphism square (arrows flipped vs algebra)
        # a --f--> b
        # |g      |d
        # Fa -Ff-> Fb
        d = square("a", "b", "F a", "F b", "f", "γ", "δ", "F f", center=[-1.2, 0.35, 0],
                   w=4.6, h=2.6, dash_bottom=False, size=36, lsize=28)
        eqn = mixed("F f ∘ γ  =  δ ∘ f", size=34, color=SEAL).move_to([-1.2, -2.35, 0])
        with self.beat(3):
            self.play(FadeOut(g2), run_time=0.4)
            draw_square(self, d, rt=2.4)
            self.at(3, 0.45)
            self.play(d["top"].animate.set_color(SEAL), d["right"].animate.set_color(SEAL), run_time=0.8)
            self.at(3, 0.7)
            self.play(d["left"].animate.set_color(TYPE_C), d["bot"].animate.set_color(TYPE_C), run_time=0.8)
            self.play(FadeIn(eqn), run_time=0.6)
        self._sq = VGroup(d["all"], eqn)
        cat = panel(
            mixed("CoAlg(F)", size=44, color=TYPE_C),
            body("对象：余代数　箭头：同态", size=30, color=INK),
            body("恒等 · 复合：函子保持，方块可拼接", size=26, color=INK2),
            mixed("CoAlg(F)  ≅  Alg(F)^op", size=32, color=SEAL),
        )
        with self.beat(4):
            self.swap(self._sq, cat)
        self.end_scene()


# =====================================================================================
class S3Terminal(Base):
    SID = "S3Terminal"
    TITLE = "三 · 终余代数与 ana"

    def construct(self):
        self.head_only()
        # terminal coalgebra square: a --ana--> ν ; Fa --F ana--> Fν ; vertical γ and out
        d = square("a", "ν", "F a", "F ν", "∃!", "γ", "out", "F ana", center=[-1.6, 0.4, 0],
                   w=4.8, h=2.6, size=38, lsize=26, dash_bottom=False)
        # Make top the dashed unique arrow
        d["top"].set_color(SEAL)
        d["l_top"].set_color(SEAL)
        side = VGroup(
            body("终余代数 (ν, out)", size=30, color=INK),
            body("对任意余代数 (a, γ)", size=26, color=INK2),
            body("同态存在且唯一", size=26, color=SEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.9, 0.6, 0])
        with self.beat(0):
            draw_square(self, d, rt=3.0, bottom_last=True)
            self.play(FadeIn(side, shift=LEFT * 0.1), run_time=0.8)
        name = VGroup(
            mixed("ana γ", size=34, color=TYPE_C),
            body("终对象的唯一入射", size=28, color=SEAL),
            body("入门 04：ana 就是 unfold", size=24, color=INK3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.9, 0.4, 0])
        with self.beat(1):
            self.play(FadeOut(side), run_time=0.35)
            self.play(Indicate(d["top"], color=SEAL, scale_factor=1.05), Indicate(d["l_top"], color=SEAL), run_time=1.0)
            nl = mixed("ana γ", size=28, color=SEAL).move_to(d["l_top"])
            self.play(Transform(d["l_top"], nl), FadeIn(name, shift=LEFT * 0.1), run_time=1.0)
        two = VGroup(
            VGroup(body("存在", size=34), body("= 算法", size=28, color=TYPE_C),
                   body("任选余代数 → 一条展法", size=24, color=INK2)).arrange(DOWN, buff=0.2),
            VGroup(body("唯一", size=34), body("= 证明原则", size=28, color=TYPE_C),
                   body("同一方块 → 函数相等", size=24, color=INK2)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=1.6).move_to([-0.3, 0.5, 0])
        no = body("共归纳：方块替你说完", size=26, color=SEAL).move_to([-0.3, -1.6, 0])
        with self.beat(2):
            self.play(FadeOut(d["all"]), FadeOut(name), run_time=0.4)
            self.play(FadeIn(two[0], shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(two[1], shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(no), run_time=0.5)
        lam = panel(
            body("兰贝克的对偶", size=28, color=INK3),
            mixed("out : ν  ≅  F ν", size=36, color=TYPE_C),
            body("ν 是 F 的不动点 —— 最大的那个", size=28, color=INK2),
            mixed("ν  =  νF", size=34, color=SEAL),
        )
        with self.beat(3):
            self.swap(VGroup(two, no), lam)
        ex = panel(
            body("F = StreamF e", size=28, color=INK3),
            mixed("无空构造子 → 无穷流", size=32, color=TYPE_C),
            body("F = ListF e（在 Set）", size=28, color=INK3),
            mixed("μ List  ⊂  ν List", size=32, color=SEAL),
            body("终余代数还装着极限点", size=26, color=INK2),
        )
        with self.beat(4):
            self.swap(lam, ex)
        self.end_scene()


# =====================================================================================
class S4Flip(Base):
    SID = "S4Flip"
    TITLE = "四 · 翻转：图与代码"

    def construct(self):
        self.head_only()
        # beat 0: two squares side by side
        left = square("F i", "F a", "i", "a", "F cata", "ι", "α", "cata",
                      center=[-3.5, 0.5, 0], w=3.6, h=2.3, size=28, lsize=22)
        right = square("a", "ν", "F a", "F ν", "ana", "γ", "out", "F ana",
                       center=[2.8, 0.5, 0], w=3.6, h=2.3, size=28, lsize=22, dash_bottom=False)
        right["top"].set_color(SEAL); right["l_top"].set_color(SEAL)
        tl = body("cata", size=26, color=INK3).move_to([-3.5, -1.9, 0])
        tr = body("ana", size=26, color=SEAL).move_to([2.8, -1.9, 0])
        flip = body("箭头全部翻转", size=28, color=SEAL).move_to([-0.3, 2.4, 0])
        with self.beat(0):
            self.play(FadeIn(flip), run_time=0.5)
            draw_square(self, left, rt=1.8)
            self.play(FadeIn(tl), run_time=0.3)
            self.at(0, 0.45)
            draw_square(self, right, rt=1.8)
            self.play(FadeIn(tr), run_time=0.3)
        g0 = VGroup(left["all"], right["all"], tl, tr, flip)
        # beat 1: code duality
        cata_l = VGroup(
            body("cata", size=28, color=INK3),
            mixed("alg ∘ fmap (cata alg) ∘ unFix", size=26, color=TYPE_C),
        ).arrange(DOWN, buff=0.2)
        ana_l = VGroup(
            body("ana", size=28, color=SEAL),
            mixed("Fix ∘ fmap (ana coa) ∘ coa", size=26, color=TYPE_C),
        ).arrange(DOWN, buff=0.2)
        VGroup(cata_l, ana_l).arrange(DOWN, buff=0.7).move_to([-0.3, 0.6, 0])
        tip = body("复合倒序 · unFix ↔ Fix", size=28, color=SEAL).move_to([-0.3, -2.0, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            self.play(FadeIn(cata_l), run_time=1.0)
            self.at(1, 0.4)
            self.play(FadeIn(ana_l), run_time=1.0)
            self.play(FadeIn(tip), run_time=0.5)
        g1 = VGroup(cata_l, ana_l, tip)
        compress = panel(
            body("对偶是一种压缩", size=32, color=INK),
            body("记住一张方块，掉头即得另一张", size=28, color=INK2),
            body("记住一行复合，倒序即得另一行", size=28, color=INK2),
            mixed("反者道之动", size=36, color=SEAL),
        )
        with self.beat(2):
            self.swap(g1, compress)
        fix_role = panel(
            body("Haskell 里 Fix 兼任两边", size=28, color=INK3),
            mixed("Fix  =  ι  =  out⁻¹", size=34, color=TYPE_C),
            mixed("unFix  =  ι⁻¹  =  out", size=34, color=TYPE_C),
            body("惰性把 μ 与 ν 揉进同一个语法", size=26, color=SEAL),
        )
        with self.beat(3):
            self.swap(compress, fix_role)
        # beat 4: 有无相生 echo — colimit vs limit chains
        up = VGroup(
            mixed("0 → F0 → F²0 → ⋯", size=28, color=TYPE_C),
            body("从无生长 · μF", size=26, color=INK2),
        ).arrange(DOWN, buff=0.2)
        dn = VGroup(
            mixed("1 ← F1 ← F²1 ← ⋯", size=28, color=TYPE_C),
            body("从有逼近 · νF", size=26, color=INK2),
        ).arrange(DOWN, buff=0.2)
        VGroup(up, dn).arrange(DOWN, buff=0.7).move_to([-0.3, 0.5, 0])
        echo = body("有无相生，又出现了一次", size=30, color=SEAL).move_to([-0.3, -2.1, 0])
        with self.beat(4):
            self.play(FadeOut(fix_role), run_time=0.35)
            self.play(FadeIn(up, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(dn, shift=DOWN * 0.1), run_time=0.9)
            self.play(FadeIn(echo), run_time=0.5)
        self.end_scene()


# =====================================================================================
class S5MuNu(Base):
    SID = "S5MuNu"
    TITLE = "五 · μF 与 νF"

    def construct(self):
        self.head_only()
        # beat 0: Set distinction
        mu = VGroup(mixed("μF", size=48, color=TYPE_C), body("最小不动点", size=28),
                    body("从无长出的有限阶段", size=24, color=INK2)).arrange(DOWN, buff=0.2)
        nu = VGroup(mixed("νF", size=48, color=SEAL), body("最大不动点", size=28),
                    body("从有逼近的相容体系", size=24, color=INK2)).arrange(DOWN, buff=0.2)
        VGroup(mu, nu).arrange(RIGHT, buff=2.0).move_to([-0.3, 0.6, 0])
        incl = mixed("Set：  μF  ⊂  νF", size=34, color=INK).move_to([-0.3, -1.8, 0])
        with self.beat(0):
            self.play(FadeIn(mu, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(nu, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(incl), run_time=0.6)
        g0 = VGroup(mu, nu, incl)
        # beat 1: classic examples
        ex = panel(
            body("恒等函子 Id", size=28, color=INK3),
            mixed("μ Id = ∅     ν Id = 1", size=34, color=TYPE_C),
            body("列表函子 1 + a × (−)", size=28, color=INK3),
            mixed("μ = 有限列表     ν ⊃ 极限点", size=32, color=TYPE_C),
        )
        with self.beat(1):
            self.swap(g0, ex)
        # beat 2: Haskell same Fix
        hs = panel(
            body("Haskell · 惰性", size=30, color=INK3),
            mixed("Fix f  兼任  μF  与  νF", size=36, color=TYPE_C),
            body("有限结构可折 · 无穷流可展", size=28, color=INK2),
            body("同一语法，两种语义", size=28, color=SEAL),
        )
        with self.beat(2):
            self.swap(ex, hs)
        # beat 3: impedance mismatch
        mismatch = panel(
            body("阻抗失配", size=36, color=SEAL),
            serif("impedance mismatch", size=30, color=INK2),
            body("集合里分得很清的两样东西", size=28, color=INK),
            body("惰性语言里共用一个语法", size=28, color=INK),
            body("便利是真的 · 代价也是真的", size=28, color=INK2),
        )
        with self.beat(3):
            self.swap(hs, mismatch)
        # beat 4: divergence cost
        cost = panel(
            body("代价", size=32, color=INK3),
            body("展开若不终止", size=30, color=INK),
            body("依赖它的计算也会永远算下去", size=30, color=INK),
            mixed("惰性写下无穷 ≠ 保证停机", size=32, color=SEAL),
        )
        with self.beat(4):
            self.swap(mismatch, cost)
        self.end_scene()


# =====================================================================================
class S6Hylo(Base):
    SID = "S6Hylo"
    TITLE = "六 · hylo：先生而后归"

    def construct(self):
        self.head_only()
        # beat 0: ana then cata pipeline
        n_a = node("a", size=40).move_to([-4.2, 0.5, 0])
        n_f = node("Fix f", size=36).move_to([-0.3, 0.5, 0])
        n_b = node("b", size=40).move_to([3.6, 0.5, 0])
        a1 = arrow(n_a, n_f, color=SEAL, sw=3.4)
        a2 = arrow(n_f, n_b, color=TYPE_C, sw=3.4)
        l1 = mixed("ana", size=28, color=SEAL).next_to(a1, UP, buff=0.12)
        l2 = mixed("cata", size=28, color=TYPE_C).next_to(a2, UP, buff=0.12)
        motto = body("先生，而后归  ·  hylo", size=32, color=INK).move_to([-0.3, -1.6, 0])
        with self.beat(0):
            self.play(FadeIn(n_a), FadeIn(n_f), FadeIn(n_b), run_time=0.8)
            self.play(GrowArrow(a1), FadeIn(l1), run_time=0.9)
            self.play(GrowArrow(a2), FadeIn(l2), run_time=0.9)
            self.play(FadeIn(motto), run_time=0.5)
        g0 = VGroup(n_a, n_f, n_b, a1, a2, l1, l2, motto)
        # beat 1: 生而不有 — Fix fades
        mid = node("Fix f", size=40).move_to([-0.3, 0.8, 0])
        ghost = body("从未完整存在于内存", size=28, color=INK2).move_to([-0.3, -0.6, 0])
        calli = callig("生而不有", size=64).move_to([-0.3, -1.9, 0])
        with self.beat(1):
            self.play(FadeOut(g0), run_time=0.4)
            self.play(FadeIn(mid, scale=1.05), run_time=0.8)
            self.at(1, 0.35)
            self.play(mid.animate.set_opacity(0.15), FadeIn(ghost), run_time=1.2)
            self.play(FadeIn(calli, scale=0.95), run_time=0.9)
        g1 = VGroup(mid, ghost, calli)
        # beat 2: fact
        fact_box = panel(
            mixed("fact = hylo alg coa", size=34, color=TYPE_C),
            body("coa：n ↦ ConsF n (n-1) · 0 ↦ NilF", size=26, color=INK2),
            body("alg：ConsF n r ↦ n * r · NilF ↦ 1", size=26, color=INK2),
            body("生和归各是一份不递归的菜谱", size=28, color=SEAL),
        )
        with self.beat(2):
            self.swap(g1, fact_box)
        # beat 3: fusion
        fuse = panel(
            mixed("hylo alg coa  =  cata alg ∘ ana coa", size=30, color=TYPE_C),
            body("语义相同", size=28, color=INK2),
            body("但 hylo 不建中间那棵树", size=30, color=INK),
            body("融合律在代码里的样子", size=28, color=SEAL),
        )
        with self.beat(3):
            self.swap(fact_box, fuse)
        # beat 4: closing dao
        close = panel(
            mixed("定理  ⟷  对偶定理", size=36, color=TYPE_C),
            body("每证明一个，翻转箭头，白得另一个", size=28, color=INK),
            body("弱者道之用", size=30, color=SEAL),
            body("更弱的假设 · 对无穷结构发言", size=26, color=INK2),
        )
        with self.beat(4):
            self.swap(fuse, close)
        self.end_scene()


# =====================================================================================
class S7Haskell(Base):
    SID = "S7Haskell"
    TITLE = "七 · 短 Haskell"

    def construct(self):
        self.head_only()
        code_f = make_code("s_fix", size=25, line_h=0.40).place(-6.2, 2.35)
        with self.beat(0):
            self.play(code_f.write(), run_time=2.0)
            self.at(0, 0.55)
            self.play(code_f.focus(10, 12), run_time=0.7)
            tip = body("同一张方块 · 两种读法", size=26, color=SEAL).move_to([3.4, -2.6, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._g = VGroup(code_f, tip)
        code_h = make_code("s_hylo", size=26, line_h=0.44).place(-6.2, 2.0)
        code_l = make_code("s_list", size=25, line_h=0.40).place(-6.2, 2.3)
        with self.beat(1):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_h.write(), run_time=1.0)
            self.at(1, 0.35)
            self.play(FadeOut(code_h), run_time=0.35)
            self.play(code_l.write(), run_time=1.4)
            tip = mixed("fact 5 = 120", size=30, color=SEAL).move_to([3.5, -2.5, 0])
            self.at(1, 0.7)
            self.play(FadeIn(tip), run_time=0.5)
            self._g = VGroup(code_l, tip)
        code_s = make_code("s_stream", size=25, line_h=0.42).place(-6.2, 2.2)
        with self.beat(2):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_s.write(), run_time=1.6)
            self.at(2, 0.45)
            self.play(code_s.focus(4, 5), run_time=0.7)
            tip = mixed("takeS 8 nats = [0..7]", size=28, color=SEAL).move_to([3.2, -2.5, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._g = VGroup(code_s, tip)
        code_r = make_code("s_range", size=26, line_h=0.44).place(-6.2, 1.8)
        with self.beat(3):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(code_r.write(), run_time=1.4)
            tip = VGroup(
                mixed("cata sum (range (1,10)) = 55", size=28, color=TYPE_C),
                body("有限与无穷 · 同一套机关", size=26, color=SEAL),
            ).arrange(DOWN, buff=0.2).move_to([2.8, -2.0, 0])
            self.at(3, 0.55)
            self.play(FadeIn(tip), run_time=0.7)
            self._g = VGroup(code_r, tip)
        demo = VGroup(
            mixed("$ cabal run tao-category-fan-zhe", size=24, color=INK3),
            mixed("fact 5                     = 120", size=28, color=TYPE_C),
            mixed("fact 10                    = 3628800", size=28, color=TYPE_C),
            mixed("takeS 8 nats               = [0,1,2,3,4,5,6,7]", size=26, color=TYPE_C),
            mixed("cata sumL (range (1, 10))  = 55", size=28, color=TYPE_C),
            mixed("hylo sumL rangeCoa (1, 5)  = 15", size=28, color=TYPE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-0.2, 0.55, 0])
        motto = body("图怎么说，代码就怎么应", size=30, color=SEAL).move_to([-0.2, -2.4, 0])
        with self.beat(4):
            self.play(FadeOut(self._g), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in demo], lag_ratio=0.28), run_time=2.6)
            self.at(4, 0.75)
            self.play(FadeIn(motto), run_time=0.6)
        self.end_scene()


# =====================================================================================
class S8Next(TaoScene):
    SID = "S8Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.55, frac=tr.get_value(), seed=23).move_to([0, 1.45, 0]))
        glyph = callig("反", size=96).move_to([0, 1.45, 0])
        points = VGroup(
            body("余代数与同态组成范畴 CoAlg(F)", size=28),
            body("终余代数的唯一入射 = ana", size=28),
            body("μF 与 νF：Set 分家，Hask 共用 Fix", size=28),
            body("hylo 先生后归，中间不落地", size=28),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.95, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            self.play(FadeIn(glyph, scale=0.9), run_time=0.7)
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.42)
        next_title = callig("知其雄，守其雌", size=52).move_to([0, 1.15, 0])
        topics = VGroup(
            body("伴随登场", size=30, color=INK2),
            body("左伴随 ⊣ 右伴随 · 单位与余单位", size=30, color=INK2),
            body("同一条溪 · 单子与余单子", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([0, -0.45, 0])
        next_tag = body("下集预告", size=26, color=INK3).move_to([0, -2.15, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), FadeOut(glyph), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(topics), FadeIn(next_tag), run_time=1.4)
        motto = callig("反者道之动", size=68).move_to([0, 0.7, 0])
        bye = body("对偶不是修辞，而是生产力。下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(topics), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
