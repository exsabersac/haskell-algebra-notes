# 实现思路与 finitary：从签名到 `return` / `join`

这篇把 Lawvere theory、finitary monad 和可运行的 Haskell 草图串成一条实现路线。它不是另起一套定义，而是把 [与finitary-monad](与finitary-monad.md)、[多种finitary-monad](多种finitary-monad.md) 和 Demo `[7]`–`[12]` 中已经出现的对象按「怎么落地」重排。

---

## 1. `finitary` 到底说什么

这里的 **finitary** 不是「所有东西都是有限的」，而是说：每个元素都由某个**有限 arity** 的输入槽和一个形状／运算决定；函子或 monad 在 `Set` 上的行为可以由有限集上的行为经 coend 重建：

\[
F a \cong \int^{n} a^n \times F n,
\qquad
T_{\mathbf L}a \cong \int^{n} a^n \times \mathbf L(n,1).
\]

在第二个公式里，`a^n` 是填入有限个槽的内容，`L(n,1)` 是 `n` 元运算（形状）；coend 把换标签、投影和复制造成的重复表示识别掉。对 monad 还可记住：

\[
\mathbf L(n,1) \cong Tn.
\]

### 三个容易混的词

| 词 | 这里真正关心的是什么 | 不应读成什么 |
|---|---|---|
| **finitary** | 运算／项只需要有限 arity；整体由有限集上的行为决定 | 不是说某个 `Ta`、某个理论或运算总数一定有限 |
| **finite** | 某个集合、载体或 arity 的基数有限 | 不等于 finitary；例如 `List a` 可以是无限集合，但每个列表是有限项 |
| **finitely presented** | 用有限的 generators 和 relations 描述一个 presentation | 不是 finitary 的同义词；finitary 讨论有限 arity，有限表示还要求 presentation 本身有限 |

所以，一个 finitary Lawvere theory 可以有无穷多个由有限 arity 产生的态射；反过来，「有限」也不会自动给出这里需要的 finitary monad 互译。本文只采用经典的 finitary 对应：

```text
Lawvere theory L  ── free ⊣ forgetful ──▶  finitary monad T_L
finitary monad T  ── Kleisli^op|fin ────▶  Lawvere theory L
```

**Cont 不在这条线里**：`Cont r a = (a -> r) -> r` 依赖任意高阶输入，不能按有限 `n` 的 `a^n × T n` coend 展开，因此没有经典的 finitary Lawvere theory 对应。见 [与finitary-monad](与finitary-monad.md) §4 和 [多种finitary-monad](多种finitary-monad.md) §7。

---

## 2. 五步实现 pipeline

把「一个代数效果怎样变成可运行的 monad」写成五步：

```text
signature
    │  运算符号及 arity，加上 equations
    ▼
L(n,1)
    │  闭合于 projection / diagonal / composition，并按定律识别
    ▼
T a
    │  ∫^n a^n × L(n,1)，有限槽位填入 a
    ▼
return / join
    │  生成元嵌入；项的项 flatten／substitution
    ▼
model eval
       把理论中的运算解释到具体 carrier 上
```

### Step 1 — signature

先写 `n`-ary operations：在 Lawvere 方向上是 `n → 1`。例如 monoid 有

- `η : 0 → 1`（nullary unit）；
- `μ : 2 → 1`（binary multiplication）；
- equations 是 associativity 和左右 unit laws。

signature 只给出语法入口；等式会在后面的态射相等中体现。

### Step 2 — 得到 `L(n,1)`

`L` 以 `F^op` 的 finite-product skeleton 为骨架，所以 projection、diagonal 等 basic product operations 本来就在那里。把 signature 的 interesting morphisms 加进去，再用 composition 和 equations 闭合，就得到全部派生的 `n`-ary operations：

```text
L(n,1) = 从 n 个输入到一个输出的全部理论项／态射
```

例如在 `L_Mon` 中，`L(2,1)` 的元素是两个生成元的 words：`ε, A, B, AA, AB, ...`。

### Step 3 — 组装 `T a`

把一个理论 operation 和一组实际输入配对：

\[
T a \cong \int^{n} a^n \times L(n,1).
\]

