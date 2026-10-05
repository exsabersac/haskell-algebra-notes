# 道可道 · 进阶深讲 11 —— 知其雄，守其雌
*伴随、单位/余单位、State、Store、lens｜Adjunctions, State, Store, lens — Advanced Deep Dive 11*
- 成片时长：**11:51**（711.8 秒），1920×1080，30 fps
- 受众：已完成入门深讲 01–06 与进阶 07–10；先范畴论陈述，再短 Haskell。
- 结构：道德经钩子 → 伴随：hom 同构 → 单位、余单位与三角 → R∘L：State → L∘R：Store → 知其雄守其雌与 lens → 短 Haskell → 下集无为而无不为。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-11.srt`。
- 屏幕代码摘自 `haskell/src/XiongCi.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。印章语出《道德经》第二十八章，与本集钩子同章。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 知其雄守其雌 | 10 Adjunctions | 3.2 Adjunctions |
| 伴随：hom 同构 | 10 Adjunction between functors；The Currying Adjunction | 3.2 |
| 单位、余单位与三角 | 10 Unit and Counit；Triangle identities | 3.2 |
| R∘L：State | 16 Monads from Adjunctions；currying → state | 3.6 Monads Categorically |
| L∘R：Store | 17 Comonads from Adjunctions；Costate | 3.7 The Store Comonad |
| 知其雄守其雌 / lens | 16–17；17 Comonad coalgebras；Lenses | 3.6 / 3.7 |
| 短 Haskell | 10 / 16 / 17 · 本集 XiongCi.hs | 3.2 / 3.6 / 3.7 |
| 下集预告 | 米田 / Kan | 3.3–3.4 |

## 术语表

| 中文 | English |
|---|---|
| 伴随 L ⊣ R | adjunction L ⊣ R |
| hom 集自然同构 | natural isomorphism of hom-sets |
| 单位 η / 余单位 ε | unit η / counit ε |
| 三角恒等式 | triangle identities |
| 转置（伴随同构） | transpose (adjunct) |
| 笛卡尔闭范畴 CCC | cartesian closed category |
| 柯里化伴随 (−, s) ⊣ (s → −) | currying adjunction |
| 单子 T = R∘L · μ = RεL | monad from adjunction |
| 余单子 W = L∘R · δ = LηR | comonad from adjunction |
| State / Store（余状态） | State / Store (costate) comonad |
| lens = Store 余代数 | lens as Store-coalgebra |

---

## 知其雄，守其雌　`00:00–00:59`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 知其雄，守其雌。欢迎来到「道可道」进阶深讲——第十一集。 | 宣纸背景，圆相一笔画出；标题「知其雄，守其雌」浮现 |
| 00:08 | 前两集一生一归：初始代数与 cata，终余代数与 ana。今天换一种普遍性：不在一个对象上，而在两个方向相反的函子之间。它叫伴随。 | 小字：进阶 10 → 11；对象的普遍性 → 函子之间的伴随 |
| 00:23 | 本集四根钉子：伴随是 hom 集之间的自然同构；单位、余单位与三角恒等式；R∘L 生出单子，柯里化给出 State；L∘R 生出余单子，柯里化给出 Store，顺带认出 lens。 | 四行提纲 |
| 00:40 | 框架仍是 Milewski 的两本书：《函数式编程之道》与《程序员的范畴论》里伴随、单子、余单子各章。片中都是释义，不是照录。印章「知白守黑」，恰好出自同一章。 | DaoFP ch.10 / 16 / 17 · CTFP 3.2 / 3.6 / 3.7；印章「知白守黑」 |

---

## 一 · 道德经钩子　`00:59–02:15`

> **知其雄，守其雌，为天下溪。**　——《道德经》第二十八章

参考：DaoFP ch.10 Adjunctions；CTFP 3.2 Adjunctions

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 01:00 | 知其雄，守其雌，为天下溪。 | 竖排书法原文，右起 |
| 01:07 | 雄与雌，不是两样东西争高下，而是同一条溪的两岸：一岸向外流，一岸向内收。伴随正是这样：两个方向相反的函子，谁也不是谁的逆，却彼此知道得清清楚楚。 | 两岸 · 一溪；L 与 R 方向相反 |
| 01:23 | 同构：来回一圈，回到原处。等价：回到一个与原处同构的地方。伴随更松：回不到原处，只留下两支见证箭头——单位与余单位。Milewski 称之为「半个等价」。 | 同构 = · 等价 ≅ · 伴随 η / ε |
| 01:41 | 伴随无处不在。和与积，都是对角函子的伴随；极限与余极限也是；自由与遗忘也是。一旦认出 hom 集之间的这种同构，你会发现它到处冒头。 | + ⊣ Δ ⊣ ×；colim ⊣ Δ ⊣ lim；Free ⊣ U |
| 01:57 | 今天只抓最朴素的一对：与 s 配对，以及从 s 出发的函数。每个 Haskell 程序员天天在用它，只是叫它 curry。从这一对里，会流出 State 与 Store 两条支流。 | (−, s) ⊣ (s → −) ⇒ State · Store |

