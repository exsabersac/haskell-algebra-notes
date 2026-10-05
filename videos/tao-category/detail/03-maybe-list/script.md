# 道可道 · 深讲 03 —— Maybe 与 List
*从无生长的代数数据类型｜Maybe and List — Deep Dive 03*
- 成片时长：**07:50**（470.8 秒），1920×1080，30 fps
- 受众：会一点编程；Haskell 零基础或略知即可。先范畴论陈述，再短 Haskell。
- 结构：道生一钩子 → Maybe = 1+A → List 递归 → 从无生长 → 代码 → 预告构造与折叠。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-03.srt`。
- 屏幕代码摘自 `haskell/src/MaybeList.hs`（`-- {{snip:…}}`），GHC `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。系列：入门篇六句总览；深讲把每点拆成单集。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 道生一 | 7 Recursion（开篇） | 1.6 |
| Maybe = 1+A | 7；4 Sum Types | 1.6 Maybe ≅ Either () a |
| List 递归 | 7 Lists | 1.6 recursive ADT |
| 从无生长 | 7；入门篇计数 | 1.6 |
| 下一集预告 | 11 Algebras / 12 Coalgebras | 3.8 F-Algebras |

## 术语表

| 中文 | English |
|---|---|
| Maybe / 列表 | Maybe / list |
| 代数数据类型 | algebraic data type (ADT) |
| 构造子 / 引入规则 | constructor / introduction rule |
| 余积 / 求和 | coproduct / sum type |
| 递归类型 | recursive type |
| 折叠 / 展开 | fold / unfold |

---

## Maybe 与 List　`00:00–00:49`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 道生一。欢迎来到「道可道」深讲第三集。 | 宣纸背景，圆相一笔画出；标题「Maybe 与 List」浮现 |
| 00:06 | 上一集钉牢了零与一：Void 是始对象，单元类型是终对象。这一集，我们从这对标尺里，生出两样最熟的东西——Maybe，和列表。 | 小字：深讲 02 → 03；提纲 Maybe / List |
| 00:20 | 范畴论里，它们是代数数据类型：用求和与递归，把构造子写清楚。先把话说明白，再落到几行 Haskell。 | 三行：Maybe = 1+A · List 递归 · 构造直觉 |
| 00:33 | 框架仍是 Milewski 的两本书：《函数式编程之道》讲递归的那一章，以及《程序员的范畴论》里简单代数数据类型那一节。片中表述都是释义，不是照录。 | DaoFP ch.7 · CTFP 1.6；印章「知白守黑」 |

---

## 一 · 道生一　`00:49–01:53`

> **道生一，一生二，二生三，三生万物。**　——《道德经》第四十二章

参考：DaoFP ch.7 Recursion（以此句开篇）；CTFP 1.6 Simple Algebraic Data Types

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:50 | 道生一，一生二，二生三，三生万物。 | 竖排书法原文，右起 |
| 00:57 | 《函数式编程之道》讲递归的那一章，正是以这句话开篇的。入门篇扫过一遍；这一集，我们把 Maybe 和列表单独拉开。 | 小字：DaoFP ch.7；入门篇 → 深讲 03 |
| 01:10 | 先问范畴论的问题：一个类型，有哪些构造方式？每种方式对应一条引入规则。构造子一旦写清，值怎么数、箭头怎么画，都跟着定了。 | 引入规则 / 构造子示意 |
| 01:25 | Maybe 说的是：要么什么都没有，要么装着一个东西。列表说的是：要么空，要么头，再加上另一份列表。一个是有限的选择；一个是自己指回自己。 | Maybe 盒子 / List 链 并排 |
| 01:40 | 从「无」开始想，一层层包下去，选择越来越多——道生一的感觉，就在这里。慢一点，只把构造看明白。 | 书法小字：从无生长 |

---

## 二 · Maybe = 1 + A　`01:53–03:16`

