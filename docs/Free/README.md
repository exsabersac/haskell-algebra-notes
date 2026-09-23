# Free、生成元与 fold

1. [生成元](生成元.md)
2. [`Fix` 与 `Free` 对照](Fix与Free对照.md)
3. [`foldFree` 与 `cata`](foldFree与cata.md)
4. [`Free ≅ Fix (Sum (Const a) f)` 编码](Fix编码.md)

## 可运行代码

- [`src/FreeDemo/Demo.hs`](../../src/FreeDemo/Demo.hs) — `Pure` 生成元、`toFix`/`fromFix`、`foldFree`≡`cata`、`Free ((,) e) ≅ ([e], a)`
- 共用积木：[`src/Algebra/Core.hs`](../../src/Algebra/Core.hs)

```bash
cabal run algebra-demos
```
