# Optics By Example — 各章中文要点摘要

《Optics By Example》（Chris Penner）是一本以 Haskell `lens` 库为例、偏实践的 optics 教程。全书按 Lens → Fold → Traversal → Prism → Iso 等主线递进，强调可组合的双向数据变换、运算符与常见数据结构/JSON/Monad 场景。本书标注为早期访问/仍在完善，末尾有练习答案与若干计划中的章节。


---

## Ch.1 Obligatory Preamble（必要前言）

## 主要小节
- 1.1 About this book
- 1.2 Why should I read this book?
- 1.3 How to read this book
- 1.4 Chosen language and optics encodings
- 1.5 Your practice environment
- 1.6–1.8 示例约定、类型签名与练习说明

## 要点
- 本书仍是 **work in progress**，章节可能未完成或不精致；作者会迭代回改。
- 目标：让读者快速上手 optics，同时理解背后原理；建议 **线性阅读**，每节后做练习并对照书末答案。
- 示例语言/库固定为 **Haskell + `lens`**；其他语言/编码（encoding）需自行“翻译”语法与组合子名，但概念大多通用。
- 推荐用 `stack` 建练习项目，依赖含 `lens`、`containers`、`aeson`、`lens-aeson`、`mtl`、`text` 等；REPL 中 `import Control.Lens`。
- 教学中常给 **简化类型签名**，再逐步推广；初学不必被完整签名吓到。
- 练习是学习核心：做完一节练习再进入下一节。


---

## Ch.2 Optics（Optics 总览）

## 主要小节
- 2.1 What are optics?
- 2.2 Strengths / 2.3 Weaknesses
- 2.4 Practical optics at a glance
- 2.5 Impractical optics at a glance

## 要点
- Optics 是一族 **可互相组合** 的工具：Lens、Fold、Traversal、Prism、Iso 等；新种类仍在出现。
- 一句话：optics = 用于构建 **双向数据变换** 的可组合组合子族。
- **优势**：组合深入嵌套数据；把“选哪块数据”与“对数据做什么”分离；写法常极短；可当稳定对外接口（类似 getter/setter）；生态成熟。
- **劣势/成本**：学习曲线陡；底层编码（encoding）多样且复杂；组合子数量巨大，需学会检索而非死记。
- 实用一瞥：`view`/`set`/`over`/`sumOf`、深层路径、按条件截断字符串等。
- “不实用但炫技”示例展示适应性：`partsOf` 重排偶数、`biplate` 全域改数、按词首大写等——说明同一套抽象能覆盖很广操作。


---

## Ch.3 Lenses（透镜（Lens））

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


---

## Ch.4 Polymorphic Optics（多态 Optics）

## 主要小节
- 4.1 Introduction to polymorphic optics
- 4.2 When do we need polymorphic lenses
- 4.3 Composing Lenses

## 要点
- Simple：`Lens' s a`；Polymorphic：`Lens s t a b`。
- 含义：`s`/`a` 是动作 **前** 的结构/焦点类型，`t`/`b` 是动作 **后**；`Lens' s a = Lens s s a a`。
- 需要多态透镜的典型场景：更新字段时 **改变字段类型**（如 `String`→`Text`，或改 `Either e` 的错误类型等）。
- 组合是 Lens 真正强项：深层嵌套记录用 `person.address.streetAddress.streetName` 一类路径，避免手写层层 record update。
- 组合用 `(.)`（从左到右读“先外后内”的路径直觉与函数复合方向需习惯）；路径像 OO 的点号链。
- `makeLenses` 应放在相关 `data` 声明之后，避免“类型不在作用域”错误。


---

## Ch.5 Operators（运算符）

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


---

## Ch.6 Folds（折叠（Fold））

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


---

## Ch.7 Traversals（遍历（Traversal））

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


---

## Ch.8 Indexable Structures（可索引结构）

