import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Thumb(Scene):
    def construct(self):
        ring = enso(R=2.55, seed=23, width=0.42).move_to([-3.75, 0.05, 0])
        dao = callig("链", size=250).move_to([-3.7, 0.12, 0])
        t1 = callig("Monad 与 do", size=80).move_to([2.55, 1.85, 0])
        t2 = body("道可道 · 深讲 06", size=52, weight=BOLD).move_to([2.55, 0.35, 0])
        t3 = body("bind · 定律 · do", size=36, color=INK2).move_to([2.55, -0.85, 0])
        t4 = body("Tao × CT × Haskell", size=36, color=SEAL).move_to([2.55, -1.85, 0])
        s = seal(1.0).move_to([5.9, -3.0, 0])
        self.add(ring, dao, t1, t2, t3, t4, s)
