# 副作用小品：Maybe 的 Lawvere 理论

CTFP 3.14「Lawvere Theory of Side Effects」：用**单一 nullary 运算**描述「可抛异常、不可捕获」的副作用，对应 `Maybe` monad。  
术语：nullary operation、raise、coend、\(a^0+a^1\)。

相关：[与finitary-monad](与finitary-monad.md)（coend 公式）· [对照表](对照表.md) · Demo `[5]`
更细的原文顺序见 [CTFP原文细讲](CTFP原文细讲.md)。

---

## 1. 理论：只加一个 \(0\to 1\)

在平凡骨干 \(\mathbf{F}^{\mathrm{op}}\) 上增加**一个**有趣态射

\[
\mathrm{raise} : 0 \to 1
\]

没有 handler、没有 catch——理论只引入「异常点」，不谈恢复。

模型 \(M\)：载体 \(a=M(1)\)，把 `raise` 解释成函数 \(1\to a\)，即在 \(a\) 里挑出一个特殊元素（「异常值」的占位）。更准确地说，经 coend 得到的 monad 把「无值 / 有值」分成两支（下一节）。

```haskell
-- Demo [5]
raise :: Maybe a
raise = Nothing          -- nullary op 0→1 的解释

embed :: a -> Maybe a
embed = Just             -- 纯值嵌入（≅ a¹ 支）
```

---

## 2. 从 coend 得到 \(T a \cong a^0 + a^1\)

套用

\[
T_{\mathbf{L}} a \;=\; \int^{n} a^n \times \mathbf{L}(n,1)
\]

加了 `raise` 之后，\(\mathbf{L}(n,1)\) 比 \(\mathbf{F}^{\mathrm{op}}\) 多出一批态射：它们来自复合

\[
n \to 0 \to 1
\]

（先走 \(\mathbf{F}\) 里存在的 \(n\to 0\) 的对偶，再接 `raise`）。  
这些贡献在 coend 里与 \(a^0\times\mathbf{L}(0,1)\) 等同（对 \(f:0\to n\) 走两条 cowedge 路径）。

还剩下与「普通恒等 / 投影骨干」对应的 \(a^1\) 项。于是

\[
T_{\mathbf{L}} a \;\cong\; a^0 + a^1
\]

Haskell：

```haskell
-- a^0 ≅ ()    ；  a^1 ≅ a
-- Either () a  ≅  Maybe a
data Maybe a = Nothing | Just a
-- Nothing ≅ Left ()     （来自 raise / a^0 支）
-- Just x  ≅ Right x     （来自 a^1 支）
```

| coend 项 | 含义 | `Maybe` |
|----------|------|---------|
| \(a^0\times\mathbf{L}(0,1)\) | 无槽位 + raise | `Nothing` |
| \(a^1\times\mathbf{L}(1,1)\) | 单槽 + id | `Just a` |
| 更高 \(n\) 的「纯 raise 复合」 | 被 cowedge 吸进 \(a^0\) 项 | 不另增构造子 |

---

## 3. Demo：只有 raise，没有 handle

```text
cabal run algebra-demos
-- [5] Maybe Lawvere snack --
  raise        = Nothing
  embed 42     = Just 42
  raise >> embed "…"  → Nothing   （无 handler，异常一直传）
```

```haskell
prog1 = raise :: Maybe String
prog2 = embed "ok"
prog3 = raise >> embed "unreachable"  -- >>= 传播 Nothing
```

| 有 | 无 |
|----|-----|
| 抛出（nullary → `Nothing`） | `catch` / `handle` / 恢复续算 |
| `>>=` 传播失败 | 把 `Nothing` 变回有值的理论运算 |

若要「可处理的异常」，需要更丰富的理论（或换代数效应叙事）；本小品刻意停在 Maybe 的 raise-only 片段。

---

## 4. 与列表对照

| | \(L_{\mathrm{Mon}}\) → `[]` | raise-only → `Maybe` |
|--|----------------------------|----------------------|
| 有趣运算 | \(\eta:0\to1\)、\(\mu:2\to1\) 及全部词 | 仅 \(\mathrm{raise}:0\to1\) |
| \(T a\) | \(\int^n a^n\times L(n,1)\cong[a]\) | \(a^0+a^1\cong\mathrm{Maybe}\,a\) |
| EM / Mod | \(\simeq\mathbf{Mon}\) | 代数 = 带一点「可选失败」的求值结构 |
| Demo | `[1]`–`[4]` | `[5]` |

二者都是 finitary，故都落在 Lawvere ↔ monad 互译内；`Cont` 则否（见 [与finitary-monad](与finitary-monad.md) §4）。

---

## 一句话

单一 nullary \(0\to1\)（raise）的 Lawvere 理论经 coend 给出 \(Ta\cong a^0+a^1\cong\mathrm{Maybe}\,a\)；Demo 用 `raise`/`embed` 展示「只抛不接」；处理异常超出该小品的签名。
