{-# LANGUAGE DeriveFunctor #-}
-- | 进阶深讲第 10 集「反者道之动」：余代数、ana、hylo、μF/νF 与阻抗失配。
--   参考：DaoFP 第12章 Coalgebras（Anamorphisms, Infinite data structures,
--         Hylomorphisms, The impedance mismatch）；
--         DaoFP 第11章 Algebras（对偶侧）；CTFP 3.8 F-Algebras（Coalgebras）
--   （按 CTFP 惯例在 Hask 中忽略 ⊥；入门 04 浅提 ana，本集写正式对偶）
module FanZhe
  ( Fix (..)
  , Algebra
  , Coalgebra
  , cata
  , ana
  , hylo
  , ListF (..)
  , fact
  , StreamF (..)
  , nats
  , takeS
  , range
  ) where

-- {{snip:s_fix}}
-- 不动点：构造子 Fix 兼任 ι（代数侧）与 ν（余代数侧）
newtype Fix f = Fix { unFix :: f (Fix f) }

type Algebra f a = f a -> a
type Coalgebra f a = a -> f a

-- cata：砍树　alg . fmap (cata alg) . unFix
cata :: Functor f => Algebra f a -> Fix f -> a
cata alg = alg . fmap (cata alg) . unFix

-- ana：种树　把复合顺序倒过来，unFix 换成 Fix
ana :: Functor f => Coalgebra f a -> a -> Fix f
ana coa = Fix . fmap (ana coa) . coa
-- {{/snip}}

-- {{snip:s_hylo}}
-- hylo：先生，而后归。定义里没有 Fix——中间结构边生边消
hylo :: Functor f => Algebra f b -> Coalgebra f a -> a -> b
hylo alg coa = alg . fmap (hylo alg coa) . coa
-- {{/snip}}

-- {{snip:s_list}}
data ListF e x = NilF | ConsF e x
  deriving Functor

-- 先生：n, n-1, …, 1；后归：乘起来
fact :: Integer -> Integer
fact = hylo alg coa where
  coa 0 = NilF
  coa n = ConsF n (n - 1)
  alg NilF        = 1
  alg (ConsF n r) = n * r
-- {{/snip}}

-- {{snip:s_stream}}
-- 惰性：同一个 Fix 承载无限流（终余代数 νF）
data StreamF e r = StreamF e r
  deriving Functor

nats :: Fix (StreamF Integer)
nats = ana (\n -> StreamF n (n + 1)) 0

takeS :: Int -> Fix (StreamF e) -> [e]
takeS 0 _                 = []
takeS k (Fix (StreamF e r)) = e : takeS (k - 1) r
-- {{/snip}}

-- {{snip:s_range}}
-- ana 也能种有限树：从区间展开出列表
range :: (Integer, Integer) -> Fix (ListF Integer)
range = ana coa where
  coa (lo, hi)
    | lo > hi   = NilF
    | otherwise = ConsF lo (lo + 1, hi)
-- {{/snip}}
