# Lawvere 理论与 finitary monad

Lawvere theory 与 monad 通过自由–遗忘伴随互译；**仅 finitary** monad 对应 Lawvere theory。  
术语：forgetful \(U\)、free \(F\)、finitary functor、coend、Kleisli、continuation monad。

相关：[模型](模型.md) · [幺半群理论](幺半群理论.md) · [对照表](对照表.md) · [List的EM代数与Monoid](../幺半范畴/List的EM代数与Monoid.md)

---

## 1. 从理论到 monad：自由 ⊣ 遗忘

遗忘函子 \(U:\mathrm{Mod}(\mathbf{L},\mathbf{Set})\to\mathbf{Set}\)：取模型在对象 \(1\) 上的值 \(M\mapsto M(1)\)。  
等价路径：\(\mathbf{F}^{\mathrm{op}}\) 是 \(\mathbf{Law}\) 的初对象 ⇒ 唯一 \(\mathbf{F}^{\mathrm{op}}\to\mathbf{L}\) ⇒ 诱导模型范畴上的函子落到 \(\mathrm{Mod}(\mathbf{F}^{\mathrm{op}},\mathbf{Set})\simeq\mathbf{Set}\)。

\(U\) 有左伴随——**自由函子** \(F\)。有限生成情形可用可表函子

\[
F(n) = \mathbf{L}(n,-) : \mathbf{L}\to\mathbf{Set}
\]

Yoneda 给出伴随：

\[
\mathrm{Mod}(\mathbf{L},\mathbf{Set})\bigl(\mathbf{L}(n,-),\,M\bigr)
\;\cong\;
\mathbf{Set}(n,\,U M)
\;\cong\;
M n.
\]

合成为 \(\mathbf{Set}\) 上的 monad \(T = U\circ F\)。该 monad 的 **EM 代数**范畴等价于 \(\mathrm{Mod}(\mathbf{L},\mathbf{Set})\)。

直觉：Lawvere theory 提供造表达式的 \(n\)-元运算；model / EM 代数提供求值。

---

## 2. Finitary：coend 公式

**Finitary functor** \(F:\mathbf{Set}\to\mathbf{Set}\) 由其在有限集上的行为决定：

\[
F a \;=\; \int^{n} a^n \times (F n)
\]

（形状 \(Fn\) + 内容 \(a^n\) 的「幂级数／容器」展开。）

Lawvere theory 生成的 monad 皆 finitary：

\[
T_{\mathbf{L}} a \;=\; \int^{n} a^n \times \mathbf{L}(n,1)
\]

即：\(n\)-元运算集合 \(\mathbf{L}(n,1)\) 配上 \(n\)-元组。  
列表是典型 finitary 例子（每个 arity 一个形状）；continuation monad **不是** finitary。

短 Haskell（monoid 情形：\(T=\;[\,]\)）：

```haskell
-- T_L a ≅ ∫^n  a^n × L(n,1)
-- monoid：L(n,1) ≅ 自由 monoid on n 的「词」形状 ≈ 长度相关；
-- 合起来得到列表：
listAsFinitarySketch :: [a]   -- ≅ 所有有限 arity 的「词应用」
listAsFinitarySketch = []     -- 演示占位；见 Demo.hs
```

---

## 3. 从 finitary monad 回到理论：Kleisli\(^{\mathrm{op}}\)

给定 finitary monad \(T\)，取其 Kleisli 范畴限制在有限集上：态射 \(m\to n\) 为底层 \(m\to T n\)。  
则

\[
\mathbf{L} \;\simeq\; \bigl(\mathbf{Kl}_T\big|_{\mathrm{fin}}\bigr)^{\mathrm{op}}
\]

特别地，\(n\)-元运算集

\[
\mathbf{L}(n,1) \;=\; \mathbf{Kl}_T(1,n) \;=\; \mathbf{Set}(1,\, T n) \;\cong\; T n.
\]

（对 monoid / 列表：\(T n\cong n^*\)，与上一篇一致。）

---

## 4. 覆盖边界：什么**不是**

| 覆盖 | 不覆盖（或需扩展） |
|------|-------------------|
| 有限元运算的代数理论 | 无限元／非 finitary 运算 |
| List、Maybe、Writer、State（有限状态）等常见编程 monad | **continuation monad**（典型非 finitary） |
| 与 EM 代数等价的模型范畴 | 任意「副作用」叙事（需另论） |

Lawvere theories 可用 coproduct / tensor 组合（相对 monad transformer 更整齐）；但与任意 monad 的互译止于 finitary。可扩展「超越 finitary」的 Lawvere 变体，CTFP 仅点到为止。

Maybe 小品：单一 nullary \(0\to 1\)（抛异常）⇒ coend 给出 \(T a\cong a^0+a^1\cong\mathrm{Maybe}\,a\)（只 raise，不 handle）。

---

## 一句话

每个 Lawvere theory 经自由⊣遗忘给出 finitary monad \(T_L a=\int^n a^n\times L(n,1)\)；每个 finitary monad 经有限 Kleisli\(^{\mathrm{op}}\) 找回理论；continuation 落在边界之外。
