# List 的 EM 代数与 Monoid

在 \(\mathbf{Set}\) 上，列表 monad `[]` 的 **Eilenberg–Moore（EM）代数**范畴与 **Monoid** 范畴等价：\(\mathrm{EM}([]) \simeq \mathbf{Mon}\)。  
术语保留精确英文：EM、ListF、mconcat、foldMap、Kleisli、UP。

相关：[自由幺半群与列表](自由幺半群与列表.md) · [自由幺半群与ListF代数](自由幺半群与ListF代数.md) · [例子与Monad.md](例子与Monad.md) · [与自由代数和Monad](../初始代数/与自由代数和Monad.md) · [自由函子与自由代数](../Free/自由函子与自由代数.md)

---

## 1. 一般 EM 代数

对 monad \(T\)，一个 **EM 代数**是载体 \(A\) 配上结构映射

\[
\alpha : T A \to A
\]

满足（单位与结合）：

\[
\alpha \circ \eta = \mathrm{id}_A, \qquad
\alpha \circ \mu = \alpha \circ T\alpha
\]

Haskell 草图：

```haskell
-- α :: t a -> a
-- α . return = id
-- α . join   = α . fmap α
```

直觉：monad 描述可组合的结构；EM 代数是在载体上**合法消去**该结构的方式。

---

## 2. 特化到列表 monad `[]`

取 \(T = []\)：\(\eta\,a = [a]\)，\(\mu = \mathrm{concat}\)（即 `join`）。  
则 \(\alpha : [A] \to A\) 须满足：

```haskell
-- α [a]           = a                    -- α ∘ η = id
-- α (concat xss)  = α (map α xss)        -- α ∘ μ = α ∘ fmap α
```

即：单例列表映回元素；嵌套列表先对内层消再对外层消，与先 `concat` 再消一致。

---

## 3. 定理（Set）：\(\mathrm{EM}([]) \simeq \mathbf{Mon}\)

双向构造互逆。

### 正向：Monoid \(\Rightarrow\) EM

给定 monoid \(M\)，取 \(\alpha = \mathrm{mconcat}\)：

```haskell
mconcat :: Monoid m => [m] -> m
mconcat = foldr (<>) mempty
-- mconcat [a] = a
-- mconcat (concat xss) = mconcat (map mconcat xss)
```

### 反向：EM \(\Rightarrow\) Monoid

给定 \(\alpha : [A] \to A\) 满足上节两律，定义

```haskell
mempty  = α []
a <> b  = α [a, b]
```

可验证 \((A,\langle\rangle,\mathrm{mempty})\) 为 monoid，且由此恢复的 \(\mathrm{mconcat}\) 即原 \(\alpha\)。

### 互相逆

- 从 monoid 出发：\(\mathrm{mconcat}\,[]=\mathrm{mempty}\)，\(\mathrm{mconcat}\,[a,b]=a\langle\rangle b\)，再 \(\mathrm{mconcat}\) 回去得原 \(\alpha\)。
- 从 EM 出发：用 \(\alpha[]\)、\(\alpha[a,b]\) 定义的 monoid，其 \(\mathrm{mconcat}\) 因结合律与 \(\alpha\circ\mu=\alpha\circ\mathrm{fmap}\,\alpha\) 回到 \(\alpha\)。

因此对象与态射在等价意义下对齐：**列表 monad 的 EM 代数就是 monoid**。

---

## 4. 短例

```haskell
-- Sum：α = mconcat . map Sum 的载体直觉（示意）
mconcat [Sum 1, Sum 2, Sum 3]  -- Sum 6

-- 列表自身作为 monoid：α = concat（= join / mconcat for []）
concat ["ab", "c"]             -- "abc"

-- 自由 EM 代数 on X：载体 [X]，α = join = concat
-- （见下节）
```

---

## 5. 对照表：ListF-代数 / monoid 诱导 / List-EM

| | 一般 ListF-代数 | monoid 诱导的 ListF-代数 | List 的 EM 代数 |
|--|-----------------|---------------------------|-----------------|
| 数据 | \(\varphi : \mathrm{ListF}\,x\,A \to A\)，即任意 \((e,\mathrm{step})\) | \(\varphi=\mathrm{fromMonoid}\,f\)：\(e=\mathrm{mempty}\)，\(\mathrm{step}\,x=(f\,x\langle\rangle)\) | \(\alpha : [A]\to A\)，\(\alpha\circ\eta=\mathrm{id}\)，\(\alpha\circ\mu=\alpha\circ T\alpha\) |
| 范畴角色 | \(\mathrm{Alg}(\mathrm{ListF}\,x)\) | 上述的特殊对象（由 monoid + \(f:x\to m\) 产生） | \(\mathrm{EM}([])\) |
| 与 Monoid | 一般**不是** monoid | 来自 monoid，但一层 `ListF` 数据不够自动恢复完整 \(\langle\rangle\)（见 [ListF 笔记](自由幺半群与ListF代数.md)） | **≃ Monoid**（上节双射） |
| 折叠 | `cata` | `foldMap f ≡ cata (fromMonoid f)` | `mconcat`（\(A\) 上已是 monoid） |

