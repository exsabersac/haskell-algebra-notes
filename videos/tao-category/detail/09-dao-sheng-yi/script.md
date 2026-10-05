# 道可道 · 进阶深讲 09 —— 道生一
*初始代数、兰贝克引理、Fix 与 cata｜Initial algebras, Lambek, Fix — Advanced Deep Dive 09*
- 成片时长：**11:17**（677.1 秒），1920×1080，30 fps
- 受众：已完成入门深讲 01–06 与进阶 07–08；先范畴论陈述，再短 Haskell。
- 结构：道德经钩子 → 代数与同态 → 初始代数与 cata → 兰贝克引理 → Fix 与 cata 的来历 → 从无出发：余极限 → 短 Haskell → 下集反者道之动。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-09.srt`。
- 屏幕代码摘自 `haskell/src/DaoShengYi.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。比入门 03（Maybe/List 计数）与 04（fold 直觉、「今天不写 Lambek」）更深：代数范畴、初始性、兰贝克证明、Fix 的来历、Adámek 余极限、Church 编码。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 道生一 | 7 Recursion（以此句开篇）；11 导言（递归机关 vs 可插拔零件） | 3.8 |
| 代数与同态 | 11 Algebras from Endofunctors；Category of Algebras | 3.8 F-Algebras |
| 初始代数与 cata | 11 Initial algebra；Catamorphisms（Examples, Lists as initial algebras） | 3.8 |
| 兰贝克引理 | 11 Lambek's Lemma and Fixed Points | 3.8 |
| Fix 与 cata 的来历 | 11 Fixed point in Haskell；Catamorphisms | 3.8 |
| 从无出发：余极限 | 11 Initial Algebra as a Colimit；Initial Algebra from Universality | 3.8 |
| 短 Haskell | 11 / 本集 DaoShengYi.hs | 3.8 |
| 下集预告 | 12 Coalgebras | 3.8 Coalgebras |

## 术语表

| 中文 | English |
|---|---|
| 自函子 F | endofunctor F |
| F-代数 / 载体 / 结构映射 | F-algebra / carrier / structure map |
| 代数同态 · 代数范畴 Alg(F) | algebra morphism · category of algebras |
| 初始代数 (i, ι) | initial algebra |
| 折叠 cata ⦇α⦈ | catamorphism (banana brackets) |
| 兰贝克引理 | Lambek's lemma |
| 最小不动点 μF / 最大不动点 νF | least / greatest fixed point |
| 余极限 / ω-链 | colimit / ω-chain |
| Adámek 定理 | Adámek's theorem |
| Church 编码 Mu | Church encoding |

---

## 道生一　`00:00–00:54`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 道生一。欢迎来到「道可道」进阶深讲——第九集。 | 宣纸背景，圆相一笔画出；标题「道生一」浮现 |
| 00:07 | 上一集立起了始对象：从它出发，到谁都恰有一支箭头。今天把同一句话搬进另一个范畴——F-代数的范畴。那里的始对象，就是「一」：初始代数。 | 小字：进阶 08 → 09；始对象 → 初始代数 |
| 00:22 | 本集四根钉子：代数与同态；初始代数与 cata；兰贝克引理与不动点；从无出发的余极限。入门三、四集给了直觉；今天把定理写正式。 | 四行提纲 |
| 00:37 | 框架仍是 Milewski 的两本书：《函数式编程之道》第七章递归与第十一章代数，以及《程序员的范畴论》F-代数那一节。片中表述都是释义，不是照录。 | DaoFP ch.7 / ch.11 · CTFP 3.8；印章「知白守黑」 |

---

## 一 · 道德经钩子　`00:54–02:00`

> **道生一，一生二，二生三，三生万物。**　——《道德经》第四十二章

