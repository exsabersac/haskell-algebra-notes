# CTFP 3.14 Lawvere Theories — 原文顺序细讲

按 Milewski《Category Theory for Programmers》**第 3.14 章**原文小节顺序细讲；通俗拆分见同目录其它文档，可运行草图见 Demo `[1]`–`[6]`。

| 读法 | 去处 |
|------|------|
| **按原文顺序细讲（本文）** | 自上而下 §0–§9 |
| 按主题拆分 | [定义与骨架](定义与骨架.md) · [模型](模型.md) · [幺半群理论](幺半群理论.md) · [与finitary-monad](与finitary-monad.md) · [副作用与Maybe](副作用与Maybe.md) · [对照表](对照表.md) |
| 可运行 | [`src/Lawvere/Demo.hs`](../../src/Lawvere/Demo.hs)：`cabal run algebra-demos` |

术语保留精确英文：Lawvere theory、FinSet、skeleton \(\mathbf{F}\)、\(\mathbf{F}^{\mathrm{op}}\)、model、\(\mathrm{Mod}\)、finitary、coend、cowedge、Kleisli、EM algebra。

---

## §0 章首动机（Moggi / Lawvere vs monads）

现今谈函数式编程几乎绕不开 **monads**。CTFP 开篇设想另一条时间线：若 Eugenio Moggi 当时把注意力放在 **Lawvere theories** 而非 monads 上，副作用与计算效应会怎样被组织？

| 视角 | 长处 | 短板（本章语境） |
|------|------|------------------|
| monad | `return`/`join`、do-记法、EM / Kleisli 成熟 | **组合**无通用配方（monad transformer 个案） |
| Lawvere theory | 运算与定律收成一个范畴；理论可用 **coproduct / tensor** 组合 | 经典互译只覆盖 **finitary** monad；`Cont` 是反例 |

本章路线：universal algebra → Lawvere 定义 → models → monoid 例 → 与 monad / coend → Maybe 小品 → 练习与延伸阅读。

---

## §1 Universal Algebra

### 1.1 运算 + 全称等式

monoid、group、ring……在最朴素一层是：一组 **\(n\)-元运算**（operations）加上一组**全称量化**的等式定律（equational laws）。

| 结构 | 运算 | 定律 |
|------|------|------|
| monoid | 二元 \(\mu\)；单位作 **nullary** \(\eta\) | 结合；左右单位 |
| group | 再加一元逆 | 左右逆 |
| ring | 两套二元运算等 | 分配等 |

**arity** = 运算元数。一般 \(n\)-元运算：

\[
\alpha_n : a^n \to a
\]

零元运算：从终对象（\(a^0\cong 1\)）到 \(a\)。

> **字段（field）不在此框架内**：零关于乘法无逆，逆律不能对全部元素全称量化。

```haskell
unit :: ()     -> a   -- a^0 → a
inv  :: a      -> a   -- a^1 → a
mul  :: (a, a) -> a   -- a^2 → a
```

### 1.2 范畴化核心理念

在一般范畴里用态射代替函数：选定 **generic object** \(a\)，对象皆为其有限幂，同态集编码运算与定律 —— 这就是 Lawvere theory 的种子。

### 1.3 路线图

| # | 对象 | 作用 |
|---|------|------|
| 1 | \(\mathbf{FinSet}\) | 有限集合；对象由单点经 **coproduct** 生成 |
| 2 | \(\mathbf{F}\) | FinSet 的 **skeleton**（同构类合并）；对象 ≅ \(\mathbb{N}\) |
| 3 | \(\mathbf{F}^{\mathrm{op}}\) | 对偶：coproduct ↔ product；injection ↔ projection |
| 4 | \(\mathbf{L}\) | Lawvere theory（\(\mathbf{Law}\) 中的对象） |
| 5 | \(M\in\mathrm{Mod}(\mathbf{L},\mathbf{Set})\) | **model**：保有限积的 \(M:L\to\mathbf{Set}\) |

```text
FinSet ──skeleton──▶ F ──op──▶ F^op ──I_L──▶ L ──models──▶ Mod(L, Set)
```

对应拆分：[定义与骨架](定义与骨架.md)。Demo `[1]`：`op0`/`op2`。

---

## §2 Lawvere Theories（定义）

### 2.1 共同骨干：为何要 \(\mathbf{F}^{\mathrm{op}}\)

所有 Lawvere theory 的对象都由**一个**对象经有限积（幂）生成。积可用更简单范畴的 **coproduct** 经 **contravariant** 嵌入得到（对偶把 coproduct 变 product、injection 变 projection）。

