-- | 深讲第 5 集「Functor 直觉」：保形、fmap、定律；Maybe / List。
--   参考：DaoFP 第8章 Functors；CTFP 1.7 Functors / 1.8 Functoriality
--   本集用手写 class，避免与 Prelude.Functor 混谈；不引入 Bifunctor / Contravariant。
module FunctorIntuition
  ( Functor(..)
  , maybeFmap
  , listFmap
  , demoMaybe
  , demoList
  ) where

import Prelude hiding (Functor, fmap)

-- {{snip:s_class}}
-- 函子：把「值上的箭头」抬到「结构上的箭头」
-- fmap 保形：结构的外壳不动，只改里头的值
class Functor f where
  fmap :: (a -> b) -> f a -> f b
-- {{/snip}}

-- {{snip:s_maybe}}
-- Maybe：空仍空；有值则对里头的值施 f
instance Functor Maybe where
  fmap _ Nothing  = Nothing
  fmap f (Just x) = Just (f x)

-- 同一箭头，两种写法对照
maybeFmap :: (a -> b) -> Maybe a -> Maybe b
maybeFmap = fmap
-- {{/snip}}

-- {{snip:s_list}}
-- 列表：对每个元素施 f，长度与顺序不变 —— 保形
instance Functor [] where
  fmap _ []     = []
  fmap f (x:xs) = f x : fmap f xs

listFmap :: (a -> b) -> [a] -> [b]
listFmap = fmap
-- {{/snip}}

-- {{snip:s_demo}}
-- 演示：(+1) 抬到 Maybe / List；结构外壳不动
demoMaybe :: Maybe Int
demoMaybe = fmap (+ 1) (Just 41)   -- Just 42

demoList :: [Int]
demoList = fmap (* 2) [1, 2, 3]    -- [2, 4, 6]
-- {{/snip}}
