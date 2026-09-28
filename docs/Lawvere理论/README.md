# Lawvere 理论（CTFP 3.14）

整理自 Milewski《Category Theory for Programmers》第 3.14 章 **Lawvere Theories**。  
术语保留精确英文：Lawvere theory、FinSet、skeleton \(\mathbf{F}\)、\(\mathbf{F}^{\mathrm{op}}\)、model、Mod、finitary monad、coend、Kleisli。

风格：先范畴陈述，再短 Haskell；邻近概念用对照表。可运行草图见 [`src/Lawvere/Demo.hs`](../../src/Lawvere/Demo.hs)（`cabal run algebra-demos` 打印分节）。

## 文档目录

1. [定义与骨架](定义与骨架.md)（universal algebra；FinSet → \(\mathbf{F}\) → \(\mathbf{F}^{\mathrm{op}}\) → \(I_L\)；路线图）
2. [模型](模型.md)（product-preserving \(M:L\to\mathbf{Set}\)；Nat；平凡理论 \(\simeq\mathbf{Set}\)）
3. [幺半群理论](幺半群理论.md)（\(L_{\mathrm{Mon}}\)；自由 monoid 的 opposite；\(\mathrm{Mod}\simeq\mathbf{Mon}\)）
4. [与finitary-monad](与finitary-monad.md)（自由–遗忘伴随；\(T a=\int^n a^n\times L(n,1)\)；Kleisli 重建；continuation 非 finitary；Maybe 小品）
5. [对照表](对照表.md)（Lawvere / signature+equations / finitary monad / 任意 monad）

相关主题：[List的EM代数与Monoid](../幺半范畴/List的EM代数与Monoid.md)（\(\mathrm{EM}([])\simeq\mathbf{Mon}\)）；[自由幺半群与列表](../幺半范畴/自由幺半群与列表.md)；[余密度单子](../Kan扩展/余密度单子.md)（coend 公式语境）。

## 一句话路线

```text
FinSet ──skeleton──▶ F ──op──▶ F^op ──I_L──▶ L（Lawvere theory）
                                              │
                                   product-preserving
                                              ▼
                                         Mod(L, Set)  ≃  algebras
                                              │
                                    free ⊣ forgetful
                                              ▼
                                    finitary monad T_L
```

## Demo 分节（`Lawvere.Demo`）

与 CTFP / 上文笔记对照，stdout 横幅：

| 横幅 | 内容 | 主要对应 |
|------|------|----------|
| `-- [1] nullary/binary ops --` | `op0`/`op2`；在 `(Sum,0,+)`、`([a],++)`、`Endo` 上解释 | [幺半群理论](幺半群理论.md) §1 |
| `-- [2] L(2,1) free-words --` | 枚举 ε,A,B,AA,… 作 \(2\to 1\) stand-in；投影/单位特例 | [幺半群理论](幺半群理论.md) §2 |
| `-- [3] laws checks --` | 结合 / 左右单位，PASS/FAIL | [模型](模型.md) |
| `-- [4] finitary monad List --` | `return`/`join`；`foldMap` 求值词 | [与finitary-monad](与finitary-monad.md) §1–2 |
| `-- [5] Maybe Lawvere snack --` | nullary raise；`Maybe ≅ 1+a`；无 handler | [与finitary-monad](与finitary-monad.md) §4 |
| `-- [6] theory morphism sketch --` | Monoid→Semigroup：忘掉单位 | [对照表](对照表.md) |