自然骨干：\(\mathbf{FinSet}\)（\(\varnothing\)、\(1\)、\(2=1+1\)、…）。但 \(\mathbf{Set}\) 的 coproduct **不严格结合**（\(1+\varnothing\)、\(\varnothing+1\)、\(1\) 同构却不相等）。

**Skeleton** \(\mathbf{F}\)：每个同构类一个代表；对象 = 自然数（元素个数）；coproduct = 加法。

| \(\mathbf{F}\) 中态射 | 含义 |
|------------------------|------|
| \(\varnothing\to n\) | 唯一（初对象） |
| \(n\to\varnothing\)（\(n>0\)） | 不存在 |
| \(1\to n\) | \(n\) 条注入 |
| \(n\to 1\) | 唯一 |
| \(m\to n\) | 有限集函数（可重复选） |

### 2.2 定义：\(I_L:\mathbf{F}^{\mathrm{op}}\to\mathbf{L}\)

**Lawvere theory** = 范畴 \(\mathbf{L}\) + 函子

\[
I_{\mathbf{L}} : \mathbf{F}^{\mathrm{op}} \to \mathbf{L}
\]

满足：

1. **对对象双射**（常称 identity-on-objects；对象用 \(0,1,2,\ldots\) 标记）；
2. **保有限积**：\(I_L(m\times n)=I_L m\times I_L n\)（\(\mathbf{F}^{\mathrm{op}}\) 的积 = \(\mathbf{F}\) 的 coproduct）。

同态集 \(\mathbf{L}(m,n)\) 一般比 \(\mathbf{F}^{\mathrm{op}}\) **更富**：

| 来源 | 名称 | 例子 |
|------|------|------|
| \(I_L\) 的像 | **boring** / basic product operations | 投影 \(1^n\to 1\)、对角 \(1\to 1^n\) |
| 额外 | **interesting** morphisms | 乘法 \(2\to 1\)、单位 \(0\to 1\)、逆… |

直觉：\(1\in\mathbf{F}\) ↦ \(1\in\mathbf{L}\)，其余对象自动是其幂；\(\mathbf{F}\) 像 \(\mathbf{L}\) 的「对数」。投影 \(p_k:1^n\to 1\) ≈「\(n\) 个变量里只取第 \(k\) 个」；对角 ≈ 变量复制。

复合态射 \(n\to m\)（即 \(1^n\to 1^m\)）= 若干 \(n\to 1\) 的积（hom-函子连续）。

```haskell
π1, π2 :: (a, a) -> a
diag   :: a -> (a, a)
op0    :: Monoid m => m              -- interesting: η
op2    :: Monoid m => m -> m -> m    -- interesting: μ
```

### 2.3 \(\mathbf{Law}\) 中的态射；平凡理论

\(\mathbf{Law}\)：对象 = Lawvere theories；态射 = **保有限积且与 \(I\) 交换**的函子。解释：把一个理论的运算翻译进另一个（群乘法当 monoid 乘法、忘掉逆）。Demo `[6]`：Monoid → Semigroup（忘掉单位）。

最简：\(\mathbf{L}=\mathbf{F}^{\mathrm{op}}\)，\(I_L=\mathrm{id}\)。无额外运算与定律 —— \(\mathbf{Law}\) 的**初对象**。

对应拆分：[定义与骨架](定义与骨架.md)。

---

## §3 Models of Lawvere Theories

### 3.1 定义

一个理论概括**一整类**代数；具体代数是其 **model**（亦称 \(\mathbf{L}\) 上的代数）：

\[
M : \mathbf{L} \to \mathbf{Set},\qquad
M(a\times b)\;\cong\; Ma\times Mb
\]

积只需保到**同构**（up to isomorphism）。严格相等会杀掉绝大多数有趣例子。

记 \(a=M(1)\)（**sort**；此处 single-sorted）：

| \(\mathbf{L}\) 态射 | \(M\) 给出 |
|---------------------|------------|
| \(0\to 1\) | \(1\to a\)（挑元素） |
| \(1\to 1\) | \(a\to a\) |
| \(2\to 1\) | \(a\times a\to a\) |
| \(m\to n\) | \(a^m\to a^n\) |

多个 \(\mathbf{L}\)-态射可塌缩为 \(\mathbf{Set}\) 中同一函数。因定律皆全称等式，恒有**平凡模型**：常值到单点集。

