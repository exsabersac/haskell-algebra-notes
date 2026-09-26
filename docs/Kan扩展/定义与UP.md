# Kan 扩展：定义与 UP

澄清 **Kan 扩展**（Kan extension）回答什么问题：已有小定义域上的函子 \(F\)，如何沿 \(K:\mathcal{C}\to\mathcal{D}\) **延拓**到大地盘 \(\mathcal{D}\) 上。  
术语保留精确英文：Lan、Ran、UP、end、coend、Yoneda、Coyoneda、Nat。

相关：[左伴随作为右Kan](左伴随作为右Kan.md) · [余密度单子](余密度单子.md)

---

## 1. 问题图景

给定函子 \(F:\mathcal{C}\to\mathcal{E}\) 与 \(K:\mathcal{C}\to\mathcal{D}\)，想找 \(G:\mathcal{D}\to\mathcal{E}\)，使「沿 \(K\) 拉回」尽量贴近 \(F\)：

```text
     F
 C ──────▶ E
  \       ▲
 K \     / G  （待求）
    \   /
     ▼ /
      D
```

口语：小地盘 \(\mathcal{C}\) 上已有 \(F\)；\(K\) 把 \(\mathcal{C}\) 嵌进（或映到）大地盘 \(\mathcal{D}\)；Kan 扩展给出在 \(\mathcal{D}\) 上的延拓 \(G\)。

---

## 2. 左 Kan 与右 Kan（正式）

### 左 Kan 扩展 \(\mathrm{Lan}_K F\)（最自由）

若存在 \(L=\mathrm{Lan}_K F:\mathcal{D}\to\mathcal{E}\) 与单位（unit）自然变换

\[
\eta:\; F \;\Rightarrow\; L\circ K
\]

使得对任意 \(G:\mathcal{D}\to\mathcal{E}\) 与任意 \(\alpha:F\Rightarrow G\circ K\)，存在**唯一** \(\overline{\alpha}:L\Rightarrow G\) 满足 \(\overline{\alpha}_K\circ\eta=\alpha\)。用 Nat 写 UP：

\[
\mathrm{Nat}(\mathrm{Lan}_K F,\, G)
\;\cong\;
\mathrm{Nat}(F,\, G\circ K)
\]

（左端的映射经后复合 \(-\circ K\) 再配 \(\eta\) 对应到右端。）

### 右 Kan 扩展 \(\mathrm{Ran}_K F\)（最保守）

若存在 \(R=\mathrm{Ran}_K F:\mathcal{D}\to\mathcal{E}\) 与余单位（counit）

\[
\varepsilon:\; R\circ K \;\Rightarrow\; F
\]

UP：

\[
\mathrm{Nat}(G,\, \mathrm{Ran}_K F)
\;\cong\;
\mathrm{Nat}(G\circ K,\, F)
\]

| | Lan | Ran |
|--|-----|-----|
| 口号 | 最自由延拓 | 最保守延拓 |
| 比较箭头 | \(F\Rightarrow(\mathrm{Lan}_K F)\circ K\) | \((\mathrm{Ran}_K F)\circ K\Rightarrow F\) |
| UP（Nat） | \(\mathrm{Nat}(\mathrm{Lan}_K F,G)\cong\mathrm{Nat}(F,G\circ K)\) | \(\mathrm{Nat}(G,\mathrm{Ran}_K F)\cong\mathrm{Nat}(G\circ K,F)\) |

---

## 3. 点值公式（\(\mathbf{Set}\) 里）

当 \(\mathcal{E}=\mathbf{Set}\)（或足够完备／余完备且可写 end／coend 时），常用：

\[
(\mathrm{Lan}_K F)(d)
\;=\;
\int^{c}\, \mathcal{D}(Kc,\,d)\cdot F(c)
\qquad\text{（coend；加权余极限味道）}
\]

\[
(\mathrm{Ran}_K F)(d)
\;=\;
\int_{c}\, \bigl[\mathcal{D}(d,\,Kc),\, F(c)\bigr]
\qquad\text{（end；加权极限味道）}
\]

记忆：Lan ↔ coend／「求和」；Ran ↔ end／「求积／函数空间」。

---

## 4. 与极限／伴随的分界

| 概念 | 在说什么 | 不是什么 |
|------|----------|----------|
| **极限／余极限** | 收拢**一个图**（diagram）成对象 | 不是「把函子延到更大定义域」 |
| **Kan 扩展** | 沿 \(K\) **延拓函子** \(F\mapsto G\) | 不是单纯「算一个 lim」口号（虽可用加权 lim／colim 实现点值） |
| **伴随** \(L\dashv R\) | 两函子之间的 Hom 同构 | 可用**特殊** Kan 刻画（见 [左伴随作为右Kan](左伴随作为右Kan.md)），但伴随 ≠ 一般 Kan |

一句话：极限管「图 → 对象」；Kan 管「小函子 → 大函子」；伴随是 Kan 的特殊情形之一。

---

## 5. Yoneda / Coyoneda（Haskell 影子，一句）

不必展开细证，只记味道：

- **Coyoneda** 有左 Kan 扩展的自由延拓味道（「多加一层再解释」）。
- **Yoneda** 有右 Kan／表示的保守味道（「用 Hom 测出来」）。

具体编码与证明留在表示／Yoneda 专题；此处仅作记忆锚点。

---

## 已澄清结论

1. Kan 扩展回答：已有 \(F:\mathcal{C}\to\mathcal{E}\)，沿 \(K:\mathcal{C}\to\mathcal{D}\) 延到 \(G:\mathcal{D}\to\mathcal{E}\)。
2. \(\mathrm{Lan}_K F\) 最自由，单位 \(F\Rightarrow(\mathrm{Lan}_K F)\circ K\)；\(\mathrm{Ran}_K F\) 最保守，\((\mathrm{Ran}_K F)\circ K\Rightarrow F\)；UP 用 Nat 表述。
3. \(\mathbf{Set}\) 点值：Lan 用 coend \(\int^c\mathcal{D}(Kc,d)\cdot F(c)\)；Ran 用 end \(\int_c[\mathcal{D}(d,Kc),F(c)]\)。
4. 极限收拢图；Kan 延拓函子；伴随可用特殊 Kan 刻画，三者勿混为一谈。
5. Coyoneda≈左 Kan 味道，Yoneda≈右 Kan 味道（影子记忆，细证另文）。

## 易混点

| 易混 | 澄清 |
|------|------|
| Lan「更大」所以更保守 | 反了：Lan 最自由；Ran 最保守 |
| Kan = 极限 | 极限是对象级收拢；Kan 是函子级延拓（点值可写成加权 lim／colim） |
| 单位方向记反 | Lan：\(F\Rightarrow L\circ K\)；Ran：\(R\circ K\Rightarrow F\) |
| 每个 Kan 都是伴随 | 否；伴随是特殊 Kan（见下一篇） |
| end / coend 谁配谁 | Lan↔coend；Ran↔end |

## 另见

- [左伴随作为右Kan](左伴随作为右Kan.md) — \(L\cong\mathrm{Ran}_R(\mathrm{Id})\) 等
- [余密度单子](余密度单子.md) — \(T^G=\mathrm{Ran}_G(G)\)
