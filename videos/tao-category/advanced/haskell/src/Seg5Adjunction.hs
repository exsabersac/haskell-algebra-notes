-- | 第五段「知其雄，守其雌」：柯里化伴随 (,) s ⊣ (->) s 生出 State 单子与 Store 余单子。
--   参考：DaoFP 第10章 Adjunctions（The Currying Adjunction, unit/counit）；
--         第16章 Monads and Adjunctions（currying adjunction and the state monad）；
--         第17章 Comonads（Costate comonad, Lenses）；CTFP 3.2, 3.6, 3.7
module Seg5Adjunction where

-- {{snip:s5a}}
-- 柯里化伴随：((a, s) -> b)  ≅  (a -> (s -> b))
leftAdjunct :: ((a, s) -> b) -> a -> (s -> b)
leftAdjunct = curry

rightAdjunct :: (a -> (s -> b)) -> (a, s) -> b
rightAdjunct = uncurry

unit :: a -> (s -> (a, s))        -- η：State 的 return
unit = curry id

counit :: (s -> b, s) -> b        -- ε：Store 的 extract
counit = uncurry id
-- {{/snip}}

-- {{snip:s5b}}
-- R ∘ L：State 单子；join = R ε L
newtype State s a = State { runState :: s -> (a, s) }

join :: State s (State s a) -> State s a
join mma = State (fmap (uncurry runState) (runState mma))
-- {{/snip}}

-- {{snip:s5c}}
-- L ∘ R：Store 余单子；duplicate = L η R
data Store s c = St (s -> c) s

extract :: Store s c -> c
extract (St f s) = f s

duplicate :: Store s c -> Store s (Store s c)
duplicate (St f s) = St (St f) s
-- {{/snip}}

instance Functor (State s) where
  fmap g (State h) = State (\s -> let (a, s') = h s in (g a, s'))

instance Applicative (State s) where
  pure a = State (unit a)
  sf <*> sa = join (fmap (\f -> fmap f sa) sf)

instance Monad (State s) where
  m >>= k = join (fmap k m)

instance Functor (Store s) where
  fmap g (St f s) = St (g . f) s

-- {{snip:s5d}}
-- 合法的 lens 恰是 Store 余单子的余代数
type Lens s a = s -> Store a s

_1 :: Lens (a, b) a
_1 (a, b) = St (\a' -> (a', b)) a
-- {{/snip}}

tick :: State Int Int
tick = State (\n -> (n, n + 1))
