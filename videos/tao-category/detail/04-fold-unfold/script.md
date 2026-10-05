# 道可道 · 深讲 04 —— 构造与折叠
*从代数到 cata / foldr，浅提 ana｜Fold and Unfold — Deep Dive 04*
- 成片时长：**08:50**（530.7 秒），1920×1080，30 fps
- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。
- 结构：钩子 → 构造代数 → 折叠 cata/foldr → 展开 ana（浅提）→ 代码 → 预告 Functor。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-04.srt`。
- 屏幕代码摘自 `haskell/src/FoldUnfold.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 各复归其根 | 11 Algebras（cata 直觉） | 3.8 F-Algebras |
| 构造代数 | 11 Algebras | 3.8 |
| 折叠 cata / foldr | 11 Catamorphisms | 3.8 |
| 展开 ana（浅提） | 12 Coalgebras | 3.8 Coalgebras |
| 下一集预告 | Functor 相关 | 1.7–1.8 Functors |

## 术语表

| 中文 | English |
|---|---|
| 构造 / 代数 | constructor / algebra |
| 折叠 / catamorphism | fold / catamorphism (cata) |
| 展开 / anamorphism | unfold / anamorphism (ana) |
| 合态射 / hylo | hylomorphism (hylo) |
| 引入 / 消解 | introduction / elimination |
| F-代数（直觉） | F-algebra (intuition) |

---

## 构造与折叠　`00:00–00:55`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 夫物芸芸，各复归其根。欢迎来到「道可道」深讲第四集。 | 宣纸背景，圆相一笔画出；标题「构造与折叠」浮现 |
| 00:08 | 上一集把 Maybe 和列表生出来了：构造子往外长。这一集，我们把方向反过来——沿着构造的逆方向，把结构收成一个值。生，与归，是同一枚硬币的两面。 | 小字：深讲 03 → 04；提纲 构造 / 折叠 / 展开 |
| 00:24 | 范畴论里，这叫沿着代数去折叠：构造子是引入，折叠是消解。先把话说明白，再落到几行 Haskell。不着急写代码。 | 三行：构造代数 · cata / foldr · ana 浅提 |
| 00:39 | 框架仍是 Milewski 的两本书：《函数式编程之道》讲代数与余代数的那几章，以及《程序员的范畴论》里 F-代数那一节。片中表述都是释义，不是照录。 | DaoFP ch.11–12 · CTFP 3.8；印章「知白守黑」 |

---

## 一 · 各复归其根　`00:55–02:02`

> **夫物芸芸，各复归其根。**　——《道德经》第十六章

参考：DaoFP ch.11 Algebras（Catamorphisms，直觉层）；CTFP 3.8 F-Algebras（fold 直觉）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:56 | 夫物芸芸，各复归其根。 | 竖排书法原文，右起 |
| 01:02 | 入门篇扫过折叠与展开；深讲第三集只把「生」看清楚。这一集，我们把「收回去」单独拉开。生出来之后，还要能归回去。 | 小字：入门篇 → 深讲 04；生 → 归 |
| 01:16 | 先问范畴论的问题：一个递归类型，有哪些构造方式？每种构造子对应一条引入规则。消解，则是沿着这些规则往回走——不是另起炉灶，而是原路返还。 | 引入 / 消解 对照 |
| 01:32 | 列表要么空，要么头加尾。折叠就是：遇到空，给一个起点；遇到头加尾，说清如何把头和已折叠的尾合成一步。两句话，就定下整条折法。 | Nil → init；Cons → step |
| 01:48 | 你没有写循环——你只说清了一步，递归替你走完全程。慢一点，先把「代数」这两个字看明白；后面的 fold，都站在它上面。 | 书法小字：只说清一步 |

---

## 二 · 构造代数　`02:02–03:38`

