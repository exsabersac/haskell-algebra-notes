# 进阶深讲 09 · 道生一 — Haskell

```bash
cd haskell
cabal build
cabal run tao-category-dao-sheng-yi
```

包名 `tao-category-dao-sheng-yi`（无纯数字连字符段）。屏幕代码见 `src/DaoShengYi.hs` 中 `-- {{snip:…}}`。

内容：`Fix` / `Algebra` / `cata`（DaoFP ch.11 写法）、`ExprF` 的两份代数 `eval` / `pretty`、
兰贝克引理的见证 `lambekOut = cata (fmap Fix)`、`Nat = Fix Maybe`、Church 编码 `Mu f`。
