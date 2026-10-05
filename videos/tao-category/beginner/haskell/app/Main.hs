module Main (main) where

import Seg1Compose
import Seg2YouWu
import Seg3Maybe hiding (Maybe(..), Nothing, Just)
import Seg4FoldUnfold
import Seg5Functor
import Seg6Monad

main :: IO ()
main = do
  putStrLn "== 1 道可道 =="
  print (shout 42, identity "道", compose reverse show (123 :: Int))
  putStrLn "== 2 有无相生 =="
  print (you "万物", prodUnit ((), 'a'), sumUnit (Right 'b' :: Either a Char))
  putStrLn "== 3 道生一 =="
  print (length one, length two, length three)
  print (sumList [1 .. 10], sumList' [1 .. 10])
  putStrLn "== 4 反者道之动 =="
  print (countdown 5, fact 10, factHylo 10)
  putStrLn "== 5 知其雄，守其雌 =="
  print (incrMaybe (Just 3), incrMaybe Nothing, doubleList [1, 2, 3])
  print (lawId [1, 2, 3], lawComp [1, 2, 3], appEx, appList)
  putStrLn "== 6 无为而无不为 =="
  print (chain, Just (7 :: Int) >>= half, pipeline, pipelineBind)
