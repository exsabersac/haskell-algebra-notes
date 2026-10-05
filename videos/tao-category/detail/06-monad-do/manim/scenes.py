# -*- coding: utf-8 -*-
"""Manim scenes for 深讲 06 · Monad 与 do 记法."""
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
        title = callig("Monad 与 do 记法", size=68).move_to([0, 0.62, 0])
        sub = body("道可道 · 深讲 06 · Haskell", size=30, color=INK2).move_to([0, -2.15, 0])
        tag = body("bind · 定律 · do", size=26, color=SEAL).move_to([0, -2.65, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(title, scale=0.92), run_time=1.1)
            self.play(FadeIn(sub, shift=UP * 0.1), FadeIn(tag), run_time=0.7)
        ring.clear_updaters()
        left = VGroup(ring, title)
        series = VGroup(
            body("深讲 05", size=28, color=INK3),
            body("→", size=28, color=INK3),
            body("深讲 06", size=32, color=INK),
            body("入门深讲 · 收束", size=26, color=SEAL),
        ).arrange(RIGHT, buff=0.3).move_to([2.0, 1.6, 0])
        with self.beat(1):
            self.play(left.animate.scale(0.55).move_to([-4.2, 0.55, 0]),
                      FadeOut(sub), FadeOut(tag), run_time=1.1)
            self.play(FadeIn(series, shift=LEFT * 0.1), run_time=0.9)
        outline = VGroup(
            body("①  bind / 鱼子", size=32),
            body("②  三条定律", size=32),
            body("③  do 记法", size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.4, 0.1, 0])
        with self.beat(2):
            self.play(FadeOut(series), run_time=0.4)
            for row in outline:
                self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.55)
        refs = VGroup(
            body("参考：DaoFP ch.15  ·  CTFP 3.4–3.6", size=24, color=INK3),
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
            body("函子改内容 · Monad 接下一步", size=30, color=INK2),
            body("效应如何串联", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.4, 0])
        icons = VGroup(
            callig("效", size=48, color=INK),
            body("→", size=36, color=INK3),
            callig("链", size=48, color=SEAL),
        ).arrange(RIGHT, buff=0.35).move_to([-0.3, -1.4, 0])
        with self.beat(1):
            self.play(FadeIn(note), FadeIn(icons), run_time=1.5)
        q = body("效应值 + 下一步箭头，能否接成更长的链？", size=28, color=INK).move_to([-0.3, 0.8, 0])
        tip = body("能 → Monad　·　效应不拆掉，只往前走", size=28, color=INK2).move_to([-0.3, -0.3, 0])
        with self.beat(2):
            self.play(FadeOut(note), FadeOut(icons), run_time=0.4)
            self.play(FadeIn(q), run_time=1.0)
            self.at(2, 0.45)
            self.play(FadeIn(tip), run_time=0.8)
        coat = VGroup(
            body("函子是外套", size=32, color=INK),
            body("Monad 多一枚钮扣", size=28, color=INK2),
            body("解开「外套里的外套」→ 下一段旅程", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(q), FadeOut(tip), run_time=0.35)
            self.play(FadeIn(coat), run_time=1.5)
        motto = callig("绑定", size=72).move_to([-0.3, 0.4, 0])
        sub = body("一生二，二生三 —— 链长出来", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(4):
            self.play(FadeOut(coat), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S2Bind(TaoScene):
    SID = "S2Bind"
    QUOTE = ""
    TITLE = "二 · bind 与鱼子"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        # beat 0 return
        inj = VGroup(
            mixed("return", size=42, color=SEAL),
            mixed(":: a → m a", size=32, color=TYPE_C),
            body("纯值放进效应壳", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(inj), run_time=1.5)
        # beat 1 bind
        bnd = VGroup(
            mixed("(>>=)", size=40, color=SEAL),
            mixed(":: m a → (a → m b) → m b", size=28, color=TYPE_C),
            body("效应值 + 下一步 → 更长的效应", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(inj), run_time=0.35)
            self.play(FadeIn(bnd), run_time=1.4)
        # beat 2 fmap vs bind
        vs = VGroup(
            mixed("fmap  :: (a → b) → m a → m b", size=28, color=INK3),
            mixed("bind  :: m a → (a → m b) → m b", size=28, color=SEAL),
            body("纯箭头  vs  带效应的箭头", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(bnd), run_time=0.35)
            self.play(FadeIn(vs), run_time=1.4)
        # beat 3 fish
        fish = VGroup(
            mixed("(>=>)", size=42, color=SEAL),
            body("鱼子 · Kleisli 复合", size=30, color=INK2),
            mixed("f >=> g  =  \\x → f x >>= g", size=28, color=TYPE_C),
            body("先跑 f，再把结果交给 g", size=26, color=INK3),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, 0.25, 0])
        with self.beat(3):
            self.play(FadeOut(vs), run_time=0.35)
            self.play(FadeIn(fish), run_time=1.5)
        # beat 4 metaphor
        meta = VGroup(
            callig("下一步", size=52),
            body("说明书本身也可能失败", size=28, color=INK2),
            body("也可能分出多条岔路", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(fish), run_time=0.35)
            self.play(FadeIn(meta), run_time=1.4)
        # beat 5
        shape = VGroup(
            body("Monad ≠ 再写一个 map", size=32, color=INK),
            body("在效应的形状上，把计算接成链", size=28, color=INK2),
            body("形状里多了「如何继续」的记忆", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(meta), run_time=0.35)
            self.play(FadeIn(shape), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S3Laws(TaoScene):
    SID = "S3Laws"
    QUOTE = ""
    TITLE = "三 · 定律浅讲"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        three = VGroup(
            body("三条定律", size=36, color=INK),
            mixed("①  左单位", size=32, color=TYPE_C),
            mixed("②  右单位", size=32, color=TYPE_C),
            mixed("③  结合律", size=32, color=SEAL),
        ).arrange(DOWN, buff=0.28).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(three), run_time=1.5)
        leftu = VGroup(
            mixed("return a >>= f  =  f a", size=34, color=SEAL),
            body("注入不能偷偷加料", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(1):
            self.play(FadeOut(three), run_time=0.35)
            self.play(FadeIn(leftu), run_time=1.4)
        rightu = VGroup(
            mixed("m >>= return  =  m", size=36, color=SEAL),
            body("结尾不能无故拆掉或加厚外壳", size=28, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(leftu), run_time=0.35)
            self.play(FadeIn(rightu), run_time=1.4)
        assoc = VGroup(
            mixed("(m >>= f) >>= g", size=30, color=TYPE_C),
            body("=", size=28, color=INK3),
            mixed("m >>= (f >=> g)", size=30, color=SEAL),
            body("怎么加括号，结果一样", size=26, color=INK2),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(rightu), run_time=0.35)
            self.play(FadeIn(assoc), run_time=1.4)
        why = VGroup(
            body("没有定律，bind 只是同名函数", size=30, color=INK),
            body("可以乱序 · 吞步骤 · 伪造成败", size=28, color=INK2),
            body("有了定律，效应链才可组合", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(assoc), run_time=0.35)
            self.play(FadeIn(why), run_time=1.4)
        motto = callig("道生一", size=64).move_to([-0.3, 0.5, 0])
        sub = body("单位是起点 · 结合让链一直生下去", size=28, color=INK2).move_to([-0.3, -1.0, 0])
        with self.beat(5):
            self.play(FadeOut(why), run_time=0.35)
            self.play(FadeIn(motto, scale=0.95), FadeIn(sub), run_time=1.4)
        self.end_scene()


# =====================================================================================
class S4Do(TaoScene):
    SID = "S4Do"
    QUOTE = ""
    TITLE = "四 · do 记法"
    CHAPTER = ""

    def construct(self):
        self.hold(0.3)
        head = body(self.TITLE, size=30, color=INK).to_corner(UL, buff=0.45)
        self.add(head)
        self.head = head
        self.margin = VGroup()
        sugar = VGroup(
            callig("do", size=64, color=SEAL),
            body("语法糖 · 语义仍是 bind", size=30, color=INK2),
            body("顺序可读的人话写法", size=28, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(0):
            self.play(FadeIn(sugar), run_time=1.5)
        bindname = VGroup(
            mixed("x <- mx", size=36, color=TYPE_C),
            body("从效应壳取出纯值，供下一行使用", size=28, color=INK2),
            mixed("return …", size=32, color=SEAL),
            body("或另一块效应，作为最后一行", size=26, color=INK3),
        ).arrange(DOWN, buff=0.25).move_to([-0.3, 0.25, 0])
        with self.beat(1):
            self.play(FadeOut(sugar), run_time=0.35)
            self.play(FadeIn(bindname), run_time=1.4)
        nosem = VGroup(
            body("do 不引入新语义", size=34, color=INK),
            body("不会让纯函数突然有副作用", size=28, color=INK2),
            body("只是把已有实例写成人话", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(2):
            self.play(FadeOut(bindname), run_time=0.35)
            self.play(FadeIn(nosem), run_time=1.4)
        translate = VGroup(
            body("看到 do → 还原成 bind 链", size=30, color=INK),
            body("看到 bind → 也可写成 do", size=30, color=INK2),
            body("两种字体 · 同一条道", size=28, color=SEAL),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(nosem), run_time=0.35)
            self.play(FadeIn(translate), run_time=1.4)
        seq = VGroup(
            mixed(">>", size=40, color=TYPE_C),
            body("只保留效应顺序 · 丢掉纯值", size=28, color=INK2),
            body("今天点到为止", size=26, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(4):
            self.play(FadeOut(translate), run_time=0.35)
            self.play(FadeIn(seq), run_time=1.4)
        ladder = VGroup(
            callig("梯子", size=56),
            body("do 是入门的梯子，不是终点", size=28, color=INK2),
            body("变换器 · IO · 解析器 —— 仍是 return 与 bind", size=26, color=INK3),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(seq), run_time=0.35)
            self.play(FadeIn(ladder), run_time=1.4)
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
        code_c = make_code("s_class", size=24, line_h=0.40).place(-6.2, 2.0)
        code_f = make_code("s_fish", size=22, line_h=0.36).place(-6.2, -0.6)
        with self.beat(0):
            self.play(code_c.write(), run_time=1.6)
            self.play(code_f.write(), run_time=1.2)
            tip = body("注入 · 绑定 · 鱼子", size=26, color=INK2).move_to([3.4, -2.0, 0])
            self.play(FadeIn(tip), run_time=0.45)
            self._tip = tip
            self._code_c = code_c
            self._code_f = code_f
        code_m = make_code("s_maybe", size=22, line_h=0.36).place(-6.3, 2.2)
        with self.beat(1):
            self.play(FadeOut(self._code_c), FadeOut(self._code_f), FadeOut(self._tip), run_time=0.4)
            self.play(code_m.write(), run_time=1.8)
            self.play(code_m.focus(3, 6), run_time=0.7)
            note = body("失败短路 · 效应最直观的一种", size=26, color=SEAL).move_to([3.2, -2.0, 0])
            self.play(FadeIn(note), run_time=0.5)
            self._note = note
            self._code_m = code_m
        code_l = make_code("s_list", size=22, line_h=0.36).place(-6.3, 2.0)
        with self.beat(2):
            self.play(FadeOut(self._code_m), FadeOut(self._note), run_time=0.4)
            self.play(code_l.write(), run_time=1.8)
            tip2 = body("不确定计算 · 搜索所有可能", size=26, color=INK2).move_to([3.2, -1.9, 0])
            self.play(FadeIn(tip2), run_time=0.5)
            self._tip2 = tip2
            self._code_l = code_l
        demo = VGroup(
            mixed("Just 20 >>= … → Just 42", size=30, color=TYPE_C),
            mixed("[1,2] >>= … → [1,10,2,20]", size=30, color=SEAL),
            body("链往前走 · 效应形状跟着走", size=28, color=INK2),
        ).arrange(DOWN, buff=0.35).move_to([-0.3, 0.3, 0])
        with self.beat(3):
            self.play(FadeOut(self._code_l), FadeOut(self._tip2), run_time=0.4)
            self.play(FadeIn(demo), run_time=1.3)
            self._demo = demo
        code_d = make_code("s_do", size=22, line_h=0.34).place(-6.3, 2.3)
        with self.beat(4):
            self.play(FadeOut(self._demo), run_time=0.35)
            self.play(code_d.write(), run_time=1.8)
            tip3 = body("糖，熔掉还是糖", size=28, color=SEAL).move_to([3.4, -2.0, 0])
            self.play(FadeIn(tip3), run_time=0.5)
            self._tip3 = tip3
            self._code_d = code_d
        laws = VGroup(
            body("左单位 · 右单位 · 结合", size=32, color=INK),
            body("屏幕代码都能编译", size=28, color=SEAL),
            body("图对齐了，代码只是把图念出来", size=26, color=INK2),
        ).arrange(DOWN, buff=0.3).move_to([-0.3, 0.3, 0])
        with self.beat(5):
            self.play(FadeOut(self._code_d), FadeOut(self._tip3), run_time=0.35)
            self.play(FadeIn(laws), run_time=1.3)
        self.end_scene()


# =====================================================================================
class S6Next(TaoScene):
    SID = "S6Next"

    def construct(self):
        self.hold(0.3)
        tr = ValueTracker(0.001)
        ring = always_redraw(lambda: enso(R=1.9, frac=tr.get_value(), seed=23).move_to([0, 0.9, 0]))
        points = VGroup(
            body("bind 把效应接成链", size=30),
            body("鱼子是克莱斯利复合", size=30),
            body("三条定律写成契约", size=30),
            body("do 是人话写法", size=30),
        ).arrange(DOWN, buff=0.22).move_to([0, -1.55, 0])
        with self.beat(0):
            self.add(ring)
            self.play(tr.animate.set_value(1.0), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
            ring.clear_updaters()
            for p in points:
                self.play(FadeIn(p, shift=UP * 0.08), run_time=0.45)
        next_title = callig("进阶篇", size=56).move_to([0, 1.1, 0])
        topics = VGroup(
            body("不动点 · 折叠与生成", size=30, color=INK2),
            body("伴随 · 左右最优翻译", size=30, color=INK2),
            body("米田 · 箭头认识对象", size=30, color=INK2),
        ).arrange(DOWN, buff=0.22).move_to([0, -0.5, 0])
        next_tag = body("深讲收束 · 进阶开启", size=26, color=SEAL).move_to([0, -2.2, 0])
        with self.beat(1):
            self.play(FadeOut(points), FadeOut(ring), run_time=0.5)
            self.play(FadeIn(next_title, scale=0.95), FadeIn(topics), FadeIn(next_tag), run_time=1.4)
        motto = callig("道生一", size=64).move_to([0, 0.7, 0])
        bye = body("先看形状，再看映射，再看效应。进阶篇见。", size=28, color=INK2).move_to([0, -0.8, 0])
        s = seal(0.85).move_to([0, -2.2, 0])
        with self.beat(2):
            self.play(FadeOut(next_title), FadeOut(topics), FadeOut(next_tag), run_time=0.45)
            self.play(FadeIn(motto, scale=0.94), run_time=1.1)
            self.play(FadeIn(bye), FadeIn(s, scale=1.4), run_time=0.9)
        self.end_scene()