参考：DaoFP ch.7；CTFP 1.6（Maybe ≅ Either () a）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 01:53 | 先看 Maybe。Maybe a 表示「也许有一个 a，也许没有」。两个构造子：Nothing，什么都没有；Just x，装着一个 x。像一个可能空的盒子。 | data Maybe；Nothing / Just 图示 |
| 02:08 | 用类型代数的语言：Maybe a 就是一加 a。一是单元类型——那个唯一的点；加号是 Either，二选一。要么选左边的点，要么选右边的 a。 | Maybe a ≅ Either () a ≅ 1 + A |
| 02:23 | 选左边：只剩那一个点，没有额外信息——这就是 Nothing。选右边：带着一个 a——这就是 Just。盒子的两种打开方式，正好对应求和的两支。 | Left () ↔ Nothing；Right x ↔ Just x |
| 02:39 | 所以 Maybe 不是凭空发明的关键字。它是终对象与余积拼出来的：把「有」和「一个 a」并排放在一起，就得到「也许有 a」。 | () + A → Maybe A；小字：terminal + coproduct |
| 02:51 | 为什么程序员在乎？因为失败、缺失、尚未加载，都可以用同一形状表达——不必用魔法空值，也不必假装总有答案。 | 小字：缺失 / 失败 / 尚未加载 → Maybe |
| 03:03 | 日常比喻：Maybe 像一封可能空的信——要么信封是空的，要么里面有一张纸条。你拆开之前，两种可能都合法。 | 信封：空 / 有纸条 |

---

## 三 · List：递归　`03:16–04:43`

参考：DaoFP ch.7 Lists；CTFP 1.6（recursive ADT）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:17 | 再看列表。列表的定义自己指回自己：要么是空列表，要么是「一个元素，再加上另一份列表」。空是终点；接上去的那一步，才是生长。 | Nil / Cons 图示；箭头指回 List |
| 03:31 | 两个构造子：Nil，什么都没有，对应单元那一侧。Cons，吃一个头和一个尾，拼出更长的列表。尾的类型，还是列表本身——这就是递归。 | Nil :: List a；Cons :: a → List a → List a |
| 03:46 | 空是无；接一个元素是一；再接一个是二。万物，就是任意长的列表。长度不封顶，因为 Cons 可以永远再套一层。 | [] / (1:[]) / (1:2:[]) 展开 |
| 03:59 | 跟 Maybe 对比：Maybe 的选择是有限的——有或没有，两支就够。列表的选择是开放的——每接一次，就多一个元素的位置。有限求和，对上无限递归。 | Maybe：有限 · List：递归 |
| 04:15 | 消解规则，是构造的反面：遇到 Nil，给一个起点；遇到 Cons，把头和已处理的尾合成一步。今天只点到这里——完整的折叠，留给下一集。 | init / step 示意；预告 fold |
| 04:29 | Milewski 提醒：递归构造子，是引入规则里自己用到自己的那一支。自然数用后继；列表用 Cons。形状不同，手法一样。 | 小字：introduction rules · successor / Cons |

---

## 四 · 从无生长　`04:43–06:00`

参考：DaoFP ch.7；入门篇「道生一」计数直觉；CTFP 1.6

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 04:44 | 回到道生一。从「无」开始：Void 一个值都没有——这是零。Maybe 作用于 Void，只能是 Nothing——这是一。 | Void → Maybe Void；点数 0 → 1；书法「无 · 一」 |
| 04:55 | 再包一层：Maybe 的 Maybe 作用于 Void。两个可能：Nothing，或 Just Nothing——这是二。再一层，三个可能——这是三。 | Maybe² Void / Maybe³ Void；点数 2、3 |
| 05:09 | 每包一层，就多一个「在这一层停住」的选择。一层层包下去，选择越来越多——三生万物的感觉，就在精确的计数里。 | 层数与值的个数对齐；「无一二三」 |
| 05:20 | 列表也是这样长出来的：Nil 是种子；Cons 一次，多一个格子。你不是在循环里「追加」，你是在用构造子声明形状——值跟着形状出现。 | Nil ─Cons→ Cons x Nil ─Cons→ … |
| 05:33 | 自然数也是同一手法：零，或一个数的后继。列表把「后继」换成「再接一个元素」。形状不同，从无生长的节奏一样。 | Z / S ⟷ Nil / Cons |
| 05:46 | 构造，是往外长；折叠，是往回收。今天只把「生」看清楚。收回去的那半边——fold 与 unfold——留给下一集。 | 生 → ；归 ← ；预告折叠 |

