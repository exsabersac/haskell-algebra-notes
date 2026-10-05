import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Thumb(Scene):
    def construct(self):
        ring = enso(R=2.55, seed=7, width=0.42).move_to([-3.75, 0.05, 0])
        dao = callig("道", size=250).move_to([-3.7, 0.12, 0])
        t1 = callig("类型与箭头", size=120).move_to([2.55, 1.85, 0])
        t2 = body("道可道 · 深讲 01", size=52, weight=BOLD).move_to([2.55, 0.35, 0])
        t3 = body("对象 · 态射 · 复合 · 恒等", size=38, color=INK2).move_to([2.55, -0.85, 0])
        t4 = body("Tao × CT × Haskell", size=36, color=SEAL).move_to([2.55, -1.85, 0])
        s = seal(1.0).move_to([5.9, -3.0, 0])
        self.add(ring, dao, t1, t2, t3, t4, s)
