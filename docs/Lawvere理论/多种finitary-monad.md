# 多种 finitary monad 的 Lawvere 草图

在 [与finitary-monad](与finitary-monad.md) 的 coend / Kleisli 框架下，把若干常见 **finitary** monad 对照到各自的 Lawvere theory（运算签名 + \(L(n,1)\) + \(T\)）。  
术语：Lawvere theory、\(L(n,1)\)、coend、Kleisli、finitary、Identity、Semigroup / NonEmpty、Writer、Either、Reader、State；**Cont 非 finitary**。

相关：[与finitary-monad](与finitary-monad.md) · [副作用与Maybe](副作用与Maybe.md) · [对照表](对照表.md) · Demo `[7]`–`[12]`（兼 `[4]` List、`[5]` Maybe）

---

## 0. 总对照表

统一公式：

\[
T a \;\cong\; \int^{n} a^{n}\times L(n,1)
\qquad\text{（或）}\qquad
L(n,1)\;\cong\; T\,n
\]

| Monad \(T\) | 理论要点（ops） | \(L(n,1)\)（草图） | \(T a\) | Demo |
|-------------|-----------------|-------------------|---------|------|
| **Identity** | 平凡 \(\mathbf{F}^{\mathrm{op}}\)：仅投影 | \(\cong n\) | \(a\) | `[7]` |
| **List** | monoid：\(\eta:0\to1\), \(\mu:2\to1\) | \(\cong n^{*}\)（词） | \([a]\) | `[4]` |
| **Maybe** | 单一 nullary `raise` | 见 Maybe 文 | \(1+a\) | `[5]` |
| **Semigroup / NE** | 仅 \(\mu:2\to1\) + assoc | 非空词 / nonempty 形状 | `NE a` \(\cong a\times[a]\) | `[8]` |
| **Writer \(W\)** | 「挑槽 + 写 \(w\in W\)」族 | \(\cong n\times W\) | \((a,W)\) | `[9]` |
| **Either \(E\)** | \(\lvert E\rvert\) 个 nullary `raise_e` | \(L(0,1)\cong E\) 等 | \(E+a\) | `[10]` |
| **Reader \(E\)**（有限） | 每环境挑投影槽 | \(\cong E\to n\cong n^{\lvert E\rvert}\) | \(E\to a\) | `[11]` |
| **State \(S\)**（有限） | 每起始态：输出槽+下一态 | \(\cong(n\times S)^{S}\) | \(S\to(a,S)\) | `[12]` |
| **Cont** | — | **非 finitary** | \((a\to r)\to r\) | （边界） |

`cabal run algebra-demos` 打印 `[7]`…`[12]` 横幅。

---

## 1. Identity — 平凡理论 \(\mathbf{F}^{\mathrm{op}}\)

- **理论**：无 interesting morphisms；只有 basic product operations（投影 / 对角等）。
- \(L(n,1)\cong n\)（\(n\) 个投影 \(\pi_i:n\to1\)）。
- coend 全部塌到 \(a\)：\(T a\cong a\)。
- `return = id`，`join = id`。

```haskell
-- Demo [7]
retId, joinId :: a -> a
retId = id
joinId = id
```

---

## 2. Semigroup / NonEmpty — 仅 binary mul

- **理论**：单一有趣运算 \(\mu:2\to1\) + 结合律；**无** unit（对比 monoid / List）。
- 自由 semigroup = **非空**列表；\(T a\cong\mathrm{NE}\,a\cong a\times[a]\)。
- `return` = singleton；`join` = 展平 nonempty-of-nonempty。
- 与 `[6]`：理论态射 \(L_{\mathrm{Semigroup}}\to L_{\mathrm{Monoid}}\)（模型侧忘掉单位）。

```haskell
-- Demo [8]
data NE a = NE a [a]
neSingleton x = NE x []
neJoin (NE (NE x xs) rest) = NE x (xs ++ concatMap neToList' rest)
```

---

## 3. Writer（固定 monoid \(W\)）

- **理论**：在平凡骨干上，对每个 \(w\in W\) 增加「写日志」方向的运算族。
- \(L(n,1)\cong n\times W\)：选一个变量槽，并附带一段日志。
- \(T a\cong a\times W\)；`return x = (x, mempty)`；`join ((x,w1),w2)=(x,w1<>w2)`（教育序；与 transformers 外内拼接顺序对照即可）。

```haskell
-- Demo [9]；W = Sum Int 或 [Char]
type Writer w a = (a, w)
writerReturn x = (x, mempty)
writerJoin ((x, w1), w2) = (x, w1 <> w2)
```

---

## 4. Either / multi-exception

- **理论**：\(\lvert E\rvert\) 个 nullary `raise_e:0\to1`（无 handler）。`Maybe` = \(\lvert E\rvert=1\)。
- \(L(0,1)\cong E\)；展开得 \(T a\cong E+a\cong\mathrm{Either}\,E\,a\)。
- `return = Right`；`join` 传播 `Left`，否则拆内层。

```haskell
-- Demo [10]；E = Exc | String
raiseE = Left
embedE = Right
```

---

## 5. Reader（有限 env）

- **env 必须有限**才是经典 finitary Lawvere（本仓库取 `Bool`，\(\lvert\mathrm{env}\rvert=2\)）。
- \(L(n,1)\cong\mathrm{env}\to n\cong n^{\lvert\mathrm{env}\rvert}\)（每个环境挑一个投影槽）。
- \(T a\cong(\mathrm{env}\to a)\)；`return = const`；`join f e = f e e`。

```haskell
-- Demo [11]
type Reader env a = env -> a
readerReturn = const
readerJoin f e = f e e
```

---

## 6. State（有限 \(S\)）

- **\(S\) 有限**（本仓库 `Bool`）。
- \(L(n,1)\cong(n\times S)^{S}\)：对每个起始状态，给出「输出槽 \(\in n\)」与「下一状态 \(\in S\)」。
- 计数：\(\lvert L(n,1)\rvert=(n\cdot\lvert S\rvert)^{\lvert S\rvert}\)；\(\lvert S\rvert=2\) 时 \((2n)^{2}\)（\(n=1\Rightarrow4\)，\(n=2\Rightarrow16\)）。
- \(T a\cong S\to(a,S)\)；`return x s=(x,s)`；`join`：外层跑出 `(inner,s1)` 再跑 `inner` @ `s1`。

```haskell
-- Demo [12]
type State s a = s -> (a, s)
stateReturn x s = (x, s)
stateJoin outer s0 = let (inner, s1) = outer s0 in inner s1
```

---

## 7. Cont 不是 finitary（边界）

continuation monad \(T a=(a\to r)\to r\) **不能**由有限 arity 的 \(L(n,1)\) 经 coend 展开决定（依赖任意高阶 / 任意多输入）。  
因此 **无**经典 Lawvere theory 对应——已在 [与finitary-monad](与finitary-monad.md) §4、[对照表](对照表.md) 标明。本文件只列 finitary 正面例子。

---

## 一句话

有限 arity 的运算签名（含固定有限参数集 \(W,E,S,\mathrm{env}\)）→ Lawvere \(L\) → finitary \(T_L a=\int^{n}a^{n}\times L(n,1)\)；List / Maybe / NE / Writer / Either / Reader / State（有限）都落在此列，**Cont 不在**。
