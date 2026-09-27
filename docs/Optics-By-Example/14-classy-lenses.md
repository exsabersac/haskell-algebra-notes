# Ch.14 Classy Lenses（Classy Lenses 设计模式）

## 主要小节
- 14.1 What are classy lenses and when do I need them?
- 14.2 `makeFields` vs `makeClassy`

## 要点
- Classy lenses **不是新 optic 种类**，而是设计模式：字段多态、分层解耦、限制模块“知识面”。
- 解决 Haskell 记录字段不能重名、难以对“都有 name 的类型”写多态函数的问题。
- `makeFields`：按 `_TypeField` 前缀惯例生成 `HasField` 类（如 `HasName`）及统一 `name` 透镜。
- 于是可写 `HasName s String => s -> IO ()` 一类函数，Person/Pet 共用。
- `makeClassy`：常为整个记录生成一个 class（如 `HasEnv`），内含各字段透镜，便于“只要环境里有这块配置就能跑”。
- 权衡：引入更多类型类与扩展（`FunctionalDependencies` 等）；是大型应用组织代码的工具，不是入门必选项。
