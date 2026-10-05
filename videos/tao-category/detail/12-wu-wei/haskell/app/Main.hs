module Main (main) where

import WuWei

main :: IO ()
main =
  putStrLn "== 无为而无不为 · 米田 · Kan ==" >>
  putStrLn ("fromYoneda (toYoneda [1,2,3])              = " ++ show (fromYoneda (toYoneda [1, 2, 3 :: Int]))) >>
  putStrLn ("fromYoneda (fmap (+1) (fmap (*2) y))       = " ++ show (fromYoneda (fmap (+ 1) (fmap (* 2) y)))) >>
  putStrLn ("fmap ((+1) . (*2)) [1,2,3]                 = " ++ show (fmap ((+ 1) . (* 2)) [1, 2, 3 :: Int])) >>
  putStrLn ("redeem (hear 42)                           = " ++ show (redeem (hear (42 :: Int)))) >>
  putStrLn ("fromYoneda (ranToYoneda (yonedaToRan y))   = " ++ show (fromYoneda (ranToYoneda (yonedaToRan y)))) >>
  putStrLn "ok"
  where
    y = toYoneda [1, 2, 3 :: Int]