```haskell
-- Demo [1][3]：同一理论，三种模型
-- (Sum,0,+)  ([a],[],++)  (Endo,id,.)
checkMonoidLaws x y z =
  and [ (x<>y)<>z == x<>(y<>z)
      , mempty <> x == x
      , x <> mempty == x ]
```

### 3.2 Nat；\(\mathrm{Mod}\)；平凡理论 ≃ Set

两模型间的自然变换 \(\mu_n:a^n\to b^n\)；自然性 = 保持 \(n\)-元运算（monoid 时即 monoid 同态）。全体组成 \(\mathrm{Mod}(\mathbf{L},\mathbf{Set})\)。

对初对象理论 \(\mathbf{L}=\mathbf{F}^{\mathrm{op}}\)：模型由 \(M(1)\) 完全决定，且可为任意集合；自然变换由 \(\mu_1\) 决定。故

\[
\mathrm{Mod}(\mathbf{F}^{\mathrm{op}},\mathbf{Set})\;\simeq\;\mathbf{Set}.
\]

对应拆分：[模型](模型.md)。

---

## §4 The Theory of Monoids

### 4.1 必须有的 interesting 态射

| 态射 | 方向 | 为何有趣 |
|------|------|----------|
| 单位 \(\eta\) | \(0\to 1\) | \(\mathbf{F}\) 中无 \(1\to 0\)（单点不能映入空集） |
| 乘法原型 | \(L(2,1)\) 的成员 | 模型里 ↦ \(a\times a\to a\) |

### 4.2 \(L(2,1)\) ≃ 两生成元自由词

仅用 monoid 运算能写的二元导出运算：单位、两投影、\(ab\)、\(ba\)、\(aa\)、\(bb\)、\(aab\)、… —— 个数 = **两生成元自由 monoid** 的元素数。

机制：自由 monoid 本身是一个模型；在自由情形这些词对应**不同**函数；理论侧必须先装得下自由情形。

记 \(n^*=\) \(n\) 元自由 monoid。取

\[
\mathbf{L}_{\mathrm{Mon}}(m,n)\;=\;\mathbf{Mon}(n^*,\,m^*)
\]

即 \(\mathbf{L}_{\mathrm{Mon}}\) ≃ **自由 monoid 范畴的 opposite**。

```haskell
-- Demo [2]
data Gen = A | B
type Word2 = [Gen]
applyWord :: Monoid m => Word2 -> m -> m -> m
wordsUpTo :: Int -> [Word2]   -- |w|≤2 共 7 个：ε,A,B,AA,AB,BA,BB
```

### 4.3 \(\mathrm{Mod}\simeq\mathbf{Mon}\)

\[
\mathrm{Mod}(\mathbf{L}_{\mathrm{Mon}},\mathbf{Set})\;\simeq\;\mathbf{Mon}
\]

与列表路线汇合：`EM([]) ≃ Mon ≃ Mod(L_Mon, Set)`。

单个自由 monoid 已概括许多商；Lawvere 理论再把**所有**有限生成自由 monoid 的箭头空间收成一个范畴。

对应拆分：[幺半群理论](幺半群理论.md)。Demo `[1]`–`[3]`。

---

## §5 Lawvere Theories and Monads

### 5.1 \(U\dashv F\)；\(T=U\circ F\)

**遗忘** \(U:\mathrm{Mod}(L,\mathbf{Set})\to\mathbf{Set}\)，\(U(M)=M(1)\)。  
亦可：\(\mathbf{F}^{\mathrm{op}}\) 初 ⇒ 唯一 \(\mathbf{F}^{\mathrm{op}}\to L\) ⇒ 诱导模型范畴箭头，再经 \(\mathrm{Mod}(\mathbf{F}^{\mathrm{op}},\mathbf{Set})\simeq\mathbf{Set}\)。

**自由** \(F\)（有限生成）：可表 \(F(n)=\mathbf{L}(n,-)\)。Yoneda：

\[
\mathrm{Mod}(L,\mathbf{Set})\bigl(L(n,-),\,M\bigr)
\;\cong\;\mathbf{Set}(n,UM)\;\cong\;Mn.
\]

合成为 \(\mathbf{Set}\) 上 monad \(T=U\circ F\)。**EM\((T)\) ≃ \(\mathrm{Mod}(L,\mathbf{Set})\)**。

| 视角 | 给什么 |
|------|--------|
| Lawvere | \(n\)-元运算 → 造表达式 |
| model / EM | 求值映射 → 消回载体 |

```haskell
-- monoid / 列表：T = []
ret x = [x]
jn = concat
-- Demo [4]：foldMap 在模型上求值词
```

