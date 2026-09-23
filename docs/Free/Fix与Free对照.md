# 并排：`Fix ExprF`（无生成元）与 `Free ExprF String`（有生成元）

用同一个 `ExprF`，把「无生成元」和「有生成元」并排看清楚。

## 共用的一层形状

故意让函子**只有运算、没有常量叶**：

```haskell
data ExprF r
  = AddF r r
  | NegF r
  deriving Functor
```

两种树：

```haskell
newtype Fix f = Fix (f (Fix f))

type ClosedExpr = Fix ExprF          -- μ ExprF，无外部生成元
type OpenExpr a = Free ExprF a       -- μ(a + ExprF)，生成元类型 a
```

## 无生成元：`Fix ExprF`

叶子只能来自……但 `ExprF` 里**根本没有**像 `Lit` 那样的无递归分支。于是在 Set 上，`μ ExprF` 的有限元素集其实是空的：每个 `Add`/`Neg` 都还要子树。

实务上人们会给 ADT 加上 `Lit`：

```haskell
data ExprF' r = LitF Int | AddF' r r | NegF' r
type Expr = Fix ExprF'    -- 现在有限树存在：Lit 是签名内的常量叶
```

要点：**闭项的叶子必须写进函子签名**；那不是外部生成元，是 \(F\) 自带的常量构造器。

## 有生成元：`Free ExprF String`

生成元类型取 `String`，表示变量名。

```haskell
-- Pure "x"                              变量 x
-- Free (NegF (Pure "x"))                -x
-- Free (AddF (Pure "x") (Pure "y"))     x + y
-- Free (AddF (Free (NegF (Pure "x"))) (Pure "y"))
--                                       (-x) + y
```

画成树：

```text
Free ExprF String                     Fix ExprF'（对照：Lit 在签名里）

      Add                                   Add
     /   \                                 /   \
  Pure   Pure                           Lit 2  Lit 3
   "x"    "y"

  叶子 = 外部生成元                     叶子 = F 自带的 Lit
```

`Free` 版是「先留变量，后赋值」：

```haskell
open :: Free ExprF String
open = Free (AddF (Pure "x") (Pure "y"))
```

## 生成元怎样被用掉：先换叶，再按代数折

```haskell
subst :: (a -> b) -> Free f a -> Free f b
subst = fmap

foldFree :: Functor f => (f b -> b) -> Free f b -> b

evalWith :: (String -> Int) -> Free ExprF String -> Int
evalWith env = foldFree step . fmap env
  where
    step (AddF x y) = x + y
    step (NegF x)   = negate x

-- evalWith (\v -> if v == "x" then 2 else 3) open  ==  5
```

流程：

```text
Add(Pure "x", Pure "y")
        │ fmap env
        ▼
Add(Pure 2, Pure 3)          -- 生成元变成具体 Int
        │ foldFree step
        ▼
       5                     -- 运算按代数消去
```

没有生成元的 `Fix ExprF'` 则一步 `cata` 即可，因为叶上已经是 `Lit Int`。

## 和 `>>=` 的关系（生成元当接缝）

```haskell
bindExample =
  Free (AddF (Pure "x") (Pure "y"))
    >>= \v ->
      if v == "x"
        then Free (NegF (Pure "x"))   -- 把 "x" 换成 -x
        else Pure v                  -- "y" 仍当叶子

-- 得到：(-x) + y
```

`>>=`：**遍历树，把每片生成元叶子替换成 `k` 返回的新子树**。

## 对照表

| | `Fix ExprF'`（闭 ADT） | `Free ExprF String` |
|--|------------------------|---------------------|
| 不动点公式 | \(\mu Y.\,ExprF'\,Y\) | \(\mu Y.\,String + ExprF\,Y\) |
| 叶子来源 | 签名内 `Lit Int` | 外部生成元 `Pure "x"` |
| 典型含义 | 已写死的表达式 | 带变量的表达式图式 |
| 解释 | 一次 `cata` | 先 `fmap`／赋值，再 `foldFree` |
| 能否 `>>=` 换叶 | 不自然 | 原生支持 |

## 一句话

`Fix` 把叶子焊在函子签名里；`Free` 把叶子参数化成 `a`，所以同一套 `Add`/`Neg` 形状能长出「开口」的树。