参考：DaoFP ch.11 Algebras；CTFP 3.8 F-Algebras（直觉，不引入 Lambek）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 02:03 | 构造子合在一起，就是一份代数：它告诉你，怎么从「零件」拼出「成品」。对列表来说，零件是单元，或「一个元素加上已有列表」。形状先于值。 | 代数 = 构造方式的集合；Nil / Cons |
| 02:19 | Nil 不吃任何东西，直接交出空列表。Cons 吃一个头、一个尾，交出更长的列表。两支合起来，就是列表的代数——引入规则的全体。 | Nil :: 1 → List；Cons :: A × List → List |
| 02:33 | Milewski 提醒：代数不只是「数据结构」。它是一套操作——把形状里的洞填上，得到目标类型里的一个值。洞可以是空位，也可以是递归的子结构。 | 小字：algebra = 填洞的操作 |
| 02:48 | 举例：若目标是数字，空对应零，头加尾对应「头加上已折好的尾」——这就是求和代数。同一形状，换一套操作，就变成求积、求长、拼接。结构不变，菜谱变。 | 同一 List 形状 · 不同代数 → sum / product / length |
| 03:06 | 所以折叠不是魔法关键字。它是：拿着一份代数，沿着构造子的逆方向，把整棵树——或整条列表——收成代数所指定的那个值。一步对应一个构造子。 | fold = 用代数消费结构 |
| 03:22 | 日常比喻：代数像一份菜谱。构造给出食材的摆法；折叠按菜谱一步步做完，桌上只剩一道菜——那个结果值。看懂菜谱，比背菜名有用。 | 菜谱隐喻：结构 → 结果 |

---

## 三 · 折叠 cata　`03:38–05:14`

参考：DaoFP ch.11 Catamorphisms；CTFP 3.8（cata / foldr 直觉）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:39 | 范畴论里，这种「沿着代数往回折」的唯一箭头，常叫 catamorphism，简称 cata。名字吓人，直觉很素：就是 fold。对列表，你每天都在用。 | cata = catamorphism ≈ fold |
| 03:54 | 对列表，Haskell 里最熟的是 foldr：先给空列表一个起点，再给「头与已折尾」一个二元步骤。从右往左折，形状与 Cons 对齐——这不是巧合，是设计。 | foldr step init；与 Cons 对齐 |
| 04:10 | 看求和：空是零；非空是头加上尾的总和。写成 foldr，就是把加号和零交给它——结构由列表保管，你只负责一步。一、二、三，折完是六。 | sum = foldr (+) 0；动画 1:2:3:[] → 6 |
| 04:27 | 再看求积：空是一；非空是头乘以尾的积。同一条列表，换代数，结果就变。形状不变，操作变——这正是「代数」二字的用处。 | product = foldr (*) 1 |
| 04:42 | 为什么说「唯一」？因为递归类型由构造子生成：一旦你规定了每个构造子对应哪一步，从根到叶的折叠路径就被钉死了——没有别的合法折法。今天只讲直觉，不写 Lambek。 | 小字：由构造唯一决定（直觉，非 Lambek 证明） |
| 04:59 | 入门篇那句仍在：道生一，三生万物；折叠则是万物各归其根。构造往外长，cata 往回收。生与归，合在一处。 | 书法：各复归其根 |

---

## 四 · 展开 ana（浅提）　`05:14–06:44`

参考：DaoFP ch.12 Coalgebras（Anamorphisms——直觉层）；CTFP 3.8 Coalgebras

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 05:15 | 方向一翻，故事就变了。折叠是消费结构；展开是生成结构。范畴论里对应的是 anamorphism，简称 ana——跟 cata 对偶。今天只浅提，不深挖余代数。 | fold ← ⟷ → unfold；cata ⟷ ana |
| 05:32 | 消费像拆快递：打开一层，处理里头的东西，再对剩下的箱子做同样的事。生成像种树：看着手里的种子，决定「现在结一个果，还剩下一颗更小的种子」，直到种子耗尽。 | 拆箱 / 种树 对照 |
| 05:49 | 比如从数字 n 展开：若 n 是零就停止；否则结出 n，留下 n 减一。于是五、四、三、二、一，整条链就长出来了。种子在左手，列表在右手。 | 动画：5 → 5:4:3:2:1:[] |
| 06:07 | 有了展开，有了折叠，就能接起来：先展开，再折叠。中间那条列表被生出，又立刻被消费。先生，而后归——有人叫它 hylo，合态射。今天只点到这里，知道方向即可。 | 种子 ─ana→ 列表 ─cata→ 结果；hylo 浅提 |
| 06:26 | 反者道之动：同一套结构，箭头一翻，消费变成生成。对偶不是修辞，是一种省力的思考方式——每学会一个方向，就白得相反的那个。折与展，是一对。 | 小字：fold ⟷ unfold · 反者道之动 |

---

## 五 · 落到代码　`06:44–08:09`

