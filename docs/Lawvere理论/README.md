# Lawvere 理论（CTFP 3.14）

整理自 Milewski《Category Theory for Programmers》第 3.14 章 **Lawvere Theories**。  
术语保留精确英文：Lawvere theory、FinSet、skeleton \(\mathbf{F}\)、\(\mathbf{F}^{\mathrm{op}}\)、model、\(\mathrm{Mod}\)、finitary monad、coend、Kleisli、EM algebra。

风格：**先范畴陈述，再短 Haskell**；邻近概念用对照表。机制写清楚，不用口号式类比顶替定义。  
可运行草图：[`src/Lawvere/Demo.hs`](../../src/Lawvere/Demo.hs)（`cabal run algebra-demos` 打印分节横幅 `[1]`…`[12]`）。

> **按 CTFP 原文顺序的细讲**：[CTFP原文细讲](CTFP原文细讲.md)（§0 动机 → §1–§7 正文 → §8 Challenges → §9 Further Reading）。  
> 与下方「通俗拆分」互补：细讲保留章节顺序与 coend/练习/文献；拆分按主题跳读，并链回 Demo `[1]`–`[12]`。

---

## 学习路径（按 CTFP 章节顺序）

```text
① 定义与骨架     Universal Algebra → FinSet → F → F^op → I_L → L
② 模型           product-preserving M : L → Set；Nat；平凡理论 ≃ Set
③ 幺半群理论     L_Mon；L(2,1) ≃ 自由词；Mod ≃ Mon
④ 与finitary-monad  free ⊣ forgetful；coend；Kleisli^op；Cont 边界
⑤ 副作用与Maybe  单一 nullary raise ⇒ Maybe（CTFP Side Effects）
⑥ 对照表         四层语言边界 + 何时用哪一副眼镜
⑦ 多种finitary-monad  Identity / NE / Writer / Either / Reader / State（Cont 边界）
⑧ 实现思路与finitary  signature → `L(n,1)` → `T a` → `return`/`join` → model eval；Writer；`L(3,2)`
```

建议读法：想跟 CTFP 原文走 → 先读 [CTFP原文细讲](CTFP原文细讲.md)；想按主题跳读 → 走完 ①–③ 建立「理论 / 模型」分工，再读 ④ 接列表 monad，⑤ 是 Maybe 小品，⑥ 作复习地图，⑦ 扩一览更多 finitary 例子，⑧ 把签名、monad、Writer 和 Kleisli 串成实现 pipeline。

---

## 文档目录

| # | 文档 | CTFP 对应 | 内容 |
|---|------|-----------|------|
| 0 | [**CTFP原文细讲**](CTFP原文细讲.md) | **全章 §0–§9 原文顺序** | 动机；UA→定义→模型→Mon→monad/coend→Maybe；Challenges；Further Reading |
| 1 | [定义与骨架](定义与骨架.md) | Universal Algebra；Lawvere Theories | arity；FinSet→\(\mathbf{F}\)→\(\mathbf{F}^{\mathrm{op}}\)→\(I_L\)；boring vs interesting morphisms |
| 2 | [模型](模型.md) | Models of Lawvere Theories | 保积模型；Nat；平凡理论 \(\simeq\mathbf{Set}\) |
| 3 | [幺半群理论](幺半群理论.md) | The Theory of Monoids | \(L_{\mathrm{Mon}}\)；自由词作 \(L(2,1)\)；\(\mathrm{Mod}\simeq\mathbf{Mon}\) |
| 4 | [与finitary-monad](与finitary-monad.md) | Lawvere Theories and Monads；Monads as Coends | free⊣forgetful；coend 公式拆解；Kleisli 重建；Cont 非 finitary |
| 5 | [副作用与Maybe](副作用与Maybe.md) | Lawvere Theory of Side Effects | 单一 nullary \(0\to 1\)；\(Ta\cong a^0+a^1\cong\mathrm{Maybe}\,a\) |
| 6 | [对照表](对照表.md) | （综览） | signature / Lawvere / finitary monad / 任意 monad；选用指南 |
| 7 | [多种finitary-monad](多种finitary-monad.md) | （扩例子） | Identity / NE / Writer / Either / Reader / State；Cont 非 finitary |
| 8 | [实现思路与finitary](实现思路与finitary.md) | （实现路线） | finitary 的边界；五步 pipeline；Writer 全流程；`L(3,2)` 与 List Kleisli |

