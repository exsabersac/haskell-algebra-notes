# 进阶深讲 11 · 知其雄，守其雌 — Haskell

```bash
cd haskell
cabal build
cabal run tao-category-xiong-ci
```

包名 `tao-category-xiong-ci`（无纯数字连字符段）。屏幕代码见 `src/XiongCi.hs` 中 `-- {{snip:…}}`。

内容：柯里化伴随（`leftAdjunct`/`rightAdjunct`/`unit`/`counit`）、三角恒等式、
`State`（`join` = fmap counit）、`Store`（`extract`/`duplicate`/`extend`/`sum3`）、
`_1` lens 与三条定律。参考 DaoFP ch.10 / 16 / 17 · CTFP 3.2 / 3.6 / 3.7。