参考：DaoFP ch.11–12；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:44 | 把刚才的话写成几行 Haskell。先手写列表，再写出 foldr 风格的求和与求积——同一形状，两套代数。类型写在前，递归藏在匹配里。 | 代码块：s_cata |
| 06:59 | sumList 遇到 Nil 回零，遇到 Cons 头加尾；productList 空是一，非空是乘法。你只说清一步，递归走完全程——cata 的手写版。 | 高亮 sumList / productList |
| 07:13 | 再用标准库的 foldr 写一遍乘积，对照看出：手写递归与 foldr，说的是同一件事——cata 的两种写法。一个显式，一个浓缩。 | 代码 s_foldr；foldProduct = foldr (*) 1 |
| 07:27 | 展开这边：countdown 用 unfoldr，种子为零则停，否则结出当前数、留下减一。从五展开，得到五到一。ana 的日常面目。 | 代码 s_ana；5 → [5,4,3,2,1] |
| 07:40 | 接上折叠：fact 先 countdown 再 foldProduct，就是十的阶乘。愿意的话，两步合成一步，中间列表不落地——hylo 直觉。屏幕代码都能编译。 | fact / factHylo；3628800 |
| 07:55 | 图对齐了，代码只是把图念出来。更深的 Fix、Lambek，留给以后；今天只把直觉钉牢。看构造，再看折叠。 | 对照：图 ⟷ 代码；不引入 Fix |

屏幕代码 `s_cata`（`haskell/src/FoldUnfold.hs`）：

```haskell
-- 列表：空，或「头 + 另一份列表」（构造 = 代数的引入）
data List a = Nil | Cons a (List a)
  deriving (Show)

-- 折叠（cata 直觉）：同一形状，两套代数
sumList :: List Int -> Int
sumList Nil         = 0
sumList (Cons x xs) = x + sumList xs

productList :: List Int -> Int
productList Nil         = 1
productList (Cons x xs) = x * productList xs

lengthList :: List a -> Int
lengthList Nil         = 0
lengthList (Cons _ xs) = 1 + lengthList xs
```

屏幕代码 `s_foldr`（`haskell/src/FoldUnfold.hs`）：

```haskell
-- 标准库 foldr：与 Cons 对齐的 cata
-- foldr step init  ≡  空→init；Cons x xs → step x (foldr … xs)
foldProduct :: [Integer] -> Integer
foldProduct = foldr (*) 1
```

屏幕代码 `s_ana`（`haskell/src/FoldUnfold.hs`）：

```haskell
-- 展开（ana 直觉）：种树 —— unfoldr
-- 种子 n：结出 n，留下 n-1；到 0 停止
countdown :: Integer -> [Integer]
countdown = unfoldr step
  where
    step 0 = Nothing
    step n = Just (n, n - 1)

-- 先展开再折叠：阶乘（hylo 浅提；中间列表可融掉）
fact :: Integer -> Integer
fact n = foldProduct (countdown n)

-- 合成一步的写法（先生后归，中间不落地）
factHylo :: Integer -> Integer
factHylo = go
  where
    go 0 = 1
    go n = n * go (n - 1)
```

---

## 结 · 各复归其根　`08:09–08:50`

参考：DaoFP / CTFP Functor；下一集函子

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 08:10 | 今天钉牢三件事：构造子合起来是代数；沿着代数往回折是 cata，也就是 fold；方向一翻，ana 从种子长出结构。生与归，都从构造子出发。 | 三句回顾环绕圆相 |
| 08:25 | 下一集，我们把「形状」本身提出来：Functor——在结构上描画箭头，而不拆掉结构。映射，是折叠之前的那一层薄纱。fmap 会登场。 | 预告：Functor · fmap；小字「深讲 05」 |
| 08:40 | 借 Milewski 的提醒：先看构造，再看折叠。各复归其根。我们下集见。 | 「各复归其根」书法；印章；谢谢观看 |

---

## 数学校对备注

- 依 CTFP 惯例在 Hask 中忽略 ⊥。
- 本集讲 F-代数 / cata / ana 的**直觉层**；不引入 Fix、Lambek 引理、Adámek 定理。
- foldr 与手写递归同为列表上的 catamorphism 写法；unfoldr 为 anamorphism 浅提。
- hylo = ana 后接 cata，仅点到；不展开融合证明。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。
