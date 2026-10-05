# 道可道 · 进阶深讲 10 —— 反者道之动
*余代数、ana、hylo、μF/νF｜Coalgebras, ana, hylo — Advanced Deep Dive 10*
- 成片时长：**10:26**（627.0 秒），1920×1080，30 fps
- 受众：已完成入门深讲 01–06 与进阶 07–09；先范畴论陈述，再短 Haskell。
- 结构：道德经钩子 → 余代数与同态 → 终余代数与 ana → 翻转：图与代码 → μF 与 νF → hylo → 短 Haskell → 下集知其雄守其雌。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-10.srt`。
- 屏幕代码摘自 `haskell/src/FanZhe.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。比入门 04（fold 直觉、浅提 ana）更深：余代数范畴、终余代数、对偶兰贝克、μF/νF 与阻抗失配、hylo 融合。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 反者道之动 | 12 Coalgebras | 3.8 Coalgebras |
| 余代数与同态 | 12 Coalgebras | 3.8 |
| 终余代数与 ana | 12 Anamorphisms；Infinite data structures | 3.8 |
| 翻转：图与代码 | 12 Anamorphisms | 3.8 |
| μF 与 νF | 12 Infinite data structures；The impedance mismatch | 3.8 |
| hylo | 12 Hylomorphisms | 3.8 |
| 短 Haskell | 12 / 本集 FanZhe.hs | 3.8 |
| 下集预告 | 10 Adjunctions | 3.2 Adjunctions |

## 术语表

| 中文 | English |
|---|---|
| 自函子 F | endofunctor F |
| F-余代数 / 载体 / 结构映射 | F-coalgebra / carrier / structure map |
| 余代数同态 · 余代数范畴 CoAlg(F) | coalgebra morphism · category of coalgebras |
| 终余代数 (ν, out) | terminal coalgebra |
| 展开 ana | anamorphism (ana) |
| 合态射 hylo | hylomorphism (hylo) |
| 最小不动点 μF / 最大不动点 νF | least / greatest fixed point |
| 阻抗失配 | impedance mismatch |
| 共归纳 | coinduction |
| 融合律 | fusion law |

---

## 反者道之动　`00:00–00:58`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 反者道之动。欢迎来到「道可道」进阶深讲——第十集。 | 宣纸背景，圆相一笔画出；标题「反者道之动」浮现 |
| 00:07 | 上一集立起了初始代数：从它出发，到任何代数恰有一支同态，叫 cata。今天把每一支箭头都反过来。始变终，收拢变展开，砍树变种树。 | 小字：进阶 09 → 10；初始代数 → 终余代数 |
| 00:23 | 本集四根钉子：余代数与同态；终余代数与 ana；μF 与 νF，以及 Haskell 里的阻抗失配；hylo——先生而后归。入门第四集浅提了展开；今天把对偶写正式。 | 四行提纲 |
| 00:41 | 框架仍是 Milewski 的两本书：《函数式编程之道》第十二章余代数，以及《程序员的范畴论》F-代数那一节的对偶侧。片中表述都是释义，不是照录。 | DaoFP ch.12 · CTFP 3.8；印章「知白守黑」 |

---

## 一 · 道德经钩子　`00:58–02:06`

> **反者道之动，弱者道之用。**　——《道德经》第四十章

参考：DaoFP ch.12 Coalgebras；CTFP 3.8 Coalgebras

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:58 | 反者道之动，弱者道之用。 | 竖排书法原文，右起 |
| 01:04 | 「反」不是否定，是掉头。范畴论里，把箭头全部翻转，几乎每个构造都会得到它的孪生兄弟。对偶不是修辞，而是一种机械的生产力。 | 箭头翻转；定理 ⟷ 对偶定理 |
| 01:19 | 上一集的代数，是从 F a 到 a：收拢一层结构。反过来，余代数是从 a 到 F a：从一颗种子里，长出一层结构。Milewski 说得很干脆：cata 用来砍树，ana 用来种树。 | f a → a 与 a → f a 上下对照 |
| 01:37 | 入门第四集已经让你见过 unfold：给一个种子，吐出列表。那是现象。今天要问：为什么展开恰好只有一种？为什么无穷的流也能被同一个 Fix 装下？ | 入门 04：展开是现象；两个问题 |
| 01:53 | 答案仍是普遍性质——只是始对象换成了终对象。刻画一旦掉头，递归、展开、最大不动点，全都跟着来。 | 终对象 → 终余代数 → ana |

