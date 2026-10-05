import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Thumb(Scene):
    def construct(self):
        ring = enso(R=2.55, seed=19, width=0.42).move_to([-3.75, 0.05, 0])
        dao = callig("一", size=250).move_to([-3.7, 0.12, 0])
        t1 = callig("道生一", size=88).move_to([2.55, 1.85, 0])
        t2 = body("道可道 · 进阶深讲 09", size=44, weight=BOLD).move_to([2.55, 0.35, 0])
        t3 = body("初始代数 · Fix · 兰贝克 · cata", size=32, color=INK2).move_to([2.55, -0.85, 0])
        t4 = body("Tao × CT × Haskell", size=36, color=SEAL).move_to([2.55, -1.85, 0])
        s = seal(1.0).move_to([5.9, -3.0, 0])
        self.add(ring, dao, t1, t2, t3, t4, s)