参考：DaoFP ch.7 Recursion（以此句开篇）；DaoFP ch.11 Algebras

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:55 | 道生一，一生二，二生三，三生万物。 | 竖排书法原文，右起 |
| 01:02 | 《函数式编程之道》讲递归的那一章，就以这句话开篇。入门篇把它读成计数：Maybe 套在 Void 上，一层、两层、三层。那是现象。 | 入门 03：计数是现象 |
| 01:18 | 进阶篇要问背后的结构：为什么一层层套下去，会停在一个确定的类型上？为什么从这个类型出发，折叠恰好只有一种？ | 两个问题：为何收敛 · 为何唯一 |
| 01:30 | 答案是一个普遍性质。递归类型不是被「写出来」的，而是被刻画出来的：它是一类代数里的始对象。刻画一旦成立，递归、折叠、同构，全都跟着来。 | 递归类型 = 代数范畴的始对象 |
| 01:46 | Milewski 把问题拆成两半：递归的机关，和可插拔的零件。零件是一个函子，机关只写一次。今天就把这台机关拆开看。 | 递归机关 ‖ 可插拔零件 |

---

## 二 · 代数与同态　`02:00–03:25`

参考：DaoFP ch.11 Algebras from Endofunctors；Category of Algebras；CTFP 3.8 F-Algebras

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 02:01 | 先定零件。一个自函子 F，描述「一层」形状，用洞标出子结构该放的位置。比如表达式：要么是一个整数叶子，要么是一个加号，下面挂两个洞。 | ExprF x = ValF Int | PlusF x x |
| 02:16 | F-代数是一对东西：一个载体 a，和一支结构映射 α，从 F a 到 a。读法是：假设洞里已经装好了算完的结果，这一步怎么收尾。 | (a, α : F a → a) |
| 02:31 | 同一个形状可以有许多代数。载体取整数，加号就做加法——这是求值。载体取字符串，加号就做拼接——这是打印。不评判哪一个更合理；每一种选择都是一份代数。 | eval : F Int → Int；pretty : F String → String |
| 02:49 | 代数之间的箭头，叫代数同态：载体之间的一支 f，要和两边的结构映射交换。先在 F 层用 F f 搬运，再用 β 收尾；或者先用 α 收尾，再用 f 搬运——两条路必须相等。 | 交换方块：f ∘ α = β ∘ F f |
| 03:09 | 函子保持恒等与复合，所以恒等是同态，方块可以拼接。代数和同态组成一个范畴。条件很苛刻：show 就不是从求值到打印的同态。 | Alg(F) 是范畴；show 不交换 |

---

## 三 · 初始代数与 cata　`03:25–04:46`

参考：DaoFP ch.11 Initial algebra；Catamorphisms；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:26 | 现在把上一集的定义原样搬过来。代数范畴里的始对象，叫初始代数，记作 i 和 ι：对任意代数 a 和 α，从它出发的同态存在且唯一。 | (i, ι)：∀(a, α) ∃! 同态 |
| 03:42 | 这支唯一的同态，就叫 catamorphism，简称 cata，有时写成香蕉括号包住 α。入门第四集说「cata 就是 fold」；现在知道它的身份：初始对象的唯一出射。 | ⦇α⦈ = cata α；虚线 ∃! |
| 03:58 | 存在给你算法：任选一份代数，就有一条折法。唯一给你证明原则：两个函数只要都满足同一个方块，它们就相等。不用归纳，不用逐项比较。 | 存在 = 算法 · 唯一 = 证明原则 |
| 04:13 | 取 F 为 Maybe。一份 Maybe 代数，等于两样东西：Nothing 对应的起点，和 Just 对应的一步。初始代数的 cata，正是自然数的递归子——给起点、给一步，路就定了。 | Maybe a → a ≅ (a, a → a)；Nat 递归子 |
| 04:30 | 取列表的形状函子 ListF：代数等于空表的起点，加上「头与已折尾」的一步。cata 就是 foldr。所有递归类型的折叠，都是同一个定理的特例。 | ListF e：cata = foldr |

---

## 四 · 兰贝克引理　`04:46–06:22`

