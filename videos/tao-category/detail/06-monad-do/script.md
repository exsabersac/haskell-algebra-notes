# 道可道 · 深讲 06 —— Monad 与 do 记法
*bind、鱼子、定律；do；Maybe / List｜Monad & do-notation — Deep Dive 06*
- 成片时长：**08:08**（488.8 秒），1920×1080，30 fps
- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。
- 结构：钩子 → bind / 鱼子 → 定律浅讲 → do 记法 → Maybe/List 代码 → 进阶篇预告。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-06.srt`。
- 屏幕代码摘自 `haskell/src/MonadDo.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。本集为入门深讲最后一集。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 道生一 | 15 Monads（效应链） | 3.4–3.5 Monads |
| bind / 鱼子 | 15 bind / Kleisli | 3.4 fish |
| 定律浅讲 | 15 monad laws | 3.5–3.6 |
| do 记法 | 15 do-notation | 3.4 |
| Maybe / List | 15 instances | 3.4–3.5 |
| 进阶预告 | — | 不动点 / 伴随 / 米田 |

## 术语表

| 中文 | English |
|---|---|
| 单子 / Monad | monad |
| 绑定 / bind | bind / (>>=) |
| 注入 / return | return / pure / unit |
| 鱼子 / Kleisli 复合 | fish / (>=>) / Kleisli composition |
| do 记法 | do-notation |
| 左 / 右单位定律 | left / right unit law |
| 结合律 | associativity |

---

## Monad 与 do 记法　`00:00–00:53`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 道生一。欢迎来到「道可道」深讲第六集——也是入门深讲的最后一集。 | 宣纸背景，圆相一笔画出；标题「Monad 与 do 记法」浮现 |
| 00:08 | 上一集钉牢函子：保形、抬箭头。这一集，在函子之上接「效应」——把一步一步的计算，串成一条能失败、能分支的链。函子管形状；Monad 管「下一步怎么走」。 | 小字：深讲 05 → 06；提纲 bind / 定律 / do |
| 00:25 | 范畴论里，这叫 Monad：有注入，有绑定；还有鱼子复合。先把话说明白，再落到几行 Haskell，以及 do 记法。 | 三行：bind · 定律 · do |
| 00:37 | 框架仍是 Milewski 的两本书：《函数式编程之道》第十五章，以及《程序员的范畴论》里 Monad 那几节。片中表述都是释义，不是照录。 | DaoFP ch.15 · CTFP 3.4–3.6；印章「知白守黑」 |

---

## 一 · 道生一　`00:53–01:55`

> **道生一。**　——《道德经》第四十二章

参考：DaoFP ch.15 Monads（效应链）；CTFP 3.4–3.5 Monads / Kleisli

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:54 | 道生一。 | 竖排书法原文，右起 |
| 00:58 | 入门篇扫过 Monad；深讲第五集刚把函子钉牢。这一集，我们把「效应如何串联」单独拉开。函子改内容；Monad 还要决定下一步往哪走。映射是一层；串联，是另一层。 | 小字：入门篇 → 深讲 06；效应串联 |
| 01:17 | 先问范畴论的问题：手里有一块带着效应的值，和下一步「吃纯值、交回效应」的箭头——能不能接成更长的一条？能，就叫它 Monad。 | 效应值 + 下一步 → 更长的链 |
| 01:31 | Milewski 的画面：函子是外套；Monad 还多一枚钮扣——能把「外套里的外套」解开一层，接到下一段旅程。 | 小字：join / bind · 道生一 |
| 01:42 | 慢一点。先把 bind 与鱼子看明白；后面的定律与 do，都站在它们上面。一生二，二生三——链，就这样长出来。 | 书法小字：绑定 |

---

## 二 · bind 与鱼子　`01:55–03:22`

