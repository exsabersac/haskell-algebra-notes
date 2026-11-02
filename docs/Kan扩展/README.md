# Kan 扩展

1. [定义与UP](定义与UP.md)（Lan / Ran；单位／余单位；end / coend 点值；与极限／伴随分界；Haskell 口感）
2. [左伴随作为右Kan](左伴随作为右Kan.md)（\(L\cong\mathrm{Ran}_R(\mathrm{Id})\)；\(R\cong\mathrm{Lan}_L(\mathrm{Id})\)；交叉口诀；绝对性简述）
3. [余密度单子](余密度单子.md)（\(T^G=\mathrm{Ran}_G(G)\)；Codensity；\(L\dashv R\Rightarrow T^R\cong R\circ L\)；vs Cont）

### 可运行代码

- [`src/KanDemo/Demo.hs`](../../src/KanDemo/Demo.hs) — Coyoneda（Lan 玩具）／Cont（Ran／常值余密度）／Codensity；`cabal run algebra-demos` 会打印 Kan 段

相关主题：[幺半范畴](../幺半范畴/)（End 中的 monoid／自由单子）；[函子组合](../函子组合/)（函子范畴上的结构）
