module Main (main) where

import DaoSayable

main :: IO ()
main =
  putStrLn "== 道可道 · 对象不可道 / 箭头可道 ==" >>
  putStrLn demoSpeak >>
  print demoHear >>
  putStrLn (speak (birth 7)) >>
  print (hear (10 :: Int) (* 2)) >>
  putStrLn "ok"
