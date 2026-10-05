module Main (main) where

import MonadDo
import Prelude hiding (Monad, return, (>>=))

main :: IO ()
main =
  putStrLn "== Monad 与 do 记法 ==" >>
  print demoMaybe >>
  print demoList >>
  print demoDoMaybe >>
  print demoDoList >>
  print (maybeBind (Just (7 :: Int)) (\n -> Just (n * n))) >>
  print (listBind [1, 2 :: Int] (\n -> [n, n + 1])) >>
  let f = (\n -> Just (n + 1)) :: Int -> Maybe Int
      g = (\n -> Just (n * 2)) :: Int -> Maybe Int
  in print ((return (3 :: Int) >>= f) == f 3) >>
     print ((Just (3 :: Int) >>= return) == Just 3) >>
     print (((Just (3 :: Int) >>= f) >>= g)
            == (Just 3 >>= (f >=> g))) >>
     putStrLn "ok"