---

## 二 · 伴随：hom 集的同构　`02:15–03:48`

参考：DaoFP ch.10 Adjunction between functors；The Currying Adjunction；CTFP 3.2 Adjunctions

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 02:16 | 定义。两个范畴 C 与 D：左函子 L 从 D 到 C，右函子 R 从 C 到 D。伴随 L ⊣ R 说：从 L x 出发到 y 的箭头，与从 x 出发到 R y 的箭头，一一对应。 | C(L x, y) ≅ D(x, R y)；L ⊣ R |
| 02:35 | 这一族双射，要对 x 和 y 都自然。比如对 y 自然：在左边先用 f 后复合、再转置，和先转置、再用 R f 后复合，结果一样。对应的两支箭头，互称转置。 | 自然性方块：φ(f ∘ g) = R f ∘ φ(g) |
| 02:53 | 读法很重要：左边是映出——从 L x 出去；右边是映入——进入 R y。左伴随擅长映出，右伴随擅长映入。所以左伴随保持余极限，右伴随保持极限。 | 映出 / 映入；L 保余极限 · R 保极限 |
| 03:10 | 最经典的例子是指数。从 e 与 a 之积到 b 的箭头，对应从 e 到 b 的 a 次方的箭头。左函子是乘以 a，右函子是取 a 次方。对所有 a 都有这对伴随的范畴，叫笛卡尔闭范畴。 | C(e × a, b) ≅ C(e, bᵃ)；(− × a) ⊣ (−)ᵃ；CCC |
| 03:28 | 到了 Haskell，把 a 改名为 s：从 a 与 s 的配对到 b 的函数，等同于从 a 到「从 s 到 b」的函数。两个方向，正是 curry 与 uncurry。左伴随是与 s 配对，右伴随是从 s 出发的函数。 | ((a, s) → b) ≅ (a → s → b)；(,) s ⊣ (->) s |

---

## 三 · 单位、余单位与三角　`03:48–05:23`

参考：DaoFP ch.10 Unit and Counit of an Adjunction；Triangle identities；CTFP 3.2 Adjunction and Unit/Counit Pair

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:49 | 伴随还有第二张面孔。在同构里把 y 取成 L x，左边有一支现成的箭头：恒等。它的转置，是从 x 到 R L x 的箭头，叫单位 η。拿恒等去换——这是米田式的老技巧。 | η_x = φ(id_{Lx}) : x → R(L x) |
| 04:08 | 对偶地，把 x 取成 R y，右边的恒等转置回来，是从 L R y 到 y 的箭头，叫余单位 ε。η 是从恒等函子到 R∘L 的自然变换；ε 是从 L∘R 到恒等函子的自然变换。 | ε_y = φ⁻¹(id_{Ry})；η : Id → R∘L；ε : L∘R → Id |
| 04:29 | 它们满足三角恒等式：对 L，先用 η 插入一对 R L，再用 ε 消去一对 L R，等于什么都没做；对 R 也一样。插入再消去，归于无为。 | (εL)·(Lη) = id_L；(Rε)·(ηR) = id_R |
| 04:46 | 反过来，有了 η、ε 和三角恒等式，就能还原同构：从 x 到 R y 的 f，先用 L 抬升，再用 ε 收尾；另一方向，用 R 抬升，前面接上 η。两种定义等价。 | φ⁻¹ f = ε ∘ L f；φ g = R g ∘ η |
| 05:06 | 落到柯里化伴随上：单位是 curry 作用在恒等上，把 a 变成「等一个 s，就配成一对」；余单位是 uncurry 作用在恒等上，也就是求值：手里有函数和一个 s，作用上去。 | η = curry id；ε = uncurry id = eval |

---

## 四 · R∘L：State 单子　`05:23–07:06`

