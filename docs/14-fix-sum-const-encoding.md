# 编码：`Free f a ≅ Fix (Sum (Const a) f)`

把 `Free` 编成 `Fix`，让 `foldFree` 和 `cata` 逐行变成同一个东西。

## 1. 类型同构

```haskell
{-# LANGUAGE DeriveFunctor #-}

data Free f a
  = Pure a
  | Free (f (Free f a))
  deriving Functor

newtype Fix g = Fix { unFix :: g (Fix g) }

newtype Const a r = Const a
  deriving Functor

data Sum f g r = InL (f r) | InR (g r)
  deriving Functor

-- G r = a + f r
type G f a = Sum (Const a) f

toFix :: Functor f => Free f a -> Fix (G f a)
toFix (Pure x) = Fix (InL (Const x))
toFix (Free t) = Fix (InR (fmap toFix t))

fromFix :: Functor f => Fix (G f a) -> Free f a
fromFix (Fix (InL (Const x))) = Pure x
fromFix (Fix (InR t))         = Free (fmap fromFix t)
```

`InL` 是生成元叶，`InR` 是一层 `f` 节点——正是 \(a + f(-)\)。

## 2. 目标代数：一对函数 ↔ 一个 `G`-代数

```haskell
onPure :: a -> b
onFree :: f b -> b

alg :: Functor f => (a -> b) -> (f b -> b) -> (G f a b -> b)
alg onPure onFree (InL (Const x)) = onPure x
alg onPure onFree (InR fb)        = onFree fb

cata :: Functor g => (g b -> b) -> Fix g -> b
cata φ (Fix gr) = φ (fmap (cata φ) gr)
```

## 3. 逐行对齐

```haskell
interpret :: Functor f => (a -> b) -> (f b -> b) -> Free f a -> b
interpret onPure onFree
  = cata (alg onPure onFree) . toFix
```

**`Pure` 行**

```text
interpret onPure onFree (Pure x)
  = cata ψ (Fix (InL (Const x)))
  = ψ (InL (Const x))
  = onPure x
```

**`Free` 行**

```text
interpret onPure onFree (Free t)
  = cata ψ (Fix (InR (fmap toFix t)))
  = ψ (InR (fmap (cata ψ . toFix) t))
  = onFree (fmap (interpret onPure onFree) t)
```

## 4. `foldFree` 是特化

```haskell
foldFree :: Functor f => (f a -> a) -> Free f a -> a
foldFree φ = interpret id φ
--         = cata (alg id φ) . toFix
```

交换图：

```text
         G (cata ψ)
  G (μG) ──────────▶ G b
    │                 │
 Fix│                 │ ψ = alg id φ
    ▼                 ▼
   μG  ──────────▶    b
         cata ψ

μG = Fix (G f a) ≅ Free f a
ψ (InL (Const x)) = x
ψ (InR fa)        = φ fa
```

**不是两套折叠，是一套 `cata`；`foldFree` 是 `toFix` 之后、且 `onPure = id` 的那次调用。**

## 5. 和裸 `Fix f` 的 `cata` 并排

```haskell
cataF :: Functor f => (f b -> b) -> Fix f -> b
cataF φ (Fix fr) = φ (fmap (cataF φ) fr)

cataG :: Functor f => (a -> b) -> (f b -> b) -> Fix (G f a) -> b
cataG onPure onFree = cata (alg onPure onFree)
```

```text
Fix f              ──cata φ──────────────▶  b
Fix (Sum (Const a) f) ──cata (alg env φ)──▶  b
         ≅
      Free f a
```

## 6. 小例子

```haskell
data ExprF r = AddF r r | NegF r deriving Functor

env :: String -> Int
env "x" = 2
env _   = 3

φ :: ExprF Int -> Int
φ (AddF u v) = u + v
φ (NegF u)   = negate u

e :: Free ExprF String
e = Free (AddF (Pure "x") (Pure "y"))

interpret env φ e == 5
```

## 7. 收束

```text
foldFree φ          =  cata (alg id φ)  ∘ toFix
interpret env φ     =  cata (alg env φ) ∘ toFix
cata φ_f  (Fix f)   =  同一万有性质，函子不含生成元支
```

交换图始终是初始代数那一张；对齐靠 **`Free f a ≅ Fix (a + f)`**。
