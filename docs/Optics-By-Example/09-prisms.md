# Ch.9 Prisms（棱镜（Prism））

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