参考：DaoFP ch.11 Lambek's Lemma and Fixed Points；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 04:47 | 兰贝克引理：初始代数的结构映射 ι，一定是同构。F i 与 i，是同一个东西。 | ι : F i ≅ i |
| 04:57 | 证明只靠一个观察：代数是自相似的。把 F 再作用一次，F i 配上 F ι，又是一份代数。由初始性，存在唯一同态 h，从 i 到 F i。 | 代数 (F i, F ι)；∃! h : i → F i |
| 05:13 | 把 h 的方块和一个显然交换的方块拼在一起：ι 复合 h，就是从初始代数到它自己的同态。可恒等也是这样的同态。唯一性一锤定音：ι 复合 h，等于恒等。 | 拼接方块；ι ∘ h = id |
| 05:31 | 再读 h 的方块：h 复合 ι，等于 F ι 复合 F h，也就是 F 作用在「ι 复合 h」上——恒等被 F 送到恒等。所以 h 就是 ι 的逆。 | h ∘ ι = F(ι ∘ h) = id |
| 05:49 | 所以 i 是 F 的不动点：再作用一次 F，它不变。而且它是最小的那个——因为任何不动点本身也是一份代数，初始代数到它总有一支箭头。记作 μF。 | i = μF（最小不动点） |
| 06:06 | 《道德经》说，道法自然。「自然」二字的本义，是自己如此。初始代数正是这样：它不靠外物定义，展开一层，还是它自己。 | 书法：道法自然 = 自己如此 |

---

## 五 · Fix 与 cata 的来历　`06:22–07:48`

参考：DaoFP ch.11 Fixed point in Haskell；Catamorphisms；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:22 | Haskell 直接写出这个不动点：Fix f。构造子 Fix，从 F 作用在 Fix f 上，收成 Fix f——它就是结构映射 ι。unFix 剥掉一层——它就是兰贝克给出的逆。 | Fix = ι；unFix = ι⁻¹ |
| 06:40 | 现在 cata 的定义不再是凭空背下来的。把 cata 的方块里朝上的 ι 换成 unFix：先剥一层，再用 fmap 把 cata 递归地伸进每个洞，最后用代数收尾。沿着箭头读一遍，就是定义。 | cata α = α ∘ fmap (cata α) ∘ unFix |
| 07:00 | 这一刀切得很干净：递归全部关在 Fix 和 cata 里，只写一次。使用者只提供两样不递归的东西——形状函子，和一份代数。复杂的问题，拆成了简单的零件。 | 递归只写一次；用户给 F 与 α |
| 07:16 | 一句诚实的附注。在集合范畴里，Fix 对应最小不动点 μF。Haskell 是惰性的，Fix 还能装下无穷的值，最小与最大不动点在那里重合——最大不动点，是下一集的故事。 | Set：Fix = μF；Hask：惰性 → 亦含无穷值（νF 下集） |
| 07:34 | 另外，Fix 对任何类型构造子都能写，但要真正从无生出东西，形状里必须有不依赖洞的「叶子」。没有叶子，就没有起点。 | 需要叶子：Nothing / NilF / ValF |

---

## 六 · 从无出发：余极限　`07:48–09:16`

参考：DaoFP ch.11 Initial Algebra as a Colimit；Initial Algebra from Universality

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 07:49 | 初始代数从哪里来？从无出发。把 F 作用在始对象零上：零里什么也没有，所以 F 零里只剩叶子。再作用一次，叶子可以挂进节点；再一次，树更高一层。 | 0 → F0 → F²0 → F³0 → ⋯ |
| 08:06 | 这些对象排成一条链，箭头是始对象的唯一出射，被 F 一层层抬上去。链的余极限，把所有有限阶段粘在一起。 | ω-链；箭头 !, F!, F²! |
| 08:18 | 这是 Adámek 定理：只要 F 保持这种链的余极限，链的余极限就是初始代数。多项式函子在集合范畴里都满足；Maybe 和 ListF 都在其中。无穷加一，还是无穷。 | Adámek：F 保持 ω-余极限 ⇒ colim = μF |
| 08:37 | 取 F 为 Maybe：零、一、二、三，链的余极限就是自然数。取列表：一、加 a、加 a 乘 a，一直加下去——Milewski 戏称的几何级数，在这里有了严格的意义。 | Nat；L = 1 + a + a² + ⋯ |
| 08:57 | 还有另一种看法：一个初始代数的值，等价于它对所有代数的折法。对一切载体 a，给我一份代数，我就交出一个 a。这就是 Church 编码，Mu f。「一」，是全部归途的总和。 | Mu f = ∀a. (F a → a) → a |

