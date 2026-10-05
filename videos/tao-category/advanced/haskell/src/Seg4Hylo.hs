-- | 第四段「反者道之动」：代数/余代数、cata/ana、hylo。
--   参考：DaoFP 第12章 Coalgebras（Anamorphisms, Hylomorphisms, impedance mismatch）；CTFP 3.8
module Seg4Hylo where

import Seg3Fix (Fix (..), Algebra, ListF (..), cata)

-- {{snip:s4a}}
type Coalgebra f a = a -> f a

-- cata alg = alg . fmap (cata alg) . unFix
ana :: Functor f => Coalgebra f a -> a -> Fix f
ana coa = Fix . fmap (ana coa) . coa
-- {{/snip}}

-- {{snip:s4b}}
hylo :: Functor f => Algebra f b -> Coalgebra f a -> a -> b
hylo alg coa = alg . fmap (hylo alg coa) . coa

-- 先生：n, n-1, …, 1；后归：乘起来
fact :: Integer -> Integer
fact = hylo alg coa where
  coa 0 = NilF
  coa n = ConsF n (n - 1)
  alg NilF        = 1
  alg (ConsF n r) = n * r
-- {{/snip}}

-- | hylo = cata . ana（但 hylo 从不建出中间的 Fix）
fact' :: Integer -> Integer
fact' = cata alg . ana coa where
  coa 0 = NilF
  coa n = ConsF n (n - 1)
  alg NilF        = 1
  alg (ConsF n r) = n * r

-- | 惰性：同一个 Fix 也承载无限流（终余代数）
data StreamF e r = StreamF e r

instance Functor (StreamF e) where
  fmap f (StreamF e r) = StreamF e (f r)

nats :: Fix (StreamF Integer)
nats = ana (\n -> StreamF n (n + 1)) 0

takeS :: Int -> Fix (StreamF e) -> [e]
takeS 0 _ = []
takeS k (Fix (StreamF e r)) = e : takeS (k - 1) r
