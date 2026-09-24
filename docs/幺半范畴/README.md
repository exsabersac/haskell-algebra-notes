# 幺半范畴

1. [定义与连贯](定义与连贯.md)
2. [例子与 Monad](例子与Monad.md)
3. [是不是幺半群](是不是幺半群.md)
4. [自由幺半群与列表](自由幺半群与列表.md)（\(\mathrm{FreeMon}(X)\cong[X]\)；`ListF` / `foldMap`；见 [`FunctorCombo/Demo.hs`](../../src/FunctorCombo/Demo.hs)）
5. [自由幺半群与ListF代数](自由幺半群与ListF代数.md)（FreeMon vs 初始 ListF；`fromMonoid`；UP 双射）
6. [List的EM代数与Monoid](List的EM代数与Monoid.md)（\(\mathrm{EM}([])\simeq\mathbf{Mon}\)；自由 EM；Kleisli 边界）
7. [自由单子](自由单子.md)（End 里自由 monoid-对象；`Free f` / `foldFree` / `foldFreeM`；见 [`FreeDemo/Demo.hs`](../../src/FreeDemo/Demo.hs)）

相关主题：[函子组合](../函子组合/)（`Compose` vs `Sum`/`Product`；函子范畴上的三层结构）