---

## 五 · 落到代码　`06:00–07:13`

参考：DaoFP ch.7；CTFP 1.6

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:00 | 把刚才的话写成几行 Haskell。手写一份 Maybe，好看见构造子；再写出它跟 Either 单元的互转。 | 代码块：s_maybe |
| 06:11 | fromEitherUnit：左边的单元变成 Nothing，右边的值变成 Just。toEitherUnit 反过来。类型写在前，同构藏在两支匹配里。 | 高亮 fromEitherUnit / toEitherUnit |
| 06:25 | 再看计数。One、Two、Three 是类型同义词：Maybe 套 Void，套两层，套三层。one、two、three 列出所有值——个数正好是一、二、三。 | 代码 s_count；点数对齐 |
| 06:42 | 列表这边，手写 Nil 与 Cons。sumList 遇到空回零；遇到 Cons，头加上尾的总和。你只说清一步，递归替你走完全程——折叠的预告。 | 代码 s_list；1:2:3 → 6 |
| 06:57 | 屏幕上的代码都能直接编译。自己写一遍构造子，是为了看见形状；用标准库的 Maybe 与列表，是为了日常省事。图对齐了，代码只是把图念出来。 | 对照：图 ⟷ 代码 |

屏幕代码 `s_maybe`（`haskell/src/MaybeList.hs`）：

```haskell
-- Maybe a ≅ Either () a ≅ 1 + A
data Maybe a = Nothing | Just a
  deriving (Show, Functor)

-- 与 Either () a 互转（类型代数：Maybe = 1 + A）
fromEitherUnit :: Either () a -> Maybe a
fromEitherUnit (Left ()) = Nothing
fromEitherUnit (Right x) = Just x

toEitherUnit :: Maybe a -> Either () a
toEitherUnit Nothing  = Left ()
toEitherUnit (Just x) = Right x
```

屏幕代码 `s_count`（`haskell/src/MaybeList.hs`）：

```haskell
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

屏幕代码 `s_list`（`haskell/src/MaybeList.hs`）：

```haskell
-- 列表：空，或「头 + 另一份列表」（递归构造）
data List a = Nil | Cons a (List a)
  deriving (Show, Functor)

-- 折叠预览：只说清一步（下集再展开 fold / unfold）
sumList :: List Int -> Int
sumList Nil         = 0
sumList (Cons x xs) = x + sumList xs

lengthList :: List a -> Int
lengthList Nil         = 0
lengthList (Cons _ xs) = 1 + lengthList xs
```

---

## 结 · 道生一　`07:13–07:50`

参考：DaoFP ch.11 / ch.12；CTFP 3.8；下一集构造与折叠

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 07:14 | 今天只钉牢两件事：Maybe 是一加 a，有限的选择；列表是递归的 Cons，无限的生长。从无包上去，一二三，万物跟着来。 | 三句回顾环绕圆相 |
| 07:27 | 下一集，我们把方向反过来：构造往外长，折叠往回收；展开从种子生出列表，折叠再把列表收成一个值。先生，而后归。 | 预告：构造与折叠 · fold / unfold；小字「深讲 04」 |
| 07:41 | 借 Milewski 的提醒：看构造子。道生一。我们下集见。 | 「看构造子」书法；印章；谢谢观看 |

---

## 数学校对备注

- 依 CTFP 惯例在 Hask 中忽略 ⊥。
- Maybe a ≅ Either () a ≅ 1 + A（类型代数直觉）；不引入 Yoneda、伴随、Lambek。
- `Maybeⁿ Void` 恰有 n 个值（n=0 时 Void 有 0 个）；列表为 Nil | Cons 递归 ADT。
- 本集只点到折叠预告；fold / unfold / catamorphism 留给深讲 04。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh`。