### 5.2 仅 finitary；coend 公式；Kleisli\(^{\mathrm{op}}\)；Cont

互译**不是双向任意**：只有 **finitary** monad ↔ 经典 Lawvere theory。

Finitary functor 由有限集上行为决定：

\[
Fa\;=\;\int^{n} a^n\times(Fn)
\]

Lawvere 生成的 monad：

\[
T_L a\;=\;\int^{n} a^n\times\mathbf{L}(n,1)
\]

逆：finitary \(T\) → 有限集上的 Kleisli，再取 opposite：

\[
\mathbf{L}\;\simeq\;\bigl(\mathrm{Kl}_T\big|_{\mathrm{fin}}\bigr)^{\mathrm{op}},
\qquad
\mathbf{L}(n,1)\;=\;\mathrm{Kl}_T(1,n)\;\cong\;Tn.
\]

对列表：\(Tn\cong n^*\)。

编程里多数 monad 是 finitary；**continuation monad `Cont`** 是著名例外（不能仅由有限 arity 形状表展开）。可扩展「超越 finitary」的 Lawvere 变体，CTFP 点到为止。

对应拆分：[与finitary-monad](与finitary-monad.md)。Demo `[4]`。

---

## §6 Monads as Coends（细拆）

### 6.1 Profunctor 与升降

\[
T_L a\;=\;\int^{n} a^n\times\mathbf{L}(n,1)
\]

取 profunctor \(P\,n\,m = a^n\times\mathbf{L}(m,1)\)（在 \(\mathbf{F}\) 上）。\(\mathbf{F}\) 中 \(f:m\to n\)（从 \(n\) 元选 \(m\) 个，可重复）：

- 内容侧：\(a^n\to a^m\)（按 \(f\) 选槽；方向与 \(f\) 相反）；
- 运算侧：\(f\) 在 \(\mathbf{L}\) 中对应 \(n\to m\)，预复合得 \(\mathbf{L}(m,1)\to\mathbf{L}(n,1)\)。

例：\(f_k:1\to n\) 升降为取第 \(k\) 分量；常值 \(m\to 1\) 升降为复制 \(m\) 次。

> 注意：\(\mathbf{L}(m,1)\) 对 \(m\) 本是反变的；coend 变量走的是 \(\mathbf{F}\)（经 \(I_L\) 嵌入），故相对 \(\mathbf{F}\) 的箭头方向要按对偶读。

### 6.2 Cowedge：两条路径等同

Coend ≈ 对角项的不相交并，再按 cowedge / 余等化子等同。离对角项 \(a^n\times\mathbf{L}(m,1)\)，对 \(f:m\to n\) 可作用于第一或第二因子，两条结果**等同**：

```text
          a^n × L(m,1)
         /            \
   ⟨f,id⟩              ⟨id,f⟩
       /                \
a^m × L(m,1)    ~    a^n × L(n,1)
```

### 6.3 哪些项塌缩到 \(a\times L(1,1)\)？

经 basic morphisms（\(I_L\) 像）从 \(L(1,1)\) 能到达的 \(L(n,1)\)，其对角项全部等同到 \(a\times L(1,1)\)。  
**非** basic 的真正 \(n\)-元运算**不能**仅靠升降 \(1\to n\) 从 \(L(1,1)\) 到达 —— 它们留下「真正的」额外求和贡献。

### 6.4 平凡理论 → 恒等 monad

若 \(\mathbf{L}=\mathbf{F}^{\mathrm{op}}\)：\(L(1,1)=\{\mathrm{id}\}\)，且每个 \(L(n,1)\) 恰是 \(\mathbf{F}\) 中注入 \(1\to n\) 的像（皆 basic）。全部对角项等同，得

\[
Ta\;=\;a\times L(1,1)\;=\;a
\]

即 **identity monad**。

对应拆分：[与finitary-monad](与finitary-monad.md) §2。

---

## §7 Lawvere Theory of Side Effects / Maybe

### 7.1 组合优势

Monad 组合无通用配方；Lawvere theories 可用 **coproduct / tensor** 组合。代价：易转的仍是 finitary；`Cont` 仍是 outlier。

### 7.2 Raise-only → \(1+a\)

在平凡骨干上加**一个** nullary：

\[
\mathrm{raise}:0\to 1
\]

模型：\(M(1)=a\)，raise ↦ \(1\to a\)（异常点）。**无** handler / catch。

