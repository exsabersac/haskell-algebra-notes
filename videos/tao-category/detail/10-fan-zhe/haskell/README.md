# 进阶深讲 10 · 反者道之动 — Haskell

```bash
cd haskell
cabal build
cabal run tao-category-fan-zhe
```

包名 `tao-category-fan-zhe`（无纯数字连字符段）。屏幕代码见 `src/FanZhe.hs` 中 `-- {{snip:…}}`。

内容：`Coalgebra` / `ana`（与 `cata` 对偶）、`hylo`（先生后归、中间结构不落地）、
`ListF` 阶乘、`StreamF` 无穷自然数流、`takeS`。参考 DaoFP ch.12 / CTFP 3.8 Coalgebras。
