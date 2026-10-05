# 道可道 · 进阶深讲 12 —— 无为而无不为（系列终章）
*米田引理、可表函子、Kan 扩张｜Yoneda lemma, representable functors, Kan extensions — Advanced Deep Dive 12 (FINAL)*
- 成片时长：**09:10**（550.9 秒），1920×1080，30 fps
- 受众：已完成入门深讲 01–06 与进阶 07–11；先范畴论陈述，再短 Haskell。
- 结构：钩子 → 可表函子 → 米田引理（对象由箭头决定）→ Haskell Yoneda/forall → Kan 扩张（Ran/Lan）→ 系列收束回到道可道。
- 旁白：edge-tts `zh-CN-YunxiNeural`，语速 −6%。字幕：烧录 + `final/tao-category-detail-12.srt`。
- 屏幕代码摘自 `haskell/src/WuWei.hs`（`-- {{snip:…}}`），GHC 9.14.1 `-Wall` 通过。
- 美学与入门/进阶篇一致：宣纸、印章「知白守黑」。本集赎回进阶 07 的米田预告。

## 主要参考与致谢
叙述框架与 Haskell 写法以 Bartosz Milewski 两书为参照（释义改写，不做长段照录）：

- **DaoFP** — *The Dao of Functional Programming*，<https://github.com/BartoszMilewski/DaoFP>
- **CTFP** — *Category Theory for Programmers*，<https://github.com/hmemcpy/milewski-ctfp-pdf>

| 段落 | DaoFP | CTFP |
|---|---|---|
| 钩子 / 无为 | 2 Composition（Identity = wu wei） | — |
| 可表函子 | 9 Representable Functors | 2.5（前置） |
| 米田引理 | 9 The Yoneda Lemma | 2.5 / 2.6 |
| Haskell Yoneda / Speak | 9 Yoneda lemma in programming | 2.5 |
| Kan 扩张 Ran/Lan | 20 Kan Extensions | 3.11 |
| 系列收束 | Master Yoneda: At the arrows look! | — |

## 术语表

| 中文 | English |
|---|---|
| 可表函子 / 表示元 | representable functor / representing object |
| 米田引理 | Yoneda lemma |
| 米田嵌入（满忠实） | Yoneda embedding (fully faithful) |
| 自然变换族 Nat | natural transformations Nat |
| 续体传递 / Speak | continuation-passing / Speak a |
| 右/左 Kan 扩张 Ran / Lan | right/left Kan extension |
| 沿恒等的右 Kan 扩张 | Ran along Identity ≅ Yoneda |

---

## 无为而无不为　`00:00–00:57`

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:00 | 道常无为而无不为。欢迎来到「道可道」进阶深讲——第十二集，也是本系列的终章。 | 宣纸背景，圆相一笔画出；标题「无为而无不为」浮现 |
| 00:09 | 第七集钉过一句话：对象不可道，箭头可道；并把米田轻轻挂上，说后集赎回。今天，就是赎回的日子。 | 回扣进阶 07：对象不可道 · 待赎回 |
| 00:21 | 本集四根钉子：可表函子；米田引理——对象由箭头决定；Haskell 里的 Yoneda 与 forall；Kan 扩张——Ran 与 Lan 的直觉。最后，整条系列回到道可道。 | 四行提纲 |
| 00:41 | 框架仍是 Milewski 的两本书：《函数式编程之道》第九章、第二十章，与《程序员的范畴论》里米田与 Kan 各章。片中都是释义，不是照录。 | DaoFP ch.9 / 20 · CTFP 2.5 / 2.6 / 3.11；印章「知白守黑」 |

---

## 一 · 道德经钩子　`00:57–02:06`

> **道常无为而无不为。**　——《道德经》第三十七章

