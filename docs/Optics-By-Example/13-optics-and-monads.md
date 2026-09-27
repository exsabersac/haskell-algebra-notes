# Ch.13 Optics and Monads（Optics 与 Monad）

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
