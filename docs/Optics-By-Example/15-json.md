# Ch.15 JSON（JSON）

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
