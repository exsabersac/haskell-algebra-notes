-- | 进阶深讲第 8 集「有无相生」：始/终对偶、积与余积、全局元素与否定。
--   参考：DaoFP 第1章 Clean Slate（Yin and Yang / Elements）
--         CTFP 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types
--   （按 CTFP 惯例忽略 ⊥；入门深讲 02 已见 Void/()，本集加深对偶与积/余积）
module YouWu
  ( wu
  , you
  , sumUnit
  , prodUnit
  , element
  , Not
  , demoElement
  , demoNot
  ) where

import Data.Void (Void, absurd)

-- {{snip:s_wu}}
-- 无：始对象到任意 a 的唯一出射（Hom(0, a) 恰一元）
wu :: Void -> a
wu = absurd
-- {{/snip}}

-- {{snip:s_you}}
-- 有：任意 a 到终对象的唯一入射（Hom(a, 1) 恰一元）
you :: a -> ()
you = const ()
-- {{/snip}}

-- {{snip:s_units}}
-- 无是余积（和）的单位；有是积的单位——又一对付偶
sumUnit :: Either Void a -> a
sumUnit = either absurd id

prodUnit :: ((), a) -> a
prodUnit = snd
-- {{/snip}}

-- {{snip:s_probe}}
-- 有是探针：() -> a 即 a 的全局元素；通往无即否定
element :: a -> (() -> a)
element = const

type Not a = a -> Void
-- {{/snip}}

-- {{snip:s_demo}}
-- 演示：探针挑出元素；否定无法从非空类型构造
demoElement :: Int
demoElement = element (42 :: Int) ()

-- 若有 Not Bool，则对 True / False 都能交出 Void——在忽略 ⊥ 时不存在
demoNot :: Not Void
demoNot = id          -- 唯一「成立」的否定：无否定自身
-- {{/snip}}
