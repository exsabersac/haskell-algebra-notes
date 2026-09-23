# `foldFree` 与 `cata` 的交换图如何对齐

对齐的关键是：**`cata` 是「任意函子初始代数」的唯一折；`foldFree` 是把这个函子特化成 \(a + f(-)\) 之后的 `cata`。** 交换图是同一种图，只是 \(F\) 换成了 \(a+f\)。

## 1. 标准的 `cata` 交换图

对任意函子 \(F\)，初始代数 \((\mu F,\mathrm{in})\)，目标代数 \((B,\varphi:FB\to B)\)：

```text
          F(cata φ)
    F(μF) ──────────▶ F B
      │                 │
  in  │                 │ φ
      ▼                 ▼
     μF  ──────────▶   B
            cata φ
```

等式：

\[
\operatorname{cata}\varphi \circ \mathrm{in} \;=\; \varphi \circ F(\operatorname{cata}\varphi)
\]

Haskell：

```haskell
cata φ (Fix fr) = φ (fmap (cata φ) fr)
-- 即 cata φ . Fix = φ . fmap (cata φ)
```

## 2. `Free f a` 是谁的初始代数

\[
\mathrm{Free}\,f\,a \;=\; \mu Y.\,(a + f\,Y)
\]

函子 \(G Y = a + f\,Y\)，则 `Pure` / `Free` 合在一起就是 \(G\) 的 \(\mathrm{in}\)：

```haskell
inG (Left x)  = Pure x
inG (Right t) = Free t

outG (Pure x) = Left x
outG (Free t) = Right t
```

## 3. \(G\)-代数长什么样

\(G\)-代数 \(\psi : a + f\,B \to B\) 等价于一对：

```haskell
onPure :: a -> B          -- 如何解释生成元
onFree :: f B -> B        -- 如何解释一层 f
-- ψ = either onPure onFree
```

```haskell
cataG :: Functor f => (a -> B) -> (f B -> B) -> Free f a -> B
cataG onPure onFree = go
  where
    go (Pure x) = onPure x
    go (Free t) = onFree (fmap go t)
```

交换图（相对 \(G\)）：

```text
                    G(cataG …)
    a + f (Free f a) ────────────▶ a + f B
            │                         │
       in_G │                         │ either onPure onFree
            ▼                         ▼
        Free f a  ────────────────▶   B
                    cataG onPure onFree
```

## 4. `foldFree` 如何嵌进这张图

```haskell
foldFree :: Functor f => (f a -> a) -> Free f a -> a
foldFree φ (Pure x) = x
foldFree φ (Free t) = φ (fmap (foldFree φ) t)
```

这里：

```text
onPure = id :: a -> a
onFree = φ  :: f a -> a

foldFree φ  =  cataG id φ  =  cata (either id φ)
```

## 5. 生成元类型与载体不同

```haskell
interpret :: Functor f => (a -> B) -> (f B -> B) -> Free f a -> B
interpret env φ = foldFree φ . fmap env
-- 或直接 cataG env φ
```

```text
fmap env :: Free f a → Free f B     -- 只改叶子
foldFree φ :: Free f B → B         -- 再按 f-代数折
```

## 6. 对照表

| | `cata φ`（对 `Fix f`） | `foldFree φ`（对 `Free f a`） |
|--|----------------------|------------------------------|
| 函子 | \(f\) | \(a + f\) |
| \(\mathrm{in}\) | 只有 `Fix`／构造器 | `Pure` + `Free` |
| 目标代数 | 只需 `f B → B` | 需要 `a → B` **和** `f B → B` |
| 常见简写 | — | 取 `a → a` 为 `id`，只露 `f a → a` |

**图的形状相同；对齐方式是「把 `Free` 看成 \(a+f\) 的 `Fix`，`foldFree` 看成该函子上的 `cata`」。**