Coend 中：`raise` 使 \(L(0,1)\) 新增元素，并通过复合 \(n\to 0\to 1\) 丰富 \(L(n,1)\)；这些贡献经 cowedge（升降 \(0\to n\) 的两条路径）等同到 \(a^0\times L(0,1)\)。再留下骨干 \(a^1\) 项：

\[
T_L a\;\cong\;a^0+a^1
\]

```haskell
-- Either () a ≅ Maybe a
-- Demo [5]
raise  = Nothing          -- a^0 支
embed  = Just             -- a^1 支
-- raise >> embed "…"  → Nothing   （只抛不接）
```

| coend 项 | `Maybe` |
|----------|---------|
| \(a^0\times L(0,1)\) | `Nothing` |
| \(a^1\times L(1,1)\) | `Just a` |
| 更高 \(n\) 的纯 raise 复合 | cowedge 吸进 \(a^0\) |

对应拆分：[副作用与Maybe](副作用与Maybe.md)。

---

## §8 Challenges（四题意图）

| # | 题目（CTFP） | 意图 |
|---|--------------|------|
| 1 | 枚举 \(\mathbf{F}\) 中 \(2\) 与 \(3\) 之间的全部态射 | 熟悉 skeleton：\(2\to 3\) 有 \(3^2=9\) 个函数；\(3\to 2\) 有 \(2^3=8\) 个；方向都要写清 |
| 2 | 证明 monoid 的 \(\mathrm{Mod}\) ≃ 列表 monad 的 EM 代数范畴 | 钉死三路等价：`Mod(L_Mon) ≃ Mon ≃ EM([])`；一边是保积模型，一边是 `mconcat` 型 \(\alpha:[a]\to a\) |
| 3 | 列表 monad 的二元运算可由对应 Kleisli 箭头生成 | 练「理论 ← Kleisli\(^{\mathrm{op}}\)」：\(L(2,1)\cong\mathrm{Kl}(1,2)\cong T(2)\cong 2^*\)（词） |
| 4 | 证明 finitary functor = 其限制到 FinSet 的 **左 Kan 扩张** | 把「由有限集决定」写成 Kan：\(Fa\cong\mathrm{Lan}_i(F\circ i)(a)\)（\(i:\mathbf{FinSet}\hookrightarrow\mathbf{Set}\)），与 coend 公式同一机制 |

做题时可对照 Demo `[2]`（词）、`[4]`（List / `foldMap`）与 [与finitary-monad](与finitary-monad.md) 的 Kleisli / coend 节。

---

## §9 Further Reading

1. F. William Lawvere, *Functorial Semantics of Algebraic Theories* — [TAC reprint](http://www.tac.mta.ca/tac/reprints/articles/5/tr5.pdf)
2. Gordon Plotkin & John Power, *Notions of computation determine monads* — [PDF](http://homepages.inf.ed.ac.uk/gdp/publications/Comp_Eff_Monads.pdf)

本仓库邻近：[List的EM代数与Monoid](../幺半范畴/List的EM代数与Monoid.md) · [自由幺半群与列表](../幺半范畴/自由幺半群与列表.md) · [余密度单子](../Kan扩展/余密度单子.md)（coend / 密度语境）。

---

## 附录：原文小节 ↔ 拆分文档 ↔ Demo

| CTFP | 本文 | 拆分 | Demo |
|------|------|------|------|
| 章首 | §0 | — | — |
| Universal Algebra | §1 | [定义与骨架](定义与骨架.md) | `[1]` |
| Lawvere Theories | §2 | [定义与骨架](定义与骨架.md) | `[1]` `[6]` |
| Models | §3 | [模型](模型.md) | `[1]` `[3]` |
| Theory of Monoids | §4 | [幺半群理论](幺半群理论.md) | `[1]`–`[3]` |
| Lawvere and Monads | §5 | [与finitary-monad](与finitary-monad.md) | `[4]` |
| Monads as Coends | §6 | [与finitary-monad](与finitary-monad.md) §2 | `[4]` |
| Side Effects / Maybe | §7 | [副作用与Maybe](副作用与Maybe.md) | `[5]` |
| Challenges | §8 | （练习） | `[2]` `[4]` |
| Further Reading | §9 | — | — |
| （综览） | — | [对照表](对照表.md) | `[6]` |

```text
FinSet → F → F^op → L → Mod(L,Set)
                           │
                    free F ⊣ forgetful U
                           ▼
                    finitary T_L = U∘F = ∫^n a^n × L(n,1)
                           │
              finitary T ──Kl^op|fin──▶ L
```
