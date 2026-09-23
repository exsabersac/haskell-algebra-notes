# 初始代数

1. [定义](定义.md)
2. [与不动点](与不动点.md)
3. [与递归 ADT](与递归ADT.md)
4. [与自由代数和 Monad](与自由代数和Monad.md)

## 可运行代码

- [`src/InitialAlgebra/Demo.hs`](../../src/InitialAlgebra/Demo.hs) — `ExprF`（含签名内 `Lit`）、`cata` 求值、Lambek 风格 `in`/`out`
- 共用积木：[`src/Algebra/Core.hs`](../../src/Algebra/Core.hs)

```bash
cabal run algebra-demos
```
