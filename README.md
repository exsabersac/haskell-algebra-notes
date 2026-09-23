# Haskell 中的 Algebra、初始代数与 Monad

本文整理自一次关于 Haskell / 范畴论中 **algebra**、**初始代数**、**自由代数** 与 **monad** 关系的讨论结论，便于复习查阅。

---

## 续篇目录

后续讨论已拆成独立文档，可按主题查阅：

1. [Free 中的生成元](docs/01-generators-in-free.md)
2. [并排：`Fix` 与 `Free ExprF`](docs/02-fix-vs-free-expr.md)
3. [`foldFree` 与 `cata` 的交换图对齐](docs/03-foldfree-and-cata.md)
4. [编码：`Free ≅ Fix (Sum (Const a) f)`](docs/04-fix-sum-const-encoding.md)
5. [常见函子组合](docs/05-functor-combinations.md)

---

## 1. Algebra 在 Haskell 里有几层意思

「Algebra」不是某一个固定的类型类名，常见有四层：

| 层次 | 典型形态 | 在说什么 |
|------|----------|----------|
| F-代数 | `f a -> a` | 一层函子形状的解释；`cata` / fold |
| Monad 代数（Eilenberg–Moore） | `m a -> a`（尊重 `return` / `join`） | 消去 monad 结构的合法方式 |
| 抽象代数类型类 | `Monoid`、`Semigroup`… | 运算 + 定律；许多恰是某 monad 的 EM 代数 |
| 自由代数 / Free | `Free f a`、`foldFree` | 语法与解释分离 |

另有「代数数据类型」（ADT）里的 algebraic，多指用**和**与**积**搭类型；它与 F-代数 / 初始代数有历史与数学上的接缝（见第 4 节），但口语里说「这个 algebra」通常不是单指 ADT 语法。

---

## 2. F-代数与 Monad 代数

### F-代数

对函子 `f`，F-代数是载体 `a` 加上：

```haskell
φ :: f a -> a
```

递归类型、`fold` / catamorphism 都建立在这上面。

### Monad 代数

对 monad `m`，monad 代数是：

```haskell
α :: m a -> a
```

且满足：

1. `α ∘ return = id`
2. `α ∘ join = α ∘ fmap α`

直觉：monad 描述可组合的结构／计算；代数是在载体上**合法消去**该结构的方式。

### 核心关系（Free）

若 `m = Free f`（由函子 `f` 生成的自由 monad），则：

```text
Free f 的 monad 代数  ≅  f 的 F-代数
```

双向构造：

```haskell
-- F-代数 → monad 代数
foldFree :: Functor f => (f a -> a) -> Free f a -> a
foldFree φ (Pure x) = x
foldFree φ (Free t) = φ (fmap (foldFree φ) t)

-- monad 代数 → F-代数（限制到深度 1）
toAlgebra :: Functor f => (Free f a -> a) -> (f a -> a)
toAlgebra α fa = α (Free (fmap Pure fa))
```

二者互逆（在 monad 代数法则下）。因此：用 `Free` 写语法树／效果语法，再用 `f a -> a`（或等价的 `Free f a -> a`）解释——这是 free monad 作为「自由代数」的用法。

---

## 3. 两个 list 相关的故事（不要混）

### 故事 A：`Free ((,) e) ≅ ([e], a)`

- 函子：`f = ((,) e)`（一层「再记一个 `e`」）
- `Free ((,) e) a ≅ ([e], a)`
- F-代数：`φ :: (e, a) -> a`（一步更新）
- `foldFree φ` ≡ 按列表逐步折叠（类似带种子的 fold）

元素类型 `e` 与载体 `a` **可以不同**。一般只需「逐步更新」，不要求 `a` 自己是 monoid。

### 故事 B：`[]` 的 monad 代数 = Monoid

列表 monad：`return x = [x]`，`join = concat`。

代数 `α :: [a] -> a` 满足单位与乘法法则时，等价于 `a` 上的 monoid：

```haskell
-- monoid → 代数
α = mconcat

-- 代数 → monoid
mempty  = α []
x <> y  = α [x, y]
```

这里列表元素类型与载体相同；折叠必须形成 monoid。

| | `Free ((,) e)` | `[]` 的 EM 代数 |
|--|----------------|-----------------|
| 典型映射 | `([e], a) -> a` | `[a] -> a` |
| 一步 | `(e, a) -> a` | 无单独的「异型 e」 |
| 额外结构 | 逐步更新即可 | 单位 + 结合 ⇒ Monoid |

---

## 4. 初始代数：定义、不动点、递归 ADT

### 定义

固定自函子 \(F\)。\(F\)-代数是 \((A, \varphi: F A \to A)\)；同态 \(h\) 满足 \(h \circ \varphi = \psi \circ F h\)。

**初始 \(F\)-代数** \((\mu F, \mathrm{in})\) 是 \(F\)-代数范畴的初始对象：对任意代数 \((A, \varphi)\) 存在**唯一**同态

\[
\operatorname{cata}\varphi : \mu F \to A
\]

使交换图成立。Haskell 中常写作：

```haskell
newtype Fix f = Fix { unFix :: f (Fix f) }

cata :: Functor f => (f a -> a) -> Fix f -> a
cata φ = φ . fmap (cata φ) . unFix
```

### 与不动点的关系（Lambek）

