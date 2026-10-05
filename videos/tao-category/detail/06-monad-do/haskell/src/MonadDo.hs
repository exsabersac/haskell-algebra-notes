-- | 深讲第 6 集「Monad 与 do 记法」：bind、鱼子、定律浅讲；Maybe / List；do。
--   参考：DaoFP 第15章 Monads；CTFP 3.4–3.6 Monads / Kleisli
--   本集用手写 class，避免与 Prelude.Monad 混谈；不引入 transformer / IO。
module MonadDo
  ( Monad(..)
  , (>=>)
  , maybeBind
  , listBind
  , demoMaybe
  , demoList
  , demoDoMaybe
  , demoDoList
  ) where

import Prelude hiding (Monad, return, (>>=), (>>))

-- {{snip:s_class}}
-- Monad：在函子之上，多「注入」与「绑定」
-- return 把纯值放进效应；>>= 把「值上的下一步」接进效应链
class Monad m where
  return :: a -> m a
  (>>=)  :: m a -> (a -> m b) -> m b
-- {{/snip}}

-- {{snip:s_fish}}
-- 鱼子 / Kleisli 复合：先跑 f，再把结果交给 g
(>=>) :: Monad m => (a -> m b) -> (b -> m c) -> (a -> m c)
f >=> g = \x -> f x >>= g
-- {{/snip}}

-- {{snip:s_maybe}}
-- Maybe：空则整条链停；有值则交给下一步
instance Monad Maybe where
  return = Just
  Nothing  >>= _ = Nothing
  Just x   >>= k = k x

maybeBind :: Maybe a -> (a -> Maybe b) -> Maybe b
maybeBind = (>>=)
-- {{/snip}}

-- {{snip:s_list}}
-- 列表： nondeterminism —— 对每个元素展开下一步，再拼平
instance Monad [] where
  return x = [x]
  xs >>= k = concatMap k xs

listBind :: [a] -> (a -> [b]) -> [b]
listBind = (>>=)
-- {{/snip}}

-- {{snip:s_demo}}
-- 演示：链式绑定；外壳形状随效应走
demoMaybe :: Maybe Int
demoMaybe = Just 20 >>= \x -> Just (x + 1) >>= \y -> Just (y * 2)  -- Just 42

demoList :: [Int]
demoList = [1, 2] >>= \x -> [x, x * 10]  -- [1,10,2,20]
-- {{/snip}}

-- {{snip:s_do}}
-- do 记法：把 >>= 写成顺序可读的人话（语法糖，语义同 bind）
demoDoMaybe :: Maybe Int
demoDoMaybe = do
  x <- Just 20
  y <- Just (x + 1)
  return (y * 2)          -- Just 42

demoDoList :: [Int]
demoDoList = do
  x <- [1, 2]
  y <- [x, x * 10]
  return y                -- [1,10,2,20]
-- {{/snip}}