## 主要小节
- 8.1 What’s an “indexable” structure?
- 8.2 Accessing and updating with `Ixed`
- 8.3 Inserting & Deleting with `At`
- 8.4 Custom Indexed Data Structures
- 8.5 Handling missing values

## 要点
- 可索引结构：值存在 **命名位置**（list 用 `Int`，Map 用 key，Tree 用 `[Int]` 路径等）。
- `Ixed` / `ix`：按索引得到 **Traversal'**（位置可能不存在故非 Lens）；统一 list/Map/Text/ByteString 等接口。
- `Index` / `IxValue` 是 type family，描述索引与值类型。
- `At` / `at`：面向 Map 类结构，焦点为 `Maybe v`，可 **插入/删除**（`Nothing` 表示删除）；与仅更新已有位置的 `ix` 不同。
- `sans` 等辅助删除键。
- 可自定义 `Ixed`/`At`（如循环取模的 `Cycled`、大小写不敏感 Map、甚至非容器类型）。
- 缺失处理：`failover`（更新若无焦点则失败/`empty`）；`failing`（路径内主备回退）；`non` 为 `Maybe` 提供默认值，常与 `at` 搭配做“缺省则当默认再写回”。


---

## Ch.9 Prisms（棱镜（Prism））

## 主要小节
- 9.1 Introduction to Prisms
- 9.2 Writing Custom Prisms
- 9.3 Laws
- 9.4 Case Study: Simple Server

## 要点
- Prism：最多聚焦 **0 或 1** 个值；是合法 Traversal；额外能力 **Embed**（反向嵌入/构造）。
- 适合 **和类型（sum）** 与模式匹配语义；构造子棱镜常命名 `_Left`、`_Just` 等。
- 匹配用 `preview`/`^?`；匹配成功可 `set`/`over`/`traverse`；嵌入用 `review` / `#`。
- `has` / `isn't`（及 Extras 中的 `is`）做“是否匹配”检查。
- 自定义：`prism` / `prism'`（注入函数 + 匹配函数返回 `Either`）。
- 定律核心：可逆的模式匹配——**Review-Preview**、**Prism Complement**、**Pass-through Reversion**；`_Show` 等可能因规范化格式轻微违法。
- 案例：简单服务器路由/请求匹配等，展示 Prism 组合表达协议分支。


---

## Ch.10 Isos（同构（Iso））

## 主要小节
- 10.1 Introduction to Isos
- 10.2 Building Isos
- 10.3 Flipping isos with `from`
- 10.4 Modification under isomorphism
- 10.5 Varieties of isomorphisms
- 10.6 Projecting Isos
- 10.7 Isos and newtypes
- 10.8 Laws

## 要点
- Iso = isomorphism：两表示间 **完全可逆、无损** 的变换（如 `String`↔`Text`）。
- 约束最强：必须对所有输入成功且可逆；因此 Iso 可当作 Lens/Traversal/Prism/Fold 等使用。
- 本质是一对互逆函数 `to`/`from`：`to . from = id`，`from . to = id`。
- 构建：`iso to from`；用 `from` 翻转方向。
- 可在“另一视图”下修改再自动转回（把 `String` 当 `Text` 编辑等）。
- 品种：涉及单位、打包/解包、枚举映射、坐标变换等；可 **投影**（project）到结构的一部分。
- 与 **newtype** 关系密切（包装/解包同构）。
- 定律强调往返恒等；排序列表等若丢失原顺序信息则无法做成合法 Iso。


---

## Ch.11 Indexed Optics（带索引的 Optics）

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


---

## Ch.12 Dealing with Type Errors（处理类型错误）

## 主要小节
- 12.1 Interpreting expanded optics types
- 12.2 Type Error Arena

## 要点
- Optics 能力强，类型错误也吓人；关键是拆解信息、练启发式，不要气馁。
- Van Laarhoven 展开后，错误常表现为 **约束 + 具体类型构造器** 不匹配（如 `Contravariant Identity`）。
- 对照附录“Optic Ingredients”：`Identity` 常见于 `set`/`over`；`Contravariant` 常见于 **Fold**——故对 Fold 做写入会炸，应改用 `traversed` 等 Traversal。
- Type Error Arena：通过故意写错的表达式练读 GHC 报错并修复。
- 实践建议：记常用 optic 的约束画像，比死背完整签名更有效。


