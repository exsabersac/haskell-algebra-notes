module Main (main) where

import YouWu
import Data.Void (Void)

main :: IO ()
main =
  putStrLn "== 有无相生 · 始/终对偶 · 积与余积 ==" >>
  print demoElement >>
  putStrLn ("prodUnit ((), \"道\") = " ++ prodUnit ((), "道")) >>
  putStrLn ("sumUnit (Right 7) = " ++ show (sumUnit (Right 7 :: Either Void Int))) >>
  putStrLn ("demoNot is id on Void") >>
  putStrLn "ok"
