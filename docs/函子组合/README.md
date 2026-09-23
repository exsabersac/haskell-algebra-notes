# 函子组合

1. [常见组合](常见组合.md)
2. [函子的作用与组合能力](函子的作用与组合能力.md)
3. [函子范畴上的代数](函子范畴上的代数.md)

相关主题：[幺半范畴](../幺半范畴/)（\((\mathrm{End},\circ,\mathrm{Id})\) 与 Monad）

## 可运行代码

- [`src/FunctorCombo/Demo.hs`](../../src/FunctorCombo/Demo.hs) — `ListF` / `NonEmptyF`，以及 `Sum`/`Product`/`Const` 拼列表形状
- 共用积木：[`src/Algebra/Core.hs`](../../src/Algebra/Core.hs)

```bash
cabal run algebra-demos
```
