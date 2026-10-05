# YouTube 发布信息（草案）

## 标题
道可道：用《道德经》读范畴论与 Haskell | The Dao of Categories: Fixpoints, Adjunctions & Yoneda

（80 字符，YouTube 上限 100）

## 说明
```
用六句《道德经》，重读范畴论里最核心的几件事：始对象与终对象、初始代数与兰贝克引理、代数与余代数的对偶、伴随（State 与 Store），以及米田引理。每一段都是同一个节奏：先读原文，再给出范畴论的陈述，最后落到几行 Haskell。

老子是钩子，数学是正文。本片面向已经会 Haskell、读过《程序员的范畴论》（CTFP）或《函数式编程之道》（DaoFP）的观众，跳过基本定义，只讲新的视角：
· 对象不可道，只有箭头可道——直到米田引理把这句话赎回来
· 道生一，一生二，二生三：从 Void 出发反复作用 Maybe，恰好得到 0、1、2、3 个值，这条链的余极限就是自然数（Adámek 定理）
· 道法自然：Fix f ≅ f (Fix f)，道是它自己的不动点
· 反者道之动：翻转箭头，cata 变成 ana；hylo 先生后归，生而不有
· 知其雄，守其雌：同一个柯里化伴随 (,) s ⊣ (->) s，一面是 State 单子，一面是 Store 余单子
· 无为而无不为：forall x. (a -> x) -> f x ≅ f a

章节
00:00 开场：六句话，一件事
00:42 一 道可道：对象不可道，箭头可道
02:15 二 有无相生：始对象与终对象
04:13 三 道生一：初始代数、兰贝克引理与 cata
06:52 四 反者道之动：余代数、ana 与 hylo
09:20 五 知其雄，守其雌：伴随生出 State 与 Store
11:20 六 无为而无不为：米田引理与 Kan 扩张
13:44 结语：看箭头

参考（本片框架主要参照 Bartosz Milewski 的两本书，叙述为释义改写）
· The Dao of Functional Programming（DaoFP）：第 1 章 Clean Slate、第 2 章 Composition、第 3 章 Isomorphism、第 7 章 Recursion、第 9 章 Natural Transformations（Yoneda）、第 10 章 Adjunctions、第 11 章 Algebras、第 12 章 Coalgebras、第 16 章 Monads and Adjunctions、第 17 章 Comonads、第 20 章 Kan Extensions —— https://github.com/BartoszMilewski/DaoFP
· Category Theory for Programmers（CTFP）：1.5、1.6、2.5 Yoneda Lemma、2.6 Yoneda Embedding、3.2 Adjunctions、3.6 Monads Categorically、3.7 Comonads、3.8 F-Algebras、3.11 Kan Extensions —— https://github.com/hmemcpy/milewski-ctfp-pdf
· 《道德经》第一、二、二十八、三十七、四十、四十二章

代码：片中全部 Haskell 代码均可用 GHC 编译运行（仓库链接待补）。
制作：Manim Community · 旁白 Microsoft Edge 神经语音（zh-CN-YunxiNeural）· 字体 霞鹜文楷 / Ma Shan Zheng / IBM Plex Mono / EB Garamond（均为 SIL OFL）。无背景音乐。

#范畴论 #Haskell #道德经
```

## 章节（与成片实际时间一致，成片总长 14:06）
```
00:00 开场：六句话，一件事
00:42 一 道可道：对象不可道，箭头可道
02:15 二 有无相生：始对象与终对象
04:13 三 道生一：初始代数、兰贝克引理与 cata
06:52 四 反者道之动：余代数、ana 与 hylo
09:20 五 知其雄，守其雌：伴随生出 State 与 Store
11:20 六 无为而无不为：米田引理与 Kan 扩张
13:44 结语：看箭头
```

## 标签
范畴论, Haskell, 道德经, 老子, 函数式编程, 米田引理, Yoneda lemma, 伴随, adjunction, 初始代数, initial algebra, 兰贝克引理, Lambek lemma, catamorphism, anamorphism, hylomorphism, 递归模式, recursion schemes, State monad, Store comonad, Kan extension, category theory, Bartosz Milewski, Dao of Functional Programming, Category Theory for Programmers, Manim

## 其他
- 缩略图：`final/thumbnail.png`（1280×720）
- 字幕：画面已烧录中文字幕；`final/tao-category.srt` 可作为 YouTube 中文字幕轨上传（便于搜索与自动翻译；如上传，建议默认关闭以免与烧录字幕重叠），或改用无烧录版本 `final/tao-category-nosubs.mp4` + 上传 SRT。
- 分类建议：教育（Education）；语言：中文（简体）。
