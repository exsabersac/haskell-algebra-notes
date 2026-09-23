{-# LANGUAGE DeriveFunctor #-}
-- | 初始代数演示：F-代数、cata、带 Lit 的 ExprF、Lambek 风格 in/out。
-- 对应：docs/初始代数/定义.md、与不动点.md、与递归ADT.md、与自由代数和Monad.md
module InitialAlgebra.Demo
  ( ExprF(..)
  , Expr
  , lit
  , add
  , neg
  , eval
  , demo
  ) where

import Algebra.Core (Fix(..), cata)

-- | 一层形状：签名内常量叶 Lit + Add/Neg。
-- 注意：Lit 是 F 自带的常量分支，不是外部生成元 X。
-- 见 docs/初始代数/与自由代数和Monad.md、docs/Free/Fix与Free对照.md
data ExprF r
  = LitF Int
  | AddF r r
  | NegF r
  deriving (Functor, Show)

type Expr = Fix ExprF

-- | in ≈ Fix；构造器 = in ∘ 注入
lit :: Int -> Expr
lit n = Fix (LitF n)

add :: Expr -> Expr -> Expr
add x y = Fix (AddF x y)

neg :: Expr -> Expr
neg x = Fix (NegF x)

-- | 目标 F-代数：解释成 Int
evalAlg :: ExprF Int -> Int
evalAlg (LitF n)   = n
evalAlg (AddF x y) = x + y
evalAlg (NegF x)   = -x

-- | 唯一同态 cata evalAlg
eval :: Expr -> Int
eval = cata evalAlg

-- | Lambek：in = Fix，out = unFix；μF ≅ F(μF)
-- out . in = id；in . out = id（在有限树上）
roundtrip :: Expr -> Bool
roundtrip e = Fix (unFix e) `same` e
  where
    -- 结构相等：比 Show 字符串即可（演示用）
    same a b = showExpr a == showExpr b

showExpr :: Expr -> String
showExpr = cata go
  where
    go (LitF n)   = "Lit " ++ show n
    go (AddF x y) = "(" ++ x ++ " + " ++ y ++ ")"
    go (NegF x)   = "(-" ++ x ++ ")"

-- | 演示：μF 有载体（Expr），不是「没有载体」；
-- 初始代数 ≈ 无外部生成元的自由 F-代数，载体就是 μF。
demo :: IO ()
demo = do
  putStrLn "=== InitialAlgebra (docs/初始代数/) ==="
  let e = add (lit 2) (neg (lit 3))  -- 2 + (-3)
  putStrLn $ "expr      = " ++ showExpr e
  putStrLn $ "cata eval = " ++ show (eval e)   -- expect -1
  putStrLn $ "Lambek roundtrip (in∘out) ok? " ++ show (roundtrip e)
  putStrLn "note: Lit is signature-internal; carrier of μ ExprF is Expr itself."
