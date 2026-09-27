# Ch.1 Obligatory Preamble（必要前言）

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