---

## 二 · 余代数与同态　`02:06–03:30`

参考：DaoFP ch.12 Coalgebras；CTFP 3.8 Coalgebras

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 02:07 | 先定零件。还是那个自函子 F，描述「一层」形状。只是方向反了：现在不是把装好的结果收进来，而是从载体里观察出一层形状。 | 自函子 F；观察 vs 收尾 |
| 02:21 | F-余代数是一对东西：一个载体 a，和一支结构映射 γ，从 a 到 F a。读法是：给我一个种子，它这一步长出什么形状，洞里又留下什么种子。 | (a, γ : a → F a) |
| 02:38 | 同一个形状可以有许多余代数。从整数展开出列表：零映到空，非零映到头与减一——这是阶乘的生。从整数展开出流：映到自身与加一——这是自然数流的种。 | range / nats 两份余代数 |
| 02:55 | 余代数之间的箭头，叫余代数同态：载体之间的一支 f，要和两边的结构映射交换。先用 γ 观察，再用 F f 搬运；或者先用 f 搬运，再用 δ 观察——两条路必须相等。 | 交换方块：F f ∘ γ = δ ∘ f |
| 03:13 | 函子保持恒等与复合，所以恒等是同态，方块可以拼接。余代数和同态组成一个范畴，记作 CoAlg(F)。它正是 Alg(F) 的对偶范畴。 | CoAlg(F) ≅ Alg(F)^op |

---

## 三 · 终余代数与 ana　`03:30–04:52`

参考：DaoFP ch.12 Anamorphisms；Infinite data structures；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:31 | 现在把上一集的定义原样对偶过来。余代数范畴里的终对象，叫终余代数，记作 ν 和它的结构映射：对任意余代数 a 和 γ，通往它的同态存在且唯一。 | (ν, out)：∀(a, γ) ∃! 同态 |
| 03:47 | 这支唯一的同态，就叫 anamorphism，简称 ana。入门第四集说「ana 就是 unfold」；现在知道它的身份：终对象的唯一入射。 | ana γ；虚线 ∃! |
| 04:00 | 存在给你算法：任选一份余代数，就有一条展法。唯一给你证明原则：两个函数只要都满足同一个方块，它们就相等。不用共归纳的逐项比较，方块替你说完。 | 存在 = 算法 · 唯一 = 共归纳证明原则 |
| 04:17 | 兰贝克的对偶也成立：终余代数的结构映射一定是同构。ν 与 F ν 是同一个东西。所以 ν 是 F 的不动点——而且是最大的那个。记作 νF。 | out : ν ≅ F ν；ν = νF（最大不动点） |
| 04:33 | 取 F 为 StreamF：没有空构造子，每一层都有头和尾。终余代数就是无穷流。取列表形状：终余代数在集合里比初始代数更大——它还允许「假无穷」的极限情况。 | Stream = ν StreamF；List 在 Set 中 μ ⊂ ν |

---

## 四 · 翻转：图与代码　`04:52–06:18`

参考：DaoFP ch.12 Anamorphisms；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 04:53 | 图也一样：把 cata 那张交换图的箭头全部翻转，就是 ana 的交换图。左边的 ι 朝上变成右边的 out 朝下；虚线的唯一出射，变成唯一入射。 | cata 方块 ↔ ana 方块；箭头逐一翻转 |
| 05:09 | 代码也一样。cata 是：先剥一层 unFix，再 fmap 递归，最后用代数收尾。把复合的顺序倒过来，unFix 换成 Fix，就是 ana：先用余代数观察，再 fmap 递归，最后用 Fix 封一层。 | 代码 cata / ana 对照高亮 |
| 05:28 | 所以你不必另背一套定义。记住一张方块，掉头即得另一张；记住一行复合，倒序即得另一行。反者道之动——对偶是一种压缩。 | 一图两读 · 一行两式 |
| 05:43 | Haskell 里，构造子 Fix 同时扮演两边：作为代数的结构映射，它是 ι；作为余代数的逆，它是 out 的逆，把一层形状封回不动点。unFix 则是对面的那一支。 | Fix 兼任 ι 与 out⁻¹ |
| 06:00 | 这里藏着第二集与第九集的回声：初始代数从始对象，也就是无，一层层生长出来；终余代数则从终对象，也就是有，一层层逼近。有无相生，又出现了一次。 | 0 → F0 → F²0 → …  与  1 ← F1 ← F²1 ← … |

