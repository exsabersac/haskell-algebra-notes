module Main (main) where

import FunctorIntuition
import Prelude hiding (Functor, fmap)

main :: IO ()
main = do
  putStrLn "== Functor 直觉 =="
  print demoMaybe
  print demoList
  print (maybeFmap (show :: Int -> String) (Just (7 :: Int)))
  print (listFmap length ["a", "bb", "ccc"])
  -- 定律抽检（直觉层）
  print (fmap id (Just (3 :: Int)) == Just 3)
  print (fmap id ([1, 2, 3] :: [Int]) == [1, 2, 3])
  let f = (+ 1) :: Int -> Int
      g = (* 2) :: Int -> Int
  print (fmap (g . f) [1, 2] == (fmap g . fmap f) [1, 2])
  putStrLn "ok"
