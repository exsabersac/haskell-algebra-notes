{-# LANGUAGE DeriveFunctor #-}
-- | 第三段「道生一，一生二，二生三，三生万物」：初始代数、不动点、兰贝克引理、cata。
--   参考：DaoFP 第7章 Recursion；第11章 Algebras（11.5 Lambek，11.8 Initial Algebra as a Colimit）；CTFP 3.8
module Seg3Fix where

import Data.Void (Void)

-- 从无开始，反复作用 Maybe：0, 1, 2, 3 个值
type One   = Maybe Void                 -- 只有 Nothing
type Two   = Maybe (Maybe Void)         -- Nothing, Just Nothing
type Three = Maybe (Maybe (Maybe Void))

one :: [One]
one = [Nothing]

two :: [Two]
two = [Nothing, Just Nothing]

three :: [Three]
three = [Nothing, Just Nothing, Just (Just Nothing)]

-- {{snip:s3a}}
newtype Fix f = Fix { unFix :: f (Fix f) }
-- 兰贝克引理：Fix 与 unFix 互逆，Fix f ≅ f (Fix f)

type Algebra f a = f a -> a

cata :: Functor f => Algebra f a -> Fix f -> a
cata alg = alg . fmap (cata alg) . unFix
-- {{/snip}}

-- {{snip:s3b}}
type Nat = Fix Maybe   -- 道生一……

zero :: Nat
zero = Fix Nothing

suc :: Nat -> Nat
suc n = Fix (Just n)

-- 唯一的归途
toInt :: Nat -> Int
toInt = cata (maybe 0 (+ 1))
-- {{/snip}}

-- {{snip:s3c}}
-- 列表：ListF 的不动点
data ListF e r = NilF | ConsF e r
  deriving Functor

type List e = Fix (ListF e)

total :: List Int -> Int
total = cata alg where
  alg NilF        = 0
  alg (ConsF e r) = e + r
-- {{/snip}}

fromList :: [e] -> List e
fromList = foldr (\e r -> Fix (ConsF e r)) (Fix NilF)
