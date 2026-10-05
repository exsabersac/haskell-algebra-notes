import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Thumb(Scene):
    def construct(self):
        ring = enso(R=2.55, seed=7, width=0.42).move_to([-3.75, 0.05, 0])
        dao = callig("道", size=250).move_to([-3.7, 0.12, 0])
        t1 = callig("道可道", size=150).move_to([2.75, 1.85, 0])
        t2 = body("范畴论 × Haskell", size=62, weight=BOLD).move_to([2.75, 0.15, 0])
        t3 = mixed("Fix f ≅ f (Fix f)", size=38, color=INK2).move_to([2.75, -1.05, 0])
        t4 = body("不动点 · 伴随 · 米田引理", size=40, color=INK2).move_to([2.75, -1.95, 0])
        s = seal(1.0).move_to([5.9, -3.0, 0])
        self.add(ring, dao, t1, t2, t3, t4, s)