---

## Ch.13 Optics and Monads（Optics 与 Monad）

## 主要小节
- 13.1 Reader Monad and View
- 13.2 State Monad Combinators
- 13.3 Magnify & Zoom

## 要点
- `view` 的真实约束含 `MonadReader`：在 Reader 环境中可直接 `view someLens`；纯函数情形因 `(->) s` 也是 `MonadReader`。
- 同理 `preview` 可在 Reader 上跑 Fold/Prism 路径。
- State 侧有一族更新运算符：`.=`（对应 `.~`）、`%=`（对应 `%~`）等，在 `State`/`StateT` 里对焦点读写改。
- `magnify`：把 Reader 环境“缩小”到子结构（透镜聚焦的那部分）再跑子计算。
- `zoom`：对 State 做类似的事——在子状态上运行 `State` 动作。
- 这些是 QoL 组合子，让 optics 与常见 monad 栈自然配合。


---

## Ch.14 Classy Lenses（Classy Lenses 设计模式）

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


---

## Ch.15 JSON（JSON）

## 主要小节
- 15.1 Introspecting JSON
- 15.2 Diving deeper into JSON structures
- 15.3 Traversing into multiple JSON substructures
- 15.4 Filtering JSON Queries
- 15.5 Serializing & Deserializing within an optics path
- 15.6 Exercises: Kubernetes API

## 要点
- 优先把 JSON 反序列化成记录再用 optics；但松散 JSON 上，optics + `lens-aeson` 极适合即席查询/修改。
- `aeson` 的统一类型是 `Value`；用 `_String`/`_Number`/`_Object`/`_Array` 等 Prism 探查。
- 助手：`key`（=`_Object . ix k`）、`nth`（=`_Array . ix i`）；插入新键常用 `_Object . at k`。
- 分支遍历：`values`（数组元素）、对象 values/members 等；不匹配的棱镜会静默跳过（异构数组只取数字等）。
- 可过滤、可与 indexed 动作配合拿下标。
- 路径中可嵌入（反）序列化，在子树与强类型之间切换。
- 练习以 Kubernetes API JSON 为题材：版本、容器计数、端口、标签、资源请求等综合路径。


---

## Ch.16 Appendices（附录）

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


---

## Ch.17 Answers to Exercises（练习答案）

## 说明
- 本章是全书练习的参考答案，按主题分节（约 17.1–17.33），对应前面各章习题。
- **不是**新概念章节；学习时应先自解再对照。

## 覆盖主题（目录级）
- Optic Anatomy、Lens 动作与记录、虚拟字段、自校正透镜
- 多态 Lens、组合、运算符
- Fold（简单/自定义/查询/高阶/过滤）
- Traversal（动作/自定义/定律/`partsOf`）
- 可索引结构、缺失值
- Prism / Iso / Indexed Optics
- 类型错误 Arena、Kubernetes JSON 练习

## 要点
- 答案强调正确 optic 选型（Lens vs Traversal vs Prism vs Iso）与惯用运算符。
- 对“违法但有用”的 optic，答案常讨论为何仍可接受。


---

## Ch.18 Upcoming Chapters（计划中的章节（WIP））

## 状态
- **未完成 / 预告**：作者列出拟新增内容，正文尚未写入（或仅占位）。

## 预告主题
- Classy prisms 及其在异常处理中的应用
- Uniplate / Biplate 组合子
- `failover`（正文索引章已涉及部分，或将扩写）
- Generic optics（`generic-lens`）

## 要点
- 现有正文已是较完整的 Haskell optics 实用指南；上述主题属于扩展与进阶补篇。
- 阅读早期访问版时，以已完成章节 + 附录/答案为主即可。
