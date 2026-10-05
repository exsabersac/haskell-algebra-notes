module Main (main) where

import Control.Monad (replicateM)
import XiongCi

main :: IO ()
main =
  putStrLn "== 知其雄，守其雌 · 伴随 · State · Store ==" >>
  putStrLn ("triangleL (7, 's')                 = " ++ show (triangleL (7 :: Int, 's'))) >>
  putStrLn ("triangleR (+1) 41                  = " ++ show (triangleR (+ 1) (41 :: Int))) >>
  putStrLn ("runState (replicateM 3 tick) 0     = " ++ show (runState (replicateM 3 tick) 0)) >>
  putStrLn ("map (`peek` extend sum3 sq) [0..4] = " ++ show (map (`peek` extend sum3 sq) [0 .. 4])) >>
  putStrLn ("set _1 (1, 'x') 9                  = " ++ show (set _1 (1 :: Int, 'x') 9)) >>
  putStrLn ("lens laws on _1                    = " ++ show laws) >>
  putStrLn "ok"
  where
    sq = St (\i -> i * i) 0
    p = (1 :: Int, 'x')
    laws =
      [ set _1 p (get _1 p) == p                      -- set s (get s) = s
      , get _1 (set _1 p 9) == 9                      -- get (set s a) = a
      , set _1 (set _1 p 9) 5 == set _1 p 5           -- set (set s a) a' = set s a'
      ]
