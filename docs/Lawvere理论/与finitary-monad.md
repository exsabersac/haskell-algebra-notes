# Lawvere 理论与 finitary monad

Lawvere theory 与 monad 通过自由–遗忘伴随互译；**仅 finitary** monad 对应经典 Lawvere theory。  
术语：forgetful \(U\)、free \(F\)、finitary functor、coend、Kleisli、continuation monad。

相关：[模型](模型.md) · [幺半群理论](幺半群理论.md) · [副作用与Maybe](副作用与Maybe.md) · [对照表](对照表.md) · [List的EM代数与Monoid](../幺半范畴/List的EM代数与Monoid.md) · Demo `[4]`
更细的原文顺序见 [CTFP原文细讲](CTFP原文细讲.md)。

---

## 1. 从理论到 monad：自由 ⊣ 遗忘

### 遗忘 \(U\)

\[
U : \mathrm{Mod}(\mathbf{L},\mathbf{Set}) \to \mathbf{Set},
\qquad
U(M) = M(1)
\]

等价构造：\(\mathbf{F}^{\mathrm{op}}\) 是 \(\mathbf{Law}\) 的初对象 ⇒ 唯一 \(\mathbf{F}^{\mathrm{op}}\to\mathbf{L}\) ⇒ 诱导

\[
\mathrm{Mod}(\mathbf{L},\mathbf{Set}) \to \mathrm{Mod}(\mathbf{F}^{\mathrm{op}},\mathbf{Set}) \simeq \mathbf{Set}.
\]

### 自由 \(F\)（有限生成）

可用可表函子

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

| 视角 | 给什么 | 干什么 |
|------|--------|--------|
| Lawvere | \(n\)-元运算（造表达式） | 语法 / 定律 |
| model / EM | 求值映射 | 把表达式消回载体 |

```haskell
-- monoid / 列表：T = []
-- return = 嵌入生成元；join = 展平「词的词」
ret :: a -> [a]
ret x = [x]

jn :: [[a]] -> [a]
jn = concat

-- 自由 monoid 元素在模型上求值（Demo [4]）
-- foldMap interpret gens  ≡  唯一 monoid 同态扩展
```

```text
cabal run algebra-demos
-- [4] finitary monad List --
  return A            = [A]
  join [[A],[B,A],[]] = [A,B,A]
  eval in (Sum,+): … foldMap = …
  hint: EM([]) ≃ Mon ≃ Mod(L_Mon, Set)
```

---

## 2. Finitary：coend 公式（通俗拆解）

### 何谓 finitary

**Finitary functor** \(F:\mathbf{Set}\to\mathbf{Set}\) 由其在有限集上的行为完全决定：

\[
F a \;=\; \int^{n} a^n \times (F n)
\]

把 coend 先当成「带等同的求和」读：

\[
\int^{n} a^n \times (F n)
\;\;\approx\;\;
\Bigl(\coprod_{n\in\mathbb{N}} a^n \times F(n)\Bigr)\Big/\sim
\]

| 零件 | 含义（容器直觉，可核对公式） |
|------|------------------------------|
| \(n\) | 有限 arity（装几个槽） |
| \(F n\) | **形状**集合：有多少种「\(n\) 元槽位的布局」 |
| \(a^n\) | **内容**：往 \(n\) 个槽里填的元素元组 |
| \(\sim\) | cowedge：用有限集函数改标签时，改形状与改内容视为同一 |

列表是典型 finitary：每个 arity **一种**形状（「长度为 \(n\) 的列表」），故 \(Fn\) 对每个 \(n\) 单点，展开后得到 \(\coprod_n a^n \cong [a]\)（有限列表）。

### Lawvere 生成的 monad

\[
T_{\mathbf{L}} a \;=\; \int^{n} a^n \times \mathbf{L}(n,1)
\]

此时「形状」= \(n\)-元运算集合 \(\mathbf{L}(n,1)\)，「内容」= \(n\)-元组。  
一对 \((\,(x_1,\ldots,x_n),\,f:n\to 1\,)\) 读作：**用运算 \(f\) 作用在元组上**（再按 \(\sim\) 消掉可由投影 / 复制改写的重复表示）。

```haskell
-- T_L a ≅ ∫^n  a^n × L(n,1)
-- monoid：L(n,1) ≃ n* 的元素（词）形状
-- 合起来：有限词 + 填槽 = 列表
--
-- 非正式一对一草图（忽略 cowedge 等同）：
--   元素 of T a  ↔  (词 w ∈ n*,  元组 t ∈ a^n) 再求值
--   求值         ↔  apply / foldMap
type ListSketch a = [a]   -- 真正的 T；Demo 用 [] 的 return/join
```

