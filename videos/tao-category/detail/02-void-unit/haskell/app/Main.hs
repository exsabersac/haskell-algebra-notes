module Main (main) where

import Data.Void (Void)
import VoidUnit

main :: IO ()
main = do
  putStrLn "== Void 与 () =="
  -- you：万物归一
  print (you (42 :: Int), you "道", you True)
  -- sumUnit：丢掉不可能的 Left
  print (sumUnit (Right "ok" :: Either Void String))
  -- prodUnit：丢掉单位
  print (prodUnit ((), 7 :: Int))
  -- wu / absurd 无法从值上演示（没有 Void），仅保留类型层意义
  let _proof :: Void -> Int
      _proof = wu
  putStrLn ("absurd/wu at type: Void -> a  (unused: " ++ show (const True _proof) ++ ")")
  putStrLn "ok"
