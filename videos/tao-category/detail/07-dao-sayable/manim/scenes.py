# -*- coding: utf-8 -*-
"""Manim scenes for 进阶深讲 07 · 道可道."""
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
        ring = always_redraw(lambda: enso(R=2.15, frac=tr.get_value(), seed=23).move_to([0, 0.55, 0]))
        title = callig("道可道", size=88).move_to([0, 0.62, 0])
        sub = body("道可道 · 进阶深讲 07 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("对象不可道 · 箭头可道", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("入门 01–06", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("进阶 07", size=32, color=INK),
            body("进阶篇 · 开篇", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.3).move_to([2.0, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.55).move_to([-4.2, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  对象不可道", size=32),
            body("②  箭头可道", size=32),
            body("③  米田一句", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.1 / ch.3  ·  CTFP 1.1–1.2", size=24, color=INK3),
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
            body("钩子开门 · 论点在门后", size=30, color=INK2),
            body("对象本身说不出口", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.4, 0])
        with self.beat(1):
            self.play(FadeIn(note), run_time=1.5)
        q1 = serif("“The type that can be described", size=34, color=INK)
        q1b = serif("is not the eternal type.”", size=34, color=INK)
        q2 = body("能被描述的类型，不是恒常的类型。", size=30, color=INK2)
        q3 = body("—— DaoFP 第 1 章", size=24, color=INK3)
        quote = VGroup(q1, q1b, q2, q3).arrange(DOWN, buff=0.22).move_to([-0.3, 0.2, 0])
        with self.beat(2):
            self.play(FadeOut(note), run_time=0.35)
            self.play(FadeIn(q1), FadeIn(q1b), run_time=1.0)
            self.play(FadeIn(q2), FadeIn(q3), run_time=0.9)
        axioms = VGroup(
            body("公理里写得进的只有", size=28, color=INK3),
            body("对象 · 箭头 · 复合 · 恒等", size=34, color=INK),
            body("没有「打开对象看内部」", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(quote), run_time=0.35)
            self.play(FadeIn(axioms), run_time=1.5)
        roadmap = VGroup(
            body("① 不可道 → ② 可道 → ③ Haskell → ④ 米田一句", size=28, color=INK2),
            callig("慢", size=56, color=INK),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(axioms), run_time=0.35)
            self.play(FadeIn(roadmap), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S2Object(TaoScene):
    SID = "S2Object"
    QUOTE = ""
    TITLE = "二 · 对象不可道"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        thesis = VGroup(
            body("论点", size=26, color=INK3),
            body("对象不可言说", size=44, color=INK),
            body("元素这个词，不在范畴的词典里", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.4, 0])
        with self.beat(0):
            self.play(FadeIn(thesis), run_time=1.5)
        blob = ink_blob(0.72, seed=11).move_to([-0.3, 0.35, 0])
        la = mixed("a", size=32, color=INK2).next_to(blob, DOWN, buff=0.35)
        notes = VGroup(
            body("没有部分", size=30, color=INK2),
            body("不是袋子 · 不能枚举", size=28, color=INK3),
        ).arrange(DOWN, buff=0.25).next_to(blob, RIGHT, buff=1.8)
        with self.beat(1):
            self.play(FadeOut(thesis), run_time=0.4)
            self.play(FadeIn(blob, scale=0.6), FadeIn(la), run_time=1.5)
            self.at(1, 0.4)
            self.play(FadeIn(notes), run_time=0.9)
        probe = VGroup(
            callig("探测", size=64),
            body("不靠打开 · 靠箭头", size=30, color=INK2),
            body("空是把内部让出来", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(blob), FadeOut(la), FadeOut(notes), run_time=0.4)
            self.play(FadeIn(probe), run_time=1.4)
        abs_t = VGroup(
            body("抽象类型 · 不导出构造子", size=32, color=INK),
            body("模块外看不见内部", size=28, color=INK2),
            body("了解只来自参数 / 结果上的函数", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(probe), run_time=0.35)
            self.play(FadeIn(abs_t), run_time=1.4)
        rel = VGroup(
            body("可说之词不在「里面」", size=32, color=INK),
            body("而在与别的对象之间的关系上", size=30, color=INK2),
            body("对象存在 · 对象沉默", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(abs_t), run_time=0.35)
            self.play(FadeIn(rel), run_time=1.4)
        handoff = VGroup(
            body("下一节", size=28, color=INK3),
            callig("箭头", size=72, color=INK),
            body("话筒交给可道者", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(rel), run_time=0.35)
            self.play(FadeIn(handoff), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S3Arrow(TaoScene):
    SID = "S3Arrow"
    QUOTE = ""
    TITLE = "三 · 箭头可道"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        blob = ink_blob(0.58, seed=11).move_to([-0.3, 0.35, 0])
        la = mixed("a", size=28, color=INK2).next_to(blob, DOWN, buff=0.3)
        with self.beat(0):
            self.play(FadeIn(blob, scale=0.7), FadeIn(la), run_time=1.0)
            ins, outs = radiating(blob, r_in=2.0, r_out=2.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.22), run_time=1.4)
            self.at(0, 0.35)
            self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.22), run_time=1.4)
            cap = body("结构由箭头探测出来", size=28, color=INK2).move_to([-0.3, -2.4, 0])
            self.play(FadeIn(cap), run_time=0.6)
            self._diag = VGroup(blob, la, ins, outs, cap)
        motto = VGroup(
            serif("At the arrows look!", size=40, color=INK),
            body("先别盯着对象，盯着箭头看", size=30, color=INK2),
            body("—— DaoFP ch.3", size=24, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(self._diag), run_time=0.4)
            self.play(FadeIn(motto), run_time=1.5)
        say = VGroup(
            mixed("a → x", size=42, color=SEAL),
            body("一种说法：在 x 的语境里如何使用 a", size=28, color=INK2),
            body("换 x · 多一种说法 · 说法可复合", size=28, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(motto), run_time=0.35)
            self.play(FadeIn(say), run_time=1.4)
        speak_t = VGroup(
            mixed("Speak a = ∀x. (a → x) → x", size=32, color=TYPE_C),
            body("从 a 出发的全部可道", size=30, color=INK2),
            body("续体风格 · 说法的收集器", size=28, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(say), run_time=0.35)
            self.play(FadeIn(speak_t), run_time=1.4)
        couplet = callig("可道者箭头也　不可道者对象也", size=40).move_to([-0.3, 0.5, 0])
        sub = body("对象沉默 · 箭头替它说话", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(4):
            self.play(FadeOut(speak_t), run_time=0.35)
            self.play(FadeIn(couplet, scale=0.95), FadeIn(sub), run_time=1.4)
        a = ink_blob(0.4, seed=5).move_to([-2.5, 0.4, 0])
        b = ink_blob(0.4, seed=9).move_to([1.8, 0.4, 0])
        iso = mixed("≅ ?", size=56).move_to([-0.35, 0.4, 0])
        lab_a = mixed("a", size=28, color=INK2).next_to(a, DOWN, buff=0.4)
        lab_b = mixed("b", size=28, color=INK2).next_to(b, DOWN, buff=0.4)
        hole = body("漏洞：凭什么断定两个对象相同？", size=28, color=SEAL).move_to([-0.35, -1.7, 0])
        with self.beat(5):
            self.play(FadeOut(couplet), FadeOut(sub), run_time=0.35)
            self.play(FadeIn(a, scale=0.7), FadeIn(b, scale=0.7), FadeIn(lab_a), FadeIn(lab_b), run_time=1.0)
            self.play(Write(iso), run_time=0.7)
            self.at(5, 0.55)
            self.play(FadeIn(hole), run_time=0.7)
        self.end_scene()


# =====================================================================================
class S4Yoneda(TaoScene):
    SID = "S4Yoneda"
    QUOTE = ""
    TITLE = "四 · 自然性铺垫 / 米田一句"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=28, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        ans = VGroup(
            body("相同不靠打开", size=34, color=INK),
            body("靠发出的箭头「一样」", size=32, color=SEAL),
            body("同构活在箭头层面", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(ans), run_time=1.5)
        nat = VGroup(
            callig("自然性", size=56),
            body("说法对齐的纪律", size=30, color=INK2),
            body("对齐的不只是点 · 还有路上每一步", size=28, color=INK3),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(ans), run_time=0.35)
            self.play(FadeIn(nat), run_time=1.5)
        yon = VGroup(
            body("米田一句", size=28, color=INK3),
            body("对象被它出发的所有箭头完全刻画", size=30, color=INK),
            mixed("a  ≃  Hom(a, −)", size=34, color=TYPE_C),
            body("全部说法可道 · 而且恰好够用", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, 0.25, 0])
        with self.beat(2):
            self.play(FadeOut(nat), run_time=0.35)
            self.play(FadeIn(yon), run_time=1.5)
        nail = VGroup(
            body("今天只钉钉子 · 不写证明", size=30, color=INK),
            body("可道在箭头 · 同构在说法对齐", size=28, color=INK2),
            body("米田 = 后面赎回这句话的钥匙", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(yon), run_time=0.35)
            self.play(FadeIn(nail), run_time=1.4)
        square = VGroup(
            body("自然变换方块", size=32, color=INK),
            body("入门篇已见过 · 进阶篇会一次次回来", size=28, color=INK2),
            body("方块 = 自然性的图示", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(nail), run_time=0.35)
            self.play(FadeIn(square), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S5Haskell(TaoScene):
    SID = "S5Haskell"
    QUOTE = ""
    TITLE = "五 · 短 Haskell"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        code_d = make_code("s_dao", size=24, line_h=0.40).place(-6.2, 2.1)
        with self.beat(0):
            self.play(code_d.write(), run_time=1.8)
            tip = body("构造子不导出 · 内部不可见", size=26, color=SEAL).move_to([3.2, -2.0, 0])
            self.play(FadeIn(tip), run_time=0.5)
            self._code_d = code_d
            self._tip = tip
        with self.beat(1):
            self.play(self._code_d.focus(3, 7), run_time=0.8)
            tip2 = body("birth 射入 · speak 射出", size=26, color=INK2).move_to([3.2, -2.0, 0])
            self.play(FadeOut(self._tip), FadeIn(tip2), run_time=0.5)
            self._tip2 = tip2
        code_s = make_code("s_speak", size=26, line_h=0.42).place(-6.0, 1.2)
        with self.beat(2):
            self.play(FadeOut(self._code_d), FadeOut(self._tip2),
                      FadeOut(self._code_d.hl) if self._code_d.hl else Wait(0.01), run_time=0.4)
            self.play(code_s.write(), run_time=1.4)
            tip3 = body("一切说法的收集器", size=26, color=TYPE_C).move_to([3.4, -1.5, 0])
            self.play(FadeIn(tip3), run_time=0.5)
            self._code_s = code_s
            self._tip3 = tip3
        code_h = make_code("s_hear", size=26, line_h=0.42).place(-6.0, 1.4)
        with self.beat(3):
            self.play(FadeOut(self._code_s), FadeOut(self._tip3), run_time=0.4)
            self.play(code_h.write(), run_time=1.4)
            tip4 = body("米田侧的最小种子", size=26, color=SEAL).move_to([3.4, -1.5, 0])
            self.play(FadeIn(tip4), run_time=0.5)
            self._code_h = code_h
            self._tip4 = tip4
        demo = VGroup(
            mixed('speak (birth 42)  →  "道42"', size=30, color=TYPE_C),
            mixed("hear 42 (+1)      →  43", size=30, color=SEAL),
            body("不可道在边界 · 可道在签名", size=28, color=INK2),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(self._code_h), FadeOut(self._tip4), run_time=0.35)
            self.play(FadeIn(demo), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S6Next(TaoScene):
    SID = "S6Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=23).move_to([0, 0.9, 0]))
        points = VGroup(
            body("对象不可道", size=30),
            body("箭头可道", size=30),
            body("米田一句：箭头认识对象", size=30),
        ).arrange(DOWN, buff=0.25).move_to([0, -1.45, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.5)
        next_title = callig("有无相生", size=56).move_to([0, 1.1, 0])
        topics = VGroup(
            body("始对象 · Void · 无", size=30, color=INK2),
            body("终对象 · () · 有", size=30, color=INK2),
            body("对偶第一次正式上场", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.22).move_to([0, -0.5, 0])
        next_tag = body("下集预告", size=26, color=INK3).move_to([0, -2.2, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(topics), FadeIn(next_tag), run_time=1.4)
        motto = callig("道可道", size=72).move_to([0, 0.7, 0])
        bye = body("先别打开对象，先看箭头。下集见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(topics), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
