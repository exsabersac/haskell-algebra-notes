{-# LANGUAGE DeriveFunctor #-}
-- | 函子组合草图：Sum / Product / Const / Compose、ListF、NonEmptyF。
-- 对应：docs/函子组合/（常见组合、作用与组合能力、函子范畴上的代数）
module FunctorCombo.Demo
  ( ListF(..)
  , listToFix
  , listFromFix
  , NonEmptyF(..)
  , demo
  ) where

import Algebra.Core
  ( Const(..)
  , Fix(..)
  , Identity(..)
  , Product(..)
  , Sum(..)
  , cata
  )

-- | ListF e r ≅ Sum (Const ()) (Product (Const e) Identity)
-- 即 1 + e × r。μ(ListF e) ≅ [e]
data ListF e r = NilF | ConsF e r
  deriving (Functor, Show)

type List e = Fix (ListF e)

listToFix :: [e] -> List e
listToFix []     = Fix NilF
listToFix (x:xs) = Fix (ConsF x (listToFix xs))

listFromFix :: List e -> [e]
listFromFix = cata go
  where
    go NilF         = []
    go (ConsF x xs) = x : xs

-- 用积木拼出相同形状（演示用，不等同于 data ListF）
type ListFCombo e = Sum (Const ()) (Product (Const e) Identity)

comboNil :: Fix (ListFCombo e)
comboNil = Fix (InL (Const ()))

comboCons :: e -> Fix (ListFCombo e) -> Fix (ListFCombo e)
comboCons e t = Fix (InR (Product (Const e) (Identity t)))

comboToList :: Fix (ListFCombo e) -> [e]
comboToList = cata go
  where
    go (InL (Const ()))                    = []
    go (InR (Product (Const e) (Identity xs))) = e : xs

-- | NonEmptyF e r ≅ Product (Const e) (Sum (Const ()) Identity)
-- 即 e × (1 + r)。μ ≅ NonEmpty e
data NonEmptyF e r = NonEmptyF e (Maybe r)
  deriving (Functor, Show)

type NE e = Fix (NonEmptyF e)

ne :: e -> [e] -> NE e
ne h []     = Fix (NonEmptyF h Nothing)
ne h (x:xs) = Fix (NonEmptyF h (Just (ne x xs)))

neToList :: NE e -> [e]
neToList = cata go
  where
    go (NonEmptyF h Nothing)   = [h]
    go (NonEmptyF h (Just ts)) = h : ts

demo :: IO ()
demo = do
  putStrLn "=== FunctorCombo (docs/函子组合/) ==="
  let xs = [1, 2, 3] :: [Int]
      fx = listToFix xs
  putStrLn $ "ListF: cata → list  " ++ show (listFromFix fx)
  putStrLn $ "sum via cata        " ++ show (cata sumAlg fx)
  putStrLn $ "combo Sum/Product   " ++ show (comboToList (comboCons (1 :: Int) (comboCons 2 comboNil)))
  putStrLn $ "NonEmptyF           " ++ show (neToList (ne 'a' "bc"))
  putStrLn "common bricks: Sum, Product, Compose, Const with Fix/Free (see docs)."
  where
    sumAlg NilF         = 0
    sumAlg (ConsF x xs) = x + xs
