-- | Lawvere theory 教育草图（仅 base）：
-- 运算作态射、L(2,1) 自由词、定律检查、List finitary monad、Maybe 小品、理论态射草图。
-- 对应 CTFP 3.14 / docs/Lawvere理论/（定义与骨架、幺半群理论、与finitary-monad）。
module Lawvere.Demo
  ( Gen(..)
  , Word2
  , applyWord
  , wordsUpTo
  , checkMonoidLaws
  , checkMonoidLawsReport
  , demo
  ) where

import Data.Monoid (Endo(..), Sum(..))

------------------------------------------------------------------------
-- 共用：两生成元与词解释
------------------------------------------------------------------------

-- | 两个生成元：对应「运算 2→1」的自由 monoid 字母表（CTFP / 幺半群理论.md §2）。
data Gen = A | B
  deriving (Eq, Ord, Show)

-- | 2* 的元素：词。每个词给出一个由 unit/mul 导出的二元运算原型。
type Word2 = [Gen]

-- | 在具体 monoid 上解释词：A ↦ 第一个自变量，B ↦ 第二个。
applyWord :: Monoid m => Word2 -> m -> m -> m
applyWord w x y = mconcat (map pick w)
  where
    pick A = x
    pick B = y

-- | 漂亮打印词：空词写成 ε。
prettyWord :: Word2 -> String
prettyWord [] = "ε"
prettyWord w  = concatMap show w

------------------------------------------------------------------------
-- [1] Ops as morphisms：nullary unit / binary mul 及三种模型
-- 对应：docs/Lawvere理论/幺半群理论.md §1；定义与骨架.md
------------------------------------------------------------------------

-- | 零元运算 η : 0 → 1，在模型里是挑单位元（无自变量）。
op0 :: Monoid m => m
op0 = mempty

-- | 二元运算 μ : 2 → 1，在模型里是乘法。
op2 :: Monoid m => m -> m -> m
op2 = (<>)

sectionOps :: IO ()
sectionOps = do
  putStrLn "-- [1] nullary/binary ops --"
  putStrLn "  CTFP/幺半群理论: η:0→1 (unit), μ:2→1 (mul)；模型保积 ⇒ 解释成集合上的运算。"
  putStrLn "  op0 = mempty  (nullary)；  op2 = (<>)  (binary)"
  putStrLn ""
  -- 模型 1: (Sum Int, 0, +)
  let sUnit = op0 :: Sum Int
      sMul  = op2 (Sum (2 :: Int)) (Sum (3 :: Int))
  putStrLn $ "  model (Sum,0,+):  op0 = " ++ show sUnit
    ++ " ;  op2 (Sum 2) (Sum 3) = " ++ show sMul
  -- 模型 2: ([a], [], ++)
  let lUnit = op0 :: [Char]
      lMul  = op2 "ab" "cd"
  putStrLn $ "  model ([a],[],++): op0 = " ++ show lUnit
    ++ " ;  op2 \"ab\" \"cd\" = " ++ show lMul
  -- 模型 3: Endomorphism monoid (Endo a, id, .)
  let _eUnit = op0 :: Endo Int  -- 展示 nullary 类型；打印用文字说明 id
      eMul   = op2 (Endo (+1)) (Endo (*2))  -- Endo f <> Endo g = Endo (f . g)：先 *2 再 +1
      run    = appEndo eMul (10 :: Int)
  putStrLn $ "  model (Endo Int,id,.): op0 = Endo id"
    ++ " ;  op2 (Endo (+1)) (Endo (*2)) @10 = " ++ show run
    ++ "  (Endo f <> Endo g = Endo (f . g))"
  putStrLn $ "  (op0 typed as Endo Int: " ++ show (appEndo _eUnit (99 :: Int)) ++ " = id 99)"
  putStrLn ""

------------------------------------------------------------------------
-- [2] L(2,1) free-words：枚举小长度词作 2→1 态射 stand-in
-- 对应：docs/Lawvere理论/幺半群理论.md §2
------------------------------------------------------------------------

-- | 长度恰好 n 的词（生成元 A,B）。
wordsOfLength :: Int -> [Word2]
wordsOfLength 0 = [[]]
wordsOfLength n = [ g : w | g <- [A, B], w <- wordsOfLength (n - 1) ]

-- | 长度 ≤ maxLen 的全部词（含 ε）。
wordsUpTo :: Int -> [Word2]
wordsUpTo maxLen = concatMap wordsOfLength [0 .. maxLen]

-- | 词的代数语义简述。
describeWord :: Word2 -> String
describeWord []     = "\\_ _ → unit (=η)     [nullary via ignore]"
describeWord [A]    = "\\x y → x             [projection π₁]"
describeWord [B]    = "\\x y → y             [projection π₂]"
describeWord [A, B] = "\\x y → x <> y        [mul]"
describeWord [B, A] = "\\x y → y <> x        [mul flipped]"
describeWord [A, A] = "\\x y → x <> x"
describeWord [B, B] = "\\x y → y <> y"
describeWord other  = "\\x y → mconcat (map pick " ++ show other ++ ")"

