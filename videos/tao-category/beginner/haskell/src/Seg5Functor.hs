-- | 第五段「知其雄，守其雌」：函子保持形状；Maybe；Applicative 直觉。
--   参考：CTFP 1.7 Functors, 1.8；DaoFP 相关铺垫；Applicative 见 DaoFP 14 / CTFP
module Seg5Functor where

-- {{snip:s5fmap}}
-- 函子：不拆盒子，改里面的值
incrMaybe :: Maybe Int -> Maybe Int
incrMaybe = fmap (+ 1)

doubleList :: [Int] -> [Int]
doubleList = fmap (* 2)
-- {{/snip}}

-- {{snip:s5law}}
-- 函子定律（诚信条款）
-- fmap id      = id
-- fmap (g . f) = fmap g . fmap f
lawId :: [Int] -> Bool
lawId xs = fmap id xs == xs

lawComp :: [Int] -> Bool
lawComp xs = fmap ((* 2) . (+ 1)) xs == (fmap (* 2) . fmap (+ 1)) xs
-- {{/snip}}

-- {{snip:s5app}}
-- Applicative：盒子里的函数 × 盒子里的值
appEx :: Maybe Int
appEx = pure (+ 1) <*> Just 3   -- Just 4

appList :: [Int]
appList = pure (*) <*> [2, 3] <*> [10, 100]  -- [20,200,30,300]
-- {{/snip}}
