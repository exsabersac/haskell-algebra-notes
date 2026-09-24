# 自由幺半群与 ListF 代数

澄清两套概念：**自由 monoid** \(\mathrm{FreeMon}(X)\) 与**初始 \(\mathrm{ListF}\,X\)-代数**；以及 monoid 如何诱导 ListF-代数、逆向是否总成立、自由 monoid 的 UP 双射。  
术语保留精确英文：FreeMon、ListF、UP、foldMap、cata、fromMonoid、EM。

相关：[自由幺半群与列表](自由幺半群与列表.md) · [List的EM代数与Monoid](List的EM代数与Monoid.md) · [常见组合](../函子组合/常见组合.md) · [与递归ADT](../初始代数/与递归ADT.md) · [`FunctorCombo/Demo.hs`](../../src/FunctorCombo/Demo.hs)

---

## 1. 两套概念：FreeMon vs 初始 ListF-代数

### 定义所在范畴不同

| | 自由 monoid \(\mathrm{FreeMon}(X)\) | 初始 \(\mathrm{ListF}\,X\)-代数 |
|--|-------------------------------------|--------------------------------|
| 所在范畴 | \(\mathbf{Mon}\) | \(\mathrm{Alg}(\mathrm{ListF}\,X)\) |
| UP 说什么 | 任意 \(f:X\to U(M)\) **唯一**扩展为 **monoid 同态** \(\varphi:[X]\to M\) | 任意 ListF-代数 \(\varphi\) **唯一**存在 **cata** \(\mu\to|\varphi|\) |
| 典型折叠 | `foldMap f` | `cata φ` |

作为**概念／定义**它们不一样：一个谈 Mon 里的自由对象；一个谈 Alg(ListF) 里的初始对象。

### 对此特殊 \(F\)，载体重合

取 \(F = \mathrm{ListF}\,X \;\cong\; 1 + X\times(-)\)。则

\[
U\bigl(\mathrm{FreeMon}(X)\bigr)
\;\cong\;
\bigl|\mu(\mathrm{ListF}\,X)\bigr|
\;\cong\;
[X]
\]

**同一模型，两副眼镜**：载体都是列表；一副看 monoid 同态，一副看一层 `NilF`/`ConsF` 的解释。

### 桥：`foldMap` ≡ `cata (fromMonoid …)`

```haskell
-- foldMap f  ≡  cataList (fromMonoid f)
```

（`fromMonoid` 见下节。）把「经 \(f\) 进 monoid 再 `<>`」写成一层 ListF-代数，再 `cata`，即得 `foldMap`。

### 换 \(F\) 就拆开

| 例子 | 是什么 | 不是什么 |
|------|--------|----------|
| \(\mu Y.\,1+Y \;\cong\;\mathbb{N}\) | 初始代数（自然数） | **不是**某个集合上的自由 monoid |
| \(\mathrm{Free}\,f\,a = \mu Y.\,a + f\,Y\) | 自由 \(f\)-代数 | **一般不是**自由 monoid |

只有「\(1+X\times(-)\)」这一形状，才让自由 monoid 的遗忘载体与初始 ListF-代数载体重合。概览仍见 [自由幺半群与列表](自由幺半群与列表.md)。

---

## 2. Monoid 诱导的 ListF-代数：`fromMonoid`

```haskell
data ListF x r = NilF | ConsF x r

fromMonoid :: Monoid m => (x -> m) -> (ListF x m -> m)
fromMonoid f NilF       = mempty
fromMonoid f (ConsF x m) = f x <> m

-- foldMap f ≡ cataList (fromMonoid f)
```

| | 一般 ListF-代数 | monoid 诱导 |
|--|-----------------|-------------|
| 数据 | 任意 \((e,\mathrm{step})\)，即任意 \(\varphi:\mathrm{ListF}\,x\,A\to A\) | \(e=\mathrm{mempty}\)，\(\mathrm{step}\,x = (f\,x\,\langle\rangle)\)，即 \(\varphi=\mathrm{fromMonoid}\,f\) |
| 是否来自 monoid | **否**——任意一步解释即可 | **是**——由 `Monoid m` 与 \(f:x\to m\) 产生 |

**并非每个 ListF-代数都来自 monoid。** 例如取 \(e\) 与 \(\mathrm{step}\) 使结合／单位失败，仍是合法的 \(\mathrm{Alg}(\mathrm{ListF}\,x)\) 对象，只是不能写成 `fromMonoid`。

可运行 `ListF` / `cata` 草图：[FunctorCombo/Demo.hs](../../src/FunctorCombo/Demo.hs)。

---

## 3. `fromMonoid` 的逆向

### （1）总是可以：\(\varphi \mapsto (e,\mathrm{step})\)

任意 ListF-代数都可拆成对：

```haskell
-- 示意
toPair   φ = (φ NilF, \x a -> φ (ConsF x a))
fromPair (e, step) NilF       = e
fromPair (e, step) (ConsF x a) = step x a
```

这一层只是数据同构，**不**声称得到 monoid。

### （2）要成为 monoid 诱导：需要连贯条件

设 \(e=\varphi\,\mathrm{NilF}\)，\(f\,x=\varphi(\mathrm{ConsF}\,x\,e)\)。若希望 \(\varphi=\mathrm{fromMonoid}\,f\)，需要：

