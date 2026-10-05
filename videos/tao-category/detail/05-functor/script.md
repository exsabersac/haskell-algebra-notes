# 道可道 · 深讲 05 —— Functor 直觉
*保形、fmap、定律；Maybe / List｜Functor Intuition — Deep Dive 05*
- 成片时长：**08:16**（496.7 秒），1920×1080，30 fps
- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。
- 结构：钩子 → 函子保形 → fmap / 交换图 → 定律 → Maybe/List 代码 → 预告 Monad。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-05.srt`。
- 屏幕代码摘自 `haskell/src/FunctorIntuition.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 大制不割 | 8 Functors（保形） | 1.7 Functors（no-tearing） |
| 函子保形 | 8 Functors between categories | 1.7 |
| fmap / 交换图 | 8 fmap | 1.7 lifting |
| 定律 | 8 preserve id & ∘ | 1.7 laws |
| Maybe / List | 8 instances | 1.7 Maybe Functor |
| 下一集预告 | 15 Monads | 3.4–3.6 Monads |

## 术语表

| 中文 | English |
|---|---|
| 函子 / Functor | functor |
| 保形 / 不撕裂 | shape-preserving / no-tearing |
| fmap / 抬升 | fmap / lifting |
| 类型构造子 | type constructor |
| 单位定律 | identity law |
| 复合定律 | composition law |
| 自函子（浅提） | endofunctor (mention) |

---

## Functor 直觉　`00:00–00:49`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 大制不割。欢迎来到「道可道」深讲第五集。 | 宣纸背景，圆相一笔画出；标题「Functor 直觉」浮现 |
| 00:06 | 上一集讲构造与折叠：生与归，都沿着构造子走。这一集，我们把「形状」本身提出来——在结构上描画箭头，而不拆掉结构。 | 小字：深讲 04 → 05；提纲 保形 / fmap / 定律 |
| 00:20 | 范畴论里，这叫函子：对象映到对象，箭头映到箭头，还要保住复合与单位。先把话说明白，再落到几行 Haskell。 | 三行：函子保形 · fmap · 定律 |
| 00:33 | 框架仍是 Milewski 的两本书：《函数式编程之道》第八章函子，以及《程序员的范畴论》里函子那两节。片中表述都是释义，不是照录。 | DaoFP ch.8 · CTFP 1.7–1.8；印章「知白守黑」 |

---

## 一 · 大制不割　`00:49–01:52`

> **大制不割。**　——《道德经》第二十八章

参考：DaoFP ch.8 Functors（保形直觉）；CTFP 1.7 Functors（no-tearing）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:50 | 大制不割。 | 竖排书法原文，右起 |
| 00:54 | 入门篇扫过 Functor；深讲第四集刚把折叠钉牢。这一集，我们把「映射而不撕裂」单独拉开。结构可以换里头的值，外壳不许被撕开。映射，不等于拆开重装。 | 小字：入门篇 → 深讲 05；映射而不撕裂 |
| 01:12 | 先问范畴论的问题：一类结构，能不能把里头的箭头「抬」到外壳上，而外壳的形状不变？能，就叫它函子。不能，就还不是。 | 抬箭头 · 保形 |
| 01:27 | Milewski 有个画面：范畴像一张织好的网。函子可以压扁、可以粘合，但不许撕破。连续感，来自「不撕裂」。 | 小字：no-tearing · 大制不割 |
| 01:39 | 慢一点。先把「保形」看明白；后面的 fmap，都站在它上面。映射，是折叠之前的那一层薄纱。 | 书法小字：保形 |

---

## 二 · 函子保形　`01:52–03:22`