参考：DaoFP ch.15 bind / Kleisli；CTFP 3.4 fish operator

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 01:56 | Monad 先做两件事。第一，注入：把一个纯值 a，放进效应壳，得到 m a。Haskell 里常叫 return，也叫 pure。 | return :: a → m a |
| 02:09 | 第二，绑定 bind：手里有一块 m a，和一条「从 a 交回 m b」的箭头。bind 把它们接起来，交出 m b。效应不拆掉，只往前走。 | (>>=) :: m a → (a → m b) → m b |
| 02:23 | 对照函子：fmap 吃的是「纯箭头」a 到 b；bind 吃的是「带效应的箭头」a 到 m b。多出来的那一层效应，正是链式的关键。 | fmap vs bind |
| 02:36 | 把两条带效应的箭头首尾相接，就得到鱼子运算符：大于等于大于。先跑 f，再把结果交给 g。这是克莱斯利范畴里的复合。 | (>=>) 鱼子 / Kleisli |
| 02:50 | 日常比喻：函子是换衬衫；Monad 是「按说明书走下一步」——说明书本身也可能失败，也可能分出多条岔路。失败走 Maybe；分岔走列表。同一接口，两种脾气。 | 下一步可能失败 / 分支 |
| 03:07 | 所以 Monad 不是「再写一个 map」。它是：在效应的形状上，把计算接成链。形状仍先于操作——只是形状里，多了「如何继续」的记忆。 | 效应上的链式复合 |

---

## 三 · 定律浅讲　`03:22–04:41`

参考：DaoFP ch.15 monad laws；CTFP 3.5–3.6

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:23 | Monad 不止要有 return 与 bind，还要守三条定律。定律写不进类型，却写进责任：左单位、右单位、结合律。 | 三条定律：左单位 · 右单位 · 结合 |
| 03:35 | 左单位：return 一个值，再 bind 上 f，必须等于直接对那个值施 f。注入不能偷偷加料。 | return a >>= f  =  f a |
| 03:46 | 右单位：一块效应值 bind 上 return，必须原样回来。结尾不能无故拆掉或加厚外壳。 | m >>= return  =  m |
| 03:55 | 结合律：先 bind f 再 bind g，必须等于一次 bind「f 鱼子 g」。链式怎么加括号，结果一样——结合，才叫一条道。括号可以挪，终点不许偷偷改。 | (m >>= f) >>= g  =  m >>= (f >=> g) |
| 04:11 | 为什么要定律？没有它们，bind 只是同名函数——可以乱序、吞步骤、把失败变成成功。有了定律，效应链才可组合、可替换。 | 无定律 = 不合法 Monad |
| 04:25 | 道生一：单位是「生」的干净起点；结合是「生」可以一直生下去。条文三条，分量不轻。今天只浅讲，进阶篇还会从伴随回头看。 | 书法：道生一 |

---

## 四 · do 记法　`04:41–06:00`

参考：DaoFP ch.15 do-notation；CTFP 3.4

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 04:41 | 链式 bind 写多了，尖括号会淹过人话。Haskell 给了一层语法糖：do 记法——看起来像顺序语句，语义仍是 bind。糖熔掉，底下还是那条链。 | do = >>= 的语法糖 |
| 04:57 | 箭头左边的名字，是从效应壳里取出的纯值；下一行可以继续用。最后一行往往是 return，或另一块效应。 | x <- mx  ·  return … |
| 05:09 | 重要提醒：do 不引入新语义。它不会让纯函数突然有副作用；它只是把已有的 Monad 实例，写得更像人话。 | 无新语义 · 可读性 |
| 05:20 | 看到 do，心里应还原成 bind 链；看到 bind，也可以写成 do。两种字体，同一条道。考试也好，阅读也好，都要能来回翻译。 | do ⟷ >>= |
| 05:34 | 还有一行只有效应、不绑名字的写法，对应小小的双大于号——先做前一步，丢掉它的纯值，只保留效应顺序。今天点到为止。 | >> 顺序 · 浅提 |
| 05:47 | do 是入门的梯子，不是终点。梯子稳了，再去看变换器、IO、解析器——都还是同一套 return 与 bind。 | 梯子 · 同一套接口 |

---

## 五 · Maybe 与 List　`06:00–07:20`

参考：DaoFP ch.15 Maybe / List monads；CTFP 3.4–3.5

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:01 | 把刚才的话写成几行 Haskell。先声明 Monad 类型类，再写鱼子，再写 Maybe 与列表的实例。类型写在前，匹配藏在里头。图怎么说，代码就怎么应。 | 代码块：s_class / s_fish |
| 06:18 | Maybe 的 bind：遇到 Nothing 整条链停；遇到 Just，把里头的值交给下一步。失败会短路——这是效应最直观的一种。 | 代码 s_maybe；高亮 instance |
| 06:30 | 列表的 bind：对每个元素展开下一步，再拼平。一变多、多再变多——不确定计算，或者「搜索所有可能」。 | 代码 s_list；nondeterminism |
| 06:41 | 试一下：Just 二十，加一，再乘二，得到 Just 四十二；列表一对二，每个再分出自身与十倍，得到一、十、二、二十。 | demoMaybe / demoList |
| 06:55 | 同一条链，用 do 再写一遍：名字一行行绑下来，最后 return。结果与尖括号版相同——糖，熔掉还是糖。 | 代码 s_do |
| 07:08 | 再抽查定律：左单位、右单位、结合，屏幕代码都能编译。图对齐了，代码只是把图念出来。 | 三条定律抽检 |

