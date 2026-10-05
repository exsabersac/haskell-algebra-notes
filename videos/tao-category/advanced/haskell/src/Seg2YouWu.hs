-- | 第二段「有无相生」：始对象 Void 与终对象 ()。
--   参考：DaoFP 第1章 "Yin and Yang"、"Elements"；CTFP 1.5, 1.6
--   （按 CTFP 惯例忽略 ⊥）
module Seg2YouWu where

import Data.Void (Void, absurd)

-- 无：通往万物的唯一箭头
-- {{snip:s2wu}}
wu :: Void -> a
wu = absurd
-- {{/snip}}

-- 有：万物归一的唯一箭头
-- {{snip:s2you}}
you :: a -> ()
you = const ()
-- {{/snip}}

-- {{snip:s2b}}
-- 无是和的单位
sumUnit :: Either Void a -> a
sumUnit = either absurd id

-- 有是积的单位
prodUnit :: ((), a) -> a
prodUnit = snd
-- {{/snip}}

-- {{snip:s2c}}
-- 有是探针：() -> a 即元素
element :: a -> (() -> a)
element = const

-- 通往无的箭头即否定
type Not a = a -> Void
-- {{/snip}}