参考：DaoFP ch.16 Monads from Adjunctions；The currying adjunction and the state monad；CTFP 3.6 Monads Categorically

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 05:24 | 现在把两个函子接起来。先走 L 再走 R，得到 D 上的自函子 T，等于 R∘L。关键事实：对任何伴随，T 都是单子。单位就是伴随的单位 η；乘法 μ，是把余单位夹在中间：R ε L。 | T = R∘L；η；μ = R ε L : RLRL → RL |
| 05:46 | 为什么成立？两条单位律，正是两个三角恒等式；结合律，来自 ε 的自然性。Milewski 用弦图画得最清楚：T 的弦拆成并排的 L 与 R，μ 就是中间一对被 ε 收口。 | 弦图：L R L R → L R，中间 ε 收口 |
| 06:05 | 代入柯里化伴随：先配上 s，再变成从 s 出发的函数。R L a，就是从 s 到 a 与 s 之配对的函数——State s a。单位 η 把 a 原样配上当前状态，这正是 State 的 return。 | R(L a) = s → (a, s) = State s a；return = η |
| 06:25 | join 呢？R ε L 翻译成 Haskell，就是 fmap 余单位：外层拿到状态 s，跑出一个内层 State 和新状态 s′；余单位把内层作用到 s′ 上。这正是 uncurry runState。 | join = fmap counit；join mma = State (fmap (uncurry runState) (runState mma)) |
| 06:43 | 多数单子来自离开 Hask 的伴随，比如 List 来自自由幺半群与遗忘函子；柯里化伴随却两边都留在 Hask 里。反过来，每个单子也都能拆成伴随——Kleisli 与 Eilenberg–Moore 是两种拆法，并不唯一。 | List ⇐ Free ⊣ U；任何单子 = 某个伴随（Kleisli / EM，不唯一） |

---

## 五 · L∘R：Store 余单子　`07:06–08:28`

参考：DaoFP ch.17 Comonads from Adjunctions；Costate comonad；CTFP 3.7 The Store Comonad

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 07:06 | 反过来，先走 R 再走 L，得到 C 上的自函子 W，等于 L∘R。对偶的事实：它是余单子。余单位就是伴随的余单位 ε；余乘法 δ，是把单位夹在中间：L η R。 | W = L∘R；ε；δ = L η R : LR → LRLR |
| 07:26 | 代入柯里化：先变成从 s 出发的函数，再配上一个 s。L R c，就是一个从 s 到 c 的函数，加上一个 s——Store s c。它也叫余状态余单子。 | L(R c) = (s → c, s) = Store s c；costate comonad |
| 07:41 | 读法：那个函数是一整张以 s 为下标的表，那个 s 是当前位置。extract 就是余单位：在当前位置上把表查一下。 | Store = 全表 + 焦点；extract = ε |
| 07:53 | duplicate 就是 L η R：位置不动，把表的每一格都换成「以那一格为焦点的 Store」。于是得到一张由视角组成的表：每个位置看到的整个世界。 | duplicate (St f s) = St (St f) s |
| 08:08 | 有了 duplicate，就有 extend：把一条只看邻域的局部规则，推到每一个位置。s 取整数，就是一维卷积或元胞自动机——DaoFP 的一一零号规则，CTFP 的生命游戏。惰性只算你真正看的格子。 | extend k = fmap k ∘ duplicate；rule 110 / 生命游戏 |

---

## 六 · 知其雄，守其雌　`08:28–09:56`

参考：DaoFP ch.16–17；ch.17 Comonad coalgebras；Lenses；CTFP 3.6, 3.7

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 08:28 | 把两边并排。State 是雄：主动向外，Kleisli 箭头从 a 到 State s b，产生效果、改写状态。Store 是雌：接纳向内，余 Kleisli 箭头从 Store s a 到 b，守着焦点、消费语境。 | 雄 · State · a → State s b ｜ 雌 · Store · Store s a → b |
| 08:48 | 而喂养它们的，是同一对箭头。η 在 State 里是 return，在 Store 里藏在 duplicate 中间；ε 在 Store 里是 extract，在 State 里藏在 join 中间。一对 η 与 ε，两种结构。 | η / ε × State / Store 对照表 |
| 09:10 | 知其雄，守其雌，为天下溪。单子与余单子不是两套理论，而是同一条溪流的两岸；那条溪，就是伴随本身。 | 两栏之间一道墨线（溪），标注 L ⊣ R |
| 09:23 | 顺带认出一位老朋友。Store 余单子的余代数，是从 s 到 Store a s 的箭头；拆开，就是一对 get 与 set。这就是 lens：s 是整体，a 是焦点。 | φ : s → Store a s ≅ (get, set) |
| 09:38 | 余代数的两条定律翻译过来：把当前焦点原样写回，什么都不变；写进去再读，读到刚写的；连写两次，只留后一次。第十集的余代数又出现了，这次带着定律。 | set s (get s) = s；get (set s a) = a；set (set s a) a′ = set s a′ |

---

## 七 · 短 Haskell　`09:56–11:10`

