module Main (main) where

import FoldUnfold

main :: IO ()
main = do
  putStrLn "== 构造与折叠 =="
  let xs = Cons 1 (Cons 2 (Cons 3 Nil))
  print (sumList xs, productList xs, lengthList xs)
  print (foldProduct [5, 4, 3, 2, 1])
  print (countdown 5)
  print (fact 10, factHylo 10)
  putStrLn "ok"