---

## 五 · μF 与 νF　`06:18–07:31`

参考：DaoFP ch.12 Infinite data structures；The impedance mismatch；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:18 | 在集合范畴里，最小不动点与最大不动点并不相同。μF 是从无长出来的全部有限阶段；νF 是从有逼近下来的全部相容体系。一般有 μF 真包含于 νF。 | Set：μF ⊂ νF |
| 06:36 | 经典例子是恒等函子：最小不动点是空集，最大不动点是单点集。列表函子也一样：初始代数是有限列表；终余代数还装着「无限列表」的理想点。 | Id：∅ vs 1；List：有限 vs 含极限 |
| 06:52 | 但在 Haskell 里，因为惰性，同一个 Fix 既能折叠有限的结构，也能展开无限的流。最小与最大，在这里被揉成了一个类型。 | Hask：Fix 兼任 μF 与 νF |
| 07:05 | Milewski 把这种错位叫阻抗失配：范畴论在集合里分得很清的两样东西，到了惰性语言里共用一个语法。便利是真的，代价也是真的。 | impedance mismatch |
| 07:19 | 代价之一：如果展开永不终止，依赖它的计算也会永远算下去。惰性让你写下无穷，却不替你保证停机。 | 发散：ana 不终止 ⇒ 后续发散 |

---

## 六 · hylo：先生而后归　`07:31–08:46`

参考：DaoFP ch.12 Hylomorphisms；CTFP 3.8

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 07:32 | 有了生，有了归，就可以把它们接起来：先用 ana 展开，再用 cata 折叠。这就是 hylo，合态射。先生，而后归。 | a ─ana→ Fix f ─cata→ b |
| 07:46 | 妙处在于，hylo 的定义里没有不动点的影子：中间那个结构被生出，又在构造的同时被消费，从未完整存在于内存中。老子有一句话恰好描述这种融合：生而不有。 | 中间 Fix f 渐隐；书法「生而不有」 |
| 08:02 | 比如阶乘：从 n 展开出 n、n 减一，一直到一；再把这条链乘起来。写成 hylo，生和归各是一份不递归的菜谱，递归机关只出现一次。 | fact = hylo alg coa |
| 08:16 | 你也可以先 ana 再 cata，语义相同；但那会真的建出中间那棵树。hylo 把两趟合成一趟——这是融合律在代码里的样子。 | hylo = cata ∘ ana（融合后不建 Fix） |
| 08:29 | 反者道之动：每证明一个关于代数的定理，翻转箭头，就白得一个关于余代数的定理。弱者道之用——余代数这一侧，往往用更弱的假设，换来对无穷结构的发言权。 | 定理 ⟷ 对偶定理；弱者 = 共归纳 |

---

## 七 · 短 Haskell　`08:46–09:43`

参考：DaoFP ch.12；CTFP 3.8；本集 haskell/src/FanZhe.hs

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 08:46 | 把刚才的话写成几行 Haskell。Fix、Algebra、Coalgebra、cata、ana。后两行是同一张方块的两种读法。 | 代码 s_fix |
| 08:59 | hylo 一行：没有 Fix 的影子。阶乘是 ListF 上的一份代数加一份余代数。 | 代码 s_hylo / s_list |
| 09:08 | StreamF 没有空构造子。nats 从零展开，takeS 只取前几项——无穷被种下，有限被看见。 | 代码 s_stream |
| 09:18 | ana 也能种有限树：range 把闭区间展开成列表，再交给 cata 求和。同一套机关，有限与无穷共用。 | 代码 s_range |
| 09:29 | 跑一下：五的阶乘是一百二十；自然数流前八项是零到七；一到十求和得五十五。图怎么说，代码就怎么应。 | demo 输出 |

屏幕代码 `s_fix`（`haskell/src/FanZhe.hs`）：

