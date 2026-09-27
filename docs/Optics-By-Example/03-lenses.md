# Ch.3 Lenses（透镜（Lens））

## 主要小节
- 3.1 Introduction to Lenses
- 3.2 Lens actions
- 3.3 Lenses and records
- 3.4 Limitations（“Is it a Lens?”）
- 3.5 Lens Laws
- 3.6 Virtual Fields
- 3.7 Data correction and maintaining invariants

## 要点
### 解剖与动作
- 把操作拆成：**Action**（做什么）、**Path**（选哪里）、**Structure**（整块数据）、**Focus**（焦点）。
- Lens 约束：始终聚焦 **恰好一个** 焦点；获取/修改 **不能失败**。
- 核心动作：`view` / `set` / `over`（看、设、改）。

### 记录字段
- Lens 对应 OO 的 accessor 模式：getter+setter 打成 **一个一等值**。
- 用 `lens :: (s -> a) -> (s -> a -> s) -> Lens' s a` 手写；字段常命名为 `_field`，腾出 `field` 给透镜。
- `makeLenses`（Template Haskell）按去掉前导 `_` 自动生成字段透镜。
- 类型习惯：`s` = structure，`a` = focus；带 `'` 的如 `Lens'` 表示 **simple** optic。

### 限制与定律
- 不能合法做成 Lens 的典型情况：`Maybe`/`Either` 内值（可能缺失）、列表第 n 个（可能失败）、依赖条件切换焦点等——这些更适合 Prism/Traversal。
- 三大定律（指导原则）：**set-get**、**get-set**、**set-set**；保证行为可预测、无奇怪副作用。
- 违法（unlawful）透镜有时有用（虚拟字段、校正），但应知情后使用。

### 虚拟字段与不变量
- Virtual field：无真实字段、由计算呈现的“概念字段”（如 Celsius↔Fahrenheit、`fullName`）。
- 可在 setter 中做 **钳位/进位** 等校正以维持不变量（如时钟时分范围）；常违反定律，需权衡。
