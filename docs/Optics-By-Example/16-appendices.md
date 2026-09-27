# Ch.16 Appendices（附录）

## 主要小节
- 16.1 Optic Composition Table
- 16.2 Optic Compatibility Chart
- 16.3 Operator Cheat Sheet
- 16.4 Optic Ingredients

## 要点
- **组合表**：两两组合后最泛化的结果类型（Fold∘Lens→Fold，Prism∘Traversal→Traversal 等）；不兼容为 “–”；对角对称（约束并集交换）。
- **兼容表**：手里有的 optic 能否当作另一种使用（Iso 最强，Fold 最弱只读等）。
- **运算符速查**：日常 `^.` `.~` `%~` `^..` `^?` 及 State/indexed 变体的速查清单。
- **Optic Ingredients**：把 VL 编码里出现的 `Identity`/`Const`/`Contravariant`/`Applicative` 等对应回“你在用哪种 optic/动作”——排错核心参考。
