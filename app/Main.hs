module Main where

import qualified FreeDemo.Demo as Free
import qualified FunctorCombo.Demo as Combo
import qualified InitialAlgebra.Demo as Init

main :: IO ()
main = do
  putStrLn "haskell-algebra-notes demos"
  putStrLn "(base only; hand-rolled Fix / Free / cata / foldFree)"
  putStrLn ""
  Init.demo
  putStrLn ""
  Free.demo
  putStrLn ""
  Combo.demo
