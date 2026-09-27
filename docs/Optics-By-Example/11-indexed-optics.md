# Ch.11 Indexed Optics（带索引的 Optics）

## 主要小节
- 11.1 What are indexed optics?
- 11.2 Index Composition
- 11.3 Filtering by index
- 11.4 Custom indexed optics
- 11.5 Index-preserving optics

## 要点
- Indexed optics：沿路径下潜时 **累积位置信息**（list 下标、Map 键、树路径等）。
- `itraversed`（`TraversableWithIndex`）≈ 带索引的 `traversed`。
- **动作**负责把索引带进结果：如 `itoListOf`/`^@..`、`iover`/`%@~`、`iset`/.`@~` 等（名字前加 `i` 或运算符中加 `@`）。
- 索引不是焦点的一部分，组合时通常不必手传索引；有组合规则与“用谁的索引”的坑。
- 可按索引过滤；可 `reindexed` 重映射索引（如从 1 计数）。
- 可自建 indexed fold/traversal；也有保持/传播索引的组合方式（index-preserving）。
- Prism/Iso 的 indexed 变体少见；Fold/Traversal 最常用。
