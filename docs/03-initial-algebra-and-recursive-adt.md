# 「初始代数恰好给出递归 ADT」

这句话的意思是：**你在 Haskell 里写的递归 `data`，在范畴图像里就是某个多项式函子 \(F\) 的初始代数 \(\mu F\)**——构造器来自 \(\mathrm{in}\)，模式匹配／`fold` 来自唯一同态 \(\operatorname{cata}\)。

## 1. ADT 的一层形状 = 一个函子 \(F\)

代数数据类型用**和**（多个构造器）与**积**（构造器参数）搭起来。把递归出现的位置抠成参数 `r`，剩下的就是函子。

**非递归例子（热身）**

```haskell
data Bool = False | True
-- 无递归。对应 F r = 1 + 1（两个无参构造器），与 r 无关。
-- 此时「初始代数」就是 1+1 本身，载体即 Bool。
```

**列表**

```haskell
data List e = Nil | Cons e (List e)

data ListF e r = NilF | ConsF e r
  deriving Functor
-- ListF e r  ≅  1  +  (e × r)
```

**二叉树**

```haskell
data Tree e = Leaf e | Node (Tree e) (Tree e)

data TreeF e r = LeafF e | NodeF r r
-- TreeF e r  ≅  e  +  (r × r)
```

**表达式**

```haskell
data Expr
  = Lit Int
  | Add Expr Expr
  | Neg Expr

data ExprF r
  = LitF Int
  | AddF r r
  | NegF r
-- ExprF r  ≅  Int  +  (r × r)  +  r
```

规律：

- 每个构造器 → 和类型里的一个分支
- 构造器里的非递归字段 → 原样放进该分支（常量函子）
- 构造器里的递归字段 → 换成 `r`
- 整个 `data` 的「一层」→ 函子 `f`

这就是 ADT 里 “algebraic” 和 F-代数的接缝：**类型声明在描述 \(F\) 的多项式形状**。

## 2. 递归 ADT = 该函子的初始代数

递归定义要求：

```text
List e  ≅  ListF e (List e)
Tree e  ≅  TreeF e (Tree e)
Expr    ≅  ExprF Expr
```

这正是不动点方程 \(X \cong F X\)。在「有限项、Set 上多项式函子」等常见设定下，**满足方程且具有初始性的那个解**就是递归 ADT 的含义：

\[
\texttt{List e} \;=\; \mu(\texttt{ListF e})
\]

Haskell 里可以显式写成：

```haskell
newtype Fix f = Fix (f (Fix f))

type List e = Fix (ListF e)
type Expr   = Fix ExprF
```

也可以继续用熟知的 `data List e = Nil | Cons e (List e)`——那只是把 `Fix` 和构造器内联展开后的语法糖；数学对象仍是 \(\mu F\)。

初始代数的结构映射是：

\[
\mathrm{in} : F(\mu F) \to \mu F
\]

在编码里就是 `Fix`：

```haskell
inList :: ListF e (List e) -> List e
inList = Fix
-- 若用普通 data：
-- inList NilF          = Nil
-- inList (ConsF x xs)  = Cons x xs
```

## 3. 构造器从哪里来

普通 ADT 的构造器，等于「先打进 \(F\) 的某个分支，再应用 \(\mathrm{in}\)」。

```haskell
nil :: List e
nil = inList NilF

cons :: e -> List e -> List e
cons x xs = inList (ConsF x xs)

lit :: Int -> Expr
lit n = Fix (LitF n)

add :: Expr -> Expr -> Expr
add x y = Fix (AddF x y)
```

所以：**构造器不是额外魔法，而是初始代数的 \(\mathrm{in}\) 配上和类型的注入。**  
这也解释了为什么构造出来的值都是「有限层」树：初始代数／最小不动点只含有限次应用 \(\mathrm{in}\) 得到的项。

## 4. 模式匹配与 fold = 唯一同态 `cata`

初始性说：任意 F-代数 \(\varphi : F A \to A\)，有唯一同态 \(\operatorname{cata}\varphi : \mu F \to A\)。

```haskell
cata :: Functor f => (f a -> a) -> Fix f -> a
cata φ (Fix fr) = φ (fmap (cata φ) fr)
```

这正是你对递归 ADT 做的系统性模式匹配／折叠：

```haskell
evalF :: ExprF Int -> Int
evalF (LitF n)   = n
evalF (AddF x y) = x + y
evalF (NegF x)   = negate x

eval :: Expr -> Int
eval = cata evalF
```

普通手写递归与 `cata evalF` 同构：外层匹配构造器 = 匹配 `ExprF` 的分支；递归调用子树 = `fmap (cata φ)`。  
**唯一性**保证：只要你承认「同态」（与构造器相容），这种折法只有一种——这就是「递归 ADT 上的结构递归原则」。

列表上的 `foldr` 同理：`foldr f z` 对应代数

```haskell
φ NilF        = z
φ (ConsF x y) = f x y
```

## 5. 整条对应表

| ADT 说法 | 初始代数说法 |
|----------|----------------|
| `data` 一层形状（构造器+字段） | 函子 \(F\) |
| 递归类型本身 | 载体 \(\mu F\) |
| 构造器 `Nil` / `Cons` / `Add`… | \(\mathrm{in}\) ∘ 注入 |
| 类型方程 `T ≅ …T…` | \(\mu F \cong F(\mu F)\)（Lambek） |
| `fold` / 结构化递归 | \(\operatorname{cata}\varphi\) |
| 「怎样解释构造器」 | 目标代数 \(\varphi : F A \to A\) |
| 有限树／有限列表 | 初始代数里的元素 |

因此说「**初始代数恰好给出递归 ADT**」：ADT 声明定义了 \(F\)；递归类型的指称是 \(\mu F\)；构造与消除规则分别是 \(\mathrm{in}\) 与 \(\operatorname{cata}\)。

## 6. 边界说明

- **无递归的 ADT**（如 `Bool`）：初始代数退化成「和与积算出的那一层」，没有跨多层的 `cata` 问题。
- **`Free f a`**：是「\(f\) 的自由 monad」，不是「\(f\) 的初始代数」。\(\mu f\) 相当于无额外 `Pure` 叶子；`Free f a` 是叶子来自 `a`、节点来自 `f`。
- **Haskell 现实**：惰性允许「无限」值，严格说更像混进了余代数方向；讨论「初始代数给出 ADT」时，通常指**有限、完全的规范项**与类型的归纳视角。

## 7. 一句话

递归 ADT 的声明在写多项式函子 \(F\)；类型本身是 \(F\) 的初始代数 \(\mu F\)；构造器是 \(\mathrm{in}\)，折叠是唯一的 \(\operatorname{cata}\)。所以「代数数据类型」和「初始代数」不是两套隐喻，而是同一件事的语法层与范畴层。
