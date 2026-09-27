# Ch.7 Traversals（遍历（Traversal））

## 主要小节
- 7.1 Introduction to Traversals
- 7.2 Traversal Combinators
- 7.3 Traversal Composition
- 7.4 Traversal Actions
- 7.5 Custom traversals
- 7.6 Traversal Laws
- 7.7 Advanced manipulation（`partsOf`）

## 要点
- Traversal ≈ Fold + 可写：可 get/set/modify **零个或多个** 焦点；早期也称 multilens。
- 层级：Lens ⊂ Traversal ⊂（可作为）Fold；有 Traversal 时不要用 `^.`（可能失败），改用 `^?`/`^..`。
- 许多曾当 Fold 用的其实已是 Traversal：`both`、`each`、`filtered`、`taking`/`dropping` 等。
- 组合：路径上约束取并集；Lens∘Traversal → Traversal 等。
- 动作：`traverseOf` / `%%~`、`forOf`、`sequenceAOf`——把深层焦点上的效应（IO、Maybe、Validation）提到外层。
- Van Laarhoven 编码下 Traversal 类型形似 `traverse`；`traverseOf = id` 是实现细节，日常仍建议用显式动作。
- 自定义：手写满足 `Applicative` 约束的遍历；或用 `traversal` 辅助。
- 定律（更像指南）：修改不应改变“聚焦哪些元素”等；`filtered` 等常用组合子会违法，但仍实用——“先懂法再违法”。
- `partsOf`：把 Traversal 变成“焦点列表”上的 Lens，改列表再写回原结构（强力高级工具）。