参考：DaoFP ch.8 Functors between categories；CTFP 1.7

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 01:52 | 函子做两件事：把对象映成对象，把箭头映成箭头。对类型来说，对象是类型，箭头是函数。类型构造子，先完成第一步——把 a 映成 F a。 | F : 对象 → 对象；Maybe a / List a |
| 02:09 | Maybe 把 a 变成「也许有一个 a」；列表把 a 变成「一串 a」。它们本身不是类型，是类型构造子——要喂进一个类型，才变成类型。 | type constructor ≠ type |
| 02:22 | 第二步更要紧：手里有一条箭头 f，从 a 到 b。函子要交出一条新箭头，从 F a 到 F b。外壳还在，里头的值被 f 改写。 | f : a → b  ⇒  F f : F a → F b |
| 02:37 | 这就是保形：结构记得自己怎么被造出来。你只改「内容」那一层记忆，不改构造的骨架。Just 还是 Just，空列表还是空列表。 | 记得构造 · 只改内容 |
| 02:50 | 日常比喻：函子像一件外套。你换里头的衬衫，外套的剪裁不变。换衬衫是 fmap；剪裁是那个类型构造子。 | 外套隐喻：剪裁不变 |
| 03:03 | 所以函子不是「随便一个 map」。它是：在同一张网的形状上，把箭头抬过去。形状先于操作——这话，跟上一集的代数遥相呼应。先认形状，再谈映射。 | 形状先于操作 |

---

## 三 · fmap 与交换图　`03:22–04:48`

参考：DaoFP ch.8 fmap；CTFP 1.7（lifting / commuting square）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:22 | Haskell 里，把箭头抬上去的那一步，叫 fmap。类型写出来很素：吃一条 a 到 b，交出一条 F a 到 F b。 | fmap :: (a → b) → (F a → F b) |
| 03:35 | 画成交换图更清楚：左边是原来的 f，右边是抬上去的 F f；上下是「放进结构」的虚线。两条路径，说的是同一件事——结构与箭头一起走。 | 交换正方形：a→b 与 Fa→Fb |
| 03:49 | 看 Maybe：空还是空；有值，就对里头那个值施 f，再包回 Just。外壳两支，一支不动，一支只动内容。 | Nothing 不动；Just x → Just (f x) |
| 04:01 | 看列表：对每个元素施 f，长度与顺序都不动。一、二、三，乘二之后，仍是三个格子——二、四、六。保形，肉眼可见。 | 动画 [1,2,3] → [2,4,6] |
| 04:18 | 术语上，这叫 lifting：把在值上的计算，抬到结构里去做。你不用拆开结构自己循环——函子替你保管形状。 | lifting · 抬升 |
| 04:29 | 交换图不是装饰。它强迫你核对：先映射再装箱，与先装箱再映射，是否一致。一致，才叫函子；不一致，只是碰巧同名的函数。图在说话，代码在应和。 | 路径一致 = 函子 |

---

## 四 · 函子定律　`04:48–06:14`

参考：DaoFP ch.8（preserve composition & identity）；CTFP 1.7 laws

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 04:49 | 函子不止要有 fmap，还要守两条定律。定律写不进 Haskell 的类型，却写进你的责任：单位，与复合。 | 两条定律：id · 复合 |
| 05:02 | 第一，单位：fmap id，等于 id。对结构施「什么都不做」，结构必须原样回来。Just 三还是 Just 三；列表不增不减。 | fmap id = id |
| 05:16 | 第二，复合：先 fmap f 再 fmap g，必须等于一次 fmap「g 圆点 f」。抬两次，等于抬一次复合后的箭头。顺序不许偷偷调换。 | fmap (g ∘ f) = fmap g ∘ fmap f |
| 05:31 | 为什么要定律？因为没有它们，fmap 只是个同名函数——可以撕破形状，可以乱序，可以吞掉元素。有了定律，保形才被钉死。 | 无定律 = 不合法函子 |
| 05:45 | Milewski 提醒：编译器认的是类型类实例；合法与否，要人来核对。坏的 map 也能过类型检查——所以定律不是口号，是契约。 | typeclass ≠ laws |
| 05:59 | 大制不割：定律就是「不割」的条文。单位保真，复合保序。守住这两条，函子才名副其实。条文简单，分量不轻。 | 书法：大制不割 |

---

## 五 · Maybe 与 List　`06:14–07:34`

