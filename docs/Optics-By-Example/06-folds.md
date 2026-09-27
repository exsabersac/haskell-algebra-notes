# Ch.6 Folds（折叠（Fold））

## 主要小节
- 6.1 Introduction to Folds
- 6.2 Custom Folds
- 6.3 Fold Actions
- 6.4 Higher Order Folds
- 6.5 Filtering folds
- 6.6 Fold Laws（基本无严格定律）

## 要点
- Fold ≈ **查询**：可聚焦 **多个**（或零个）焦点；只能读，不能设。
- 相对 Lens：失去 set/over，换来任意过滤与“空结果合法”；Fold **几乎没有定律**。
- 隐喻：像把食材揉进面团——合起来好吃，但难再拆开写回原结构。
- 基础：`folded`（任意 `Foldable`）、`both`/`each`、与 Lens 路径组合；收集用 `toListOf` / `^..`，可能空则用 `preview`/`^?`。
- 自定义 Fold：`folding` / `to` 等，把任意“取出若干值”的逻辑变成可组合查询（如船员名列表、Map 的 keys）。
- 动作族：`sumOf`/`lengthOf`/`maximumOf`/`minimumByOf`、带效应的 `traverseOf_`/`forOf_` 等——像 `Data.Foldable` 的 a-la-carte 版。
- Higher-order：`taking`/`dropping`/`takingWhile` 等对 Fold 再截取。
- `filtered`：像 SQL 的 WHERE，在路径中间按谓词缩焦点，再继续深入；威力大、极常用。
