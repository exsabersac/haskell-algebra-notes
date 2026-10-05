module Main (main) where

import TypesArrows

main :: IO ()
main = do
  putStrLn "== 类型与箭头 =="
  print (identity "道", identity (42 :: Int))
  print (shout 42, shoutDot 42)
  print (compose reverse toString (123 :: Int))
  print (notBool True, identity False)
  putStrLn "ok"
