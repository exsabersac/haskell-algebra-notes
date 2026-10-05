-- | 第六段「无为而无不为」：单子 = 用 bind 串联效果；do 记法。
--   参考：DaoFP 第15章 Monads；CTFP 3.4 Kleisli, 3.6 Monads（入门直觉，非 Yoneda）
module Seg6Monad where

-- {{snip:s6bind}}
-- 会返回盒子的函数，用 bind 串联（摊平套叠）
half :: Int -> Maybe Int
half n | even n    = Just (n `div` 2)
       | otherwise = Nothing

-- Just 8 >>= half >>= half  =  Just 2
-- Just 7 >>= half           =  Nothing
chain :: Maybe Int
chain = Just 8 >>= half >>= half
-- {{/snip}}

-- {{snip:s6do}}
-- do 记法：看起来像一步一步，底下仍是 bind
readConfig :: Maybe String
readConfig = Just "path.txt"

openFile :: String -> Maybe String
openFile p = Just ("contents of " ++ p)

parse :: String -> Maybe Int
parse _ = Just 42

pipeline :: Maybe Int
pipeline = do
  path <- readConfig
  body <- openFile path
  parse body
-- {{/snip}}

-- 等价的 bind 链
pipelineBind :: Maybe Int
pipelineBind =
  readConfig >>= \path ->
  openFile path >>= \body ->
  parse body
