-- | Lawvere theory 教育草图（仅 base）：monoid 运算 + 定律检查；
-- 两生成元自由 monoid 的词 ≈ L_Mon(2,1) 直觉；List 作为 finitary monad 提示。
-- 对应：docs/Lawvere理论/
module Lawvere.Demo
  ( Gen(..)
  , Word2
  , applyWord
  , checkMonoidLaws
  , demo
  ) where

import Data.Monoid (Sum(..))

-- | 两个生成元：对应「运算 2→1」的自由 monoid 字母表。
data Gen = A | B
  deriving (Eq, Show)

-- | 2* 的元素：词。每个词给出一个由 unit/mul 导出的二元运算原型。
type Word2 = [Gen]

-- | 在具体 monoid 上解释词：A ↦ 第一个自变量，B ↦ 第二个。
applyWord :: Monoid m => Word2 -> m -> m -> m
applyWord w x y = mconcat (map pick w)
  where
    pick A = x
    pick B = y

-- | 若干「有趣」词（教材列举的直觉子集，非枚举全部 2*）。
sampleWords :: [Word2]
sampleWords =
  [ []           -- 忽略两边 → unit
  , [A]          -- 投影 π₁
  , [B]          -- 投影 π₂
  , [A, B]       -- mul x y
  , [B, A]       -- mul y x
  , [A, A]       -- mul x x
  , [A, A, B]    -- (x <> x) <> y
  ]

-- | 在例子上检查 monoid 定律（教育用；非形式化证明）。
checkMonoidLaws :: (Eq m, Monoid m) => m -> m -> m -> Bool
checkMonoidLaws x y z =
  and
    [ (x <> y) <> z == x <> (y <> z)   -- 结合
    , mempty <> x == x                   -- 左单位
    , x <> mempty == x                   -- 右单位
    ]

-- | List 作为 monoid 理论对应的 finitary monad：自由 monoid = 列表。
-- join = concat；return = (:[])。EM 代数 ≃ Monoid（见 docs/幺半范畴/）。
listFinitaryHint :: [String]
listFinitaryHint =
  [ "T a = [a]  ≃  ∫^n  a^n × L_Mon(n,1)  （词形状 × n-元组）"
  , "L_Mon(n,1) ≃ 自由 monoid on n  ≃  [Gen_n]"
  , "EM([]) ≃ Mon  ≃  Mod(L_Mon, Set)"
  ]

demo :: IO ()
demo = do
  putStrLn "=== Lawvere (docs/Lawvere理论/) ==="
  putStrLn "monoid ops: nullary unit = mempty; binary mul = (<>)"
  let x = Sum (2 :: Int)
      y = Sum (3 :: Int)
      z = Sum (5 :: Int)
  putStrLn $ "laws on Sum Int (2,3,5)? " ++ show (checkMonoidLaws x y z)
  putStrLn "words in free monoid on {A,B} ≈ ops 2→1 prototypes:"
  mapM_ showWord sampleWords
  putStrLn $ "apply [A,B] to (Sum 2, Sum 3) = "
    ++ show (applyWord [A, B] x y)
  putStrLn $ "apply [B,A] to (Sum 2, Sum 3) = "
    ++ show (applyWord [B, A] x y)
  putStrLn $ "apply []    to (Sum 2, Sum 3) = "
    ++ show (applyWord [] x y)
  putStrLn "finitary monad hint (List for monoids):"
  mapM_ (\s -> putStrLn $ "  " ++ s) listFinitaryHint
  where
    showWord w =
      putStrLn $ "  " ++ show w ++ "  ⇒  " ++ describe w
    describe []      = "\\_ _ → mempty"
    describe [A]     = "\\x y → x"
    describe [B]     = "\\x y → y"
    describe [A, B]  = "\\x y → x <> y"
    describe [B, A]  = "\\x y → y <> x"
    describe [A, A]  = "\\x y → x <> x"
    describe other   = "\\x y → mconcat (map pick " ++ show other ++ ")"