---

## 七 · 短 Haskell　`09:16–10:32`

参考：DaoFP ch.11；CTFP 3.8；本集 haskell/src/DaoShengYi.hs

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 09:17 | 把刚才的话写成几行 Haskell。Fix、Algebra、cata，三行就是全部机关；最后一行，是沿着方块读出来的定义。 | 代码 s_fix |
| 09:30 | 零件：ExprF 是一层表达式的形状。eval 和 pretty 是同一形状上的两份代数。cata eval 把 e9 折成九；cata pretty 折成「二加三加四」。 | 代码 s_expr / s_algs |
| 09:45 | 兰贝克引理也能写成代码：把 fmap Fix 当作代数——这正是提升后的 F ι——它的 cata 就是那支 h。可以检验，它和 unFix 一模一样。 | 代码 s_lambek |
| 10:00 | 自然数是 Maybe 的不动点；toInt 用 maybe 零 加一 作代数。Mu 把值存成「全部折法」：fromMu 只需把 Fix 本身当作代数交进去。 | 代码 s_nat / s_mu |
| 10:14 | 跑一下：e9 求值得九，打印得二加三加四；兰贝克检验为真；三个后继得三；一到十的 Mu 列表求和，五十五。图怎么说，代码就怎么应。 | demo 输出 |

屏幕代码 `s_fix`（`haskell/src/DaoShengYi.hs`）：

```haskell
-- 不动点：构造子 Fix 即初始代数的结构映射 ι
newtype Fix f = Fix { unFix :: f (Fix f) }

-- F-代数：载体 a 与结构映射 f a -> a
type Algebra f a = f a -> a

-- 读交换方块：cata α = α ∘ F (cata α) ∘ ι⁻¹
cata :: Functor f => Algebra f a -> Fix f -> a
cata alg = alg . fmap (cata alg) . unFix
```

屏幕代码 `s_expr`（`haskell/src/DaoShengYi.hs`）：

```haskell
-- 形状：一层表达式，x 标出子树的洞
data ExprF x = ValF Int | PlusF x x
  deriving Functor

val :: Int -> Fix ExprF
val n = Fix (ValF n)

plus :: Fix ExprF -> Fix ExprF -> Fix ExprF
plus a b = Fix (PlusF a b)
```

屏幕代码 `s_algs`（`haskell/src/DaoShengYi.hs`）：

```haskell
-- 同一形状，两份代数：载体不同，菜谱不同
eval :: Algebra ExprF Int
eval (ValF n)    = n
eval (PlusF m n) = m + n

pretty :: Algebra ExprF String
pretty (ValF n)    = show n
pretty (PlusF s t) = s ++ " + " ++ t

e9 :: Fix ExprF
e9 = plus (plus (val 2) (val 3)) (val 4)
```

屏幕代码 `s_lambek`（`haskell/src/DaoShengYi.hs`）：

```haskell
-- 兰贝克：把 F 作用于初始代数，得代数 (F i, F ι)；
-- 唯一的同态 h 就是 ι 的逆
lambekOut :: Functor f => Fix f -> f (Fix f)
lambekOut = cata (fmap Fix)
-- 定理：lambekOut = unFix，且 Fix . lambekOut = id
```

屏幕代码 `s_nat`（`haskell/src/DaoShengYi.hs`）：

