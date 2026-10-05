-- | 第二段「有无相生」：始对象 Void 与终对象 ()。
--   参考：DaoFP 第1章 "Yin and Yang"；CTFP 1.5, 1.6
module Seg2YouWu where

import Data.Void (Void, absurd)

-- {{snip:s2wu}}
-- 无：通往万物的唯一箭头
wu :: Void -> a
wu = absurd
-- {{/snip}}

-- {{snip:s2you}}
-- 有：万物归一的唯一箭头
you :: a -> ()
you = const ()
-- {{/snip}}

-- {{snip:s2b}}
-- 无是「或者」的单位
sumUnit :: Either Void a -> a
sumUnit = either absurd id

-- 有是「并且」的单位
prodUnit :: ((), a) -> a
prodUnit = snd
-- {{/snip}}