`a^n` 提供内容，`L(n,1)` 提供形状／运算；coend 负责把只是换了有限标签的两种写法视为同一个项。于是 `T a` 是「由 `a` 中生成元生成的自由项／自由代数元素」。

### Step 4 — 实现 `return` / `join`

- `return` 把一个生成元放进最简单的项：对 List 是 singleton，对 Writer 是 `(x,mempty)`。
- `join` 把「项的项」做 flatten，也就是 substitution：List 用 `concat`，Writer 合并两层日志。

因此 `return` / `join` 不是额外的副作用故事，而是自由项的 unit 和 substitution 的程序接口。Kleisli composition 正是「先产生项，再把项交给下一步并拼接／代入」。

### Step 5 — model eval

给定一个 model `M : L → Set`（保有限积），每个 `f : L(n,1)` 被解释成 carrier 上的函数 `M(1)^n → M(1)`；把生成元送到载体，再按 composition 求值，就得到具体结果。等价的 monad 说法是 EM algebra 的结构映射：

\[
\alpha : T a \to a.
\]

所以 `Lawvere` 层负责「有什么项、哪些项相等」，`model / EM` 层负责「把项算成什么值」。例如 `foldMap` 把 List 中的自由 word 求值到 `(Sum,+)` 或 `([a],++,[])`。

### 三层对照

| layer | 核心对象 | 做什么 | 典型接口 |
|---|---|---|---|
| **Theory** | `L`，尤其 `L(n,1)` | 记录有限 arity 的 operations、composition、equations | `n → 1`；projection / `μ` / `η`；word substitution |
| **Monad** | `T a = ∫^n a^n × L(n,1)` | 生成自由项，并提供 substitution | `return`、`join`、Kleisli `>=>` |
| **EM / model** | `α : T a → a` 或 `M : L → Set` | 在具体 carrier 上解释并求值 | `foldMap`、`mconcat`、具体 `Writer` action |

对来自 Lawvere theory 的 monad，有 `EM(T_L) ≃ Mod(L,Set)`；不要把 Kleisli 和 EM 混在一起：前者重建 theory 的运算空间，后者描述如何求值。

---

## 3. Writer：五步走完一个例子

固定一个 monoid `W`。Writer 的效果是「选一个输入槽，并写入一段 `w ∈ W`」。本节沿用 Demo 中的约定：

```haskell
type Writer w a = (a, w)
writerReturn x = (x, mempty)
writerJoin ((x, w1), w2) = (x, w1 <> w2)
```

### 3.1 signature：挑槽 + 写日志

在平凡的 `F^op` 骨架上，对每个 `w ∈ W` 加入写日志的运算族。直观地说，一个操作先从输入中挑一个槽，再附带写入 `w`；`W` 的 monoid unit 和 multiplication 控制空日志与日志合并。

这里的关键不是把 `W` 当成有限集合，而是固定一个 monoid 参数 `W`；`W` 的元素作为效果标签，arity 仍然是有限的。

### 3.2 `L(n,1)`：一个槽位加一段日志

`n` 个输入槽中选一个，再选 `w ∈ W`，所以

\[
L(n,1) \cong n \times W.
\]

一个元素可以写成 `(i,w)`：`i` 是被挑中的变量槽，`w` 是附带日志。`w = mempty` 的情形包含普通 projection。

### 3.3 `T a`：coend 塌成 `(a,W)`

把输入内容 `a^n` 和 `(i,w) ∈ n×W` 配起来，coend 用选中的槽把内容缩成一个 `a`，留下日志：

\[
T a
  \cong \int^{n} a^n \times (n\times W)
  \cong a\times W.
\]

因此 Writer 的 monad 值就是 `(a,w)`：一个结果和一段累积日志。

### 3.4 `return`、`join` 与 Kleisli

自由生成元不写日志，所以

```haskell
return x = (x, mempty)
```

两层 Writer 的 substitution 是

```haskell
join ((x, w1), w2) = (x, w1 <> w2)
```

Kleisli 箭头 `f : a -> Writer w b`、`g : b -> Writer w c` 的桥接写成：

```haskell
f >=> g = \x ->
  let (y, w1) = f x
      (z, w2) = g y
  in (z, w1 <> w2)
```