sectionWords :: IO ()
sectionWords = do
  putStrLn "-- [2] L(2,1) free-words --"
  putStrLn "  CTFP/幺半群理论: L_Mon(2,1) ≃ 两生成元自由 monoid 的元素（词）。"
  putStrLn "  下列枚举长度 ≤ 2 的词，作为「不同」态射 2→1 的 stand-in："
  let ws = wordsUpTo 2
  putStrLn $ "  count(|w|≤2) = " ++ show (length ws)
    ++ "  （ε,A,B,AA,AB,BA,BB）"
  mapM_
    (\w -> putStrLn $ "    " ++ prettyWord w
      ++ replicate (4 - length (prettyWord w)) ' '
      ++ "  ⇒  " ++ describeWord w)
    ws
  let x = Sum (2 :: Int)
      y = Sum (3 :: Int)
  putStrLn "  interpret on (Sum 2, Sum 3):"
  mapM_
    (\w -> putStrLn $ "    apply " ++ prettyWord w
      ++ " ↦ " ++ show (applyWord w x y))
    ws
  putStrLn ""

------------------------------------------------------------------------
-- [3] Laws checks：结合律 / 左右单位，带 PASS/FAIL
-- 对应：docs/Lawvere理论/模型.md（方程在模型里成立）
------------------------------------------------------------------------

-- | 在例子上检查 monoid 定律（教育用；非形式化证明）。
checkMonoidLaws :: (Eq m, Monoid m) => m -> m -> m -> Bool
checkMonoidLaws x y z =
  and
    [ (x <> y) <> z == x <> (y <> z)
    , mempty <> x == x
    , x <> mempty == x
    ]

-- | 逐条报告，返回是否全部通过。
checkMonoidLawsReport :: (Eq m, Show m, Monoid m) => String -> m -> m -> m -> IO Bool
checkMonoidLawsReport label x y z = do
  putStrLn $ "  model " ++ label ++ ":"
  let assoc = (x <> y) <> z == x <> (y <> z)
      leftU = mempty <> x == x
      rightU = x <> mempty == x
      tag b = if b then "PASS" else "FAIL"
  putStrLn $ "    associativity  (x<>y)<>z == x<>(y<>z) : " ++ tag assoc
    ++ "   [" ++ show ((x <> y) <> z) ++ " vs " ++ show (x <> (y <> z)) ++ "]"
  putStrLn $ "    left unit      mempty <> x == x       : " ++ tag leftU
    ++ "   [" ++ show (mempty <> x) ++ " vs " ++ show x ++ "]"
  putStrLn $ "    right unit     x <> mempty == x       : " ++ tag rightU
    ++ "   [" ++ show (x <> mempty) ++ " vs " ++ show x ++ "]"
  pure (assoc && leftU && rightU)

sectionLaws :: IO ()
sectionLaws = do
  putStrLn "-- [3] laws checks --"
  putStrLn "  CTFP/模型: monoid 方程 = 理论里的等式；模型必须使它们成立。"
  ok1 <- checkMonoidLawsReport "(Sum Int; 2,3,5)"
           (Sum (2 :: Int)) (Sum (3 :: Int)) (Sum (5 :: Int))
  ok2 <- checkMonoidLawsReport "([Char]; \"a\",\"b\",\"c\")"
           "a" "b" "c"
  ok3 <- do
    let f = Endo (+1) :: Endo Int
        g = Endo (*2) :: Endo Int
        h = Endo (`subtract` 3) :: Endo Int
        -- 用 @0 比较 Endo（Endo 无 Eq）
        eqEndo p q = appEndo p (0 :: Int) == appEndo q (0 :: Int)
        assoc = eqEndo ((f <> g) <> h) (f <> (g <> h))
        leftU = eqEndo (mempty <> f) f
        rightU = eqEndo (f <> mempty) f
        tag b = if b then "PASS" else "FAIL"
    putStrLn "  model (Endo Int @0; +1,*2,-3):"
    putStrLn $ "    associativity : " ++ tag assoc
    putStrLn $ "    left unit     : " ++ tag leftU
    putStrLn $ "    right unit    : " ++ tag rightU
    pure (assoc && leftU && rightU)
  putStrLn $ "  all models: " ++ if ok1 && ok2 && ok3 then "PASS" else "FAIL"
  putStrLn ""

------------------------------------------------------------------------
-- [4] Finitary monad List：return / join；词在模型上求值
-- 对应：docs/Lawvere理论/与finitary-monad.md §1–2
------------------------------------------------------------------------