- \(\varphi(\mathrm{ConsF}\,x\,a) = f\,x\,\langle\rangle\,a\)（对相关的 \(a\)），且
- \(\langle\rangle\) 是真正的 monoid 乘法（结合、单位为 \(e\)）。

仅从一层 ListF 结构出发，完整的 \(\langle\rangle:A\times A\to A\) **可能欠定**：除非 \(A\) 由 \(\mathrm{im}\,f\)（及单位）生成，否则「只对列表形状出现的元素」定出的运算，不必唯一延拓到整个 \(A\times A\)。

### （3）干净的逆向在 EM 层，不在 ListF 层

「任意合法 \(\alpha:[A]\to A\) ↔ monoid」的双射，发生在 **列表 monad 的 EM 代数** 上，而不是在随意的 ListF-代数上。详见 [List的EM代数与Monoid](List的EM代数与Monoid.md)。

对照：下一节自由 monoid 的 UP **逆向对任意 monoid 同态总成立**——与此处「ListF → monoid」逆向不必总成立，形成对比。

---

## 4. UP = 全体性质；自由 monoid 的双射

**UP（universal property）**：「对任意…存在唯一…使…」的刻画；自由构造的**唯一扩展**。

自由 monoid 的 UP 即双射

\[
\mathrm{Hom}_{\mathbf{Set}}\bigl(X,\,U(M)\bigr)
\;\cong\;
\mathrm{Hom}_{\mathbf{Mon}}\bigl([X],\,M\bigr)
\]

### 正向 \(\Phi\) 与反向 \(\Psi\)

```text
Φ : f ↦ foldMap f          -- Set 箭头 → monoid 同态
Ψ : φ ↦ φ ∘ η              -- monoid 同态 → Set 箭头；η x = [x]
```

```haskell
-- Φ
foldMap :: Monoid m => (x -> m) -> [x] -> m

-- Ψ
-- ψ φ = φ . (:[])          -- φ ∘ η
```

### 反向**总是**对任意 monoid 同态成立

- 复合 \(\varphi\circ\eta\) **总有定义**（同态的载体函数可与 \(\eta\) 复合）。
- 每个列表都是单例的积：\([x_1,\ldots,x_n]=[x_1]{++}\cdots{++}[x_n]\)，故 \(\varphi=\mathrm{foldMap}(\varphi\circ\eta)\)。
- 因而 \(\Phi\circ\Psi=\mathrm{id}\)，\(\Psi\circ\Phi=\mathrm{id}\)。

**对比**：§3 的「ListF-代数 → monoid」逆向**不总是**；UP 这一侧的 \(\Psi\) **总是**。不要把两层逆向混为一谈。

---

## 5. 已澄清结论

1. FreeMon 与初始 ListF-代数：**概念／UP 不同范畴**；对 \(F=\mathrm{ListF}\,X\cong 1+X\times(-)\)，**载体同构** \([X]\)——同一模型两副眼镜。
2. 桥：`foldMap f ≡ cata (fromMonoid f)`。
3. 换 \(F\) 则拆开（\(\mathbb{N}=\mu Y.1+Y\) 非自由 monoid；`Free f a` 一般非自由 monoid）。
4. `fromMonoid`：monoid + \(f\) → 特殊 ListF-代数；一般 ListF-代数 = 任意 \((e,\mathrm{step})\)，**不都**来自 monoid。
5. ListF → monoid：总可拆成 \((e,\mathrm{step})\)；成 monoid 诱导需连贯，且完整 \(\langle\rangle\) 可能欠定；干净逆向在 EM。
6. UP 双射：\(\Phi=\)`foldMap`，\(\Psi=\varphi\mapsto\varphi\circ\eta\)；\(\Psi\) 对任意 monoid 同态总成立，与 ListF 逆向对照。

### 易混点

| 易混 | 澄清 |
|------|------|
| FreeMon = 初始 ListF？ | 概念否；此 \(F\) 下载体是。 |
| 每个 ListF-代数来自 monoid？ | 否；仅 `fromMonoid` 形才是。 |
| ListF 逆向 = UP 的 \(\Psi\)？ | 否。前者不总成 monoid；后者对任意 monoid 同态总有 \(\varphi=\mathrm{foldMap}(\varphi\circ\eta)\)。 |
| \(\mathbb{N}\) / `Free f a` 也是自由 monoid？ | 一般否；见 §1「换 \(F\)」。 |

### 另见

- [自由幺半群与列表](自由幺半群与列表.md) — \(\mathrm{FreeMon}(X)\cong[X]\) 概览；`foldMap`；对象 vs \(\mathrm{EM}([])\simeq\mathrm{Monoid}\)
- [List的EM代数与Monoid](List的EM代数与Monoid.md) — EM([])≃Mon；与 ListF 对照表
- [常见组合](../函子组合/常见组合.md) — \(\mu Y.\,1+e\times Y\)
- [与递归ADT](../初始代数/与递归ADT.md) — ListF 与 \(\mu\)
- [`src/FunctorCombo/Demo.hs`](../../src/FunctorCombo/Demo.hs) — ListF / cata 草图
