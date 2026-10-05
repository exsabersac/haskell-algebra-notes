{-# LANGUAGE DeriveFunctor #-}
{-# LANGUAGE RankNTypes #-}
-- | 进阶深讲第 9 集「道生一」：F-代数、初始代数、兰贝克引理、Fix 与 cata、Church 编码 Mu。
--   参考：DaoFP 第7章 Recursion；第11章 Algebras
--         （Category of Algebras / Initial algebra / Lambek's Lemma and Fixed Points /
--          Catamorphisms / Initial Algebra from Universality / Initial Algebra as a Colimit）
--         CTFP 3.8 F-Algebras
--   （按 CTFP 惯例在 Hask 中忽略 ⊥；入门 03/04 已见 Maybe/List 与 fold 直觉，本集写正式）
module DaoShengYi
  ( Fix (..)
  , Algebra
  , cata
  , ExprF (..)
  , val
  , plus
  , eval
  , pretty
  , e9
  , lambekOut
  , Nat
  , zero
  , suc
  , toInt
  , Mu (..)
  , cataMu
  , toMu
  , fromMu
  , ListF (..)
  , fromList
  , sumAlg
  ) where

-- {{snip:s_fix}}
-- 不动点：构造子 Fix 即初始代数的结构映射 ι
newtype Fix f = Fix { unFix :: f (Fix f) }

-- F-代数：载体 a 与结构映射 f a -> a
type Algebra f a = f a -> a

-- 读交换方块：cata α = α ∘ F (cata α) ∘ ι⁻¹
cata :: Functor f => Algebra f a -> Fix f -> a
cata alg = alg . fmap (cata alg) . unFix
-- {{/snip}}

-- {{snip:s_expr}}
-- 形状：一层表达式，x 标出子树的洞
data ExprF x = ValF Int | PlusF x x
  deriving Functor

val :: Int -> Fix ExprF
val n = Fix (ValF n)

plus :: Fix ExprF -> Fix ExprF -> Fix ExprF
plus a b = Fix (PlusF a b)
-- {{/snip}}

-- {{snip:s_algs}}
-- 同一形状，两份代数：载体不同，菜谱不同
eval :: Algebra ExprF Int
eval (ValF n)    = n
eval (PlusF m n) = m + n

pretty :: Algebra ExprF String
pretty (ValF n)    = show n
pretty (PlusF s t) = s ++ " + " ++ t

e9 :: Fix ExprF
e9 = plus (plus (val 2) (val 3)) (val 4)
-- {{/snip}}

-- {{snip:s_lambek}}
-- 兰贝克：把 F 作用于初始代数，得代数 (F i, F ι)；
-- 唯一的同态 h 就是 ι 的逆
lambekOut :: Functor f => Fix f -> f (Fix f)
lambekOut = cata (fmap Fix)
-- 定理：lambekOut = unFix，且 Fix . lambekOut = id
-- {{/snip}}

-- {{snip:s_nat}}
-- 道生一：Maybe 的最小不动点即自然数
type Nat = Fix Maybe

zero :: Nat
zero = Fix Nothing

suc :: Nat -> Nat
suc = Fix . Just

-- Maybe 代数 = (起点, 一步)；cata 即递归子
toInt :: Nat -> Int
toInt = cata (maybe 0 (+ 1))
-- {{/snip}}

-- {{snip:s_mu}}
-- 从普遍性看初始代数：一个值 = 它全部的折法
newtype Mu f = Mu (forall a. Algebra f a -> a)

cataMu :: Algebra f a -> Mu f -> a
cataMu alg (Mu h) = h alg

toMu :: Functor f => Fix f -> Mu f
toMu t = Mu (\alg -> cata alg t)

fromMu :: Mu f -> Fix f
fromMu (Mu h) = h Fix
-- {{/snip}}

-- {{snip:s_list}}
data ListF e x = NilF | ConsF e x
  deriving Functor

fromList :: [e] -> Mu (ListF e)
fromList es = Mu (\alg -> foldr (\e r -> alg (ConsF e r)) (alg NilF) es)

sumAlg :: Algebra (ListF Int) Int
sumAlg NilF        = 0
sumAlg (ConsF e r) = e + r
-- {{/snip}}
