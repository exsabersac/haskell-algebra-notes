# 例子与 Monad

两个最常用的幺半范畴，以及「Monad = monoid 对象」这句口号的落点。

## 1. \((\mathbf{Set},\times,1)\)

- 对象：集合；箭头：函数
- 张量：笛卡尔积 \(A\otimes B = A\times B\)
- 单位：单点集 \(1=\{*\}\)
- \(\alpha,\lambda,\rho\)：标准的重新括号／丢掉 `*` 的双射

这是对称幺半范畴。集合上的 monoid，恰是该幺半范畴里的 **monoid 对象**（见下）。

## 2. \((\mathrm{End}(\mathcal{C}),\circ,\mathrm{Id})\)

- 对象：自函子 \(F:\mathcal{C}\to\mathcal{C}\)
- 张量：复合 \(F\otimes G = F\circ G\)
- 单位：恒等函子 \(\mathrm{Id}\)
- 结合／单位：复合的结合与单位（在自然同构意义下；严格化后可当等式）

Haskell 里 `End` 的直觉就是 `Type -> Type` 上的函子，张量是 `Compose`。

## 3. Monoid 对象（一般定义）

在幺半范畴 \((\mathcal{C},\otimes,I)\) 里，一个 **monoid 对象** 是 \((M, \eta, \mu)\)：

\[
\eta : I \to M, \qquad \mu : M \otimes M \to M
\]

使单位与结合图交换（用 \(\alpha,\lambda,\rho\) 填括号）。  
在 \((\mathbf{Set},\times,1)\) 里这正好是普通 monoid：`mempty` / `(<>)`。

## 4. Monad = \((\mathrm{End},\circ,\mathrm{Id})\) 里的 monoid 对象

取 \(T:\mathcal{C}\to\mathcal{C}\)，则 monoid 对象数据是：

| 范畴论 | Haskell |
|--------|---------|
| \(\eta : \mathrm{Id} \to T\) | `return` / `pure` |
| \(\mu : T \circ T \to T\) | `join` |
| 单位律 | `join . return = id` 等 |
| 结合律 | `join . join = join . fmap join` |

短素描：

```haskell
return :: a -> t a                 -- η
join   :: t (t a) -> t a           -- μ

-- 单位（示意）
join . return      = id
join . fmap return = id

-- 结合
join . join        = join . fmap join
```

`>>=` 可由 `join` 与 `fmap` 恢复：`m >>= k = join (fmap k m)`。因此「monad 是端函子范畴里的幺半群」不是比喻，而是 monoid 对象的特例。

## 5. `Compose` ≠ `Product` / `Sum`

| | `Compose f g` | `Product f g` / `Sum f g` |
|--|---------------|---------------------------|
| 运算 | 函子复合（\(\circ\)） | 逐点积／和（形状算术） |
| 所在口号 | 幺半范畴张量；Monad 的乘法 | 多项式签名；效果／构造器拼装 |
| 单位 | `Identity` | 常函子一侧的「1」等，另一套故事 |

拼效果语言用 `Sum`；谈 monad 定律用 `Compose`／`join`。详见 [函子范畴上的代数](../函子组合/函子范畴上的代数.md)。

## 一句话

\((\mathbf{Set},\times,1)\) 给普通 monoid；\((\mathrm{End},\circ,\mathrm{Id})\) 给 Monad。同一句「monoid 对象」，张量换了，含义就从 `<>` 换成 `join`。
