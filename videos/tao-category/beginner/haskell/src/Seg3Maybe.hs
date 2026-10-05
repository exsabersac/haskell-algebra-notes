{-# LANGUAGE DeriveFunctor #-}
-- | 第三段「道生一」：Maybe / 列表从无中生长；简单折叠（求和）。
--   参考：DaoFP 第7章 Recursion；CTFP 1.6；折叠直觉见 CTFP 3.8 / DaoFP 11（不引入 Lambek）
module Seg3Maybe where

import Data.Void (Void)
import Prelude hiding (Maybe(..), maybe)

-- 手写一份 Maybe，便于屏幕展示（与 Prelude 同构）
-- {{snip:s3maybe}}
data Maybe a = Nothing | Just a
  deriving (Show, Functor)

-- 从无出发：Maybe Void 只有 Nothing —— 一
-- Maybe (Maybe Void) 有两个值 —— 二
type One   = Maybe Void
type Two   = Maybe (Maybe Void)
type Three = Maybe (Maybe (Maybe Void))

one :: [One]
one = [Nothing]

two :: [Two]
two = [Nothing, Just Nothing]

three :: [Three]
three = [Nothing, Just Nothing, Just (Just Nothing)]
-- {{/snip}}

-- {{snip:s3list}}
-- 列表：空，或「头 + 另一份列表」
-- data [] a = [] | a : [a]   —— 标准库已有

-- 折叠：只说清一步，递归走完全程
sumList :: [Int] -> Int
sumList []     = 0
sumList (x:xs) = x + sumList xs
-- {{/snip}}

-- 也可用 foldr 写出同一件事
sumList' :: [Int] -> Int
sumList' = foldr (+) 0
