module Main (main) where

import FanZhe

main :: IO ()
main =
  putStrLn "== 反者道之动 · 余代数 · ana · hylo ==" >>
  putStrLn ("fact 5                    = " ++ show (fact 5)) >>
  putStrLn ("fact 10                   = " ++ show (fact 10)) >>
  putStrLn ("takeS 8 nats              = " ++ show (takeS 8 nats)) >>
  putStrLn ("cata sumL (range (1, 10)) = " ++ show (cata sumL (range (1, 10)))) >>
  putStrLn ("hylo sumL rangeCoa (1,5)  = " ++ show (hylo sumL rangeCoa (1, 5 :: Integer))) >>
  putStrLn "ok"
  where
    sumL NilF        = 0
    sumL (ConsF e r) = e + r
    rangeCoa (lo, hi)
      | lo > hi   = NilF
      | otherwise = ConsF lo (lo + 1, hi)
