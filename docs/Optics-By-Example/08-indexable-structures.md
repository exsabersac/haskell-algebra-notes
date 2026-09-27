# Ch.8 Indexable Structures（可索引结构）

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
