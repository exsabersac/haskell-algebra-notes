{-# LANGUAGE ExistentialQuantification #-}
{-# LANGUAGE RankNTypes #-}
-- | Kan 短 demo：Coyoneda≈Lan 玩具、Ran/end 的 forall 口感、Codensity vs Cont。
-- 对应：docs/Kan扩展/定义与UP.md、余密度单子.md
-- 仅 base；手写最小模型，不引入 kan-extensions 等包。
module KanDemo.Demo
  ( Coyoneda(..)
  , liftCoy
  , lowerCoy
  , Cont(..)
  , Codensity(..)
  , demo
  ) where

------------------------------------------------------------------------
-- (a) Coyoneda ≈ 左 Kan 玩具
-- Coyoneda f a = ∃b. (b → a, f b)
-- 口号：先多挂一层「任意 b→a」，再 fmap 解释 —— Lan 的「最自由延拓」口感。
-- （严格：Coyoneda f ≅ Lan_U (f∘U) 一类说法；此处只记味道。）
------------------------------------------------------------------------

data Coyoneda f a = forall b. Coyoneda (b -> a) (f b)

instance Functor (Coyoneda f) where
  fmap g (Coyoneda k fb) = Coyoneda (g . k) fb

liftCoy :: f a -> Coyoneda f a
liftCoy fa = Coyoneda id fa

-- lower 需要 f 已是 Functor：把挂着的箭头推进去
lowerCoy :: Functor f => Coyoneda f a -> f a
lowerCoy (Coyoneda k fb) = fmap k fb

------------------------------------------------------------------------
-- (b) Ran / end 的 forall 玩具
-- Set 点值：(Ran_K F)(d) = ∫_c [ D(d, Kc), F c ]
-- 离散/「点」味道 → Haskell：∀c. (d → K c) → F c
-- 取 K = F = 常值到 r（单对象），就塌成 Cont：
------------------------------------------------------------------------

-- Cont r a ≅ (a → r) → r  —— 单对象常值函子 *↦r 的余密度
newtype Cont r a = Cont { runCont :: (a -> r) -> r }

-- 用 Cont 跑一个数字：把「到答案」的 continuation 喂进去
-- （完整 end 公式见笔记；此处只用 Cont 承载 forall 口感）
runContInt :: Cont Int Int -> Int
runContInt (Cont k) = k id

------------------------------------------------------------------------
-- (c) Codensity vs Cont（对照 docs/Kan扩展/余密度单子.md）
-- Codensity g a = ∀b. (a → g b) → g b  ≅ Ran_g(g)(a) 的 end 点值
-- Cont r        = Codensity (Const r) 的味道（常值特例）
------------------------------------------------------------------------

newtype Codensity g a = Codensity
  { runCodensity :: forall b. (a -> g b) -> g b }

-- Identity 上的 Codensity：跑出来就是值本身（「解释器」喂 id）
newtype Id a = Id { runId :: a }

codensityToId :: Codensity Id a -> a
codensityToId (Codensity k) = runId (k Id)

-- Cont 嵌入「常值余密度」口感：目标固定为 r
contAsCodensityShape :: Cont r a -> (a -> r) -> r
contAsCodensityShape (Cont k) = k

------------------------------------------------------------------------
-- demo
------------------------------------------------------------------------

demo :: IO ()
demo = do
  putStrLn "=== KanDemo (docs/Kan扩展/) ==="

  -- Coyoneda：lift/lower roundtrip + fmap 在「外面」做
  let coy0 = liftCoy (Just (3 :: Int))           -- Coyoneda Maybe Int
      coy1 = fmap (* 10) coy0                    -- 还不碰 Maybe，只改箭头
      back = lowerCoy coy1                       -- Just 30
  putStrLn "Coyoneda ≈ Lan 玩具：∃b.(b→a, f b)；lift/lower"
  putStrLn $ "  lift (Just 3) |> fmap (*10) |> lower = " ++ show back
  putStrLn $ "  roundtrip lift/lower (Just 7) ok? "
    ++ show (lowerCoy (liftCoy (Just (7 :: Int))) == Just 7)

  -- Ran/end → Cont：数字结果
  let c = Cont $ \k -> k (2 + 5)                 -- 先算 7，再交给续
      n = runContInt c
  putStrLn "Ran/end 味道 → Cont r a = (a→r)→r（常值 *↦r 的余密度）"
  putStrLn $ "  runCont (Cont $ \\k -> k (2+5)) id = " ++ show n

  -- Codensity Id vs Cont
  let cd = Codensity $ \k -> k (4 :: Int)
      v  = codensityToId cd
      -- Cont：固定答案类型 Int；Codensity Id：答案类型跟着 g 走
      contN = contAsCodensityShape (Cont $ \k -> k (1 + 2 + 3 :: Int)) id
  putStrLn "Codensity g a = ∀b.(a→g b)→g b；Cont = 常值特例"
  putStrLn $ "  Codensity Id 4  →  " ++ show v
  putStrLn $ "  Cont Int (1+2+3) id = " ++ show contN
  putStrLn "  对照：整条 R 的 T^R≅R∘L；Cont_A 只对应单对象常值（见余密度单子.md）"
