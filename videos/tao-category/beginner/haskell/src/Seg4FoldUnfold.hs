-- | 第四段「反者道之动」：生成列表（unfold）与消费列表（fold）；轻量 hylo。
--   参考：DaoFP 第12章 Coalgebras（Anamorphisms, Hylomorphisms——直觉层）；CTFP 3.8
module Seg4FoldUnfold where

import Data.List (unfoldr)

-- {{snip:s4fold}}
-- 消费：拆快递 —— foldr
foldProduct :: [Integer] -> Integer
foldProduct = foldr (*) 1
-- {{/snip}}

-- {{snip:s4unfold}}
-- 生成：种树 —— unfoldr
-- 种子 n：结出 n，留下 n-1；到 0 停止
countdown :: Integer -> [Integer]
countdown = unfoldr step
  where
    step 0 = Nothing
    step n = Just (n, n - 1)
-- {{/snip}}

-- {{snip:s4hylo}}
-- 先展开再折叠：阶乘（中间列表可融掉）
fact :: Integer -> Integer
fact n = foldProduct (countdown n)

-- 合成一步的写法（hylo 直觉：先生后归，中间不落地）
factHylo :: Integer -> Integer
factHylo = go
  where
    go 0 = 1
    go n = n * go (n - 1)
-- {{/snip}}