### cowedge 在干什么（机制，非口号）

profunctor \(P(n,m)=a^n\times\mathbf{L}(m,1)\)。对 \(\mathbf{F}\) 中的 \(f:m\to n\)，可作用于内容侧（\(a^n\to a^m\)：按 \(f\) 选槽）或运算侧（预复合得到 \(\mathbf{L}(m,1)\to\mathbf{L}(n,1)\)）。两条路径到对角项后**等同**——这就是 coequalizer / cowedge。

推论（平凡理论 \(\mathbf{L}=\mathbf{F}^{\mathrm{op}}\)）：每个 \(\mathbf{L}(n,1)\) 都能从 \(\mathbf{L}(1,1)\) 经 basic morphisms 到达，全部对角项等同到 \(a\times\mathbf{L}(1,1)\cong a\)，得 **恒等 monad**。

非平凡运算（不能仅靠 \(I_L\) 从 \(\mathbf{F}\) 搬来的）会留下「真正的」额外求和项——见 [副作用与Maybe](副作用与Maybe.md) 的 \(a^0+a^1\)。

---

## 3. 从 finitary monad 回到理论：Kleisli\(^{\mathrm{op}}\)

给定 finitary monad \(T\)，取其 Kleisli 范畴限制在有限集上：态射 \(m\to n\) 为底层箭头 \(m\to T n\)。则

\[
\mathbf{L} \;\simeq\; \bigl(\mathbf{Kl}_T\big|_{\mathrm{fin}}\bigr)^{\mathrm{op}}
\]

特别地，\(n\)-元运算集

\[
\mathbf{L}(n,1) \;=\; \mathbf{Kl}_T(1,n) \;=\; \mathbf{Set}(1,\, T n) \;\cong\; T n.
\]

对 monoid / 列表：\(T n\cong n^*\)（\(n\) 元自由 monoid），与 [幺半群理论](幺半群理论.md) 一致。

```haskell
-- Kleisli 箭头 1 → n  （底层：1 → T n ≅ T n）
-- 对 T = []：选一个「n 元词」= 长度为任意的 [Fin n] 元素
-- 对偶后成为 L(n,1) 的成员

-- 列表的 Kleisli 复合 = >=> = 先产生列表再拼接
kleisliCompose :: (a -> [b]) -> (b -> [c]) -> (a -> [c])
kleisliCompose f g = \x -> concatMap g (f x)
```

| 方向 | 得到 |
|------|------|
| \(\mathbf{L}\) → free⊣forgetful → \(T_L\) | 「理论 ⇒ monad」 |
| finitary \(T\) → \(\mathrm{Kl}^{\mathrm{op}}|_{\mathrm{fin}}\) → \(\mathbf{L}\) | 「monad ⇒ 理论」 |
| EM\((T_L)\) ≃ Mod\((\mathbf{L},\mathbf{Set})\) | 「求值」两端一致 |

**不要混**：Kleisli 重建的是**运算空间**（理论）；EM 描述的是**如何求值**（模型）。

---

## 4. 覆盖边界：什么是 / 不是 finitary

| 覆盖（有经典 Lawvere 对应） | 不覆盖（或需扩展） |
|----------------------------|-------------------|
| 有限元运算的代数理论 | 无限元／本质上非 finitary 的运算 |
| `[]`、`Maybe`、Writer、有限状态 State 等 | **continuation monad** `Cont`（标准反例） |
| 与 EM 代数等价的模型范畴 | 「任意副作用叙事」本身（需另论） |

**为何 Cont 不是 finitary（机制）**：finitary 要求 \(Ta\) 由有限 \(n\)、形状 \(Tn\)、内容 \(a^n\) 的 coend 展开。continuation 的典型形式 \(Ta = (a\to r)\to r\) 依赖「任意多／高阶」的输入，不能仅由有限 arity 的形状表决定。

Lawvere theories 可用 coproduct / tensor 组合（相对 monad transformer 往往更整齐）；与任意 monad 的互译止于 finitary。可扩展「超越 finitary」的 Lawvere 变体，CTFP 仅点到为止。

Maybe 小品（单一 nullary raise）见专文 [副作用与Maybe](副作用与Maybe.md)。

---

## 一句话

每个 Lawvere theory 经自由⊣遗忘给出 finitary monad \(T_L a=\int^n a^n\times L(n,1)\)；每个 finitary monad 经有限 Kleisli\(^{\mathrm{op}}\) 找回理论；EM\((T_L)\simeq\mathrm{Mod}(L,\mathbf{Set})\)；continuation 落在边界之外。
