# Ch.5 Operators（运算符）

## 主要小节
- 5.1 Lens Operators
- 5.2 `view` a.k.a. `^.`
- 5.3 `set` a.k.a. `.~`
- 5.4 Chaining many operations
- 5.5 `%∼` a.k.a. `over`
- 5.6 Learning Hieroglyphics
- 5.7 Modifiers
- 5.8 When to use operators vs named actions?
- 5.9 Exercises

## 要点
- `lens` 提供大量 **中缀运算符**，让读写改更短、更“淡化语法”。
- 常用对应：`^.` ↔ `view`；`.~` ↔ `set`；`%~` ↔ `over`。
- 用 `&`（反向应用）串联多次更新：`struct & lens1 .~ v & lens2 %~ f`。
- “象形文字”有规律：同一家族运算符共享符号骨架；陌生运算符可用 Hoogle。
- 另有 `+~`、`*~`、`||~` 等 **修饰符**，在焦点上做常见算术/逻辑更新。
- 命名动作更利教学与跨语言迁移；Haskell 实践中运算符更常见——别滥用到不可读。
