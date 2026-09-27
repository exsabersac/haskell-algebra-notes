# Ch.4 Polymorphic Optics（多态 Optics）

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
