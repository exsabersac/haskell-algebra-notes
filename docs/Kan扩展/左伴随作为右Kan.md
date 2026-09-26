# 左伴随作为右 Kan

**已更正的定理**：伴随可用沿另一方对恒等的 Kan 扩展刻画——且左右是**交叉**的。  
术语保留精确英文：Lan、Ran、UP、end、Yoneda、绝对 Kan（absolute Kan extension）。

相关：[定义与UP](定义与UP.md) · [余密度单子](余密度单子.md)

---

## 1. 定理陈述

设 \(L:\mathcal{C}\to\mathcal{D}\)、\(R:\mathcal{D}\to\mathcal{C}\)，且 \(L\dashv R\)。则（在 Kan 存在的前提下）：

\[
L \;\cong\; \mathrm{Ran}_R(\mathrm{Id}_{\mathcal{D}})
\qquad\text{（左伴随 = 沿右伴随对恒等的**右** Kan）}
\]

\[
R \;\cong\; \mathrm{Lan}_L(\mathrm{Id}_{\mathcal{C}})
\qquad\text{（右伴随 = 沿左伴随对恒等的**左** Kan）}
\]

### 口诀

> **左伴随 ↔ 右 Kan；右伴随 ↔ 左 Kan**（交叉一次）

不要记成「左对左、右对右」——那是错的（见 §5 反例警示）。

---

## 2. 证明路径（三条，任选一条作主线）

### （1）UP 对上

伴随给出（对合适的函子 \(G:\mathcal{C}\to\mathcal{D}\)）：

\[
\mathrm{Nat}(G,\, L)
\;\cong\;
\mathrm{Nat}(G\circ R,\, \mathrm{Id}_{\mathcal{D}})
\]

这正是 \(\mathrm{Ran}_R(\mathrm{Id}_{\mathcal{D}})\) 的 UP（见 [定义与UP](定义与UP.md)）：\(\mathrm{Nat}(G,\mathrm{Ran}_R(\mathrm{Id}))\cong\mathrm{Nat}(G\circ R,\mathrm{Id})\)。故 \(L\cong\mathrm{Ran}_R(\mathrm{Id})\)。

对偶：\(\mathrm{Nat}(R,G)\cong\mathrm{Nat}(\mathrm{Id},G\circ L)\) 对上 \(\mathrm{Lan}_L(\mathrm{Id})\) 的 UP，得 \(R\cong\mathrm{Lan}_L(\mathrm{Id})\)。

### （2）end 公式 + 伴随改 Hom + Yoneda

点值（\(\mathcal{D}\) 取到 \(\mathbf{Set}\) 等可写 end 的情形，精神上）：

\[
\mathrm{Ran}_R(\mathrm{Id}_{\mathcal{D}})(c)
\;=\;
\int_{d}\, \bigl[\mathcal{C}(c,\, Rd),\, d\bigr]
\;\cong\;
\int_{d}\, \bigl[\mathcal{D}(Lc,\, d),\, d\bigr]
\;\cong\;
Lc
\]

中间步用伴随 \(\mathcal{C}(c,Rd)\cong\mathcal{D}(Lc,d)\)；最后一步是（协变）Yoneda／余 Yoneda 味道的 end 消去。

### （3）比较变换对应单位／余单位

- 余单位 \(\varepsilon:LR\Rightarrow\mathrm{Id}_{\mathcal{D}}\) 对应 Ran 的比较（\((\mathrm{Ran}_R\mathrm{Id})\circ R\Rightarrow\mathrm{Id}\)）。
- 单位 \(\eta:\mathrm{Id}_{\mathcal{C}}\Rightarrow RL\) 对应 Lan 的比较（\(\mathrm{Id}\Rightarrow(\mathrm{Lan}_L\mathrm{Id})\circ L\)）。

---

## 3. 绝对 Kan（简述）

上述刻画里的 Kan 扩展常常是**绝对的**（absolute）：被任意后复合函子仍保持为 Kan 扩展（「后复合绝对保持」）。

- 本笔记只记这句直觉；**不**展开 Street 等文献的精确定义／域名版本。
- 精确定义与充分必要条件可另文；此处承认「绝对性」作为标签，细节另文。

---

## 4. 短例：\(A\times-\;\dashv\;(-)^A\)

在 \(\mathbf{Set}\)：\(L(X)=A\times X\)，\(R(Y)=Y^A\)。则

\[
L(X)=A\times X
\;\cong\;
\int_{Y}\, \bigl[\mathbf{Set}(X,\, Y^A),\, Y\bigr]
\]

精神上：end 公式写出 \(\mathrm{Ran}_R(\mathrm{Id})(X)\)，再经伴随 \(\mathbf{Set}(X,Y^A)\cong\mathbf{Set}(A\times X,Y)\) 与 Yoneda 回到 \(A\times X\)。

（余密度侧 \(T^R\cong R\circ L\) 见 [余密度单子](余密度单子.md)。）

---

## 5. 反例警示

\[
L \;\cong\; \mathrm{Lan}_R(\mathrm{Id})
\quad\text{是错的}
\]

UP 对不上：\(\mathrm{Lan}_R(\mathrm{Id})\) 的 UP 是 \(\mathrm{Nat}(\mathrm{Lan}_R(\mathrm{Id}),G)\cong\mathrm{Nat}(\mathrm{Id},G\circ R)\)，与伴随给出的 \(\mathrm{Nat}(G,L)\cong\mathrm{Nat}(G\circ R,\mathrm{Id})\) **方向与位置都不匹配**。口诀必须交叉一次。

---

## 已澄清结论

1. \(L\dashv R\) ⇒ \(L\cong\mathrm{Ran}_R(\mathrm{Id}_{\mathcal{D}})\)，\(R\cong\mathrm{Lan}_L(\mathrm{Id}_{\mathcal{C}})\)（交叉）。
2. 证明可走：UP 对上；或 end + 伴随改 Hom + Yoneda；比较箭头对应 \(\varepsilon\)／\(\eta\)。
3. 这些 Kan 常具绝对性（后复合仍保持为 Kan）；精确定义另文，勿写错 Street 域名版陈述。
4. \(L\cong\mathrm{Lan}_R(\mathrm{Id})\) 错误；\(A\times-\dashv(-)^A\) 作短例。

## 易混点

| 易混 | 澄清 |
|------|------|
| 左伴随 = 左 Kan | **否**：左伴随 = **右** Kan（沿 \(R\) 对 \(\mathrm{Id}\)） |
| 右伴随 = 右 Kan | **否**：右伴随 = **左** Kan（沿 \(L\) 对 \(\mathrm{Id}\)） |
| \(L\cong\mathrm{Lan}_R(\mathrm{Id})\) | UP 对不上，是常见记反 |
| 「绝对 Kan」已给完全定理 | 本笔记仅简述；Street 等精确定义另文 |
| Kan 刻画 ⇒ 每个 Kan 都是伴随 | 否；此处是伴随的特殊表示 |

## 另见

- [定义与UP](定义与UP.md) — Lan／Ran 的 UP 与点值
- [余密度单子](余密度单子.md) — \(T^R=\mathrm{Ran}_R(R)\cong R\circ L\)