参考：DaoFP ch.8 Maybe / List instances；CTFP 1.7

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:15 | 把刚才的话写成几行 Haskell。先声明 Functor 类型类，再写出 Maybe 与列表的实例。类型写在前，匹配藏在里头。 | 代码块：s_class |
| 06:28 | Maybe 的 fmap：遇到 Nothing 原样返回；遇到 Just，对里头的值施 f。空不生有，有则改内容——保形的最小例子。 | 代码 s_maybe；高亮 instance |
| 06:41 | 列表的 fmap：空还是空；非空则头施 f，尾递归同样做。长度不变，顺序不变。你每天写的 map，就是它。 | 代码 s_list |
| 06:54 | 试一下：对 Just 四十一加一，得到 Just 四十二；对一、二、三乘二，得到二、四、六。外壳没动，数字动了。 | demoMaybe / demoList |
| 07:09 | 再抽查定律：fmap id 不改 Just，不改列表；先加一再乘二，与一次复合再 fmap，结果相同。屏幕代码都能编译。 | id / 复合 抽检 |
| 07:22 | 图对齐了，代码只是把图念出来。Bifunctor、Contravariant，留给以后；今天只把协变函子的直觉钉牢。 | 对照：图 ⟷ 代码；不引入反变 |

屏幕代码 `s_class`（`haskell/src/FunctorIntuition.hs`）：

```haskell
-- 函子：把「值上的箭头」抬到「结构上的箭头」
-- fmap 保形：结构的外壳不动，只改里头的值
class Functor f where
  fmap :: (a -> b) -> f a -> f b
```

屏幕代码 `s_maybe`（`haskell/src/FunctorIntuition.hs`）：

```haskell
-- Maybe：空仍空；有值则对里头的值施 f
instance Functor Maybe where
  fmap _ Nothing  = Nothing
  fmap f (Just x) = Just (f x)

-- 同一箭头，两种写法对照
maybeFmap :: (a -> b) -> Maybe a -> Maybe b
maybeFmap = fmap
```

屏幕代码 `s_list`（`haskell/src/FunctorIntuition.hs`）：

```haskell
-- 列表：对每个元素施 f，长度与顺序不变 —— 保形
instance Functor [] where
  fmap _ []     = []
  fmap f (x:xs) = f x : fmap f xs

listFmap :: (a -> b) -> [a] -> [b]
listFmap = fmap
```

屏幕代码 `s_demo`（`haskell/src/FunctorIntuition.hs`）：

```haskell
-- 演示：(+1) 抬到 Maybe / List；结构外壳不动
demoMaybe :: Maybe Int
demoMaybe = fmap (+ 1) (Just 41)   -- Just 42

demoList :: [Int]
demoList = fmap (* 2) [1, 2, 3]    -- [2, 4, 6]
```

---

## 结 · 大制不割　`07:34–08:16`

参考：DaoFP ch.15 Monads；CTFP 3.4–3.6；下一集 Monad / do

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 07:35 | 今天钉牢三件事：函子保形，不撕裂结构；fmap 把箭头抬到外壳上；单位与复合两条定律，把保形写成契约。形状清楚了，效应才接得上。 | 三句回顾环绕圆相 |
| 07:50 | 下一集，我们把「效应」接进来：Monad——在函子之上，多一层绑定与注入。do 记号会登场，把链式计算写成人话。函子是底，Monad 往上长。 | 预告：Monad · do；小字「深讲 06」 |
| 08:06 | 借 Milewski 的提醒：先看形状，再看映射。大制不割。我们下集见。 | 「大制不割」书法；印章；谢谢观看 |

---

## 数学校对备注

- 依 CTFP 惯例在 Hask 中忽略 ⊥。
- 本集讲函子的**直觉层**（保形 / fmap / 定律）；不引入 Bifunctor、Contravariant、Profunctor、Yoneda。
- 用手写 `class Functor` 避免与 Prelude 混谈；实例覆盖 Maybe 与 []。
- 「自函子」仅在叙述中作为 Hask→Hask 的背景，不单独展开。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。
