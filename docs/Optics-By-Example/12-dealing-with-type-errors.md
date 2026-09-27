# Ch.12 Dealing with Type Errors（处理类型错误）

## 主要小节
- 12.1 Interpreting expanded optics types
- 12.2 Type Error Arena

## 要点
- Optics 能力强，类型错误也吓人；关键是拆解信息、练启发式，不要气馁。
- Van Laarhoven 展开后，错误常表现为 **约束 + 具体类型构造器** 不匹配（如 `Contravariant Identity`）。
- 对照附录“Optic Ingredients”：`Identity` 常见于 `set`/`over`；`Contravariant` 常见于 **Fold**——故对 Fold 做写入会炸，应改用 `traversed` 等 Traversal。
- Type Error Arena：通过故意写错的表达式练读 GHC 报错并修复。
- 实践建议：记常用 optic 的约束画像，比死背完整签名更有效。