- **有初始代数 ⇒ 载体是不动点**：\(\mathrm{in}: F(\mu F) \to \mu F\) 必为同构，故 \(\mu F \cong F(\mu F)\)（Lambek 引理）。
- **是不动点 ⇏ 是初始代数**：还需要万有性质（唯一 `cata`）。更大的不动点可以满足 \(A \cong F A\) 却不是初始的。
- 在许多友好设定下，初始代数的载体即（序／逼近意义下的）**最小不动点**；终余代数对应**最大不动点**。

### 初始代数给出递归 ADT

1. 把 `data` 的一层形状写成多项式函子 `f`（和 = 多构造器，积 = 字段；递归位换成参数 `r`）。
2. 递归类型的指称是 \(\mu F\)（`Fix f`）。
3. 构造器 = \(\mathrm{in}\) ∘ 注入；结构化递归 / fold = \(\operatorname{cata}\)。

例：

```haskell
data ListF e r = NilF | ConsF e r   -- ≅ 1 + e × r
-- List e ≅ Fix (ListF e) ≅ μ(ListF e)
```

「代数数据类型」与「初始代数」是同一件事的语法层与范畴层。

> 现实中的惰性 Haskell 可出现无限值，严格说混有余代数方向；「初始代数给出 ADT」通常指有限规范项与归纳视角。

---

## 5. 初始代数、自由代数、Monad：三者关系

### 公式层面（你的直觉成立的部分）

造载体用的是同一套「取初始代数／最小不动点」技术，差别是塞进公式的函子：

```text
μF            =  μY.  F Y           -- Fix f：递归 ADT
Free_F(X)     =  μY.  X + F Y       -- Free f a：带生成元的自由 F-代数
```

### 概念层面（还差的半步）

| | \(\mu F\) | \(\mathrm{Free}_F(X)\) |
|--|-----------|-------------------------|
| 是谁的初始代数 | \(F\) | \(X + F(-)\) |
| 外部生成元 | 无（\(X = 0\)） | 有（叶子可来自 \(X\)，如 `Pure a`） |
| 随 \(X\) 变化 | 单个类型 | 可打包成**自由 monad** |

修正后的记忆句：

> **初始代数 = 无外部生成元的自由代数；其载体就是单纯由 \(F\) 长出的递归结构 \(\mu F\)。**

注意：不是「没有载体」——载体仍在，就是 \(\mu F\) 本身。`Lit Int` 这类叶子是 \(F\) **签名内**的常量分支，不算外部生成元 \(X\)；外部生成元对应公式里的 \(X+\) / `Pure a`。

### Monad 不是「初始代数的下属应用」

- **自由 monad `Free f`**：把 \(X \mapsto \mathrm{Free}_F(X)\) 打成 monad——紧贴自由代数这条线。
- **一般 monad**（`[]`、`State`…）：来自任意伴随或直接给出，不都等于某个 \(\mu Y.(X+FY)\)；其代数是 EM 代数（如 `[]` ↔ Monoid），是更广的一层。

```text
F-代数范畴的初始对象          →  μF           （递归 ADT / Fix f）
X+F 的初始对象                →  Free_F(X)    （自由 F-代数）
X ↦ Free_F(X) 做成的 monad    →  Free F       （自由 monad）
任意 monad T 的自由代数 on X  →  (T X, join)  （EM 意义下的自由）
任意 monad T 的全部代数       →  EM(T)        （如 [] ↦ Monoid）
```

---

## 6. 总图

```text
ADT / Fix f
    ↑ 初始代数（无外部生成元）
F-代数  f a -> a
    │
    │ 当 m = Free f 时一一对应
    ↓
Monad 代数  m a -> a
    │
    │ 特例 m = []
    ↓
Monoid 等抽象代数类型类

旁路：Free_F(X) = μ(X+F) ──随 X──▶ 自由 monad Free F
```

读代码口令：

- `f a -> a`、`cata`、`Fix` → F-代数 / 初始代数
- `m a -> a` + `return`/`join` 法则 → monad 代数
- `<>`、`mempty`、`mconcat` → 抽象代数（常兼为 EM 代数）
- `Free`、`foldFree`、`foldMap` → 自由代数：先语法后解释

---

## 7. 讨论中达成的简短结论

1. Algebra 与 monad 的要紧关系：monad 规定如何组合；该 monad 的代数规定如何解释／消去。
2. `Free f` 使「一层 F-代数」与「整树 monad 代数」信息量相同。
3. List 有两条线：`Free ((,) e)`（异型日志 + 种子）与 `[]` 的 EM 代数（monoid）；不要混。
4. 初始代数 ⇒ 不动点（Lambek）；不动点 ⇏ 初始代数。
5. 递归 ADT ≅ 对应多项式函子的初始代数。
6. \(\mu F\) 与 \(\mathrm{Free}_F(X)\) 是**不同函子**的初始代数，公式差一个 \(X+\)；不是同一概念的两种写法。
7. 初始代数 ≈ 无外部生成元的自由代数（载体 = 纯递归结构）；一般 monad 不能收成「初始代数的一个应用」。

---

## 参考编码速查

```haskell
data Free f a = Pure a | Free (f (Free f a))

foldFree :: Functor f => (f a -> a) -> Free f a -> a
foldFree φ (Pure x) = x
foldFree φ (Free t) = φ (fmap (foldFree φ) t)

newtype Fix f = Fix (f (Fix f))

cata :: Functor f => (f a -> a) -> Fix f -> a
cata φ (Fix fr) = φ (fmap (cata φ) fr)
```

---

*整理自对话讨论，便于个人查阅；术语以范畴论／Haskell 习惯用法为准。*
