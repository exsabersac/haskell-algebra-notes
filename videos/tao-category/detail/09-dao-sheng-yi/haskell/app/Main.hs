module Main (main) where

import DaoShengYi

-- 检查 lambekOut 与 unFix 一致：两边都再折成字符串比较
agree :: Bool
agree = map (cata pretty) (kids (lambekOut e9)) == map (cata pretty) (kids (unFix e9))
  where
    kids (PlusF a b) = [a, b]
    kids (ValF _)    = []

main :: IO ()
main =
  putStrLn "== 道生一 · 初始代数 · Fix · Lambek · cata ==" >>
  putStrLn ("cata eval e9   = " ++ show (cata eval e9)) >>
  putStrLn ("cata pretty e9 = " ++ cata pretty e9) >>
  putStrLn ("lambekOut agrees with unFix: " ++ show agree) >>
  putStrLn ("cata pretty (Fix (lambekOut e9)) = " ++ cata pretty (Fix (lambekOut e9))) >>
  putStrLn ("toInt (suc (suc (suc zero))) = " ++ show (toInt (suc (suc (suc zero))))) >>
  putStrLn ("cataMu sumAlg (fromList [1..10]) = " ++ show (cataMu sumAlg (fromList [1 .. 10 :: Int]))) >>
  putStrLn ("cata eval (fromMu (toMu e9)) = " ++ show (cata eval (fromMu (toMu e9)))) >>
  putStrLn "ok"
