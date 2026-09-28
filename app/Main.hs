module Main where

import qualified FreeDemo.Demo as Free
import qualified FunctorCombo.Demo as Combo
import qualified InitialAlgebra.Demo as Init
import qualified Lawvere.Demo as Lawvere

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
  putStrLn ""
  Lawvere.demo