```haskell
-- 不动点：构造子 Fix 兼任 ι（代数侧）与 ν（余代数侧）
newtype Fix f = Fix { unFix :: f (Fix f) }

type Algebra f a = f a -> a
type Coalgebra f a = a -> f a

-- cata：砍树　alg . fmap (cata alg) . unFix
cata :: Functor f => Algebra f a -> Fix f -> a
cata alg = alg . fmap (cata alg) . unFix

-- ana：种树　把复合顺序倒过来，unFix 换成 Fix
ana :: Functor f => Coalgebra f a -> a -> Fix f
ana coa = Fix . fmap (ana coa) . coa
```

屏幕代码 `s_hylo`（`haskell/src/FanZhe.hs`）：

```haskell
-- hylo：先生，而后归。定义里没有 Fix——中间结构边生边消
hylo :: Functor f => Algebra f b -> Coalgebra f a -> a -> b
hylo alg coa = alg . fmap (hylo alg coa) . coa
```

屏幕代码 `s_list`（`haskell/src/FanZhe.hs`）：

```haskell
data ListF e x = NilF | ConsF e x
  deriving Functor

-- 先生：n, n-1, …, 1；后归：乘起来
fact :: Integer -> Integer
fact = hylo alg coa where
  coa 0 = NilF
  coa n = ConsF n (n - 1)
  alg NilF        = 1
  alg (ConsF n r) = n * r
```

屏幕代码 `s_stream`（`haskell/src/FanZhe.hs`）：

```haskell
-- 惰性：同一个 Fix 承载无限流（终余代数 νF）
data StreamF e r = StreamF e r
  deriving Functor

nats :: Fix (StreamF Integer)
nats = ana (\n -> StreamF n (n + 1)) 0

takeS :: Int -> Fix (StreamF e) -> [e]
takeS 0 _                 = []
takeS k (Fix (StreamF e r)) = e : takeS (k - 1) r
```

屏幕代码 `s_range`（`haskell/src/FanZhe.hs`）：

```haskell
-- ana 也能种有限树：从区间展开出列表
range :: (Integer, Integer) -> Fix (ListF Integer)
range = ana coa where
  coa (lo, hi)
    | lo > hi   = NilF
    | otherwise = ConsF lo (lo + 1, hi)
```

---

## 结 · 下集知其雄守其雌　`09:43–10:26`

参考：下集预告：知其雄，守其雌 · 伴随与单子余单子

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 09:43 | 今天钉牢四件事：余代数与同态组成范畴；终余代数的唯一入射就是 ana；μF 与 νF 在集合里分家，在 Haskell 里共用 Fix；hylo 先生后归，中间不落地。 | 四句回顾环绕圆相 |
| 10:01 | 下一集《知其雄，守其雌》：伴随登场。左伴随与右伴随，单位与余单位——同一条溪流的两岸，喂养出单子与余单子。 | 预告：伴随 · State · Store |
| 10:15 | 借 Milewski 的提醒：对偶不是修辞，而是生产力。反者道之动。进阶篇，我们下集见。 | 「反者道之动」书法；印章；谢谢观看 |

---

## 数学校对备注

- F-余代数 (a, γ : a → F a)；同态 f 满足 F f ∘ γ = δ ∘ f；CoAlg(F) ≅ Alg(F)^op。
- 终余代数 (ν, out) 是 CoAlg(F) 的终对象；从 (a, γ) 出发的唯一同态即 ana γ。存在＝算法，唯一＝共归纳证明原则。
- 兰贝克对偶：终余代数的 out 是同构，ν ≅ F ν，且为最大不动点 νF（任何不动点都是余代数，故有 x → ν）。
- ana 由交换方块读出：ana γ = Fix ∘ fmap (ana γ) ∘ γ；与 cata 复合顺序对偶。
- Set 中一般 μF ⊂ νF（例：Id 的 ∅ ⊂ 1；列表的有限列表 ⊂ 含极限点）。Hask 因惰性，`Fix f` 兼任二者（DaoFP ch.12 “impedance mismatch”）。
- hylo alg coa = alg ∘ fmap (hylo alg coa) ∘ coa；语义等于 cata alg ∘ ana coa，但定义中无 Fix，中间结构边生边消（融合）。
- 若 coa 不终止，hylo 发散。依 CTFP 惯例忽略 ⊥。

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。
