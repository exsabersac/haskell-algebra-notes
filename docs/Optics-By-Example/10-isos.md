# Ch.10 Isos（同构（Iso））

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