细节：一般 ListF vs monoid 诱导、逆向是否总成立，见 [自由幺半群与ListF代数](自由幺半群与ListF代数.md)。

---

## 6. 自由 EM 代数：\(([X],\mathrm{join})\)

对任意 monad \(T\)，自由 EM 代数 on \(X\) 的载体是 \(T X\)，结构为 \(\mu_X\)（`join`）。  
对 \(T=[]\)：

\[
\bigl([X],\,\mathrm{join}=\mathrm{concat}\bigr)
\]

正是自由 monoid \(\mathrm{FreeMon}(X)\) 作为 EM 对象的那一面：同一故事，眼镜换成「相对遗忘 \(\mathrm{EM}([])\to\mathbf{Set}\) 的自由」。  
对象层展开见 [自由幺半群与列表](自由幺半群与列表.md)；与「\(F\)-初始代数」分界见 [与自由代数和Monad](../初始代数/与自由代数和Monad.md)。

```text
FreeMon(X) ≅ ([X], ++, [])     （Mon 里的自由对象）
自由 EM on X ≅ ([X], join)     （EM([]) 里的自由对象）
—— 同一载体与同一消去；范畴包装不同，故事相同。
```

---

## 7. Kleisli 边界（简）

| | 落点 | 典型箭头 |
|--|------|----------|
| EM / Mon | 对象带结构 \(\alpha\)（或 \(\langle\rangle\)） | monoid 同态 \(M\to N\)；EM 同态（与 \(\alpha\) 交换） |
| Kleisli | 箭头形如 \(A \to T B\) | 列表情形：\(A\to[B]\)（Kleisli 复合用 `>>=`） |

monoid 同态活在 **EM / Mon 一侧**；不要把「随便一个 \(A\to[B]\)」当成 monoid 同态。  
Kleisli 谈的是 monad 的**箭头范畴**包装；EM 谈的是**代数对象**。

---

## 8. 已澄清结论

1. 一般 EM：\(\alpha:TA\to A\)，\(\alpha\circ\eta=\mathrm{id}\)，\(\alpha\circ\mu=\alpha\circ T\alpha\)。
2. List：\(\alpha:[A]\to A\)，\(\alpha[a]=a\)，\(\alpha(\mathrm{concat}\,xss)=\alpha(\mathrm{map}\,\alpha\,xss)\)。
3. 在 Set 上 \(\mathrm{EM}([])\simeq\mathbf{Mon}\)：正向 `mconcat`；反向 \(\mathrm{mempty}=\alpha[]\)，\(a\langle\rangle b=\alpha[a,b]\)；互逆。
4. 自由 EM on \(X\) 为 \(([X],\mathrm{join})\)，与自由 monoid 同一故事。
5. ListF-代数 ⊃ monoid 诱导的 ListF-代数；List-EM ≃ Monoid——三层不要并成一句。
6. monoid 同态在 EM/Mon 侧；Kleisli 箭头是 \(A\to TB\)。

### 易混点

| 易混 | 澄清 |
|------|------|
| 「\([X]\) 是自由 monoid」≠「\(\mathrm{EM}([])\simeq\mathrm{Monoid}\)」 | 前者是**一个自由对象**；后者是**整个代数范畴**与 Mon 等价。已见 [自由幺半群与列表](自由幺半群与列表.md) §易混；此处再钉一句。 |
| ListF-代数 = EM？ | 否。ListF 是一层 \(1+X\times(-)\)；EM 是对整段列表 monad（`return`/`join`）的合法消去。 |
| `mconcat` = `foldMap id` | 对 monoid 载体成立；`foldMap f` 则先经 \(f:X\to M\) 再消——自由 monoid 的 UP 侧，见 [ListF 笔记](自由幺半群与ListF代数.md)。 |
| Kleisli 箭头 = monoid 同态 | 否。\(A\to[B]\) 是 Kleisli；monoid 同态要求保 \(\langle\rangle\)/单位，落在 EM/Mon。 |

### 另见

- [自由幺半群与列表](自由幺半群与列表.md) — \(\mathrm{FreeMon}(X)\cong[X]\)；对象 vs 范畴易混
- [自由幺半群与ListF代数](自由幺半群与ListF代数.md) — FreeMon vs 初始 ListF；`fromMonoid`；UP 双射
- [例子与Monad.md](例子与Monad.md) — Monad = End 中 monoid 对象
- [与自由代数和Monad](../初始代数/与自由代数和Monad.md) — EM 自由代数载体是 \(TX\)
- [自由函子与自由代数](../Free/自由函子与自由代数.md) — EM 自由代数 vs \(\mu Y.\,a+f\,Y\)
