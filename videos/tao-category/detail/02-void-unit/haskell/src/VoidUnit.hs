-- | 深讲第 2 集「Void 与 ()」：始对象、终对象与对偶直觉。
--   参考：DaoFP 第1章 Yin and Yang / Elements
--         CTFP 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types
module VoidUnit
  ( wu
  , you
  , sumUnit
  , prodUnit
  ) where

import Data.Void (Void, absurd)

-- {{snip:s_wu}}
-- 无：通往万物的唯一箭头（始对象的出射）
wu :: Void -> a
wu = absurd
-- {{/snip}}

-- {{snip:s_you}}
-- 有：万物归一的唯一箭头（终对象的入射）
you :: a -> ()
you = const ()
-- {{/snip}}

-- {{snip:s_sum}}
-- 无是「或者」的单位：Either Void a ≅ a
sumUnit :: Either Void a -> a
sumUnit = either absurd id
-- {{/snip}}

-- {{snip:s_prod}}
-- 有是「并且」的单位：((), a) ≅ a
prodUnit :: ((), a) -> a
prodUnit = snd
-- {{/snip}}