参考：DaoFP ch.2 Composition（Identity = wu wei）；DaoFP ch.9 The Yoneda Lemma；CTFP 2.5

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 00:57 | 道常无为而无不为。 | 竖排书法原文，右起 |
| 01:02 | 无为，不是什么都不做；是不做多余的事。DaoFP 第二章把恒等箭头称为无为：什么也不改变，也不花时间。米田的证明，正是从一支恒等出发。 | id = wu wei；一支自环 |
| 01:18 | 无不为，是说：正因为不掺私货，它被完全确定，因而能应对一切。喂给它 id，就得到一个值；有了值，用 fmap 就能应对任何箭头。 | fromYoneda = g id；toYoneda = fmap |
| 01:33 | 第七集留下的漏洞是：若对象不可言说，凭什么断定两个对象相同？米田说：看它们出发的全部箭头是否自然同构。同构，在范畴论里就是相同的全部含义。 | 回扣 a ≅ b ? → Hom(a,−) ≅ Hom(b,−) |
| 01:50 | 今天的路线：先认识可表函子，再陈述米田引理，落到 Haskell 的 forall，再瞥一眼 Kan 扩张，最后用米田嵌入把道可道整句赎回。 | 本集路线图 |

---

## 二 · 可表函子　`02:06–03:32`

参考：DaoFP ch.9 Representable Functors；CTFP 2.5 The Yoneda Lemma（前置）

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 02:07 | 从一个对象 a 出发，对每个对象 x，收集从 a 到 x 的全部箭头，得到一个集合 Hom(a, x)。这对 x 是函子：箭头 f 从 x 到 y，就把 g 后复合变成 f 复合 g。 | Hom(a, −) : C → Set；后复合 |
| 02:25 | 这个函子叫可表函子，a 是它的表示元。反过来，从 a 射入的箭头，给出反变可表函子 Hom(−, a)。正变看出去，反变看进来。 | 可表 · 表示元 a；Hom(−, a) 反变 |
| 02:40 | 可表的意思是：这个函子长得像某个 Hom。若 F 与 Hom(a, −) 自然同构，就说 F 被 a 表示。a 是什么？是那支被挑出来的「万能箭头」所瞄准的对象。 | F ≅ Hom(a, −) ⇒ F 被 a 表示 |
| 02:57 | Haskell 程序员天天见可表：从 a 出发的函数类型，a 到 x，就是 Hom(a, x)。continuation 类型 Speak a，是把 Hom(a, −) 喂进一个「取元素」的函子——后面赎回会用到。 | (a → −) 可表；Speak a = forall x. (a → x) → x |
| 03:17 | 米田引理要回答的，正是：自然变换从 Hom(a, −) 到任意函子 F，长什么样？答案短得惊人——它们一一对应于 F 在 a 上的一个元素。 | Nat(Hom(a,−), F) ≅ F a |

---

## 三 · 米田引理　`03:32–05:15`

参考：DaoFP ch.9 The Yoneda Lemma；Yoneda lemma in programming；CTFP 2.5 The Yoneda Lemma

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 03:33 | 陈述。设 F 是从 C 到集合范畴的函子。从可表函子 Hom(a, −) 到 F 的自然变换，与 F 在 a 处的元素，一一对应。 | Nat(C(a,−), F) ≅ F(a) |
| 03:47 | 为什么？一个自然变换 α，对每个 x，给出从 Hom(a, x) 到 F x 的函数。它必须对后复合自然。取 x 等于 a，左边有一支现成的箭头：恒等。α 在恒等上的值，就是 F a 里的那个元素。 | α_a(id_a) ∈ F a；无为：只看 id |
| 04:10 | 反过来，有了 F a 里的一个元素，怎么造出整族 α？对任意箭头 h 从 a 到 x，用 F 作用在 h 上，推到 F x。自然性保证：这样做出来的，恰好是唯一可能的那一个。 | α_x(h) = F(h)(ξ)；无不为 |
| 04:28 | 所以：无为——它不能检查 x，不能凭空造 x，只能把你给的箭头原样用上；无不为——正因为如此，整族变换被一个元素完全钉死。 | 参数性 / 自然性 = 无为而无不为 |
| 04:42 | 取 F 为另一个可表函子 Hom(b, −)，就得到米田嵌入：从 a 到 b 的箭头，一一对应 Hom(a, −) 到 Hom(b, −) 的自然变换。嵌入是满忠实的。 | C(a,b) ≅ Nat(Hom(a,−), Hom(b,−))；满忠实 |
| 04:59 | 于是：两个对象同构，当且仅当它们的可表函子自然同构。对象不可道；「它的全部说法」可道——而且恰好够用。第七集挂起的那句话，在这里落地。 | a ≅ b ⟺ C(a,−) ≅ C(b,−)；赎回 |

