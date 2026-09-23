{-# LANGUAGE DeriveFunctor #-}
-- | Free 演示：生成元、Free≅Fix(Sum (Const a) f)、foldFree=cata、Free ((,) e)。
-- 对应：docs/Free/生成元.md、Fix与Free对照.md、foldFree与cata.md、Fix编码.md
module FreeDemo.Demo
  ( ExprF(..)
  , toFix
  , fromFix
  , demo
  ) where

import Algebra.Core
  ( Const(..)
  , Fix(..)
  , Free(..)
  , Sum(..)
  , cata
  , foldFree
  )

-- | 故意只有运算、无常量叶（与 docs/Free/Fix与Free对照.md 一致）
data ExprF r
  = AddF r r
  | NegF r
  deriving (Functor, Show)

-- G r = a + f r
type G f a = Sum (Const a) f

toFix :: Functor f => Free f a -> Fix (G f a)
toFix (Pure x) = Fix (InL (Const x))
toFix (Free t) = Fix (InR (fmap toFix t))

fromFix :: Functor f => Fix (G f a) -> Free f a
fromFix (Fix (InL (Const x))) = Pure x
fromFix (Fix (InR t))         = Free (fmap fromFix t)

-- | G-代数 ← 一对 (onPure, onFree)
alg :: (a -> b) -> (f b -> b) -> G f a b -> b
alg onPure _      (InL (Const x)) = onPure x
alg _      onFree (InR fb)        = onFree fb

-- foldFree φ = cata (alg id φ) . toFix
foldFreeViaCata :: Functor f => (f a -> a) -> Free f a -> a
foldFreeViaCata phi = cata (alg id phi) . toFix

-- ----- Free ((,) e) ≅ ([e], a) -----

-- 一层「再记一个 e」
type LogF e = (,) e

-- Free (LogF e) a ≈ 先攒 [e]，最后得到 a
toPair :: Free (LogF e) a -> ([e], a)
toPair (Pure x)      = ([], x)
toPair (Free (e, t)) =
  let (es, x) = toPair t
  in  (e : es, x)

fromPair :: ([e], a) -> Free (LogF e) a
fromPair ([], x)     = Pure x
fromPair (e : es, x) = Free (e, fromPair (es, x))

-- F-代数 (e, a) -> a：逐步更新（不必 monoid）
stepSum :: (Int, Int) -> Int
stepSum (e, acc) = acc + e

-- ----- demos -----

openExpr :: Free ExprF String
openExpr = Free (AddF (Pure "x") (Free (NegF (Pure "y"))))  -- x + (-y)

evalWith :: (String -> Int) -> Free ExprF String -> Int
evalWith env = foldFree step . fmap env
  where
    step (AddF x y) = x + y
    step (NegF x)   = -x

demo :: IO ()
demo = do
  putStrLn "=== FreeDemo (docs/Free/) ==="

  -- 生成元 + foldFree
  let env "x" = 10
      env "y" = 3
      env _   = 0
      v       = evalWith env openExpr
  putStrLn $ "open expr  ~ x + (-y)"
  putStrLn $ "evalWith   = " ++ show v   -- 10 + (-3) = 7

  -- Free ≅ Fix (Sum (Const a) f)
  let encoded = toFix openExpr
      back    = fromFix encoded
  putStrLn $ "toFix/fromFix roundtrip ok? " ++ show (showFree back == showFree openExpr)

  -- foldFree = cata for (a + f(-))
  let step :: ExprF Int -> Int
      step (AddF x y) = x + y
      step (NegF x)   = -x
      viaFold = foldFree step (fmap env openExpr)
      viaCata = foldFreeViaCata step (fmap env openExpr)
  putStrLn $ "foldFree == cata(alg id φ).toFix ? " ++ show (viaFold == viaCata)

  -- Free ≠ Fix unless a ≅ Void：这里 a = String，有外部生成元
  putStrLn "Free ExprF String ≠ Fix ExprF (generators present; a ≇ Void)"

  -- Free ((,) e) ≅ ([e], a)；对照 [] 的 EM = Monoid（见根 README §3）
  let w = Free (1 :: Int, Free (2, Free (3, Pure 100)))
      (es, seed) = toPair w
      folded     = foldFree stepSum w  -- 100+1+2+3 但从内向外：Pure 100，再 +3,+2,+1
  putStrLn $ "Free ((,) Int) Int  →  toPair = " ++ show (es, seed)
  putStrLn $ "foldFree (+e)       = " ++ show folded
  putStrLn $ "fromPair roundtrip  = " ++ show (show (toPair (fromPair (es, seed))) == show (es, seed))
  putStrLn "contrast: [] EM algebras = Monoid (same element/carrier type); not this story."

showFree :: Show a => Free ExprF a -> String
showFree (Pure x) = "Pure " ++ show x
showFree (Free (AddF l r)) = "Add(" ++ showFree l ++ "," ++ showFree r ++ ")"
showFree (Free (NegF x))   = "Neg(" ++ showFree x ++ ")"
