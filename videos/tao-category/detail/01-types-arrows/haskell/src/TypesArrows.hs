-- | 深讲第 1 集「类型与箭头」：对象、态射、恒等与复合。
--   参考：DaoFP 第1章 Types and Functions；第2章 Composition / Identity
--         CTFP 1.1 Category: The Essence of Composition；1.2 Types and Functions
module TypesArrows
  ( identity
  , compose
  , toString
  , strlen
  , shout
  , shoutDot
  , notBool
  ) where

-- {{snip:s_id}}
-- 恒等箭头：什么也不做（范畴的单位）
identity :: a -> a
identity x = x
-- {{/snip}}

-- {{snip:s_compose}}
-- 复合：先走 f，再走 g（写作 g ∘ f；Haskell 里是 g . f）
compose :: (b -> c) -> (a -> b) -> (a -> c)
compose g f = \x -> g (f x)
-- {{/snip}}

-- {{snip:s_sig}}
-- 类型签名声明一条箭头：从 Int 到 String
toString :: Int -> String
toString = show

strlen :: String -> Int
strlen = length
-- {{/snip}}

-- {{snip:s_shout}}
-- shout = strlen ∘ toString ：Int → Int
shout :: Int -> Int
shout = compose strlen toString

-- 与标准库 (.) 等价
shoutDot :: Int -> Int
shoutDot = strlen . toString
-- {{/snip}}

-- {{snip:s_bool}}
-- 同一对类型之间可以有多条箭头
notBool :: Bool -> Bool
notBool = not
-- {{/snip}}