---

## 四 · Haskell：Yoneda 与 forall　`05:15–06:36`

参考：DaoFP ch.9 Yoneda lemma in programming；CTFP 2.5；本集 haskell/src/WuWei.hs

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 05:16 | 落到 Haskell。Yoneda f a，就是对一切 x，给定从 a 到 x 的箭头，产出一个 f x。米田说：它与 f a 同构。 | 代码 s_yoneda：newtype Yoneda |
| 05:30 | toYoneda 有了 f a，用 fmap 应对任何箭头——无不为。fromYoneda 只喂给它 id——无为。来回一圈，回到原处。 | toYoneda / fromYoneda 高亮 |
| 05:43 | Functor 实例更妙：fmap 在 Yoneda 里不做真正的映射，只把函数复合攒起来。一连串 fmap，什么也不做，直到 fromYoneda 的那一刻一次完成。无为，也是一种优化。 | fmap h . fmap g ⇒ 一次复合 |
| 06:01 | 取 f 为恒等函子：Speak a，对一切 x 能把 a 到 x 变成 x 的东西，同构于 a 本身。redeem 只给它 id。这正是续体传递风格的最小种子——第七集写下的 Speak，今天赎回。 | 代码 s_redeem；回看 ep07 Speak |
| 06:21 | 跑一下：列表包进 Yoneda，连 fmap 三次，最后取出，等于一次 fmap 复合；Speak 的 hear 与 redeem 互逆。代码怎么写，米田就怎么说。 | demo 输出 |

屏幕代码 `s_yoneda`（`haskell/src/WuWei.hs`）：

```haskell
-- 米田：Nat(Hom(a,−), f) ≅ f a
-- Yoneda f a 收集「对一切 x，用 a→x 产出 f x」
newtype Yoneda f a = Yoneda { runYoneda :: forall x. (a -> x) -> f x }

toYoneda :: Functor f => f a -> Yoneda f a
toYoneda fa = Yoneda (\h -> fmap h fa)    -- 无不为：用 fmap 应对任何箭头

fromYoneda :: Yoneda f a -> f a
fromYoneda (Yoneda g) = g id              -- 无为：只给它 id
```

屏幕代码 `s_redeem`（`haskell/src/WuWei.hs`）：

```haskell
-- 回到第七集：f = Identity
-- (forall x. (a -> x) -> x)  ≅  a
type Speak a = forall x. (a -> x) -> x

hear :: a -> Speak a
hear a = \k -> k a

redeem :: Speak a -> a
redeem s = s id
```

屏幕代码 `s_ran`（`haskell/src/WuWei.hs`）：

```haskell
-- 右 Kan 扩张：Ran_p f a = ∀b. (a → p b) → f b
-- 特例 p = Identity ⇒ Yoneda f ≅ Ran Identity f
newtype Ran g h a = Ran { runRan :: forall b. (a -> g b) -> h b }

yonedaToRan :: Yoneda f a -> Ran Identity f a
yonedaToRan (Yoneda g) = Ran (\k -> g (runIdentity . k))

ranToYoneda :: Ran Identity f a -> Yoneda f a
ranToYoneda (Ran r) = Yoneda (\k -> r (Identity . k))
```

---

## 五 · Kan 扩张：Ran 与 Lan　`06:36–08:09`

