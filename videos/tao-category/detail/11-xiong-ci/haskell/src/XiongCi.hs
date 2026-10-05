-- | 进阶深讲第 11 集「知其雄，守其雌」：伴随 → 单子 / 余单子。
--   柯里化伴随 (−, s) ⊣ (s → −)（Haskell 里常写 (,) s ⊣ (->) s）
--   生出 State 单子（R ∘ L）与 Store 余单子（L ∘ R）；lens = Store 的余代数。
--   参考：DaoFP 第10章 Adjunctions（The Currying Adjunction; Unit and Counit）；
--         第16章 Monads and Adjunctions（The currying adjunction and the state monad）；
--         第17章 Comonads（Comonads from Adjunctions; Costate comonad; Lenses）；
--         CTFP 3.2 Adjunctions, 3.6 Monads Categorically, 3.7 Comonads
--   （按 CTFP 惯例在 Hask 中忽略 ⊥）
module XiongCi
  ( leftAdjunct
  , rightAdjunct
  , unit
  , counit
  , triangleL
  , triangleR
  , State (..)
  , join
  , tick
  , Store (..)
  , extract
  , duplicate
  , extend
  , peek
  , sum3
  , Lens
  , get
  , set
  , _1
  ) where

-- {{snip:s_adj}}
-- 柯里化伴随 L ⊣ R：L a = (a, s)，R b = s -> b
-- C(L a, b) ≅ D(a, R b)：两个方向就是 curry / uncurry
leftAdjunct :: ((a, s) -> b) -> a -> (s -> b)
leftAdjunct = curry

rightAdjunct :: (a -> (s -> b)) -> (a, s) -> b
rightAdjunct = uncurry

unit :: a -> (s -> (a, s))        -- η = φ id：State 的 return
unit = curry id

counit :: (s -> b, s) -> b        -- ε = φ⁻¹ id：求值，Store 的 extract
counit = uncurry id
-- {{/snip}}

-- 三角恒等式（不能由类型系统证明，只能逐例检验）
-- (ε L) · (L η) = id_L
triangleL :: (a, s) -> (a, s)
triangleL (a, s) = counit (unit a, s)

-- (R ε) · (η R) = id_R
triangleR :: (s -> b) -> (s -> b)
triangleR f = fmap counit (unit f)

-- {{snip:s_state}}
-- R ∘ L：State 单子。return = η，join = R ε L
newtype State s a = State { runState :: s -> (a, s) }

join :: State s (State s a) -> State s a
join mma = State (fmap (uncurry runState) (runState mma))
--                 ^ fmap = 左侧的 R   ^ uncurry runState = ε

tick :: State Int Int
tick = State (\n -> (n, n + 1))
-- {{/snip}}

instance Functor (State s) where
  fmap g (State h) = State (\s -> let (a, s') = h s in (g a, s'))

instance Applicative (State s) where
  pure a = State (unit a)
  sf <*> sa = join (fmap (\f -> fmap f sa) sf)

instance Monad (State s) where
  m >>= k = join (fmap k m)

-- {{snip:s_store}}
-- L ∘ R：Store 余单子。extract = ε，duplicate = L η R
data Store s c = St (s -> c) s

extract :: Store s c -> c
extract (St f s) = f s

duplicate :: Store s c -> Store s (Store s c)
duplicate (St f s) = St (St f) s

extend :: (Store s a -> b) -> Store s a -> Store s b
extend k = fmap k . duplicate

sum3 :: Store Int Int -> Int        -- 只看邻域的局部规则
sum3 (St f i) = f (i - 1) + f i + f (i + 1)
-- {{/snip}}

instance Functor (Store s) where
  fmap g (St f s) = St (g . f) s

peek :: s -> Store s c -> c
peek s (St f _) = f s

-- {{snip:s_lens}}
-- lens = Store 余单子的余代数：s -> Store a s
type Lens s a = s -> Store a s

get :: Lens s a -> s -> a
get l s = let St _ a = l s in a

set :: Lens s a -> s -> a -> s
set l s = let St f _ = l s in f

_1 :: Lens (a, b) a
_1 (a, b) = St (\a' -> (a', b)) a
-- {{/snip}}
