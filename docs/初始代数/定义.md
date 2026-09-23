# 初始代数的定义

**初始代数**是某个函子 `f` 的 F-代数范畴里的初始对象：一份「最自由」的代数，使得任意别的 F-代数都有唯一一条从它出发的同态。

## 正式定义

先固定一个范畴 \(\mathcal{C}\)（Haskell 里多半想成类型与函数）和自函子 \(F : \mathcal{C} \to \mathcal{C}\)。

一个 **\(F\)-代数** 是一对 \((A, \varphi)\)，其中 \(A\) 是对象，\(\varphi : F A \to A\)。

两个 \(F\)-代数 \((A, \varphi)\)、\((B, \psi)\) 之间的 **同态** 是箭头 \(h : A \to B\)，使下图交换：

\[
h \circ \varphi = \psi \circ F h
\]

也就是「先按 \(A\) 的结构再翻译」等于「先翻译一层形状再按 \(B\) 的结构」。

**初始 \(F\)-代数** 是某个 \(F\)-代数 \((\mu F, \mathrm{in})\)，其中

\[
\mathrm{in} : F(\mu F) \to \mu F
\]

满足：**对任意** \(F\)-代数 \((A, \varphi)\)，存在**唯一**的同态

\[
\operatorname{cata}\varphi : \mu F \to A
\]

使得

\[
\operatorname{cata}\varphi \circ \mathrm{in} = \varphi \circ F(\operatorname{cata}\varphi)
\]

「初始」三个字指的就是这条**唯一存在的同态**（初始对象的万有性质），不是指「最先定义出来」这种时间顺序。

## Haskell 编码

```haskell
newtype Fix f = Fix { unFix :: f (Fix f) }

-- in  ≈ Fix
-- out ≈ unFix
cata :: Functor f => (f a -> a) -> Fix f -> a
cata φ = φ . fmap (cata φ) . unFix
```

`Fix f` 扮演 \(\mu F\)；`Fix` 扮演 \(\mathrm{in}\)；`cata φ` 就是那条唯一同态。

## 用列表把定义读成白话

取 \(F R = 1 + E \times R\)（Haskell：`ListF e r = NilF | ConsF e r`）。

- 初始代数的载体是 \([E]\)（有限列表）。
- \(\mathrm{in}\) 把 `NilF` 变成 `[]`，把 `ConsF x xs` 变成 `x : xs`。
- 任意别的代数是「种子 + 一步」：`φ :: ListF e b -> b`。
- 唯一同态 `cata φ :: [e] -> b` 就是用这套种子和一步去折整条列表——万有性质把折法钉死了。

「初始 / 最自由」的含义是：列表只含由 `[]` 与 `:` 搭起来的项，没有被事先解释成数字、字符串或别的东西；解释完全由你选的目标代数 \(\varphi\) 经 `cata` 唯一伸出。

## 和终余代数的对偶

对偶地，**终 \(F\)-余代数** \((\nu F, \mathrm{out})\)（\(\mathrm{out} : \nu F \to F(\nu F)\)）对任意余代数有唯一同态伸入它，对应 unfold / 共代数。有限列表是初始代数；无限流等往往落在终余代数一侧。同一函子两边可以很不一样。

## 一句话

初始代数 = \(F\)-代数范畴的初始对象 \((\mu F, \mathrm{in}: F(\mu F)\to\mu F)\)，其核心不是「长什么样」，而是：**到任意代数有且仅有一条同态**；在 Haskell 里这条同态就是 `cata` / fold，载体常实现为 `Fix f`。