sectionListMonad :: IO ()
sectionListMonad = do
  putStrLn "-- [4] finitary monad List --"
  putStrLn "  CTFP/与finitary-monad: T a = ∫^n a^n × L(n,1)；monoid ⇒ T = []。"
  putStrLn "  free⊣forgetful 直觉：return 嵌入生成元；join 展平「词的词」。"
  let ret :: a -> [a]
      ret x = [x]                 -- return = (:[])
      jn :: [[a]] -> [a]
      jn = concat                 -- join = concat
      gens = [A, B, A] :: [Gen]   -- 「项」= 生成元列表 = 自由 monoid 元素
  putStrLn $ "  return A            = " ++ show (ret A)
  putStrLn $ "  join [[A],[B,A],[]] = " ++ show (jn [[A], [B, A], []])
  putStrLn $ "  term (list of gens) = " ++ show gens
  -- 在 (Sum,+) 模型上求值：A↦2, B↦3
  let interpretSum g = case g of A -> Sum (2 :: Int); B -> Sum 3
      evaluated = foldMap interpretSum gens  -- ≡ mconcat (map interpretSum gens)
  putStrLn $ "  eval in (Sum,+): A↦2, B↦3 ; foldMap = " ++ show evaluated
    ++ "  （自由 monoid 的万有性：词 → 任意 monoid 的唯一同态）"
  -- 在列表模型上：A↦\"x\", B↦\"y\"
  let interpretList g = case g of A -> "x"; B -> "y"
  putStrLn $ "  eval in ([Char],++): A↦\"x\", B↦\"y\" ; mconcat = "
    ++ show (mconcat (map interpretList gens))
  putStrLn "  hint: EM([]) ≃ Mon ≃ Mod(L_Mon, Set)"
  putStrLn ""

------------------------------------------------------------------------
-- [5] Maybe Lawvere snack：nullary 0→1 作异常点；Maybe ≅ 1+a
-- 对应：docs/Lawvere理论/与finitary-monad.md §4 Maybe 小品
------------------------------------------------------------------------

-- | 「抛异常」：唯一的 nullary 运算解释为 Nothing（无 handler）。
raise :: Maybe a
raise = Nothing

-- | 纯值嵌入：Maybe 作为 1 + a 的 Right/Just 分支。
embed :: a -> Maybe a
embed = Just

sectionMaybe :: IO ()
sectionMaybe = do
  putStrLn "-- [5] Maybe Lawvere snack --"
  putStrLn "  CTFP/与finitary-monad §4: 单一 nullary 0→1（raise）⇒ T a ≅ a^0 + a^1 ≅ Maybe a。"
  putStrLn "  只有 raise，没有 handle：理论只加异常点，不谈捕获。"
  putStrLn $ "  raise        = " ++ show (raise :: Maybe Int) ++ "  (nullary op 0→1)"
  putStrLn $ "  embed 42     = " ++ show (embed (42 :: Int)) ++ "  (Just ≅ inl of a)"
  putStrLn $ "  1 + a shape  : Nothing | Just a   （有限 coproduct ≅ coend 两项）"
  let prog1 = raise :: Maybe String
      prog2 = embed "ok"
      prog3 = raise >> embed "unreachable"  -- >>= 传播 Nothing
  putStrLn $ "  raise                     → " ++ show prog1
  putStrLn $ "  embed \"ok\"                → " ++ show prog2
  putStrLn $ "  raise >> embed \"…\"        → " ++ show prog3
    ++ "  (无 handler，异常一直传)"
  putStrLn ""

------------------------------------------------------------------------
-- [6] Optional：理论态射草图 monoid → semigroup（忘掉单位）
-- 对应：docs/Lawvere理论/对照表.md / CTFP 理论态射直觉
------------------------------------------------------------------------

sectionTheoryMorph :: IO ()
sectionTheoryMorph = do
  putStrLn "-- [6] theory morphism sketch (Monoid → Semigroup) --"
  putStrLn "  理论态射 L_Semigroup → L_Monoid：把「只有 mul」的理论映入「mul+unit」。"
  putStrLn "  反过来，把 monoid 模型「忘掉单位」就得到 semigroup 模型（解释 mul，忽略 η）。"
  let x = Sum (2 :: Int)
      y = Sum (3 :: Int)
      mulOnly = op2 x y   -- 只用二元运算
  putStrLn $ "  forget unit: keep op2 (Sum 2) (Sum 3) = " ++ show mulOnly
    ++ " ;  op0 不再参与 semigroup 签名。"
  putStrLn "  （短：theory morphism ≃ 按签名翻译运算；模型拉回 = 预复合。）"
  putStrLn ""

------------------------------------------------------------------------
-- demo 入口
------------------------------------------------------------------------

demo :: IO ()
demo = do
  putStrLn "=== Lawvere (docs/Lawvere理论/ ; CTFP 3.14) ==="
  putStrLn "sections: [1] ops  [2] L(2,1) words  [3] laws  [4] List monad  [5] Maybe  [6] theory morph"
  putStrLn ""
  sectionOps
  sectionWords
  sectionLaws
  sectionListMonad
  sectionMaybe
  sectionTheoryMorph