相关主题：[List的EM代数与Monoid](../幺半范畴/List的EM代数与Monoid.md)（\(\mathrm{EM}([])\simeq\mathbf{Mon}\)）；[自由幺半群与列表](../幺半范畴/自由幺半群与列表.md)；[余密度单子](../Kan扩展/余密度单子.md)（coend 语境）。

---

## 一句话总路线

```text
FinSet ──skeleton──▶ F ──op──▶ F^op ──I_L──▶ L（Lawvere theory）
                                              │
                                   product-preserving M
                                              ▼
                                         Mod(L, Set)  ≃  algebras
                                              │
                                    free F ⊣ forgetful U
                                              ▼
                                    finitary monad T_L = U∘F
                                              │
                         （逆：finitary T ──Kl^op|fin──▶ L）
```

---

## 文档 ↔ Demo ↔ CTFP 对照

`cabal run algebra-demos` 中 Lawvere 段的 stdout 横幅：

| 横幅 | Demo 函数 / 符号 | 主要文档 | CTFP |
|------|------------------|----------|------|
| `-- [1] nullary/binary ops --` | `op0`、`op2`；在 `(Sum,0,+)`、`([a],++)`、`Endo` 上解释 | [幺半群理论](幺半群理论.md) §1；[定义与骨架](定义与骨架.md) | ops as morphisms |
| `-- [2] L(2,1) free-words --` | `wordsUpTo`、`applyWord`；ε,A,B,AA,… | [幺半群理论](幺半群理论.md) §2 | \(L_{\mathrm{Mon}}(2,1)\) |
| `-- [3] laws checks --` | `checkMonoidLaws` / `checkMonoidLawsReport` | [模型](模型.md) | equational laws in models |
| `-- [4] finitary monad List --` | `return`/`join`；`foldMap` 求值词 | [与finitary-monad](与finitary-monad.md) | \(T_L\)；EM≃Mod |
| `-- [5] Maybe Lawvere snack --` | `raise`、`embed`；`Maybe ≅ 1+a` | [副作用与Maybe](副作用与Maybe.md) | Side Effects |
| `-- [6] theory morphism sketch --` | Monoid→Semigroup：忘掉单位 | [对照表](对照表.md)；[定义与骨架](定义与骨架.md) §态射 | morphisms in \(\mathbf{Law}\) |
| `-- [7] Identity --` | `return`/`join` = `id`；\(L(n,1)\cong n\) | [多种finitary-monad](多种finitary-monad.md) §1 | trivial theory |
| `-- [8] Semigroup / NonEmpty --` | `NE`；mul / join flatten | [多种finitary-monad](多种finitary-monad.md) §2 | free semigroup |
| `-- [9] Writer --` | `(a,W)`；\(L(n,1)\cong n\times W\) | [多种finitary-monad](多种finitary-monad.md) §3 | Writer |
| `-- [10] Either --` | \(\lvert E\rvert\) nullary raises | [多种finitary-monad](多种finitary-monad.md) §4 | multi-exception |
| `-- [11] Reader --` | `env→a`；\(L(n,1)\cong n^{\lvert env\rvert}\) | [多种finitary-monad](多种finitary-monad.md) §5 | finite Reader |
| `-- [12] State --` | `S→(a,S)`；\(\lvert L(n,1)\rvert=(n\lvert S\rvert)^{\lvert S\rvert}\) | [多种finitary-monad](多种finitary-monad.md) §6 | finite State |

---

## 术语速查

| 英文 | 本文用法 |
|------|----------|
| arity | 运算元数；\(n\)-ary = \(a^n\to a\) |
| skeleton \(\mathbf{F}\) | FinSet 同构类合并后的范畴；对象 ≅ \(\mathbb{N}\) |
| basic product operations | 经 \(I_L\) 从 \(\mathbf{F}^{\mathrm{op}}\) 搬来的投影 / 对角等 |
| interesting morphisms | 真正的代数运算（乘法、单位等） |
| model | 保有限积（至同构）的 \(M:L\to\mathbf{Set}\) |
| finitary | 函子／monad 由其在有限集上的行为经 coend 完全决定 |
| Kleisli\(^{\mathrm{op}}\) | 从 finitary monad 重建 Lawvere theory 的路径 |
