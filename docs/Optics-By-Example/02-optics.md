# Ch.2 Optics（Optics 总览）

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