参考：DaoFP ch.10 / 16 / 17；CTFP 3.2 / 3.6 / 3.7；本集 haskell/src/XiongCi.hs

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 09:57 | 把刚才的话写成几行 Haskell。leftAdjunct 是 curry，rightAdjunct 是 uncurry；unit 是 curry id，counit 是 uncurry id。伴随的四个零件，四行写完。 | 代码 s_adj |
| 10:13 | State 就是 R 套 L。join 只有一行：先跑外层，再用 uncurry runState 把内层作用到新状态上——那就是夹在中间的余单位。 | 代码 s_state |
| 10:26 | Store 就是 L 套 R。extract 是求值；duplicate 让每一格都成为焦点；extend 由它和 fmap 拼成；sum3 是一条只看邻域的规则。 | 代码 s_store |
| 10:41 | lens 是 Store 的余代数。_1 聚焦在配对的第一个分量上；get 和 set，都从这一个函数里读出来。 | 代码 s_lens |
| 10:51 | 跑一下：两个三角恒等式在样例上成立；tick 三次，从零数到三；在平方数纸带上做邻域求和；把配对的第一项换成九，三条 lens 定律都为真。代码怎么写，伴随就怎么说。 | demo 输出 |

屏幕代码 `s_adj`（`haskell/src/XiongCi.hs`）：

```haskell
-- 柯里化伴随 L ⊣ R：L a = (a, s)，R b = s -> b
-- C(L a, b) ≅ D(a, R b)：两个方向就是 curry / uncurry
leftAdjunct :: ((a, s) -> b) -> a -> (s -> b)
leftAdjunct = curry

rightAdjunct :: (a -> (s -> b)) -> (a, s) -> b
rightAdjunct = uncurry

unit :: a -> (s -> (a, s))        -- η = φ id：State 的 return
unit = curry id

counit :: (s -> b, s) -> b        -- ε = φ⁻¹ id：求值，Store 的 extract
counit = uncurry id
```

屏幕代码 `s_state`（`haskell/src/XiongCi.hs`）：

```haskell
-- R ∘ L：State 单子。return = η，join = R ε L
newtype State s a = State { runState :: s -> (a, s) }

join :: State s (State s a) -> State s a
join mma = State (fmap (uncurry runState) (runState mma))
--                 ^ fmap = 左侧的 R   ^ uncurry runState = ε

tick :: State Int Int
tick = State (\n -> (n, n + 1))
```

屏幕代码 `s_store`（`haskell/src/XiongCi.hs`）：

```haskell
-- L ∘ R：Store 余单子。extract = ε，duplicate = L η R
data Store s c = St (s -> c) s

extract :: Store s c -> c
extract (St f s) = f s

duplicate :: Store s c -> Store s (Store s c)
duplicate (St f s) = St (St f) s

extend :: (Store s a -> b) -> Store s a -> Store s b
extend k = fmap k . duplicate

sum3 :: Store Int Int -> Int        -- 只看邻域的局部规则
sum3 (St f i) = f (i - 1) + f i + f (i + 1)
```

屏幕代码 `s_lens`（`haskell/src/XiongCi.hs`）：

```haskell
-- lens = Store 余单子的余代数：s -> Store a s
type Lens s a = s -> Store a s

get :: Lens s a -> s -> a
get l s = let St _ a = l s in a

set :: Lens s a -> s -> a -> s
set l s = let St f _ = l s in f

_1 :: Lens (a, b) a
_1 (a, b) = St (\a' -> (a', b)) a
```

---

## 结 · 下集无为而无不为　`11:10–11:51`

参考：下集预告：无为而无不为 · 米田引理与 Kan 扩张

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 11:11 | 今天钉牢四件事：伴随是 hom 集的自然同构；单位、余单位与三角恒等式是它的第二张面孔；R∘L 给出单子 State；L∘R 给出余单子 Store，lens 是它的余代数。 | 四句回顾环绕圆相 |
| 11:28 | 下一集《无为而无不为》：米田引理与 Kan 扩张。不碰对象，只看箭头，就能知道一切。 | 预告：米田 · Kan 扩张 |
| 11:38 | 借 Milewski 的提醒：伴随一旦被认出，就到处都是。知其雄，守其雌。进阶篇，我们下集见。 | 「知其雄，守其雌」书法；印章；谢谢观看 |

---

## 数学校对备注

- 伴随 L ⊣ R：C(L x, y) ≅ D(x, R y)，对 x、y 自然；转置互称 adjunct。
- 单位 η_x = φ(id_{L x}) : x → R(L x)；余单位 ε_y = φ⁻¹(id_{R y}) : L(R y) → y。
- 三角恒等式：(ε L) · (L η) = id_L；(R ε) · (η R) = id_R。有 η/ε+三角 ⇔ 有自然同构。
- 任意伴随给出单子 T = R∘L，μ = R ε L；余单子 W = L∘R，δ = L η R。
- 柯里化伴随 (−, s) ⊣ (s → −)：R(L a) = s → (a, s) = State s a；L(R c) = (s → c, s) = Store s c。
- lens 作为 Store-余代数：φ : s → Store a s ≅ (get, set)，满足 set s (get s) = s、get (set s a) = a、set (set s a) a′ = set s a′。
- 每个单子都可拆成伴随（Kleisli / Eilenberg–Moore），拆法不唯一；List 等常来自离开 Hask 的 Free ⊣ U。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。
