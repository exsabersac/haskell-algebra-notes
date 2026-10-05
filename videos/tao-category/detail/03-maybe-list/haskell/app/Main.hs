module Main (main) where

import Data.Void (Void)
import MaybeList
import Prelude hiding (Maybe(..))

main :: IO ()
main = do
  putStrLn "== Maybe 与 List =="
  putStrLn ("one   count: " ++ show (length (one :: [Maybe Void])))
  putStrLn ("two   count: " ++ show (length (two :: [Maybe (Maybe Void)])))
  putStrLn ("three count: " ++ show (length three))
  print (fromEitherUnit (Left () :: Either () Int))
  print (fromEitherUnit (Right 7 :: Either () Int))
  print (toEitherUnit (Nothing :: Maybe Int))
  print (toEitherUnit (Just 3 :: Maybe Int))
  let xs = Cons 1 (Cons 2 (Cons 3 Nil))
  print (sumList xs, lengthList xs)
  putStrLn "ok"