参考：DaoFP ch.20 Kan Extensions；Right Kan extension in Haskell；CTFP 3.11 Kan Extensions；Mac Lane: All concepts are Kan extensions

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 06:37 | 最后抬眼看一层。你有函子 f，从 A 到 C；还有一支「道路」函子 p，从 A 到 B。问：怎样把 f 沿着 p「扩张」到整个 B 上？ | f : A → C；p : A → B；扩张到 B → C |
| 06:51 | 右 Kan 扩张 Ran_p f，是最「保守」的扩张：在 B 的每个点，收集所有从该点到 p 像的箭头，再喂给 f——Haskell 里写成 forall。左 Kan 扩张 Lan 是对偶的「最慷慨」一侧。 | Ran p f a = forall b. (a → p b) → f b；Lan 对偶 |
| 07:12 | 普遍性：任何其他扩张，都唯一地经过它。Ran 是右伴随意义下的最佳逼近；Lan 是左伴随意义下的。极限、伴随、米田——都可以写成某次 Kan 扩张。 | 普遍性；lim / ⊣ / Yoneda ⊆ Kan |
| 07:32 | 特例：p 取恒等函子。右 Kan 扩张还原 f 自身——而 Yoneda f，恰好就是 Ran Identity f。米田不是旁边的小岛，是 Kan 扩张的海岸线。 | Yoneda f ≅ Ran Identity f |
| 07:51 | Mac Lane 有一句几乎成了口号：所有概念都是 Kan 扩张。极限是，伴随是，米田也是。今天只取其直觉：无为而无不为——沿恒等扩张，什么也没加，却什么都能说。 | All concepts are Kan extensions |

---

## 结 · 回到道可道　`08:09–09:10`

参考：系列收束：道可道 · 看箭头

| 时间 | 旁白 | 画面 / 代码 |
|---|---|---|
| 08:10 | 回顾本集：可表函子是 Hom；米田引理说自然变换被一个元素钉死；Haskell 的 Yoneda 与 Speak 是它的字面翻译；Kan 扩张把米田收进更大的版图。 | 四句回顾环绕圆相 |
| 08:26 | 再回看整条系列。从无与有，到生与归；从雄与雌，到无为。六句《道德经》，六次换挡，其实只说了一件事：结构在箭头里。 | 六句小字环绕；系列地图 |
| 08:41 | 第七集问：对象不可道，凭什么说相同？今天答：全部说法自然同构，就是同构。不可道的对象，被可道的箭头之全体赎回了。 | 道可道，非常道；米田嵌入满忠实 |
| 08:55 | 借 Milewski 书里米田大师的一句话：看箭头。道可道，非常道。无为而无不为。谢谢观看——「道可道」系列，到此完结。 | 「看箭头」书法；印章；系列完结 |

---

## 数学校对备注

- 米田引理：Nat(C(a,−), F) ≅ F(a)；α ↦ α_a(id_a)；ξ ↦ (h ↦ F(h)(ξ))。
- Hask 中 `forall x. (a -> x) -> f x ≅ f a` 依赖参数性；按 CTFP 惯例忽略 ⊥。
- f = Identity ⇒ `forall x. (a -> x) -> x ≅ a`（CPS / Speak）；redeem = ($ id)。
- 米田嵌入满忠实 ⇒ a ≅ b ⟺ C(a,−) ≅ C(b,−)。
- Ran_p f a ≅ ∫_b [B(a, p b), f b]；Haskell：`Ran g h a = forall b. (a -> g b) -> h b`。
- Yoneda f ≅ Ran Identity f；Mac Lane: “All concepts are Kan extensions.”

## 制作说明

- 画面：Manim Community（Cairo），白底 × 宣纸 multiply；唯一红色为印章与强调。
- 字体：Ma Shan Zheng / LXGW WenKai / IBM Plex Mono / EB Garamond（OFL）。
- 构建：`manim/tts.py` → `manim/scenes.py` → `manim/assemble.py` → `manim/finalize.sh` → `manim/make_docs.py`。