```haskell
-- 道生一：Maybe 的最小不动点即自然数
type Nat = Fix Maybe

zero :: Nat
zero = Fix Nothing

suc :: Nat -> Nat
suc = Fix . Just

-- Maybe 代数 = (起点, 一步)；cata 即递归子
toInt :: Nat -> Int
toInt = cata (maybe 0 (+ 1))
```

屏幕代码 `s_mu`（`haskell/src/DaoShengYi.hs`）：

```haskell
-- 从普遍性看初始代数：一个值 = 它全部的折法
newtype Mu f = Mu (forall a. Algebra f a -> a)

cataMu :: Algebra f a -> Mu f -> a
cataMu alg (Mu h) = h alg

toMu :: Functor f => Fix f -> Mu f
toMu t = Mu (\alg -> cata alg t)

fromMu :: Mu f -> Fix f
fromMu (Mu h) = h Fix
```

屏幕代码 `s_list`（`haskell/src/DaoShengYi.hs`）：

```haskell
data ListF e x = NilF | ConsF e x
  deriving Functor

fromList :: [e] -> Mu (ListF e)
fromList es = Mu (\alg -> foldr (\e r -> alg (ConsF e r)) (alg NilF) es)

sumAlg :: Algebra (ListF Int) Int
sumAlg NilF        = 0
sumAlg (ConsF e r) = e + r
```

---

## 结 · 下集反者道之动　`10:32–11:17`

参考：下集预告：反者道之动 · 余代数与 ana

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 10:32 | 今天钉牢四件事：代数与同态组成范畴；初始代数的唯一出射就是 cata；兰贝克说结构映射是同构，所以它是最小不动点；Adámek 说，它是从无出发那条链的余极限。 | 四句回顾环绕圆相 |
| 10:50 | 下一集《反者道之动》：把箭头全部掉头。代数变余代数，始对象变终对象，cata 变 ana——从种子展开出无穷的结构，最大不动点登场。 | 预告：余代数 · ana · νF |
| 11:05 | 借 Milewski 的提醒：机关只写一次，零件随你插。道生一。进阶篇，我们下集见。 | 「道生一」书法；印章；谢谢观看 |

---

## 数学校对备注

- F-代数 (a, α : F a → a)；同态 f 满足 f ∘ α = β ∘ F f；恒等与复合由函子律保证，Alg(F) 成范畴。
- 初始代数 (i, ι) 是 Alg(F) 的始对象；到 (a, α) 的唯一同态即 cata α（⦇α⦈）。存在＝定义，唯一＝证明原则（融合律的来源）。
- 兰贝克：(F i, F ι) 是代数，得唯一 h : i → F i；拼接得 ι ∘ h 为 i 上的自同态，故 = id；再 h ∘ ι = F ι ∘ F h = F(ι ∘ h) = id。i ≅ F i，且为最小不动点 μF（任何不动点 (x, ξ) 都是代数，故有 i → x）。
- Haskell：`Fix` 构造子＝ι，`unFix`＝ι⁻¹；`lambekOut = cata (fmap Fix)` 即证明中的 h，可检验与 `unFix` 一致。
- 在 Set 中 Fix 对应 μF；Hask 因惰性，`Fix f` 亦含无穷值，最小与最大不动点重合（DaoFP ch.12 “impedance mismatch”）——下集展开 νF。
- 初始代数未必存在；需要“叶子”（不依赖洞的构造子）。例：F x = Int × x 在 Set 中 μF = 0（空集是其初始代数载体）。
- Adámek：若 F 保持 ω-链余极限，则 colim(0 → F0 → F²0 → ⋯) 是初始代数；Set 上多项式函子满足。Maybe ⇒ ℕ；1 + a × x ⇒ 列表 1 + a + a² + ⋯。
- Church 编码 `Mu f = forall a. (f a -> a) -> a`；在 Haskell（参数性）下与 `Fix f` 同构（`toMu` / `fromMu`）。
- 依 CTFP 惯例忽略 ⊥。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。
