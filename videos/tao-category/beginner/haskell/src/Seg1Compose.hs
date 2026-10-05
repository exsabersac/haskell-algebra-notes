-- | 第一段「道可道」：类型是对象，函数是箭头；复合与恒等。
--   参考：DaoFP 第1章 Types and Functions；第2章 Composition；CTFP 1.1, 1.2
module Seg1Compose
  ( identity
  , compose
  , toString
  , strlen
  , shout
  ) where

-- {{snip:s1}}
-- 恒等箭头：什么也不做
identity :: a -> a
identity x = x

-- 复合：先走 f，再走 g（写作 g ∘ f）
compose :: (b -> c) -> (a -> b) -> (a -> c)
compose g f = \x -> g (f x)

toString :: Int -> String
toString = show

strlen :: String -> Int
strlen = length

-- shout = strlen ∘ toString ：Int → Int
shout :: Int -> Int
shout = compose strlen toString
-- {{/snip}}
