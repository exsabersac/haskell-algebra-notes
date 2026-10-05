-- | 深讲第 4 集「构造与折叠」：代数直觉、cata / foldr、ana 浅提。
--   参考：DaoFP 第11章 Algebras（Catamorphisms）；第12章 Coalgebras（Anamorphisms——直觉层）
--         CTFP 3.8 F-Algebras（fold / unfold 直觉；本集不引入 Lambek / Fix）
module FoldUnfold
  ( List(..)
  , sumList
  , productList
  , lengthList
  , foldProduct
  , countdown
  , fact
  , factHylo
  ) where

import Data.List (unfoldr)

-- {{snip:s_cata}}
-- 列表：空，或「头 + 另一份列表」（构造 = 代数的引入）
data List a = Nil | Cons a (List a)
  deriving (Show)

-- 折叠（cata 直觉）：同一形状，两套代数
sumList :: List Int -> Int
sumList Nil         = 0
sumList (Cons x xs) = x + sumList xs

productList :: List Int -> Int
productList Nil         = 1
productList (Cons x xs) = x * productList xs

lengthList :: List a -> Int
lengthList Nil         = 0
lengthList (Cons _ xs) = 1 + lengthList xs
-- {{/snip}}

-- {{snip:s_foldr}}
-- 标准库 foldr：与 Cons 对齐的 cata
-- foldr step init  ≡  空→init；Cons x xs → step x (foldr … xs)
foldProduct :: [Integer] -> Integer
foldProduct = foldr (*) 1
-- {{/snip}}

-- {{snip:s_ana}}
-- 展开（ana 直觉）：种树 —— unfoldr
-- 种子 n：结出 n，留下 n-1；到 0 停止
countdown :: Integer -> [Integer]
countdown = unfoldr step
  where
    step 0 = Nothing
    step n = Just (n, n - 1)

-- 先展开再折叠：阶乘（hylo 浅提；中间列表可融掉）
fact :: Integer -> Integer
fact n = foldProduct (countdown n)

-- 合成一步的写法（先生后归，中间不落地）
factHylo :: Integer -> Integer
factHylo = go
  where
    go 0 = 1
    go n = n * go (n - 1)
-- {{/snip}}