它和 `join` 是同一个 substitution 机制的两种写法：先把第一步产生的 `b` 交给第二步，再把两层 `W` 用 `(<>)` 合并。Demo `[9]` 用 `Sum Int` 和 `[Char]` 展示了 `return`、`join`、`tell` 的具体结果。

### 3.5 model eval：把日志操作解释到 carrier

在 model / EM 层，不再把 `(a,w)` 当成语法，而是给每个 `w` 一个对 carrier 的解释；抽象地说是

```text
α : a × W → a
```

并满足 `mempty` 对应 identity、`w1 <> w2` 对应连续应用。于是 `(x,w)` 的求值就是：从 `x` 出发，应用 model 对 `w` 的解释。换句话说：

```text
Theory：    (i,w) 是「选槽 i 并写 w」的态射
Monad：     (x,w) 是自由 Writer 值
EM/model：  α (x,w) 是具体 carrier 上的结果
```

本仓库 Demo 的重点是 monad 侧的 `T a ≅ (a,W)`、`return` 和 `join`；其它实例可直接对照 [多种finitary-monad](多种finitary-monad.md) §3。

---

## 4. `L(3,2)`：两个输出就是一对 `⟨f,g⟩`

由于 `2 ≅ 1×1` 且 `L` 保有限积，任意二输出态射都分解成两个一输出态射：

\[
L(3,2) \cong L(3,1)\times L(3,1),
\qquad
h:3\to2 \;=\; \langle f,g\rangle.
\]

这里 `f,g : 3→1` 各自是一个三元运算；`h` 的两个输出分别是 `f` 和 `g`。在 `L_Mon` 中，可以把 `f`、`g` 看成字母表 `{x₁,x₂,x₃}` 上的 words，所以 `L(3,2)` 是一对 words，而不是一个神秘的新种类的 operation。

### composition 就是 word substitution

若 `k:2→1` 是一个用 `x,y` 写的 word，而 `h=⟨f,g⟩:3→2`，则

\[
k\circ\langle f,g\rangle = k[f,g],
\]

即把 `k` 中的 `x` 替换为 `f`、`y` 替换为 `g`，再按 monoid 的 word concatenation 组合。若 `r: m→3` 是 `⟨r₁,r₂,r₃⟩`，则

\[
\langle f,g\rangle\circ r
 = \langle f[r₁,r₂,r₃],\;g[r₁,r₂,r₃]\rangle.
\]

这就是 Lawvere theory 中的 composition：多输出态射逐分量代入，和编程里把一个产生项的函数接到下一步相同。

### 与 List Kleisli 的短桥

对 `T = []`，有限 Kleisli 范畴的箭头 `2→3` 是

```text
2 → T 3 = 2 → List 3
```

也就是「两个输入各自产生一个 `3`-word」，因此是 `List 3 × List 3`。取 opposite 后正好读成

```text
L(3,2) = Kl_[] (2,3) = List 3 × List 3
```

这就是 `⟨f,g⟩` 的 List 版本。Kleisli composition 用 `concatMap` 把 words 代入 words：

```haskell
kleisliCompose f g x = concatMap g (f x)
```

所以「word substitution」是 `L` 的范畴 composition，「`concatMap` / `>=>`」是 List monad 的 Kleisli 表达；两边只是方向取 opposite 后的同一桥接。完整框架见 [与finitary-monad](与finitary-monad.md) §3。

---

## 5. 跳转链接

- 总框架、coend、`Kleisli^op` 与 Cont 边界： [与finitary-monad](与finitary-monad.md)。
- Identity / NonEmpty / **Writer** / Either / finite Reader / finite State： [多种finitary-monad](多种finitary-monad.md)。
- 可运行的 `[7]`–`[12]`： [`src/Lawvere/Demo.hs`](../../src/Lawvere/Demo.hs)，运行 `cabal run algebra-demos`。
- 上游的 `[4]` List、`[5]` Maybe，以及总览对应表： [Lawvere理论 README](README.md)。

一句话：**signature 给出入口，`L(n,1)` 收集有限 arity 的派生运算，coend 组装 `T a`，`return` / `join` 实现生成与 substitution，model / EM 再把自由项求值到具体 carrier；Writer 是 `L(n,1)≅n×W`、`T a≅(a,W)` 的完整示范。**
