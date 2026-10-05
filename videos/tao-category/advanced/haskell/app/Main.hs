module Main (main) where

import Seg1Dao
import Seg2YouWu
import Seg3Fix
import Seg4Hylo
import Seg5Adjunction
import Seg6Yoneda

main :: IO ()
main = do
  putStrLn "== 1 道可道 =="
  putStrLn (speak (birth 1))
  print (hear (42 :: Int) (+ 1))
  putStrLn "== 2 有无相生 =="
  print (you "万物", prodUnit ((), 'a'), sumUnit (Right 'b' :: Either a Char))
  print (element 'x' ())
  putStrLn "== 3 道生一 =="
  print (length one, length two, length three)
  print (toInt (suc (suc (suc zero))))
  print (total (fromList [1 .. 10]))
  putStrLn "== 4 反者道之动 =="
  print (fact 10, fact' 10)
  print (takeS 5 nats)
  putStrLn "== 5 知其雄，守其雌 =="
  print (runState (tick >> tick >> tick) 0)
  print (rightAdjunct (leftAdjunct (\(a, s) -> a + s)) (2, 3 :: Int))
  print (extract (fmap (* 2) (St (+ 1) (20 :: Int))))
  let St g _ = duplicate (St (* 10) (1 :: Int)) in print (extract (g 7))
  let St set a = _1 ('a', True) in print (a, set 'z')
  putStrLn "== 6 无为而无不为 =="
  print (fromYoneda (fmap (+ 1) (fmap (* 2) (toYoneda [1, 2, 3 :: Int]))))
  print (redeem (hear "道"))
  print (roundTrip 'x')
