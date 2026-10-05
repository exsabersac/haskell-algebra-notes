{-# LANGUAGE DeriveFunctor #-}
-- | 深讲第 3 集「Maybe 与 List」：从无生长的代数数据类型。
--   参考：DaoFP 第7章 Recursion；CTFP 1.6 Simple Algebraic Data Types
--         折叠直觉见 CTFP 3.8 / DaoFP 11（本集只点到构造，不展开 Lambek）
module MaybeList
  ( Maybe(..)
  , One, Two, Three
  , one, two, three
  , fromEitherUnit
  , toEitherUnit
  , List(..)
  , sumList
  , lengthList
  ) where

import Data.Void (Void)
import Prelude hiding (Maybe(..), maybe)

-- {{snip:s_maybe}}
-- Maybe a ≅ Either () a ≅ 1 + A
data Maybe a = Nothing | Just a
  deriving (Show, Functor)

-- 与 Either () a 互转（类型代数：Maybe = 1 + A）
fromEitherUnit :: Either () a -> Maybe a
fromEitherUnit (Left ()) = Nothing
fromEitherUnit (Right x) = Just x

toEitherUnit :: Maybe a -> Either () a
toEitherUnit Nothing  = Left ()
toEitherUnit (Just x) = Right x
-- {{/snip}}

-- {{snip:s_count}}
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

-- {{snip:s_list}}
-- 列表：空，或「头 + 另一份列表」（递归构造）
data List a = Nil | Cons a (List a)
  deriving (Show, Functor)

-- 折叠预览：只说清一步（下集再展开 fold / unfold）
sumList :: List Int -> Int
sumList Nil         = 0
sumList (Cons x xs) = x + sumList xs

lengthList :: List a -> Int
lengthList Nil         = 0
lengthList (Cons _ xs) = 1 + lengthList xs
-- {{/snip}}