屏幕代码 `s_class`（`haskell/src/MonadDo.hs`）：

```haskell
-- Monad：在函子之上，多「注入」与「绑定」
-- return 把纯值放进效应；>>= 把「值上的下一步」接进效应链
class Monad m where
  return :: a -> m a
  (>>=)  :: m a -> (a -> m b) -> m b
```

屏幕代码 `s_fish`（`haskell/src/MonadDo.hs`）：

```haskell
-- 鱼子 / Kleisli 复合：先跑 f，再把结果交给 g
(>=>) :: Monad m => (a -> m b) -> (b -> m c) -> (a -> m c)
f >=> g = \x -> f x >>= g
```

屏幕代码 `s_maybe`（`haskell/src/MonadDo.hs`）：

```haskell
-- Maybe：空则整条链停；有值则交给下一步
instance Monad Maybe where
  return = Just
  Nothing  >>= _ = Nothing
  Just x   >>= k = k x

maybeBind :: Maybe a -> (a -> Maybe b) -> Maybe b
maybeBind = (>>=)
```

屏幕代码 `s_list`（`haskell/src/MonadDo.hs`）：

```haskell
-- 列表： nondeterminism —— 对每个元素展开下一步，再拼平
instance Monad [] where
  return x = [x]
  xs >>= k = concatMap k xs

listBind :: [a] -> (a -> [b]) -> [b]
listBind = (>>=)
```

屏幕代码 `s_demo`（`haskell/src/MonadDo.hs`）：

```haskell
-- 演示：链式绑定；外壳形状随效应走
demoMaybe :: Maybe Int
demoMaybe = Just 20 >>= \x -> Just (x + 1) >>= \y -> Just (y * 2)  -- Just 42

demoList :: [Int]
demoList = [1, 2] >>= \x -> [x, x * 10]  -- [1,10,2,20]
```

屏幕代码 `s_do`（`haskell/src/MonadDo.hs`）：

```haskell
-- do 记法：把 >>= 写成顺序可读的人话（语法糖，语义同 bind）
demoDoMaybe :: Maybe Int
demoDoMaybe = do
  x <- Just 20
  y <- Just (x + 1)
  return (y * 2)          -- Just 42

demoDoList :: [Int]
demoDoList = do
  x <- [1, 2]
  y <- [x, x * 10]
  return y                -- [1,10,2,20]
```

---

## 结 · 道生一　`07:20–08:08`

参考：进阶篇预告：不动点 · 伴随 · 米田

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 07:20 | 今天钉牢四件事：bind 把效应接成链；鱼子是克莱斯利复合；三条定律写成契约；do 是人话写法。入门深讲六集，从类型到函子再到效应，到此收束。 | 四句回顾环绕圆相 |
| 07:37 | 下一阶段，进入进阶篇：不动点——折叠与生成的不动点；伴随——左右两侧的最优翻译；米田——对象被它出发的箭头所认识。深讲是底，进阶往上长。三条线，各自成章。 | 预告：不动点 · 伴随 · 米田 |
| 07:56 | 借 Milewski 的提醒：先看形状，再看映射，再看效应如何串联。道生一。我们进阶篇见。 | 「道生一」书法；印章；谢谢观看 |

---

## 数学校对备注

- 依 CTFP 惯例在 Hask 中忽略 ⊥。
- 本集讲 Monad 的**直觉层**（bind / 鱼子 / 定律 / do）；不引入 transformer、IO、Free、Codensity。
- 用手写 `class Monad` 避免与 Prelude 混谈；实例覆盖 Maybe 与 []。
- join / μ 仅在叙述中作为「解开外套」隐喻，不单独展开定义。
- 进阶篇预告：不动点、伴随、米田——不在本集展开。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。
