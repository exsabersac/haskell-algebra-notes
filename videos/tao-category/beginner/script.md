# 道可道 · 范畴入门 —— 解说稿
*用六句《道德经》入门范畴论与 Haskell｜The Dao of Categories — Beginner*
- 成片时长：**13:36**（816.9 秒），1920×1080，30 fps
- 受众：会一点编程；Haskell 零基础或略知即可。慢节奏、日常比喻、少公式、多直觉。
- 结构：每段 = 《道德经》原文 → 日常比喻 → 几行 Haskell。哲学只是钩子，数学必须正确。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-beginner.srt`。
- 屏幕上的全部代码都直接摘自 `haskell/src/*.hs`（以 `-- {{snip:…}}` 标记抽取），并经 GHC 9.14.1 `-Wall` 编译通过。
- 与进阶篇同美学：宣纸留白、朱红印章「知白守黑」、同一套字体与组装管线。进阶篇见 `/workspace/tao-category-video/`。

## 主要参考与致谢
本片的叙述框架与 Haskell 写法以 Bartosz Milewski 的两本书为主要参照（释义、改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*（hmemcpy 编排版），<https://github.com/hmemcpy/milewski-ctfp-pdf>

入门篇刻意避开 Yoneda、伴随深度、Lambek / Adámek 定理表述；对应主题改用对象/箭头/复合、Void/()、Maybe·列表与折叠、unfold/fold、Functor·Applicative、Monad·do。更深内容指向进阶篇。

| 段落 | DaoFP 章节 | CTFP 章节 |
|---|---|---|
| 一 道可道 | 1 Clean Slate（Types and Functions）；2 Composition（Identity） | 1.1, 1.2 |
| 二 有无相生 | 1 Clean Slate（Yin and Yang, Elements） | 1.5 Products and Coproducts；1.6 Simple Algebraic Data Types |
| 三 道生一 | 7 Recursion；11 Algebras（Catamorphisms——直觉层） | 1.6；3.8 F-Algebras（fold 直觉） |
| 四 反者道之动 | 12 Coalgebras（Anamorphisms, Hylomorphisms——直觉层） | 3.8（Coalgebras） |
| 五 知其雄 | Functor / Applicative 铺垫（DaoFP 相关章；14 Applicatives） | 1.7 Functors；1.8 |
| 六 无为 | 2 Composition（wu wei）；15 Monads（入门直觉） | 3.4 Kleisli；3.6 Monads（bind / join） |

## 术语表（全片统一）

| 中文 | English |
|---|---|
| 对象 / 箭头（态射） | object / arrow (morphism) |
| 复合 / 恒等 | composition / identity |
| 始对象 / 终对象 | initial / terminal object |
| Void / 单元类型 () | Void / unit type () |
| Maybe / 列表 | Maybe / list |
| 折叠 fold / 展开 unfold | fold / unfold |
| 合态射 hylo（轻提） | hylomorphism (light mention) |
| 函子 / fmap / map | functor / fmap / map |
| Applicative / pure / (<*>) | Applicative / pure / (<*>) |
| 单子 / bind / join / do 记法 | monad / bind / join / do-notation |

---

## 道可道 · 范畴入门　`00:00–00:55`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 道可道，非常道。这期视频，用六句《道德经》，带你入门范畴论。 | 宣纸背景，毛笔圆相（ensō）一笔画出；标题书法字浮现 |
| 00:09 | 不需要提前读过范畴论，也不必先会 Haskell。你会写一点程序——变量、函数、列表——就够了。屏幕上的代码，我们会一行一行念。 | 六个章节名竖排列出，逐一淡入；标注「入门」 |
| 00:25 | 每一段都是同样的节奏：先读一句老子，再用日常比喻讲清楚，最后落到几行代码。老子是钩子，直觉是正文。 | 节奏示意：原文 → 比喻 → 代码 |
| 00:37 | 框架上，我们会不断回到 Bartosz Milewski 的两本书：《程序员的范畴论》和《函数式编程之道》。更深入的一集——不动点、伴随、米田——留给进阶篇。 | 两本书名 CTFP / DaoFP；朱红印章「知白守黑」；小字「进阶篇另见」 |

---

## 一 · 道可道　`00:55–03:01`

> **道可道，非常道；名可名，非常名。**　——《道德经》第一章

参考：DaoFP ch.1 Clean Slate（Types and Functions）；DaoFP ch.2 Composition（Identity）；CTFP 1.1 Category: The Essence of Composition；CTFP 1.2 Types and Functions

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:55 | 道可道，非常道；名可名，非常名。 | 竖排书法原文，右起 |
| 01:03 | 先忘掉抽象。想象一张地图：城市是点，公路是箭头。范畴论就是这样看世界的：对象是点，箭头是从一点到另一点的路。 | 左「对象 = 点」右「箭头 = 路」；简单两点一箭头图 |
| 01:17 | 在程序里，类型就是对象：整数、字符串、布尔。函数就是箭头：把一种类型变成另一种。整数变成字符串，字符串变成整数——都是箭头。 | Int、String、Bool 三个圆点；箭头 toString、length |
| 01:35 | 两段路可以接起来。先走 f，再走 g，合起来就是 g 圆点 f。这叫复合。注意顺序：先写的 g 其实后走——像管道，从右往左读。 | 三点 A→B→C；标注 g ∘ f |
| 01:50 | 复合有个规矩：三段路，先接左边再接右边，和先接右边再接左边，结果一样。这叫结合律。你不必加括号去想先算谁。 | 结合律：(h∘g)∘f = h∘(g∘f) |
| 02:04 | 每个城市还有一条什么也不做的环路：从自己回到自己。这叫恒等箭头，Haskell 里写作 id。它是复合的单位：跟谁接，都不改变对方。 | 自环 id；代码 identity / compose |
| 02:20 | 举个例子：toString 把整数变成字符串，strlen 量字符串长度。把它们接起来，得到从整数到整数的箭头——输入四十二，输出二，因为四十二有两个字符。 | 代码 shout = compose strlen toString；示例 42 ↦ 2 |
| 02:35 | Milewski 在《程序员的范畴论》第一章说：范畴的本质，就是复合。可道者，是箭头怎样接；对象本身，只是箭头的端点。 | 引文 Composition is the essence of category |
| 02:48 | 所以第一句可以这样读：能说清楚的，是箭头怎样走；说不清楚的，是对象本身——它只存在于箭头的关系里。 | 书法小字：可道者箭头也 |

屏幕代码 `s1`（`haskell/src/Seg1Compose.hs`）：

```haskell
-- 恒等箭头：什么也不做
identity :: a -> a
identity x = x

-- 复合：先走 f，再走 g（写作 g ∘ f）
compose :: (b -> c) -> (a -> b) -> (a -> c)
compose g f = \x -> g (f x)

toString :: Int -> String
toString = show

strlen :: String -> Int
strlen = length

-- shout = strlen ∘ toString ：Int → Int
shout :: Int -> Int
shout = compose strlen toString
```

---

## 二 · 有无相生　`03:01–05:00`

> **有无相生，难易相成，长短相形，高下相倾。**　——《道德经》第二章

参考：DaoFP ch.1 Clean Slate（Yin and Yang, Elements）；CTFP 1.5 Products and Coproducts；CTFP 1.6 Simple Algebraic Data Types

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:01 | 有无相生，难易相成，长短相形，高下相倾。 | 竖排原文 |
| 03:10 | 老子说，有和无互相生成。《函数式编程之道》把这一节叫作阴与阳。程序里也有一对极端：完全空的类型，和只有一个值的类型。 | 左「无 Void」右「有 ()」；中间竖直镜面虚线 |
| 03:25 | 空的类型叫 Void。它一个值都没有。你没法构造出一个 Void，就像没法从空屋里拿出一张椅子。 | 空屋示意；Void 标注「零个值」 |
| 03:35 | 从 Void 出发到任何类型，都有唯一一个函数，叫 absurd。它永远不会被真正调用——因为你拿不出一个 Void 的值来喂给它。没有输入，就无需说任何话。 | Void 向 A、B、C 发出箭头（absurd） |
| 03:51 | 另一个极端是单元类型，写作一对空括号。它只有一个值，就是它自己。从任何类型到它，都有唯一一个函数：const 单元——不管给你什么，都丢掉，只回那个唯一的点。 | A、B、C 汇入 ()（const ()） |
| 04:08 | 看见了吗？两个定义几乎是镜像：一个是「从无出发，通往万物」；一个是「从万物出发，归于一点」。箭头方向一翻，无就变成了有。 | 左图沿镜面翻转、箭头反向，与右图重合 |
| 04:22 | 日常比喻：Void 像一封永远寄不出去的空信封——里面没东西可寄。单元类型像一个公用邮筒——不管你塞什么信，结果都是「已投递」。 | 信封 / 邮筒示意；代码 wu / you |
| 04:34 | 它们还各守一种运算：Void 是「或者」的单位——Either Void a 跟 a 一样，空的那一支永远用不上。单元类型是「并且」的单位——跟谁配对，都不增加信息。 | 代码 sumUnit / prodUnit |
| 04:49 | 有无相生：空与满、无与有，是同一枚硬币的两面。下一句，我们从「无」里生出东西来。 | 小字预告：道生一 → |

屏幕代码 `s2wu`（`haskell/src/Seg2YouWu.hs`）：

```haskell
-- 无：通往万物的唯一箭头
wu :: Void -> a
wu = absurd
```

屏幕代码 `s2you`（`haskell/src/Seg2YouWu.hs`）：

```haskell
-- 有：万物归一的唯一箭头
you :: a -> ()
you = const ()
```

屏幕代码 `s2b`（`haskell/src/Seg2YouWu.hs`）：

```haskell
-- 无是「或者」的单位
sumUnit :: Either Void a -> a
sumUnit = either absurd id

-- 有是「并且」的单位
prodUnit :: ((), a) -> a
prodUnit = snd
```

---

## 三 · 道生一　`05:00–06:57`

> **道生一，一生二，二生三，三生万物。**　——《道德经》第四十二章

参考：DaoFP ch.7 Recursion（以此句开篇）；DaoFP ch.11 Algebras（Catamorphisms，直觉层）；CTFP 1.6 Simple Algebraic Data Types；CTFP 3.8 F-Algebras（fold 直觉）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 05:01 | 道生一，一生二，二生三，三生万物。 | 竖排原文 |
| 05:08 | 《函数式编程之道》讲递归的那一章，正是以这句话开篇的。我们用程序员最熟的两样东西来读它：Maybe，和列表。 | 小字：DaoFP ch.7；Maybe / List 图标 |
| 05:21 | Maybe a 表示「也许有一个 a，也许没有」。它有两个构造子：Nothing，什么都没有；Just x，装着一个 x。像一个可能空的盒子。 | 代码 data Maybe；Nothing / Just 图示 |
| 05:34 | 从「无」开始想：Maybe 作用于 Void，只能是 Nothing——这是一。再包一层，有两个可能：Nothing，或 Just Nothing——这是二。再一层，三个可能——这是三。 | 链：Void → Maybe Void → Maybe² → Maybe³；点数 0 1 2 3；书法「无 一 二 三」 |
| 05:50 | 每包一层，就多一个「在这一层停住」的选择。一层层包下去，选择越来越多——三生万物的感觉，就在这里。 | 层数与值的个数对齐动画 |
| 06:02 | 列表也是这样长出来的：要么是空列表，要么是「一个元素，再加上另一份列表」。空是无；接一个元素是一；再接一个是二。万物，就是任意长的列表。 | [] / (1:[]) / (1:2:[]) 展开 |
| 06:17 | 生出来之后，还要能收回去。折叠，就是沿着构造的逆方向走：遇到空，给一个起点；遇到「头加尾」，说清如何把头和已折叠的尾合成一步。 | 折纸隐喻：打开的列表 → 一步步折起 |
| 06:32 | 求和就是最熟的折叠：空列表是零；非空列表是「头，加上尾的总和」。你没有写循环——你只说清了一步，递归会替你走完全程。 | 代码 sumList；动画 1:2:3:[] → 6 |
| 06:46 | 道生一，三生万物；折叠则是万物各归其根。下一句，我们把「生」和「归」反过来看。 | 书法小字：夫物芸芸，各复归其根 |

屏幕代码 `s3maybe`（`haskell/src/Seg3Maybe.hs`）：

```haskell
data Maybe a = Nothing | Just a
  deriving (Show, Functor)

-- 从无出发：Maybe Void 只有 Nothing —— 一
-- Maybe (Maybe Void) 有两个值 —— 二
type One   = Maybe Void
type Two   = Maybe (Maybe Void)
type Three = Maybe (Maybe (Maybe Void))

one :: [One]
one = [Nothing]

two :: [Two]
two = [Nothing, Just Nothing]

three :: [Three]
three = [Nothing, Just Nothing, Just (Just Nothing)]
```

屏幕代码 `s3list`（`haskell/src/Seg3Maybe.hs`）：

```haskell
-- 列表：空，或「头 + 另一份列表」
-- data [] a = [] | a : [a]   —— 标准库已有

-- 折叠：只说清一步，递归走完全程
sumList :: [Int] -> Int
sumList []     = 0
sumList (x:xs) = x + sumList xs
```

---

## 四 · 反者道之动　`06:57–08:49`

> **反者道之动，弱者道之用。**　——《道德经》第四十章

参考：DaoFP ch.12 Coalgebras（Anamorphisms, Hylomorphisms——直觉层）；CTFP 3.8 F-Algebras（Coalgebras）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:58 | 反者道之动，弱者道之用。 | 竖排原文 |
| 07:04 | 上一句我们把列表折起来，变成一个数。现在反过来：从一个种子，长出列表。方向一翻，故事就变了。 | 折叠箭头 ← 与展开箭头 → 对照 |
| 07:16 | 消费列表，像拆快递：打开一层，处理里头的东西，再对剩下的箱子做同样的事——这是 fold，折叠。 | 拆箱示意；foldr 代码 |
| 07:27 | 生成列表，像种树：看着手里的种子，决定「现在结一个果，还剩下一颗更小的种子」，直到种子耗尽——这是 unfold，展开。 | 种子→果+种子 示意；unfoldr 代码 |
| 07:39 | 比如从数字 n 展开：若 n 是零就停止；否则结出 n，留下 n 减一。于是五、四、三、二、一，整条链就长出来了。 | 动画：5 → 5:4:3:2:1:[] |
| 07:54 | 有了展开，有了折叠，就能接起来：先展开，再折叠。中间那条列表被生出，又立刻被消费。先生，而后归。 | 种子 ─unfold→ 列表 ─fold→ 结果 |
| 08:08 | 阶乘就是例子：先把 n 展开成 n 到一，再把它们乘起来。十的阶乘，是三百六十二万八千八百。 | 代码 fact；结果 3628800 |
| 08:18 | 如果你愿意，可以把这两步合成一步，中间列表从不完整出现——有人叫它 hylo，合态射。入门只需记住八个字：先生后归，生而不有。 | 代码 factHylo；书法「生而不有」 |
| 08:34 | 反者道之动：同一套结构，箭头一翻，消费变成生成。对偶不是修辞，是一种省力的思考方式——每学会一个方向，就白得相反的那个。 | 小字：fold ⟷ unfold |

屏幕代码 `s4fold`（`haskell/src/Seg4FoldUnfold.hs`）：

```haskell
-- 消费：拆快递 —— foldr
foldProduct :: [Integer] -> Integer
foldProduct = foldr (*) 1
```

屏幕代码 `s4unfold`（`haskell/src/Seg4FoldUnfold.hs`）：

```haskell
-- 生成：种树 —— unfoldr
-- 种子 n：结出 n，留下 n-1；到 0 停止
countdown :: Integer -> [Integer]
countdown = unfoldr step
  where
    step 0 = Nothing
    step n = Just (n, n - 1)
```

屏幕代码 `s4hylo`（`haskell/src/Seg4FoldUnfold.hs`）：

```haskell
-- 先展开再折叠：阶乘（中间列表可融掉）
fact :: Integer -> Integer
fact n = foldProduct (countdown n)

-- 合成一步的写法（hylo 直觉：先生后归，中间不落地）
factHylo :: Integer -> Integer
factHylo = go
  where
    go 0 = 1
    go n = n * go (n - 1)
```

---

## 五 · 知其雄，守其雌　`08:49–11:00`

> **知其雄，守其雌，为天下溪。**　——《道德经》第二十八章

参考：CTFP 1.7 Functors；CTFP 1.8 Functoriality and Functors；DaoFP 相关 Functor 铺垫；Applicative 见 DaoFP 14 / CTFP

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 08:49 | 知其雄，守其雌，为天下溪。 | 竖排原文 |
| 08:56 | 前面出现了 Maybe、列表。它们有一个共同点：都是「在某个形状里，装着一些值」。盒子可以不同，但都是盒子。 | Maybe 盒子 / 列表盒子 并排 |
| 09:08 | 函子，说的就是：你能在不拆盒子的前提下，改里面的值。形状不变，内容可换。Haskell 里，这个动作叫 fmap，或者就是大家熟悉的 map。 | 盒子外形固定；内部 a → b；代码 fmap |
| 09:25 | 对 Maybe：若是 Nothing，map 之后还是 Nothing——空的还是空的。若是 Just 三，加上一，就变成 Just 四。盒子还在，只是贴纸换了。 | Nothing ↦ Nothing；Just 3 ↦ Just 4 |
| 09:40 | 对列表：map 就是对每个元素施同一个函数，列表的长短、顺序都不动。一、二、三，乘以二，变成二、四、六。 | [1,2,3] map (*2) → [2,4,6]；标注「形不变」 |
| 09:55 | 雄，是那个主动出击的函数 f；雌，是守住形状的盒子。函数再猛，也不能把列表变成 Maybe——形状由函子守着。 | 左「雄 · 函数」右「雌 · 形状」 |
| 10:09 | 函子有两条必须守住的规矩，像诚信条款：map id，等于什么都不做；连续 map 两次，等于 map 它们的复合。不守规矩，就不是函子。 | 两条定律：fmap id = id；fmap (g∘f) = fmap g ∘ fmap f |
| 10:23 | 再往前半步：Applicative。它让你把「盒子里的函数」应用到「盒子里的值」。pure 把一个普通值抬进盒子；尖括号星号负责应用。Just 加一，作用于 Just 三，得到 Just 四。 | 代码：pure / (<*>)；Just (+1) <*> Just 3 = Just 4 |
| 10:40 | 知其雄，守其雌，为天下溪。函数是雄，容器是雌。函子让它们共处而不互相破坏；Applicative 更让盒子里的函数也能发挥作用。形状，是那条容纳一切的溪床。 | 两栏之间一道墨线（溪） |

屏幕代码 `s5fmap`（`haskell/src/Seg5Functor.hs`）：

```haskell
-- 函子：不拆盒子，改里面的值
incrMaybe :: Maybe Int -> Maybe Int
incrMaybe = fmap (+ 1)

doubleList :: [Int] -> [Int]
doubleList = fmap (* 2)
```

屏幕代码 `s5law`（`haskell/src/Seg5Functor.hs`）：

```haskell
-- 函子定律（诚信条款）
-- fmap id      = id
-- fmap (g . f) = fmap g . fmap f
lawId :: [Int] -> Bool
lawId xs = fmap id xs == xs

lawComp :: [Int] -> Bool
lawComp xs = fmap ((* 2) . (+ 1)) xs == (fmap (* 2) . fmap (+ 1)) xs
```

屏幕代码 `s5app`（`haskell/src/Seg5Functor.hs`）：

```haskell
-- Applicative：盒子里的函数 × 盒子里的值
appEx :: Maybe Int
appEx = pure (+ 1) <*> Just 3   -- Just 4

appList :: [Int]
appList = pure (*) <*> [2, 3] <*> [10, 100]  -- [20,200,30,300]
```

---

## 六 · 无为而无不为　`11:00–13:12`

> **道常无为而无不为。**　——《道德经》第三十七章

参考：DaoFP ch.2 Composition（Identity = wu wei）；DaoFP ch.15 Monads（入门直觉）；CTFP 3.4 Kleisli Categories；CTFP 3.6 Monads Categorically（bind / join 直觉）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 11:01 | 道常无为而无不为。 | 竖排原文 |
| 11:06 | 函子能改盒子里的值，但有件事它做不到：若你的函数自己会返回一个新盒子，fmap 之后会变成「盒子里套盒子」。Just 套 Just，两层皮。 | f :: a → Maybe b；fmap f (Just x) :: Maybe (Maybe b) |
| 11:20 | 单子，多了一步：把套叠的盒子摊平。这一步，Haskell 里叫 bind，写作大于大于等号；或者用 join 先摊平，再 fmap。两层变一层。 | Maybe (Maybe a) → Maybe a；代码 (>>=) |
| 11:36 | 日常比喻：你吩咐助手「去问问前台，房间号是多少」。助手回来时，不会交给你「另一个助手手里的字条」，而是直接把字条给你——bind 就是那位会拆套的助手。 | 助手拆套示意 |
| 11:51 | 举个例子：half 只对偶数动手，奇数就返回 Nothing。八 bind half bind half，得到 Just 二；七 bind half，直接是 Nothing。 | 代码 half / chain；8→4→2，7→Nothing |
| 12:04 | 有了 bind，就可以按顺序排好几件可能失败的事：先读配置，再开文件，再解析。任何一步是 Nothing，后面自动跳过。你不用满屏写 if。 | 三步管道；旁注「一步失败则全体短收」 |
| 12:19 | 这就是 do 记法：看起来像命令式，一行接一行；底下仍是 bind 在串盒子。你没有强迫每一步立刻交出普通值——你只描述顺序，让盒子自己处理失败。 | 代码 do 块与等价的 >>= 对照 |
| 12:35 | 无为：不强行把效果从盒子里掏出来。无不为：一旦排好顺序，该做的事都能做完。单子是「在效果里编程」，而不是「先消灭效果再编程」。 | 书法小字：无为而无不为 |
| 12:50 | 今天停在这里。进阶篇会走得更深：Fix 与不动点、伴随、米田引理——把「可道」与「不可道」彻底说圆。若你刚入门，先把箭头、有无、折叠、函子、单子这五块摸熟，就已经握住溪流的源头了。 | 指向「进阶篇」；五块回顾小字 |

屏幕代码 `s6bind`（`haskell/src/Seg6Monad.hs`）：

```haskell
-- 会返回盒子的函数，用 bind 串联（摊平套叠）
half :: Int -> Maybe Int
half n | even n    = Just (n `div` 2)
       | otherwise = Nothing

-- Just 8 >>= half >>= half  =  Just 2
-- Just 7 >>= half           =  Nothing
chain :: Maybe Int
chain = Just 8 >>= half >>= half
```

屏幕代码 `s6do`（`haskell/src/Seg6Monad.hs`）：

```haskell
-- do 记法：看起来像一步一步，底下仍是 bind
readConfig :: Maybe String
readConfig = Just "path.txt"

openFile :: String -> Maybe String
openFile p = Just ("contents of " ++ p)

parse :: String -> Maybe Int
parse _ = Just 42

pipeline :: Maybe Int
pipeline = do
  path <- readConfig
  body <- openFile path
  parse body
```

---

## 结 · 看箭头　`13:12–13:36`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 13:12 | 从对象与箭头，到有与无；从生与归，到形与效。六句话，其实只说了一件事：顺着箭头看。 | 六句原文小字环绕圆相 |
| 13:24 | 借 Milewski 的提醒：看箭头。道可道，非常道。谢谢观看。进阶篇见。 | 「看箭头」书法大字；印章；谢谢观看；小字进阶篇 |

---

## 数学校对备注

- 依 CTFP 惯例在 Hask 中忽略 ⊥（`Void` 作为始对象在此约定下成立）。
- 第三段：`Maybeⁿ Void` 恰有 n 个值，故「无、一、二、三」是精确计数；不引入 Lambek / Adámek 命名。
- 第四段：hylo 仅作「先生后归、中间不落地」的轻提，不展开阻抗失配。
- 第五段：函子定律与 Applicative 直觉；不讲 State/Store 伴随。
- 第六段：Monad = bind 串联效果 + do；明确不是 Yoneda；收束指向进阶篇。

## 制作说明

- 画面：Manim Community 0.21（Cairo），白底渲染后与程序生成的宣纸纹理做 multiply 合成；唯一红色为印章「知白守黑」。
- 字体：原文书法 Ma Shan Zheng（OFL）；正文/字幕 霞鹜文楷 LXGW WenKai（OFL）；代码 IBM Plex Mono（OFL）；英文引文 EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。
